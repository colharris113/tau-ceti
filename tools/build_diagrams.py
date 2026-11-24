#!/usr/bin/env python3
"""Generate the guide's explanatory figures as theme-aware SVG.

    .venv/Scripts/python tools/build_diagrams.py

Every number used by a figure comes from the game's own constants, read out
of the disassembly in the prose: the docking altitude 28, the 55-unit offset
in the aperture test, the $48 aperture ceiling, the $1C/$BF altitude range,
the 50-frame clock, the BFFF fuel value and the (speed >> 3) + 16 burn.  The
figures are inlined in the pages with pymdownx.snippets, so their colours
follow the light/dark theme through CSS classes in extra.css.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "diagrams"

# --- game constants ---------------------------------------------------------
DOCK_ALT = 0x1C           # 28: docking altitude
DOCK_TOL = 0x37           # 55: absolute altitude tolerance in the aperture test
APERTURE_MAX = 0x48       # 72: the iris opens no further
ALT_MAX = 0xBF            # 191
FUEL = 0xBFFF             # 49,151 units: the 16-bit tank, low byte included
TICK = 50                 # frames per second at 50 Hz


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x: float, y: float, body: str, cls: str = "fig-label",
         anchor: str = "start", extra: str = "") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" '
            f'text-anchor="{anchor}"{(" " + extra) if extra else ""}>{esc(body)}</text>')


def line(x1: float, y1: float, x2: float, y2: float, cls: str) -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'class="{cls}"/>')


def rect(x: float, y: float, w: float, h: float, cls: str,
         rx: float = 0) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" class="{cls}"/>')


def circle(cx: float, cy: float, r: float, cls: str) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" class="{cls}"/>'


def diamond(cx: float, cy: float, r: float, cls: str) -> str:
    pts = f"{cx:.1f},{cy - r:.1f} {cx + r:.1f},{cy:.1f} {cx:.1f},{cy + r:.1f} {cx - r:.1f},{cy:.1f}"
    return f'<polygon points="{pts}" class="{cls}"/>'


def document(slug: str, w: int, h: int, title: str, desc: str, body: list[str]) -> str:
    return "\n".join([
        f'<svg class="tc-fig" viewBox="0 0 {w} {h}" role="img" '
        f'aria-labelledby="{slug}-t {slug}-d" xmlns="http://www.w3.org/2000/svg">',
        f'<title id="{slug}-t">{esc(title)}</title>',
        f'<desc id="{slug}-d">{esc(desc)}</desc>',
        *body,
        "</svg>",
        "",
    ])


# --- figure 1: the record table --------------------------------------------
def record_table() -> str:
    w, h = 780, 626
    body: list[str] = []
    body.append(text(40, 32, "The record table: 48 records of 16 bytes", "fig-title"))
    body.append(text(40, 52, "768 bytes at $0E00-$10FF. Byte 0 sorts every record; the rest is state.",
                     "fig-muted"))

    # Key
    ky = 78
    body.append(rect(40, ky, 14, 14, "fig-cell-type", 2))
    body.append(text(60, ky + 11, "$00-$3F  live, low six bits index the type tables", "fig-label"))
    body.append(rect(390, ky, 14, 14, "fig-cell", 2))
    body.append(text(410, ky + 11, "(shown plain so the grid stays readable)", "fig-muted"))

    # 48 strips, four columns of twelve.
    strip_w = 128            # 16 bytes at 8 px
    strip_h = 15
    row_gap = 23
    cols = [70, 228, 386, 544]
    top = 128
    for c, x in enumerate(cols):
        body.append(text(x, top - 8, f"${0x0E00 + c * 0xC0:04X}", "fig-tick"))
        for r in range(12):
            y = top + r * row_gap
            body.append(rect(x, y, strip_w, strip_h, "fig-cell", 1))
            body.append(rect(x, y, 8, strip_h, "fig-cell-type", 1))
            for i in range(1, 16):
                gx = x + i * 8
                body.append(line(gx, y, gx, y + strip_h, "fig-hair"))
    body.append(text(cols[0], top + 12 * row_gap + 12,
                     "each row is one record; memory runs down a column, then across",
                     "fig-muted"))

    # One record, enlarged.
    sep_y = 438
    body.append(line(40, sep_y, 740, sep_y, "fig-hair"))
    body.append(text(40, sep_y + 26, "One record, byte by byte", "fig-title"))

    fields = [
        "type", "cell x", "cell y", "status", "sub-cell x", "sub-cell y",
        "alt / aim", "hp / height", "overload", "fire counter", "blip",
        "blip", "distance", "distance", "target lo", "target hi",
    ]
    cell_w, cell_h = 36, 26
    x0, y0 = 60, sep_y + 54
    for i in range(16):
        x = x0 + i * cell_w
        body.append(rect(x, y0, cell_w - 2, cell_h, "fig-cell-type" if i == 0 else "fig-cell", 2))
        body.append(text(x + (cell_w - 2) / 2, y0 - 5, str(i), "fig-tick", "middle"))
        lx, ly = x + (cell_w - 2) / 2, y0 + cell_h + 12
        body.append(text(lx, ly, fields[i], "fig-label", "start",
                         f'transform="rotate(42 {lx:.1f} {ly:.1f})"'))
    body.append(text(x0, y0 + 132,
                     "Byte 0: bits 7-6 are state ($80 free, $40 dying); bits 5-0 pick the type row in $C39A.",
                     "fig-muted"))

    return document("fig-record-table", w, h,
                    "The record table: 48 records of 16 bytes",
                    "A schematic of the 768-byte record table at $0E00, with one record "
                    "expanded to label all sixteen bytes.", body)


# --- figure 2: the docking envelope ----------------------------------------
def docking_envelope() -> str:
    w, h = 780, 380
    x0, x1 = 84, 700
    y0, y1 = 78, 300

    def sx(a: float) -> float:
        return x0 + a / APERTURE_MAX * (x1 - x0)

    def sy(alt: float) -> float:
        return y1 - alt / ALT_MAX * (y1 - y0)

    body: list[str] = []
    body.append(text(40, 30, "The docking window: aperture against altitude", "fig-title"))
    body.append(text(40, 50, "A dock is accepted only inside the ochre wedge.", "fig-muted"))

    for alt in range(0, 181, 20):
        y = sy(alt)
        body.append(line(x0, y, x1, y, "fig-grid"))
        body.append(text(x0 - 10, y + 3, str(alt), "fig-tick", "end"))
    for a in (0, 18, 36, 54, 72):
        x = sx(a)
        body.append(text(x, y1 + 18, str(a), "fig-tick", "middle"))
    body.append(line(x0, y1, x1, y1, "fig-axis"))
    body.append(line(x0, y0, x0, y1, "fig-axis"))

    # |alt - 28| + 55 < aperture, for aperture > 55.
    band = [
        (sx(55), sy(DOCK_ALT)),
        (sx(72), sy(DOCK_ALT + (72 - DOCK_TOL))),
        (sx(72), sy(DOCK_ALT - (72 - DOCK_TOL))),
    ]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in band)
    body.append(f'<polygon points="{pts}" class="fig-band"/>')
    body.append(line(sx(55), sy(DOCK_ALT), x1, sy(DOCK_ALT), "fig-ochre"))

    # Reference altitude.
    body.append(line(x0, sy(DOCK_ALT), x1, sy(DOCK_ALT), "fig-hair"))
    body.append(text(x0 + 6, sy(DOCK_ALT) - 6, "docking altitude 28 ($1C)", "fig-tick"))

    # Label the accepted band from the empty space above it, starting just to
    # the right of the 55 marker so the hairline does not run through it.
    body.append(text(sx(55) + 10, sy(60), "accepted: |alt - 28| + 55 < aperture",
                     "fig-label"))

    # Annotation for the empty left region.
    body.append(text(sx(24), sy(120), "no altitude can dock", "fig-label", "middle"))
    body.append(text(sx(24), sy(112), "until the door is 55/72 open", "fig-tick", "middle"))
    body.append(line(sx(55), sy(0), sx(55), sy(ALT_MAX), "fig-hair"))
    body.append(text(sx(55) - 6, sy(20), "55", "fig-tick", "end"))

    # Full-open band labels.
    body.append(text(sx(72) + 6, sy(46), "45", "fig-tick"))
    body.append(text(sx(72) + 6, sy(10), "11", "fig-tick"))

    body.append(text((x0 + x1) / 2, y1 + 42,
                     "aperture opening (record byte 8, $00-$48)", "fig-label", "middle"))
    body.append(text(28, (y0 + y1) / 2, "altitude (0-$BF)", "fig-label", "middle",
                     f'transform="rotate(-90 28 {(y0 + y1) / 2:.1f})"'))
    return document("fig-docking", w, h,
                    "The docking window: aperture against altitude",
                    "An altitude-versus-aperture plot. Docking is accepted only when the "
                    "absolute altitude error plus 55 is less than the aperture, which is "
                    "only possible once the door has opened beyond 55 of its 72 steps.", body)


# --- figure 3: aperture timeline -------------------------------------------
def aperture_timeline() -> str:
    w, h = 780, 336
    x0, x1 = 84, 700
    y0, y1 = 78, 250

    def sx(f: float) -> float:
        return x0 + f / 40 * (x1 - x0)

    def sy(a: float) -> float:
        return y1 - a / APERTURE_MAX * (y1 - y0)

    body: list[str] = []
    body.append(text(40, 30, "The iris takes 36 frames to travel", "fig-title"))
    body.append(text(40, 50, "Two points a frame, in either direction.", "fig-muted"))

    for a in (0, 18, 36, 54, 72):
        y = sy(a)
        body.append(line(x0, y, x1, y, "fig-grid"))
        body.append(text(x0 - 10, y + 3, str(a), "fig-tick", "end"))
    for f in (0, 10, 20, 30, 40):
        x = sx(f)
        body.append(text(x, y1 + 18, str(f), "fig-tick", "middle"))
    body.append(line(x0, y1, x1, y1, "fig-axis"))
    body.append(line(x0, y0, x0, y1, "fig-axis"))

    body.append(line(sx(0), sy(72), sx(36), sy(0), "fig-ochre"))
    body.append(line(sx(0), sy(0), sx(36), sy(72), "fig-blue"))

    # Legend along the bottom, clear of both ramps.
    body.append(line(84, 314, 112, 314, "fig-ochre"))
    body.append(text(118, 318, "closing (scanned or locked)", "fig-label"))
    body.append(line(340, 314, 368, 314, "fig-blue"))
    body.append(text(374, 318, "opening (inside two cells)", "fig-label"))

    body.append(line(sx(36), sy(0), sx(36), sy(72), "fig-hair"))
    body.append(text(sx(36) + 6, sy(60), "36 frames (0.72 s)", "fig-tick"))

    body.append(text(sx(9), sy(48), "−2 a frame", "fig-label", "end"))
    body.append(text(sx(5) + 10, sy(6), "+2 a frame", "fig-label"))

    body.append(text((x0 + x1) / 2, y1 + 42, "frames", "fig-label", "middle"))
    body.append(text(28, (y0 + y1) / 2, "aperture opening", "fig-label", "middle",
                     f'transform="rotate(-90 28 {(y0 + y1) / 2:.1f})"'))
    return document("fig-aperture", w, h,
                    "The aperture opening and closing over time",
                    "Two mirrored ramps: a scanned or locked building shuts its iris two "
                    "points a frame, and a building within two cells opens it at the same "
                    "rate. Both reach the end stop after 36 frames.", body)


# --- figure 4: fuel burn ----------------------------------------------------
def fuel_burn() -> str:
    w, h = 780, 392
    # Two panels, one measure each: never two scales on one plot.
    panels = [
        {"x0": 74, "x1": 350, "title": "Burn per second", "ymax": 150,
         "ticks": (0, 50, 100, 150), "fmt": "{:.0f}"},
        {"x0": 446, "x1": 722, "title": "Minutes of fuel left", "ymax": 60,
         "ticks": (0, 15, 30, 45, 60), "fmt": "{:.0f}"},
    ]
    y0, y1 = 104, 296

    def burn(speed: float, ruptured: bool) -> float:
        b = (int(speed) >> 3) + 16 + (96 if ruptured else 0)
        return float(b)

    body: list[str] = []
    body.append(text(40, 30, "Fuel: how speed and a ruptured tank change the burn", "fig-title"))
    body.append(text(40, 50,
                     "One burn a second, at the 50-frame tick. On the ground the burn is zero.",
                     "fig-muted"))

    # Legend, shared by both panels.
    body.append(line(480, 68, 508, 68, "fig-ochre"))
    body.append(text(514, 72, "tank intact", "fig-label"))
    body.append(line(620, 68, 648, 68, "fig-blue"))
    body.append(text(654, 72, "tank ruptured", "fig-label"))

    for panel in panels:
        x0, x1 = panel["x0"], panel["x1"]
        ymax = panel["ymax"]

        def sx(speed: float) -> float:
            return x0 + speed / ALT_MAX * (x1 - x0)

        def sy(value: float) -> float:
            return y1 - value / ymax * (y1 - y0)

        body.append(text(x0, y0 - 16, panel["title"], "fig-title"))
        for tick in panel["ticks"]:
            y = sy(tick)
            body.append(line(x0, y, x1, y, "fig-grid"))
            body.append(text(x0 - 10, y + 3, panel["fmt"].format(tick), "fig-tick", "end"))
        for speed in (0, 64, 128, 191):
            body.append(text(sx(speed), y1 + 18, str(speed), "fig-tick", "middle"))
        body.append(line(x0, y1, x1, y1, "fig-axis"))
        body.append(line(x0, y0, x0, y1, "fig-axis"))

        if panel["title"].startswith("Burn"):
            body.append(line(sx(0), sy(burn(0, False)), sx(191), sy(burn(191, False)), "fig-ochre"))
            body.append(line(sx(0), sy(burn(0, True)), sx(191), sy(burn(191, True)), "fig-blue"))
            body.append(text(sx(191) - 4, sy(burn(191, False)) + 16, "39 a second", "fig-label", "end"))
            body.append(text(sx(191) - 4, sy(burn(191, True)) - 8, "135 a second", "fig-label", "end"))
        else:
            def endurance(speed: float, ruptured: bool) -> float:
                return FUEL / burn(speed, ruptured) / 60.0

            body.append(line(sx(0), sy(endurance(0, False)), sx(191), sy(endurance(191, False)),
                             "fig-ochre"))
            body.append(line(sx(0), sy(endurance(0, True)), sx(191), sy(endurance(191, True)),
                             "fig-blue"))
            body.append(text(sx(191) - 4, sy(endurance(191, False)) + 16, "21 min", "fig-label", "end"))
            body.append(text(sx(191) - 4, sy(endurance(191, True)) - 8, "6.1 min", "fig-label", "end"))

        body.append(text((x0 + x1) / 2, y1 + 40, "speed ($00-$BF)", "fig-label", "middle"))

    body.append(text(40, 356,
                     "The burn is (speed >> 3) + 16, plus 96 if $039E says the tank is ruptured. "
                     "One subtraction a second from a 16-bit tank of $BFFF = 49,151 units.",
                     "fig-muted"))
    return document("fig-fuel", w, h,
                    "Fuel burn and endurance against speed",
                    "Two panels sharing the speed axis: the burn per second for an intact and "
                    "a ruptured tank, and the resulting endurance in minutes.", body)


# --- figure 5: the death animation -----------------------------------------
def dying_timeline() -> str:
    w, h = 780, 316
    x0, x1 = 84, 700
    y0, y1 = 82, 236

    def sx(f: float) -> float:
        return x0 + f / 50 * (x1 - x0)

    def sy(v: float) -> float:
        return y1 - v / 0xF8 * (y1 - y0)

    body: list[str] = []
    body.append(text(40, 30, "Death in two phases", "fig-title"))
    body.append(text(40, 50,
                     "Byte 6 falls by 8 a frame; only when it reaches zero does byte 8 climb.",
                     "fig-muted"))

    for value in (0, 0x78, 0xF8):
        y = sy(value)
        body.append(line(x0, y, x1, y, "fig-grid"))
        body.append(text(x0 - 10, y + 3, f"${value:02X}", "fig-tick", "end"))
    for f in (0, 10, 20, 30, 40, 50):
        body.append(text(sx(f), y1 + 18, str(f), "fig-tick", "middle"))
    body.append(line(x0, y1, x1, y1, "fig-axis"))
    body.append(line(x0, y0, x0, y1, "fig-axis"))

    # Legend in the empty top-left, clear of the lines and their end labels.
    body.append(line(40, 66, 68, 66, "fig-ochre"))
    body.append(text(74, 70, "ordinary death ($F8)", "fig-label"))
    body.append(line(280, 66, 308, 66, "fig-blue"))
    body.append(text(314, 70, "quick death ($78)", "fig-label"))

    start = 12
    body.append(text(sx(2), y0 + 14, "byte 6 falls (length varies)", "fig-tick"))
    body.append(line(sx(start), sy(0), sx(43), sy(0xF8), "fig-ochre"))
    body.append(line(sx(start), sy(0), sx(27), sy(0x78), "fig-blue"))
    body.append(text(sx(43) + 6, sy(0xF8) + 4, "freed at 31 frames", "fig-label"))
    body.append(text(sx(27) + 6, sy(0x78) + 16, "freed at 15 frames", "fig-label"))

    body.append(text((x0 + x1) / 2, y1 + 40, "frames after byte 6 reaches zero", "fig-label", "middle"))
    body.append(text(28, (y0 + y1) / 2, "byte 8", "fig-label", "middle",
                     f'transform="rotate(-90 28 {(y0 + y1) / 2:.1f})"'))
    return document("fig-dying", w, h,
                    "The two phases of the dying animation",
                    "The first phase, byte 6 falling, varies with the record's starting altitude. "
                    "The second phase climbs byte 8 and frees the record at $78 for quick-death "
                    "types or $F8 for the rest.", body)


# --- figure 6: the game's own character generator ---------------------------
def font_sheet(memory: dict[int, int]) -> str:
    scale = 3
    glyph, gap = 8 * scale, 6
    cols, rows = 16, 6
    x0, y0 = 56, 64
    w = x0 + cols * (glyph + gap) - gap + 20
    h = y0 + rows * (glyph + 26) - 10
    body: list[str] = []
    body.append(text(40, 30, "The game's message font, re-rendered from $9000-$92FF", "fig-title"))
    body.append(text(40, 50,
                     "96 glyphs of eight bytes; character codes in messages index this table.",
                     "fig-muted"))
    for code in range(96):
        col, row = code % cols, code // cols
        gx = x0 + col * (glyph + gap)
        gy = y0 + row * (glyph + 26)
        for byte_i in range(8):
            bits = memory.get(0x9000 + code * 8 + byte_i, 0)
            for bit in range(8):
                if bits & (0x80 >> bit):
                    body.append(rect(gx + bit * scale, gy + byte_i * scale, scale, scale,
                                     "fig-glyph"))
        if col == 0:
            body.append(text(gx - 8, gy + glyph - 4, f"{code:02X}", "fig-tick", "end"))
    return document("fig-font", w, h,
                    "The message font re-rendered from the game image",
                    "All 96 eight-by-eight glyphs at $9000-$92FF, drawn one-to-one from the "
                    "bytes in the disassembly. The message text in the game indexes these "
                    "glyphs directly.", body)


# --- figure 7: the 32 city layouts ------------------------------------------
def city_maps() -> str:
    """Draw every city sheet: one mark per three-byte record at $9400."""
    cities = json.loads((ROOT / "sources" / "data" / "cities.json")
                        .read_text(encoding="utf-8"))["cities"]
    flags = json.loads((ROOT / "sources" / "data" / "type_tables.json")
                       .read_text(encoding="utf-8"))["tables"]["flags"]["bytes"]

    cols, rows = 8, 4
    panel_w, panel_h = 92, 108
    map_lo, map_hi = 88, 168       # 80 cells covers every record in the sheet
    span = map_hi - map_lo
    x0, y0 = 40, 108
    w = x0 + cols * panel_w + 4
    h = y0 + rows * panel_h + 12

    body: list[str] = []
    body.append(text(x0, 32, "The 32 cities, drawn from the game's own table",
                     "fig-title"))
    body.append(text(x0, 52,
                     "Every mark is one of 1,005 three-byte records in the sheet at "
                     "$9400; x runs east, y south.", "fig-muted"))

    # Legend, one shape per category.
    body.append(rect(40, 69, 5, 5, "fig-mark-plain"))
    body.append(text(51, 76, "structure", "fig-label"))
    body.append(rect(150, 69, 5, 5, "fig-ochre-fill"))
    body.append(text(161, 76, "armed structure", "fig-label"))
    body.append(diamond(305, 72, 3.4, "fig-blue-fill"))
    body.append(text(315, 76, "mobile machine", "fig-label"))
    body.append(circle(465, 72, 3.1, "fig-mark-dockable"))
    body.append(text(475, 76, "dockable special", "fig-label"))

    for city in cities:
        col, row = city["index"] % cols, city["index"] // cols
        px = x0 + col * panel_w
        py = y0 + row * panel_h
        body.append(text(px, py - 10, city["name"], "fig-city"))
        body.append(rect(px, py, span, span, "fig-frame"))
        for type_byte, gx, gy in city["records"]:
            if not (map_lo <= gx <= map_hi and map_lo <= gy <= map_hi):
                continue
            cx, cy = px + (gx - map_lo), py + (gy - map_lo)
            f = flags[type_byte] if type_byte < len(flags) else 0
            if f & 0x80:
                body.append(circle(cx, cy, 3.0, "fig-mark-dockable"))
            elif f & 0x20:
                body.append(diamond(cx, cy, 2.9, "fig-blue-fill"))
            elif f & 0x40:
                body.append(rect(cx - 2, cy - 2, 4, 4, "fig-ochre-fill"))
            else:
                body.append(rect(cx - 1.5, cy - 1.5, 3, 3, "fig-mark-plain"))

    return document("fig-cities", w, h,
                    "All 32 city layouts from the city sheet at $9400",
                    "Thirty-two small maps, one per city, showing every structure in "
                    "the game's own three-byte city records, coloured by category.",
                    body)


# --- the viewport figures ---------------------------------------------------
# The C64 palette (Pepto) in the order the game indexes it.
C64 = [
    "#000000", "#ffffff", "#68372b", "#70a4b2", "#6f3d86", "#588d43",
    "#352879", "#b8c76f", "#6f4f25", "#433900", "#9a6759", "#444444",
    "#6c6c6c", "#9ad284", "#6c5eb5", "#959595",
]

PROFILE_TABLE = 0x2942      # 37 pointers to the profile bytes
PROFILE_LENGTH = 0xC3E4     # 37 lengths, indexed by the record's type
TYPE_FLAGS = 0xC39A         # bit 7 marks a dockable type


def profiles(memory: dict[int, int]) -> list[dict]:
    out = []
    for i in range(37):
        ptr = memory[PROFILE_TABLE + 2 * i] | memory[PROFILE_TABLE + 2 * i + 1] << 8
        length = memory[PROFILE_LENGTH + i]
        out.append({
            "type": i,
            "ptr": ptr,
            "length": length,
            "radii": [memory[ptr + j] & 0x3F for j in range(length)],
            "flags": [memory[ptr + j] >> 6 for j in range(length)],
            "dockable": bool(memory[TYPE_FLAGS + i] & 0x80),
        })
    return out


def screen_map() -> str:
    w, h = 860, 512
    s = 1.10
    x0, y0 = 76, 86
    sw, sh = 320 * s, 200 * s
    body: list[str] = []
    body.append(text(40, 30, "One screen, two graphics modes", "fig-title"))
    body.append(text(40, 50,
                     "A 320 × 200 display: a 16 × 16-cell bitmap viewport above a hires "
                     "instrument band.", "fig-muted"))

    body.append(rect(x0, y0, sw, sh, "fig-frame"))

    vx, vy, vs = x0 + 8 * s, y0 + 8 * s, 128 * s
    hy = y0 + 19 * 8 * s
    body.append(rect(vx, vy, vs, vs, "fig-band"))
    body.append(rect(x0, hy, sw, sh - (hy - y0), "fig-cell"))

    for i in range(1, 40):
        x = x0 + i * 8 * s
        body.append(line(x, y0, x, y0 + sh, "fig-fine"))
    for j in range(1, 25):
        y = y0 + j * 8 * s
        body.append(line(x0, y, x0 + sw, y, "fig-fine"))
    for i in range(1, 16):
        body.append(line(vx + i * 8 * s, vy, vx + i * 8 * s, vy + vs, "fig-fine"))
        body.append(line(vx, vy + i * 8 * s, vx + vs, vy + i * 8 * s, "fig-fine"))
    body.append(rect(vx, vy, vs, vs, "fig-ochre"))

    body.append(text(vx + vs / 2, vy + 16, "viewport — 16 × 16 cells", "fig-label", "middle"))
    body.append(text(vx + vs / 2, vy + 31, "matrix $CC29 · bitmap $E148 · eight bytes a cell",
                     "fig-tick", "middle"))
    body.append(text(x0 + sw / 2, hy + (y0 + sh - hy) / 2 + 4,
                     "hires message and status band — rows 19–24", "fig-label", "middle"))

    body.append(text(x0 - 6, y0 + 4, "raster 51", "fig-tick", "end"))
    body.append(text(x0 - 6, y0 + sh - 2, "250", "fig-tick", "end"))
    body.append(line(x0, hy, x0 + sw, hy, "fig-axis"))
    body.append(text(x0 + sw, hy - 6, "raster 202: the rest of the screen is hires",
                     "fig-tick", "end"))
    body.append(text(x0 + sw / 2, y0 + sh + 16,
                     "40 cells across × 25 down; each cell is 8 × 8 pixels", "fig-muted",
                     "middle"))

    # Memory map.
    mx, mw = 470, 330
    boxes = [
        ("$0400–$0BFF", "render buffer", "2,048 bytes · 128 rows of 16"),
        ("$E000–$FFFF", "bitmap", "8,192 bytes · eight bytes a cell"),
        ("$CC00–$CFE7", "matrix", "1,000 bytes · two colours a cell"),
        ("$D800–$DBFF", "colour RAM", "1,000 bytes · pair 11's colour, even in bitmap mode"),
    ]
    by = y0
    for addr, name, note in boxes:
        body.append(rect(mx, by, mw, 50, "fig-cell", 2))
        body.append(text(mx + 12, by + 19, name, "fig-label"))
        body.append(text(mx + mw - 12, by + 19, addr, "fig-tick", "end"))
        body.append(text(mx + 12, by + 34, note, "fig-tick"))
        by += 58
    body.append(text(mx, by + 8, "The VIC sees bank $C000–$FFFF ($DD00 = %00).", "fig-muted"))
    body.append(text(mx, by + 24, "$D018 = $38 puts the matrix at $CC00 and the bitmap at $E000.",
                     "fig-muted"))

    # The cell-major layout along the bottom.
    top = 380
    body.append(text(40, top, "One cell is eight consecutive bytes of bitmap", "fig-title"))
    body.append(text(40, top + 18,
                     "The buffer is stored by scanline; the bitmap is stored by cell. The blit joins them.",
                     "fig-muted"))
    cx, cy = 52, top + 46
    cw, ch = 44, 30
    for i in range(8):
        x = cx + i * (cw + 4)
        body.append(rect(x, cy, cw, ch, "fig-cell-type" if i % 2 == 0 else "fig-cell", 2))
        body.append(text(x + cw / 2, cy - 6, f"byte {i}", "fig-tick", "middle"))
        body.append(text(x + cw / 2, cy + ch + 14, str(i), "fig-tick", "middle"))
    body.append(text(cx + 8 * (cw + 4) + 2, cy + ch / 2 + 4, "consecutive in the bitmap",
                     "fig-label"))
    body.append(text(cx, cy + ch + 36,
                     "The eight bytes are scanlines 0–7 of one cell; each byte is four fat "
                     "pixels — four two-bit pairs.", "fig-muted"))

    # The cell row and its stride.
    sx, sy = 560, cy - 2
    for i in range(16):
        x = sx + i * 17
        body.append(rect(x, sy, 14, 26, "fig-cell", 1))
    body.append(text(sx + 16 * 17 / 2, sy - 8, "16 cells = one viewport cell row", "fig-tick",
                     "middle"))
    body.append(text(sx, sy + 42, "$E148", "fig-tick"))
    body.append(text(sx + 15 * 17 + 14, sy + 42, "$E1C0", "fig-tick", "end"))
    body.append(text(sx, sy + 60, "next cell row: +320 bytes ($E288)", "fig-muted"))
    body.append(text(sx, sy + 76, "128 buffer bytes become 16 cells", "fig-muted"))
    return document("fig-screen", w, h,
                    "The viewport screen layout and memory map",
                    "The 320 by 200 display with its 16 by 16-cell viewport and a hires band at the "
                    "bottom, beside the memory map of the bitmap, matrix, colour RAM and render "
                    "buffer, and a diagram of the eight bytes that make one bitmap cell.", body)


def profile_gallery(memory: dict[int, int]) -> str:
    profs = profiles(memory)
    cols, rows = 7, 6
    pw, ph = 100, 96
    x0, y0 = 40, 96
    w = x0 + cols * pw + 20
    h = y0 + rows * ph + 58
    s = 0.22
    body: list[str] = []
    body.append(text(40, 30, "The 37 shapes, painted from the profile tables", "fig-title"))
    body.append(text(40, 50,
                     "Every profile byte is a cylinder radius: the low six bits give it, the top "
                     "two bits select a blink phase.", "fig-muted"))

    for p in profs:
        col, row = p["type"] % cols, p["type"] // cols
        px, py = x0 + col * pw, y0 + row * ph
        cx, base = px + pw / 2, py + 68
        pts = []
        for j, r in enumerate(p["radii"]):
            pts.append((cx - r * s, base - j * s))
        for j in range(len(p["radii"]) - 1, -1, -1):
            pts.append((cx + p["radii"][j] * s, base - j * s))
        poly = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        body.append(f'<polygon points="{poly}" class="fig-cell-type"/>')
        body.append(line(cx - 14, base, cx + 14, base, "fig-hair"))
        body.append(text(cx, py + 84, f"{p['type']} · {p['length']}", "fig-tick", "middle"))
        if p["dockable"]:
            body.append(circle(px + pw - 12, py + 14, 3.6, "fig-mark-dockable"))

    fy = y0 + rows * ph + 22
    body.append(rect(40, fy - 10, 10, 10, "fig-cell-type", 2))
    body.append(text(58, fy, "a silhouette", "fig-label"))
    body.append(circle(170, fy - 5, 3.6, "fig-mark-dockable"))
    body.append(text(180, fy, "a dockable type (flag $80 in $C39A)", "fig-label"))
    body.append(text(40, fy + 22,
                     "Type number · profile length in rows. Scale is uniform: the shapes are "
                     "drawn with the same radius units as the projection uses.", "fig-muted"))
    return document("fig-profiles", w, h,
                    "All 37 building profiles",
                    "Thirty-seven silhouettes drawn from the radius bytes of the profile table, "
                    "one panel per record type, with the profile length beneath. Dockable types "
                    "are ringed.", body)


def lathe(memory: dict[int, int]) -> str:
    """Project one real profile and draw the spans that make it."""
    prof = profiles(memory)[23]
    distance = 640                    # 2.5 cells: distance is 8.8 in the record
    q = min(0x8000 // distance, 0x1FF)
    base_row = 96 + (((32) * (q >> 1)) >> 8)
    sun_off = 120                     # low byte of (bearing - sun - 2), signed
    tone_left, tone_right = "$AA", "$55"
    # $AA is %10101010 (pair 10 -> low nibble of the matrix byte);
    # $55 is %01010101 (pair 01 -> high nibble of the matrix byte).
    high, low = C64[8], C64[11]       # stand-ins for the two palette nibbles
    blink_ink = C64[3]                # pair 11 -> colour RAM, held at 3
    frame = 0x1E                      # $12 in the frame shown

    # Walk the profile exactly as the routine does: one screen row per 2*distance units.
    rows = []
    y, idx, frac = base_row, 0, 0
    while y >= 0 and idx < prof["length"]:
        r = prof["radii"][idx]
        wcol = (r * q) >> 8
        # $0DC0[w] = signed high byte of 2(w+1)$F8, so the terminator moves by
        # $F8/128 of the half-width; it lands on the centre column at $F8 = $78.
        bnd = -wcol + (((wcol + 1) * sun_off) >> 7)
        rows.append({"row": y, "r": r, "w": wcol, "flag": prof["flags"][idx], "bnd": bnd})
        y -= 1
        idx += (2 * distance) >> 8

    w, h = 780, 480
    body: list[str] = []
    body.append(text(40, 30, "From a profile to a painted tower", "fig-title"))
    body.append(text(40, 50,
                     "Type 23 at a distance of $0280 (2.5 cells), level with the ship. "
                     "Q = floor($8000 ÷ 640) = 51.", "fig-muted"))

    # Left: the silhouette and its radius scale.
    spx, spbase, ss = 150, 372, 1.02
    pts = [(spx - r * ss, spbase - j * ss) for j, r in enumerate(prof["radii"])]
    pts += [(spx + prof["radii"][j] * ss, spbase - j * ss)
            for j in range(len(prof["radii"]) - 1, -1, -1)]
    body.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" '
                'class="fig-cell-type"/>')
    body.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" '
                'class="fig-ochre"/>')
    body.append(line(spx - 68, spbase, spx + 68, spbase, "fig-axis"))
    for j in (0, 64, 128, 192, 255):
        yy = spbase - j * ss
        body.append(line(spx - 72, yy, spx - 62, yy, "fig-hair"))
        body.append(text(spx - 76, yy + 3, str(j), "fig-tick", "end"))
    body.append(text(spx - 76, spbase + 20, "profile row", "fig-tick", "end"))
    body.append(text(spx, spbase + 20, "radius 48 at the base", "fig-tick", "middle"))
    body.append(text(spx, spbase - 255 * ss - 12, "255 rows, one byte each", "fig-label",
                     "middle"))

    # Middle: the spans, one per few rows.
    mx = 372
    body.append(text(290, 94, "The lathe: one span a screen row", "fig-label"))
    body.append(line(mx, 104, mx, 284, "fig-hair"))
    body.append(text(mx, 296, "column 32", "fig-tick", "middle"))
    picked = rows[::6]
    for k, rr in enumerate(picked):
        yy = 104 + k * 20
        left, right = mx - rr["w"] * 4, mx + rr["w"] * 4
        bnd = mx + rr["bnd"] * 4
        if rr["w"] == 0:
            continue
        body.append(f'<rect x="{left:.1f}" y="{yy}" width="{max(bnd - left, 1):.1f}" '
                    f'height="12" fill="{high}"/>')
        body.append(f'<rect x="{bnd:.1f}" y="{yy}" width="{max(right - bnd, 1):.1f}" '
                    f'height="12" fill="{low}"/>')
        if k % 2 == 0:
            body.append(text(left - 6, yy + 10, f"{rr['r']}", "fig-tick", "end"))
    body.append(text(290, 314, "radius · left fill $AA, right fill $55", "fig-muted"))
    body.append(text(290, 330, "$F8 = $78 puts the boundary on the centre column.", "fig-muted"))

    # Right: the viewport as the buffer holds it.
    vx, vy, ps = 500, 70, 2.0
    body.append(f'<rect x="{vx}" y="{vy}" width="{64 * ps}" height="{128 * ps}" fill="#000000"/>')
    body.append(f'<rect x="{vx}" y="{vy + 96 * ps}" width="{64 * ps}" height="{ps}" '
                f'fill="{low}"/>')
    for rr in rows:
        ytop = vy + rr["row"] * ps
        left, right = 32 - rr["w"], 32 + rr["w"]
        bnd = 32 + rr["bnd"]
        lit = (rr["flag"] + frame) & 0x20
        col_l = blink_ink if lit else high
        col_r = blink_ink if lit else low
        body.append(f'<rect x="{vx + max(left, 0) * ps:.1f}" y="{ytop:.1f}" '
                    f'width="{max(min(bnd, right) - max(left, 0), 0) * ps:.1f}" height="{ps}" '
                    f'fill="{col_l}"/>')
        body.append(f'<rect x="{vx + max(bnd, left) * ps:.1f}" y="{ytop:.1f}" '
                    f'width="{max(min(right, 64) - max(bnd, left), 0) * ps:.1f}" height="{ps}" '
                    f'fill="{col_r}"/>')
    body.append(rect(vx, vy, 64 * ps, 128 * ps, "fig-frame"))
    hy = vy + 96 * ps
    body.append(text(vx + 64 * ps + 10, hy - 6, "horizon, row 96", "fig-tick"))
    body.append(line(vx + 64 * ps + 2, hy, vx + 64 * ps + 8, hy, "fig-axis"))
    body.append(text(vx + 64 * ps + 10, hy + 20, f"base, row {base_row}", "fig-tick"))
    body.append(text(vx + 64 * ps + 10, vy + rows[-1]["row"] * ps + 4,
                     f"top, row {rows[-1]['row']}", "fig-tick"))
    body.append(text(vx + 64 * ps / 2, vy + 128 * ps + 16, "64 × 128 fat pixels", "fig-tick",
                     "middle"))

    body.append(text(40, 416,
                     "Height in rows = 128 × length ÷ distance. Half-width in columns = "
                     "128 × radius ÷ distance.", "fig-label"))
    body.append(text(40, 432,
                     "The same factor on both axes, so the silhouette is never stretched.",
                     "fig-muted"))
    body.append(text(40, 448,
                     f"Every span is two fills: {tone_left} (pair 10) takes the matrix byte's low "
                     f"nibble on the left; {tone_right} (pair 01) its high nibble on the right.",
                     "fig-muted"))
    body.append(text(40, 464,
                     "Rows where (profile flags + $12) & $20 is set are filled with $FF — pair "
                     "11, colour RAM: colour 3. Shown at $12 = $1E.", "fig-muted"))
    return document("fig-lathe", w, h,
                    "One profile projected and painted",
                    "Left: the type-23 profile silhouette at its true proportions. Middle: the "
                    "spans the lathe draws row by row, with the two-colour terminator. Right: the "
                    "same structure as the buffer holds it, with the horizon at row 96.", body)


def sun_palette(memory: dict[int, int]) -> str:
    import math
    w, h = 860, 450
    body: list[str] = []
    body.append(text(40, 30, "The city's colours turn with the sun", "fig-title"))
    body.append(text(40, 48,
                     "Each viewport cell's matrix byte is $C298[(city & 3) × 16 + (sun >> 5)].",
                     "fig-muted"))
    body.append(text(40, 64,
                     "Pair 01 (the $55 fill) takes the high nibble; pair 10 (the $AA fill) takes "
                     "the low nibble.", "fig-muted"))

    # The sun dial.
    cx, cy, r = 120, 214, 62
    body.append(circle(cx, cy, r, "fig-frame"))
    for k in range(16):
        a = k / 16 * 2 * math.pi - math.pi / 2
        x1, y1 = cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        body.append(line(x1, y1, x2, y2, "fig-axis" if k % 4 == 0 else "fig-hair"))
        lx, ly = cx + (r + 12) * math.cos(a), cy + (r + 12) * math.sin(a) + 3
        if k % 4 == 0:
            body.append(text(lx, ly, str(k), "fig-tick", "middle"))
    body.append(text(cx, cy - 4, "1024 s", "fig-label", "middle"))
    body.append(text(cx, cy + 12, "a revolution", "fig-tick", "middle"))
    body.append(text(cx, cy + r + 34, "a phase every 64 s", "fig-tick", "middle"))
    body.append(text(cx, cy + r + 50, "sun bearing >> 5", "fig-tick", "middle"))

    # Four palette rows.
    px, chip_w, chip_h, gap = 250, 26, 24, 3
    for g in range(4):
        py = 92 + g * 82
        body.append(text(px, py + chip_h + 4, f"group {g}", "fig-label"))
        body.append(text(px, py + chip_h + 20, f"cities {g}, {g + 4}, {g + 8} …", "fig-tick"))
        for ph in range(16):
            byte = memory[0xC298 + g * 16 + ph]
            hi, lo = byte >> 4, byte & 0x0F
            x = px + 92 + ph * (chip_w + gap)
            body.append(f'<rect x="{x}" y="{py}" width="{chip_w}" height="{chip_h / 2 - 1}" '
                        f'fill="{C64[hi]}"/>')
            body.append(f'<rect x="{x}" y="{py + chip_h / 2 + 1}" width="{chip_w}" '
                        f'height="{chip_h / 2 - 1}" fill="{C64[lo]}"/>')
            if g == 0:
                body.append(text(x + chip_w / 2, py - 6, str(ph), "fig-tick", "middle"))
        body.append(text(px + 92, py + chip_h + 16,
                         " ".join(f"{memory[0xC298 + g * 16 + ph]:02X}" for ph in range(16)),
                         "fig-tick", "", 'font-family="monospace"'))

    body.append(text(40, 398,
                     "Each chip is one matrix byte: high nibble above, low nibble below.",
                     "fig-label"))
    body.append(text(40, 414,
                     "The high nibble colours pair 01, the $55 fill; the low nibble pair 10, "
                     "the $AA fill.",
                     "fig-label"))
    body.append(text(40, 430,
                     "Pair 11 — blink rows, aperture, stars, debris — is colour RAM, written as 3.",
                     "fig-label"))
    return document("fig-sun", w, h,
                    "The sun-driven viewport palettes",
                    "A sixteen-phase sun dial beside four rows of sixteen palette bytes from the "
                    "table at $C298. Every viewport cell carries the byte; its two nibbles are the "
                    "two body tones, so both faces of a building shift hue as the sun turns.", body)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    memory: dict[int, int] = {}
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from listing import load_byte_map
        memory = load_byte_map(sorted((ROOT / "sources").glob("dis_*.txt")))
    except Exception as exc:  # the font sheet is optional; the rest still builds
        print(f"font sheet skipped: {exc}")

    figures = {
        "record-table.svg": record_table(),
        "docking.svg": docking_envelope(),
        "aperture.svg": aperture_timeline(),
        "fuel.svg": fuel_burn(),
        "dying.svg": dying_timeline(),
        "cities.svg": city_maps(),
    }
    if memory:
        figures["font.svg"] = font_sheet(memory)
        figures["screen.svg"] = screen_map()
        figures["profiles.svg"] = profile_gallery(memory)
        figures["lathe.svg"] = lathe(memory)
        figures["sun.svg"] = sun_palette(memory)
    for name, svg in figures.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
