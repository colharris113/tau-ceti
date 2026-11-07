# Rendering Pipeline

One bitmap, four raster bands, and a small canvas doing the hard work.

---

Tau Ceti draws everything into a single 320x200 multicolour bitmap. There is no character mode, no
sprite hardware in use for the world, and no separate screen for the instruments: gauges, text, radar
and the view of the city are all pixels in the same 8000-byte picture. What makes that workable is
the raster split, which changes the VIC-II's mode partway down the screen and gives the display
different properties in different bands.

## The screen

| Setting | Value | Meaning |
|---|---|---|
| VIC bank | 3 | $DD00 low bits %00, so the VIC sees $C000-$FFFF |
| Bitmap | $E000-$FF3F | 8000 bytes, 320x200 |
| Video matrix | $CC00 | 1000 bytes, one per 8x8 cell |
| Colour RAM | $D800 | 1000 bytes |
| $D018 | $38 | matrix at $CC00, character base at $D800 (unused in bitmap mode) |
| $D016 | $18 / $08 | multicolour on in the top band, off below |

The mode is multicolour bitmap: two bits per pixel, four colours per 8x8 cell, with the cell's
colour byte at $CC00 supplying three of them. That is 16 colours with four on screen per cell at
once - not "25 colours", and not a 160x200 mode. The bitmap is 320x200 with double-width pixels in
the multicolour bands.

## The four bands

The raster handler at $3903 runs four times per frame and changes the display each time. The values
per stage are in three tables at $395C, $3960 and $3964:

| Stage | Fires at line | $D016 | $D011 |
|---|---|---|---|
| 0 | - | $18 (multicolour) | $38 |
| 1 | 202 | $08 (hires) | $38 |
| 2 | 248 | $08 | $B0 |
| 3 | 20 | $08 | $30 |

The visible result is a multicolour picture area with hires bands above and below - the top band for
the status line and instruments, the bottom for the panel. Switching multicolour off for those
bands is what makes the small text legible: in multicolour a glyph pixel is two pixels wide, and in
hires it is one.

Because $D018 never changes, all four bands share the same bitmap and matrix. The only thing that
changes is how the VIC interprets the bits.

## The view: canvas, painter, blitter

The city view is not drawn straight into the bitmap. It is drawn into a small canvas and copied
out.

The canvas at $0400 is eight rows of 64 bytes, two bits per pixel - about the size of one band. The
routine at $40AC clears it to $55. The painter at $3F93 walks the forty-eight object records at
$0E00 and plots each one into the canvas according to its type, position and depth.

Then the blitters move it. $3F29 copies the canvas into eight bands of the bitmap at $E870, $E9B0,
$EAF0, $EC30, $ED70, $EEB0, $EFF0 and $F130. A second blitter at $223E takes a wider source range,
$0400-$0BFF, and writes strips to $E148, $E288, $E3C8 and onward, splitting even and odd destination
bytes - a different mapping for a different part of the display.

This is where the perspective lives. The painter and the blitters do the scaling; the object records
carry a 16-bit X position and a depth, and the projection helpers at $26CC and $26D4 turn those into
screen offsets. There is no 768-byte perspective table and no $14D00: an earlier version of this
chapter invented both.

## The instruments

Everything in the panel is drawn by ordinary code writing into the bitmap:

- **Five bar gauges**, drawn by $3769 from the variables listed in [Game State](game-state.md) -
  four bytes per row, six rows per bar, a ramp table for partial widths.
- **The status line**, written by $4906 at row 3 from column $1E: DEMO, LAUNCHED, LANDED or DOCKED.
- **The ammo readouts**, three single glyphs at column $23 from $3500/$3514/$350A.
- **The message log**, filled by the interpreter at $41F7 and scrolled by the copies at $40E4.
- **Text in general**, through the glyph blitter at $3E17, which copies 8-byte patterns into the
  bitmap at a computed cell address.

## What the screen shows

The layout below is the manual's description, checked against the screen but not against the code
that draws each region - treat it as a map of the display, not as a list of routines:

| Region | Contents |
|---|---|
| top band | status line, view direction, clock |
| main view | the city, drawn from the object records |
| instruments | compass, the two direction finders, radar |
| gauges | height, one unidentified gauge, fuel, one unidentified gauge, speed |
| supply box | MIS, AMM, FLAR |
| message log | queued text messages |

> [!NOTE]
> This chapter previously described a "12-screen UI", 25 colours, hardware scrolling through
> $D025-$D026 and a sprite system with eight numbered sprites. None of that is in the machine: the
> register table was wrong (it had $D011 as border colour and $D018 as a raster register), there is
> no hardware scroll, and the view is redrawn. The one place the machine does use sprites is the
> bottom border - see [The Border Banner](border-banner.md).

---

[Back to the overview](../README.md)
