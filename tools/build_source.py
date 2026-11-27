#!/usr/bin/env python3
"""Generate the source-guide pages from the listings plus curated symbols.

Run from anywhere with the project venv:

    .venv/Scripts/python tools/build_source.py

Outputs (all generated; do not edit):

    docs/source/index.md
    docs/source/variables.md
    docs/source/routines/<slug>.md

The listings in ``sources/`` are a linear sweep, so their line starts are not
reliable routine boundaries.  This script rebuilds a byte map from every
``ADDR: XX XX`` line and re-disassembles the curated code ranges with py65.
Incoming references are indexed from those ranges and supplemental caller blocks.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Run isolated (python -I) from build_all.py, so the script's own directory is
# not on sys.path automatically.  Add it explicitly for ``listing``.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from listing import BRANCHES, Disassembler, load_byte_map

ROOT = Path(__file__).resolve().parent.parent
SOURCES = sorted((ROOT / "sources").glob("dis_*.txt"))
DOCS = ROOT / "docs"
SYMBOLS_PATH = ROOT / "tools" / "symbols.json"

TERMINATORS = {"RTS", "RTI", "BRK"}
ADDR_RE = re.compile(r"\$([0-9A-Fa-f]{2,4})")

GROUP_ORDER = ["Flight", "Docking", "Records", "Combat", "Messages"]


def render_text(text: str) -> str:
    """Format hexadecimal values as Markdown code spans."""
    return ADDR_RE.sub(lambda m: f'`${m.group(1).upper()}`', text)


def render_cell(text: str) -> str:
    """A table cell: prose rendering, with pipes escaped."""
    return render_text(text).replace("|", "\\|")


def walk(dis: Disassembler, entry: int, end: int | None = None,
         limit: int = 0x400) -> list[dict]:
    """Decode a routine.

    With an explicit end address this is a plain linear decode of the whole
    body, which is what we want: early ``RTS`` instructions are common and the
    code after them still belongs to the routine.  Without an end the walker
    stops at the first terminator and then resumes at any forward branch target
    it has already seen, so it does not truncate at an early return.
    """
    out: list[dict] = []
    if end is not None:
        addr = entry
        while entry <= addr < end and len(out) < 2000:
            length, mnemonic, operand = dis.instruction(addr)
            target = dis.target(addr, mnemonic, operand)
            out.append({"addr": addr, "len": length, "op": mnemonic, "arg": operand,
                        "target": target,
                        "bytes": [dis.bytes[(addr + i) & 0xFFFF] for i in range(length)]})
            addr += length
        return out

    seen: set[int] = set()
    pending: set[int] = set()
    addr = entry
    while 0 <= addr < 0x10000 and len(out) < 2000 and (addr - entry) < limit:
        length, mnemonic, operand = dis.instruction(addr)
        target = dis.target(addr, mnemonic, operand)
        if mnemonic in BRANCHES.values() and target is not None:
            pending.add(target)
        out.append({"addr": addr, "len": length, "op": mnemonic, "arg": operand,
                    "target": target, "bytes": [dis.bytes[(addr + i) & 0xFFFF] for i in range(length)]})
        seen.add(addr)
        if mnemonic in TERMINATORS or mnemonic == "JMP":
            nxt = min((t for t in pending if t > addr and t not in seen), default=None)
            if nxt is None or (nxt - entry) >= limit:
                break
            addr = nxt
            continue
        addr += length
    return out


def instruction_ranges(insns: list[dict]) -> list[tuple[int, int]]:
    """Group decoded instructions into contiguous blocks."""
    blocks: list[tuple[int, int]] = []
    for ins in insns:
        end = ins["addr"] + ins["len"]
        if blocks and blocks[-1][1] == ins["addr"]:
            blocks[-1] = (blocks[-1][0], end)
        else:
            blocks.append((ins["addr"], end))
    return blocks


def render_listing(insns: list[dict], sym_by_addr: dict[int, dict],
                   var_by_addr: dict[int, dict]) -> str:
    lines: list[str] = []
    prev_end: int | None = None
    for ins in insns:
        if prev_end is not None and ins["addr"] != prev_end:
            lines.append("")
        prev_end = ins["addr"] + ins["len"]
        raw = " ".join(f"{b:02X}" for b in ins["bytes"])
        op = ins["op"]
        arg = ADDR_RE.sub(lambda m: f"${m.group(1).upper()}", ins["arg"])
        comment = ""
        target = ins["target"]
        if target is not None and target in sym_by_addr and target != ins["addr"]:
            comment = sym_by_addr[target]["name"]
        else:
            for value in ADDR_RE.findall(ins["arg"]):
                var = var_by_addr.get(int(value, 16))
                if var:
                    comment = var["name"]
                    break
        line = f'{ins["addr"]:04X}: {raw:<8} {op:<3} {arg}'.rstrip()
        if comment:
            line += f"   ; {comment}"
        lines.append(line)
    return "\n".join(["```text", *lines, "```"])


def build_called_by(
    routines: list[dict], caller_blocks: list[list[dict]],
) -> dict[int, list[tuple[int, str, int | None]]]:
    """Index direct transfers from curated code to known instruction addresses."""
    entry_of: dict[int, int] = {}
    instructions: dict[int, dict] = {}
    for r in routines:
        for block in [r["insns"], *(extra["insns"] for extra in r["extras"])]:
            for ins in block:
                entry_of.setdefault(ins["addr"], r["entry"])
                instructions.setdefault(ins["addr"], ins)
    for block in caller_blocks:
        for ins in block:
            instructions.setdefault(ins["addr"], ins)

    index: dict[int, list[tuple[int, str, int | None]]] = {}
    for addr, ins in sorted(instructions.items()):
        if ins["op"] not in ("JSR", "JMP"):
            continue
        target_entry = entry_of.get(ins["target"])
        owner = entry_of.get(addr)
        if target_entry is not None and target_entry != owner:
            index.setdefault(target_entry, []).append((addr, ins["op"], owner))
    return index


def main() -> int:
    symbols = json.loads(SYMBOLS_PATH.read_text(encoding="utf-8"))
    memory = load_byte_map(SOURCES)
    dis = Disassembler(memory)
    sym_by_addr = {int(r["addr"], 16): r for r in symbols["routines"]}
    var_by_addr = {int(v["addr"], 16): v for v in symbols["variables"]}

    routines = []
    for spec in symbols["routines"]:
        entry = int(spec["addr"], 16)
        end = int(spec["end"], 16) if spec.get("end") else None
        insns = walk(dis, entry, end)
        extras = []
        for more in spec.get("more", []):
            if isinstance(more, dict):
                extra_addr = int(more["addr"], 16)
                extra_end = int(more["end"], 16) if more.get("end") else None
            else:
                extra_addr, extra_end = int(more, 16), None
            extras.append({"addr": extra_addr,
                           "insns": walk(dis, extra_addr, extra_end)})
        routines.append({"spec": spec, "entry": entry, "insns": insns, "extras": extras})
        if not insns:
            raise SystemExit(f"{spec['slug']}: nothing decoded at ${entry:04X}")

    caller_blocks = [walk(dis, int(block["addr"], 16), int(block["end"], 16))
                     for block in symbols["caller_blocks"]]
    called_by = build_called_by(routines, caller_blocks)

    # Per-routine pages.
    outdir = DOCS / "source" / "routines"
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.md"):
        old.unlink()

    for r in routines:
        spec = r["spec"]
        slug = spec["slug"]
        span = f"${r['insns'][0]['addr']:04X}-${r['insns'][-1]['addr'] + r['insns'][-1]['len'] - 1:04X}"
        calls: dict[int, tuple[str, int]] = {}
        jumps: dict[int, tuple[str, int]] = {}
        for ins in r["insns"] + [i for e in r["extras"] for i in e["insns"]]:
            target = ins["target"]
            if target is None or target == ins["addr"]:
                continue
            if ins["op"] == "JSR" and target in sym_by_addr and target != r["entry"]:
                calls.setdefault(target, (sym_by_addr[target]["name"], ins["addr"]))
            elif ins["op"] == "JMP" and target in sym_by_addr and target != r["entry"]:
                jumps.setdefault(target, (sym_by_addr[target]["name"], ins["addr"]))
            elif ins["op"] in BRANCHES.values() and target in sym_by_addr:
                calls.setdefault(target, (sym_by_addr[target]["name"], ins["addr"]))

        body = [
            f"# {spec['name']}",
            "",
            f"**Address** `{span}` · **Group** {spec['group']}",
            "",
            render_text(spec["summary"]),
            "",
            "## Listing",
            "",
            "*Decoded from the byte map within the curated code ranges for this "
            "routine.*",
            "",
            render_listing(r["insns"], sym_by_addr, var_by_addr),
        ]
        for extra in r["extras"]:
            body += [
                "",
                f"### Additional code at `${extra['addr']:04X}`",
                "",
                render_listing(extra["insns"], sym_by_addr, var_by_addr),
            ]

        body += ["", "## Calls", ""]
        if calls:
            for target, (name, at) in sorted(calls.items(), key=lambda kv: kv[1][1]):
                body.append(f'- [`{name}`]({sym_by_addr[target]["slug"]}.md) from `${at:04X}`')
        else:
            body.append("*None recorded in this body.*")
        if jumps:
            body += ["", "**Tail jumps**", ""]
            for target, (name, at) in sorted(jumps.items(), key=lambda kv: kv[1][1]):
                body.append(f'- [`{name}`]({sym_by_addr[target]["slug"]}.md) at `${at:04X}`')

        body += ["", "## Called by", ""]
        entries = called_by.get(r["entry"], [])
        if entries:
            for addr, mnemonic, owner in entries:
                owner_spec = sym_by_addr.get(owner) if owner is not None else None
                if owner_spec:
                    body.append(f'- `{mnemonic}` at `${addr:04X}` in '
                                f'[`{owner_spec["name"]}`]({owner_spec["slug"]}.md)')
                else:
                    body.append(f'- `{mnemonic}` at `${addr:04X}`')
        else:
            body.append("*No direct call or jump found in the curated code ranges.*")

        body += [
            "",
            "---",
            "",
            "*Generated by `tools/build_source.py` from `tools/symbols.json`. "
            "Correct the symbol file, not this page.*",
            "",
            "[Back to the source guide](../index.md)",
            "",
        ]
        (outdir / f"{slug}.md").write_text("\n".join(body), encoding="utf-8")

    # Index page, grouped.
    index = [
        "# Source guide",
        "",
        "The pages are generated from the original listing bytes "
        "and curated code ranges. The labels and summaries explain how the routines "
        "fit into the game.",
        "",
        "## How to read a listing",
        "",
        "Each line is an instruction: its address, its bytes, the mnemonic and "
        "operand, and a comment where a routine or variable has a known name. "
        "A routine can include additional code blocks at separate addresses.",
        "",
        "`Called by` lists direct `JSR` and `JMP` instructions from the curated "
        "code ranges that land on an instruction in the routine. Coverage grows "
        "as more code ranges are reviewed. Indirect jumps and fall-through paths "
        "are outside the scope of this index.",
        "",
        "## Routines",
        "",
    ]
    for group in GROUP_ORDER:
        group_routines = sorted([r for r in routines if r["spec"]["group"] == group],
                                key=lambda x: x["entry"])
        if not group_routines:
            continue
        index += [f"### {group}", "",
                  "| Routine | Address | What it does |",
                  "| --- | --- | --- |"]
        for r in group_routines:
            spec = r["spec"]
            index.append(f'| [`{spec["name"]}`](routines/{spec["slug"]}.md) | '
                         f'`${r["entry"]:04X}` | {render_cell(spec["summary"])} |')
        index.append("")
    index += [
        "## Variables",
        "",
        "The zero-page and low-memory values these routines share are listed in "
        "[Variables](variables.md).",
        "",
        "*Generated by `tools/build_source.py`.*",
        "",
        "[Back to the guide](../index.md)",
        "",
    ]
    (DOCS / "source" / "index.md").write_text("\n".join(index), encoding="utf-8")

    # Variables page.
    var_lines = [
        "# Variables",
        "",
        "The game keeps almost everything in the zero page and "
        "the first few pages of RAM. These are the values the routines in this "
        "guide read and write; names are ours, addresses are the game's.",
        "",
    ]
    for group in GROUP_ORDER:
        group_vars = sorted([v for v in symbols["variables"] if v["group"] == group],
                            key=lambda v: int(v["addr"], 16))
        if not group_vars:
            continue
        var_lines += [f"## {group}", "",
                      "| Address | Name | Notes |",
                      "| --- | --- | --- |"]
        for v in group_vars:
            var_lines.append(f'| `${v["addr"]}` | **{v["name"]}** | '
                             f'{render_cell(v["doc"])} |')
        var_lines.append("")
    var_lines += [
        "*Generated by `tools/build_source.py`.*",
        "",
        "[Back to the source guide](index.md)",
        "",
    ]
    (DOCS / "source" / "variables.md").write_text("\n".join(var_lines), encoding="utf-8")

    print(f"wrote {len(routines)} routine pages, the source index and variables page")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
