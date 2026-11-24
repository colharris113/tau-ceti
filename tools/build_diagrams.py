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
    }
    if memory:
        figures["font.svg"] = font_sheet(memory)
    for name, svg in figures.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
