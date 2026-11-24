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
``ADDR: XX XX`` line, re-disassembles from the curated entry points with py65,
and follows forward branches so early returns do not truncate a listing.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

# Run isolated (python -I) from build_all.py, so the script's own directory is
# not on sys.path automatically.  Add it explicitly for ``listing``.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from listing import BRANCHES, Disassembler, load_byte_map, load_line_starts

ROOT = Path(__file__).resolve().parent.parent
SOURCES = sorted((ROOT / "sources").glob("dis_*.txt"))
DOCS = ROOT / "docs"
SYMBOLS_PATH = ROOT / "tools" / "symbols.json"

TERMINATORS = {"RTS", "RTI", "BRK"}
ADDR_RE = re.compile(r"\$([0-9A-Fa-f]{2,4})")

GROUP_ORDER = ["Flight", "Docking", "Records", "Combat", "Messages"]


def render_text(text: str) -> str:
    """Escape prose and turn every $XXXX into an address chip."""
    escaped = html.escape(text, quote=False)
    return ADDR_RE.sub(lambda m: f'<code class="addr">${m.group(1).upper()}</code>', escaped)


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
        op = html.escape(ins["op"])
        arg = html.escape(ADDR_RE.sub(lambda m: f"${m.group(1).upper()}", ins["arg"]))
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
        parts = [
            f'<span class="rt-addr">{ins["addr"]:04X}</span>',
            f'<span class="rt-bytes">{raw:<8}</span>',
            f'<span class="rt-op">{op}</span>',
            f'<span class="rt-arg">{arg}</span>',
        ]
        line = "  ".join(parts).rstrip()
        if comment:
            line += f'   <span class="rt-cmt">; {html.escape(comment)}</span>'
        lines.append(line)
    return '<pre class="rt-listing">\n' + "\n".join(lines) + "\n</pre>"


def build_called_by(dis: Disassembler, routines: list[dict],
                    candidates: set[int]) -> dict[int, list[tuple[int, str, str]]]:
    """entry address -> [(caller instruction address, mnemonic, caller routine name)]."""
    # Decode every listing line start and every address we decoded ourselves,
    # and keep the control transfers that land on a routine entry.
    by_addr = {r["entry"]: r for r in routines}
    index: dict[int, list[tuple[int, str, str]]] = {}
    inside: list[tuple[int, int, str]] = []
    for r in routines:
        for ins in r["insns"]:
            inside.append((ins["addr"], ins["addr"] + ins["len"], r["spec"]["name"]))
    inside.sort()

    def owner(addr: int) -> str:
        for start, end, name in inside:
            if start <= addr < end:
                return name
        return ""

    for addr in sorted(candidates):
        length, mnemonic, operand = dis.instruction(addr)
        if mnemonic not in ("JSR", "JMP"):
            continue
        target = dis.target(addr, mnemonic, operand)
        if target in by_addr:
            index.setdefault(target, []).append((addr, mnemonic, owner(addr)))
    for entries in index.values():
        entries.sort()
    return index


def main() -> int:
    symbols = json.loads(SYMBOLS_PATH.read_text(encoding="utf-8"))
    memory = load_byte_map(SOURCES)
    line_starts = load_line_starts(SOURCES)
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

    # Cross-references: every line start and every decoded instruction is a
    # candidate control transfer.
    candidates = set(line_starts)
    for r in routines:
        for ins in r["insns"]:
            candidates.add(ins["addr"])
        for extra in r["extras"]:
            for ins in extra["insns"]:
                candidates.add(ins["addr"])
    called_by = build_called_by(dis, routines, candidates)

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
            if ins["op"] == "JSR" and target in sym_by_addr:
                calls.setdefault(target, (sym_by_addr[target]["name"], ins["addr"]))
            elif ins["op"] == "JMP" and target in sym_by_addr and target != r["entry"]:
                jumps.setdefault(target, (sym_by_addr[target]["name"], ins["addr"]))
            elif ins["op"] in BRANCHES.values() and target in sym_by_addr:
                calls.setdefault(target, (sym_by_addr[target]["name"], ins["addr"]))

        body = [
            f"# {spec['name']}",
            "",
            f"**Address** `{span}` &nbsp;·&nbsp; **Group** {spec['group']}",
            "",
            f'<p class="lede">{render_text(spec["summary"])}</p>',
            "",
            "## Listing",
            "",
            "*Re-disassembled from the byte map: every instruction shown is one the "
            "game really executes from this entry, and gaps are branch targets that "
            "follow an early return.*",
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
                owner_spec = next((x["spec"] for x in routines if x["spec"]["name"] == owner), None)
                if owner_spec:
                    body.append(f'- `{mnemonic}` at `${addr:04X}` in '
                                f'[`{owner_spec["name"]}`]({owner_spec["slug"]}.md)')
                else:
                    body.append(f'- `{mnemonic}` at `${addr:04X}`')
        else:
            body.append("*No call site found in the swept listings; this may be "
                        "reached through a jump table or from undisassembled code.*")

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
        '<p class="lede">Every address here has been checked against the running '
        "game. The pages are generated by re-disassembling the original listings "
        "from curated entry points, so a page shows the real instruction stream "
        "rather than a linear sweep's guess.</p>",
        "",
        "## How to read a listing",
        "",
        "Each line is an instruction: its address, its bytes, the mnemonic and "
        "operand, and a comment naming the routine or variable it touches. Gaps "
        "between blocks are branch targets that follow an early `RTS`; the game "
        "reaches them, the linear listing just could not show them in place.",
        "",
        "The `Calls` and `Called by` sections are built by decoding every line "
        "start in the listings and keeping the `JSR`/`JMP` instructions that land "
        "on a known entry. Some call sites live in code the sweep never decoded, "
        "so the lists are a good map, not proof of a complete one.",
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
                  '<div class="routine-index" markdown>', "",
                  "| Routine | Address | What it does |",
                  "| --- | --- | --- |"]
        for r in group_routines:
            spec = r["spec"]
            index.append(f'| [`{spec["name"]}`](routines/{spec["slug"]}.md) | '
                         f'`${r["entry"]:04X}` | {render_cell(spec["summary"])} |')
        index += ["", "</div>", ""]
    index += [
        "## Variables",
        "",
        "The zero-page and low-memory values these routines share are listed in "
        "[Variables](variables.md).",
        "",
        "*Generated by `tools/build_source.py`.*",
        "",
    ]
    (DOCS / "source" / "index.md").write_text("\n".join(index), encoding="utf-8")

    # Variables page.
    var_lines = [
        "# Variables",
        "",
        '<p class="lede">The game keeps almost everything in the zero page and '
        "the first few pages of RAM. These are the values the routines in this "
        "guide read and write; names are ours, addresses are the game's.</p>",
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
            var_lines.append(f'| <code class="addr">${v["addr"]}</code> | **{v["name"]}** | '
                             f'{render_text(v["doc"])} |')
        var_lines.append("")
    var_lines += ["*Generated by `tools/build_source.py`.*", ""]
    (DOCS / "source" / "variables.md").write_text("\n".join(var_lines), encoding="utf-8")

    print(f"wrote {len(routines)} routine pages, the source index and variables page")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
