#!/usr/bin/env python3
"""Recover the 32 city layouts and their names from the listing byte map.

    .venv/Scripts/python tools/extract_cities.py

The city sheet starts at $9400.  Each city owns a 96-byte block
(32 records of three bytes), so city *n* begins at $9400 + n * $60.  A
record is ``type, x, y``; a type byte of $C0 ends the list.  The names live
at $8D02 as characters stored $40 below their ASCII code, terminated by a
byte with the high bit set.

Output: sources/data/cities.json (generated; do not edit).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from listing import load_byte_map

ROOT = Path(__file__).resolve().parent.parent
SOURCES = sorted((ROOT / "sources").glob("dis_*.txt"))
OUT = ROOT / "sources" / "data" / "cities.json"

CITY_BASE = 0x9400
CITY_STRIDE = 96
CITY_RECORDS = 32
NAME_BASE = 0x8D02
CITY_COUNT = 32
TERMINATOR = 0xC0


def read_names(memory: dict[int, int]) -> list[str]:
    names: list[str] = []
    current: list[str] = []
    addr = NAME_BASE
    while len(names) < CITY_COUNT and addr < 0x9000:
        byte = memory.get(addr, 0)
        if byte & 0x80:
            if current:
                names.append("".join(current))
                current = []
        else:
            current.append(chr(byte + 0x40))
        addr += 1
    return names


def read_city(memory: dict[int, int], index: int) -> list[list[int]]:
    base = CITY_BASE + index * CITY_STRIDE
    records: list[list[int]] = []
    for slot in range(CITY_RECORDS):
        type_byte = memory.get(base + slot * 3, 0)
        if type_byte == TERMINATOR:
            break
        records.append([
            type_byte & 0x3F,
            memory.get(base + slot * 3 + 1, 0),
            memory.get(base + slot * 3 + 2, 0),
        ])
    return records


def main() -> int:
    memory = load_byte_map(SOURCES)
    if not memory:
        raise SystemExit("no bytes found; run from the repository root")
    names = read_names(memory)
    if len(names) != CITY_COUNT:
        raise SystemExit(f"expected {CITY_COUNT} names, found {len(names)}")

    cities = []
    for index in range(CITY_COUNT):
        cities.append({
            "index": index,
            "name": names[index].upper(),
            "records": read_city(memory, index),
        })

    out = {
        "generated": True,
        "note": "Recovered by tools/extract_cities.py; do not edit.",
        "sources": [p.name for p in SOURCES],
        "table": {
            "base": f"${CITY_BASE:04X}",
            "stride_bytes": CITY_STRIDE,
            "record_bytes": 3,
            "records_per_city": CITY_RECORDS,
            "terminator": f"${TERMINATOR:02X}",
        },
        "names_table": f"${NAME_BASE:04X}",
        "cities": cities,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    total = sum(len(c["records"]) for c in cities)
    print(f"wrote {len(cities)} cities, {total} records -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
