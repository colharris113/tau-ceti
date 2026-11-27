#!/usr/bin/env python3
"""Render docs/reference/type-tables.md from sources/data/type_tables.json.

    .venv/Scripts/python tools/build_type_tables.py

The JSON is produced by tools/extract_tables.py from the user's own game
image.  This script adds the interpretation worked out in the disassembly:
the flag bits, the behaviour byte, and which AI class each type uses.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "sources" / "data" / "type_tables.json"
OUT = ROOT / "docs" / "reference" / "type-tables.md"

FLAG_BITS = [
    (0x01, "quick death"),
    (0x02, "sensor"),
    (0x04, "robot missile"),
    (0x08, "player missile"),
    (0x20, "mobile"),
    (0x40, "armed"),
    (0x80, "dockable"),
]

KNOWN = {
    3: "mobile armed unit",
    7: "sensor",
    8: "sensor",
    10: "player missile",
    11: "robot missile",
    16: "jump pad (handled before the dockable flag test at $2BE0)",
    21: "mobile unit",
    24: "type-24 gun (behaviour bit 5 gate at $82B1)",
    25: "sensor",
    26: "special early path at $8202",
    27: "Gal-Corp lander",
    28: "Central reactor",
    29: "reactor substation",
    30: "civilian supply centre",
    31: "military supply centre",
    36: "mobile unit",
}


def flag_words(value: int) -> str:
    if value == 0:
        return "none"
    return ", ".join(name for bit, name in FLAG_BITS if value & bit)


def behaviour_words(value: int) -> str:
    if value == 0xFF:
        return "unused ($FF)"
    bits = []
    if value & 0x80:
        bits.append("missile")
    if value & 0x40:
        bits.append("AMM")
    if value & 0x20:
        bits.append("type-24 gate")
    klass = value & 0x0F
    label = f"class {klass}"
    if bits:
        label = ", ".join(bits) + "; " + label
    return label


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    t = data["tables"]
    flags = t["flags"]["bytes"]
    hp = t["hit_points"]["bytes"]
    alt = t["alt_tolerance"]["bytes"]
    beh = t["behaviour"]["bytes"]
    class_range = t["class_range"]["bytes"]
    class_speed = t["class_speed"]["bytes"]
    fire_mask = t["fire_mask"]["bytes"]
    fire_ticks = t["fire_ticks"]["bytes"]
    threshold = t["missile_threshold"]["bytes"]

    out = [
        "# Type tables",
        "",
        "Every object in the game is one of 37 types. Four parallel per-type "
        "tables in the `$C39A–$C408` block describe the types. Five sixteen-byte "
        "class tables below them govern combat. "
        "The record table copies the values it needs when an object "
        "spawns.",
        "",
        "These tables were extracted mechanically from the game image by "
        "`tools/extract_tables.py`. The interpretations below come from the "
        "routines that read them.",
        "",
        "## The per-type tables",
        "",
        "`$C39A` flags, `$C3BF` starting hit points (record byte 7), `$C3E4` the "
        "profile length in rows — the type's drawn height — and `$C409` the "
        "behaviour byte. A type index is the low six bits of record byte 0.",
        "",
        "| Type | Flags | Bits | Hit points | Profile length (rows) | Behaviour | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i in range(37):
        out.append(
            f"| ${i:02X} ({i}) | ${flags[i]:02X} | {flag_words(flags[i])} | "
            f"{hp[i] if hp[i] != 0xFF else '255 ($FF)'} | "
            f"{alt[i] if alt[i] != 0xFF else '255 ($FF)'} | "
            f"${beh[i]:02X} — {behaviour_words(beh[i])} | {KNOWN.get(i, '')} |"
        )

    out += [
        "",
        "A hit-point value of 255 is usually a marker that the type is not a "
        "target in the ordinary sense; the dockable structures all sit at $FF. "
        "A profile length of 255 is simply the tallest profile a one-byte length "
        "can describe.",
        "",
        "## Flag bits",
        "",
        "| Bit | Value | Meaning | Read by |",
        "| --- | --- | --- | --- |",
        "| 0 | $01 | Quick death: the record is freed at $78 after 15 frames | $4445, $444C |",
        "| 1 | $02 | Sensor record | $44A1 |",
        "| 2 | $04 | Robot missile | $44C4 |",
        "| 3 | $08 | Player missile | $44C4 |",
        "| 5 | $20 | Mobile unit | $4620, $823F |",
        "| 6 | $40 | Armed | $4620, $4975 |",
        "| 7 | $80 | Dockable | $2BFA, $4463 |",
        "",
        "Bit 4 is never set in the table. Bit 0 is what produces the 15-frame "
        "death animation for missiles and the 31-frame one for most robots.",
        "",
        "## Behaviour bits",
        "",
        "The behaviour byte at `$C409` is read by both AI routines.",
        "",
        "| Bit | Value | Meaning |",
        "| --- | --- | --- |",
        "| 7 | $80 | The unit may launch a missile |",
        "| 6 | $40 | The unit may answer a lock with an AMM |",
        "| 5 | $20 | Fire only when locked or already hit (the type-24 gate at $82B1) |",
        "| 0-3 | $0F | AI class: indexes the five tables below |",
        "",
        "## The five class tables",
        "",
        "The low nibble of the behaviour byte picks a row from five sixteen-byte "
        "tables. Range is in cells, speed is in 1/256 cell a frame, the mask is "
        "ANDed with a random byte when the fire counter reloads, the tick table "
        "sets the interval, and the threshold is the roll a missile-capable unit "
        "must beat.",
        "",
        "| Class | Range ($C42E) | Speed ($C43E) | Fire mask ($C44E) | Fire ticks ($C45E) | Missile threshold ($C46E) | Types |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for k in range(11):
        users = [f"${i:02X}" for i in range(37) if beh[i] != 0xFF and (beh[i] & 0x0F) == k]
        out.append(
            f"| {k} | {class_range[k]} | {class_speed[k]} | {fire_mask[k]} | "
            f"{fire_ticks[k]} | {threshold[k]} | {', '.join(users) if users else '—'} |"
        )

    out += [
        "",
        "Only classes 0-10 are used. Class 11-15 are $FF placeholders; type 36 "
        "carries a behaviour byte of $FF, so its class is 15 and its range byte "
        "is 255 — the type is handled by the mobile AI's own early branch at "
        "$80C8 instead.",
        "",
        "Class 5 (type $02) fires every 42 frames and has a missile threshold of "
        "240, so it rarely launches. Class 8 (type $16) has a threshold of 128, "
        "so it launches a missile on about half its fire opportunities. Class 9 "
        "(type $18) has a fire interval of zero, which makes the gun fire "
        "whenever its gate opens.",
        "",
        "*Generated by `tools/build_type_tables.py` from `sources/data/type_tables.json`.*",
        "",
        "[Back to the guide](../index.md)",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
