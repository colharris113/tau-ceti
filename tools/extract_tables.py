#!/usr/bin/env python3
"""Pull the per-type tables out of the game image for the guide.

Usage:
    python -I tools/extract_tables.py path/to/04_8900-CC00.prg

The PRG is taken from the user's own disk and is treated as data: this script
only slices bytes at known addresses.  Output is written to
sources/data/type_tables.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Every table is a fixed run of bytes in the $8900-$CC00 segment.
TABLES = [
    ("flags", 0xC39A, 37, "Per-type flags at $C39A"),
    ("hit_points", 0xC3BF, 37, "Record byte 7 at spawn ($C3BF)"),
    ("alt_tolerance", 0xC3E4, 37, "Profile length in rows ($C3E4)"),
    ("behaviour", 0xC409, 37, "Per-type behaviour byte at $C409"),
    ("class_range", 0xC42E, 16, "AI class range in cells ($C42E)"),
    ("class_speed", 0xC43E, 16, "AI class speed, 1/256 cell a frame ($C43E)"),
    ("fire_mask", 0xC44E, 16, "Random mask reloading the fire counter ($C44E)"),
    ("fire_ticks", 0xC45E, 16, "Fire interval by class ($C45E)"),
    ("missile_threshold", 0xC46E, 16, "Random threshold for a robot missile ($C46E)"),
]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    prg = Path(sys.argv[1])
    raw = prg.read_bytes()
    load = raw[0] | (raw[1] << 8)
    body = raw[2:]
    out = {"source": prg.name, "load_address": f"${load:04X}", "tables": {}}
    for name, addr, length, note in TABLES:
        off = addr - load
        if off < 0 or off + length > len(body):
            raise SystemExit(f"{name}: ${addr:04X} outside the image")
        out["tables"][name] = {
            "address": f"${addr:04X}",
            "note": note,
            "bytes": list(body[off:off + length]),
            "hex": [f"${b:02X}" for b in body[off:off + length]],
        }
    dest = Path(__file__).resolve().parent.parent / "sources" / "data" / "type_tables.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
