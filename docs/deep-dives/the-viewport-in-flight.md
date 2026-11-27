# The viewport in flight

The flight view is a 128 × 128 square in the top-left of the screen. There is no framebuffer for it: the game paints a two-kilobyte row buffer, then transposes that buffer into the cell-major bitmap the VIC reads. Every building in it is a stack of horizontal spans generated from a one-byte-per-row profile. This article follows one frame from the record table to the raster.

Tau Ceti's viewport looks like a conventional 3D view, but nothing in it is a polygon and nothing is texture-mapped. What the game calls drawing is a loop over forty-eight records, a sorted display list, and a lathe: one profile byte per screen row, extruded left and right from a centre column. The whole scene is built in ordinary RAM and copied into bitmap memory at the end of the frame.

## One screen, two modes

The screen is the standard 320 × 200 display, and almost all of it is bitmap. The VIC is pointed at bank `$C000`–`$FFFF` by clearing the low two bits of `$DD00` at `$5675`, and `$D018` is set to `$38` at `$5688`, which puts the character matrix at `$CC00` and the bitmap at `$E000`.

The flight view occupies sixteen by sixteen cells — 128 × 128 pixels — one cell in from the top and left. Its matrix therefore begins at `$CC29` (cell 41) and its bitmap at `$E148` (byte 328, eight bytes into cell 41). The one-cell inset is a frame: the view sits inside the instrument surround rather than against the screen edge.

Two graphics modes share the screen. The raster handler at `$3902` reads `$D016` from the table at `$395C`:

| Raster line | `$D016` | Mode | What is on screen |
| --- | --- | --- | --- |
| 48 (upper border) | `$18` | Multicolour on | The viewport and everything down to raster 201 |
| 202 | `$08` | Multicolour off, hires | The message and instrument band, rows 19–24 |

So the viewport is a **multicolour bitmap**. In that mode a cell has four colours, but not the four a multicolour *text* cell has: `$D021` for pair `00`, the matrix byte's high nibble for pair `01`, its low nibble for pair `10`, and the colour-RAM nibble for pair `11`. `$D022` and `$D023` play no part. The instrument band below is a hires bitmap, which is why the panel edges can be single pixels while the view's "pixels" are fat.

![Screen, viewport and bitmap memory layout](../assets/diagrams/screen.svg)

*The 320 × 200 display, the 16 × 16-cell viewport, and the memory map. The bitmap is cell-major: one cell is eight consecutive bytes, one per scanline. The 2 KB row buffer is scanline-major, so the two layouts have to be transposed every frame.*

## The 2K buffer

The scene is painted into `$0400`–`$0BFF`: 128 rows of 16 bytes. Row *r* begins at `$0400 + 16r`, and each byte holds four multicolour pixels. That is 64 fat pixels (128 screen pixels) across and 128 rows down. The buffer is exactly the viewport, stored the way a painter wants it — one contiguous row at a time — not the way the VIC wants it.

Every frame begins with the clear at `$21DF`:

- Rows 0–95, the sky, are zeroed: pair `00`, the background colour.
- Rows 96–127, the ground, are filled with `$55`: pair `01`, which takes the high nibble of the matrix byte.
- Row 96 is then forced to `$55` across all sixteen bytes. That is the horizon line, and it never moves.

The horizon is fixed because the ship never pitches. Altitude changes where objects sit relative to row 96, not where the horizon is: 96 of the 128 rows are sky, so the horizon sits three-quarters of the way down the view at all times.

Three passes then draw into the buffer before any object:

1. `$20B5` plots the sun, if the sun's bearing falls inside the view. Its disc is built from the pattern table at `$C47E`.
2. `$2176` plots the stars from a fixed table at `$BE00`. Each star is tested against the same view angle and drawn as a two-bit pixel with the masks at `$21D7` (`C0 30 0C 03`).
3. `$29B6` sets up the frame: the ship's cell and sub-cell, the view angle, the sun angle and the two body fills.

The ship's cell is copied to `$DC`/`$DD` and its sub-cell to `$DE`/`$DF`. The view angle is built at `$29CA`:

```asm
LDA $0380      ; spin offset
ASL A
PHP            ; keep the ninth bit of 2 × spin
CLC
ADC $0338      ; + heading, low
STA $DA
LDA #$00
ROL A          ; carry out of the low byte
PLP
ADC $0339      ; + heading, high + both carries
AND #$01
STA $DB
```

`$DA`/`$DB` is the **left edge** of the view, not its centre. The view is 64 columns wide, so column 32 is the nose. The flight routine confirms the relationship at `$4EF3`, where motion is advanced by the heading plus `$20`: the direction of travel lands in the centre column. An object at bearing *b* is drawn at column *b* − `$DA`; the centre of the picture is `$DA + $20`.

`$0380` is the spin offset. It is normally zero, but while the spin timer at `$036A` runs, `$3B66` adds `$40` to it every frame. The view angle is `$0338 + 2 × $0380`, so the world turns 45° a frame while the heading, and the ship's motion, stay put.

## Who is in the list

The viewport's record pass begins at `$2A4D` — the scene setup falls straight into it — and walks the forty-eight records at `$0E00`. It skips any record whose byte 0 has bit 7 set: `$80`–`$FF` is a free slot, and the low six bits still remember what used to be there. A record with `$40`–`$7F` is dying and is drawn as debris; `$00`–`$3F` is live. The same top-two-bits test drives the AI dispatch at `$43CF` later in the frame.

Every live record first has bits 6 and 7 of byte 3 cleared. Then its position is subtracted from the ship's:

```asm
LDA ($61),Y    ; byte 4, sub-cell x
SEC
SBC $DC
TAX
LDA ($61),Y    ; byte 1, cell x
SBC $DD
```

The same runs for y. If either axis' high byte is `$10` or more, the record is more than sixteen cells away and is skipped. That is a coarse box, not the visible range: it is the same test that feeds the scanner.

A record inside the box gets its distance worked out at `$2ADE`, and then the pass at `$2B60` — which also runs the docking test — scales that distance and stores the 16-bit product in record bytes 12 and 13. A product of `$1000` or more means the object is too far away and the record is dropped. A product below 128 is an object almost on top of the ship: it goes through the docking and collision tests and never enters the display list. Everything in between goes to the bearing calculation and list insertion at `$2CC0`.

### The forward half

The list itself lives at `$0D00`. Each entry is four bytes: the record pointer, then the scaled distance. Insertion is at `$2D5F`, and it contains the viewport's culling rule:

```asm
SEC
SBC $DA        ; bearing low − view low
PHP
CLC
ADC #$60
TXA
ADC #$00
PLP
SBC $DB        ; bearing high − view high
AND #$01
BNE next       ; bit 8 set: behind the ship
```

The arithmetic computes `bearing − view + $60`, modulo 512. The entry is kept only if the ninth bit is clear, which means **everything in the forward 180° is kept and everything behind is dropped**. The `$60` bias is what centres that half-circle on the nose: the window runs from 128 units to the left of the direction of travel to 128 to the right. The same insert stores the bearing in record bytes 10 and 11, where the painter reads it later.

The list has room for 32 entries: `$0D00` to `$0D7F`, with the width and terminator ramps immediately after at `$0D80`. There is no count or overflow check — a city never puts more than about twenty records in the forward half, so the list and the ramps do not collide.

## Painter's algorithm, farthest first

The list is not sorted. At `$2DA7` the painter repeatedly scans what is left, finds the entry with the largest distance, and draws it. That is a conventional painter's algorithm, done by selection rather than by sorting: each pass marks its victim by zeroing the entry's distance bytes, so the next pass cannot pick it again.

For the chosen entry the painter computes

```text
Q = floor($8000 ÷ distance)
```

with nine shift-and-subtract iterations at `$2E1F`. `Q` is the projection factor. It is stored in `$F4`/`$F5`, and a margin of `Q >> 2` is kept at `$26` for the off-screen target indicator.

The record's bearing, minus the view angle, gives `$F6`/`$F7`: the object's horizontal angle relative to the left edge of the view. `$F6` is used directly as a buffer column, which is why the left edge — not the centre — is the reference. Farthest-first ordering is the only occlusion in the renderer. There is no z-buffer and no per-pixel depth test: a nearer object is simply painted later, over the pixels of a farther one.

## The lathe

An object's vertical position is computed at `$2EC9`. Byte 6 of the record is the object's base altitude, so:

```text
base row = 96 + floor( (ship altitude − base altitude + $20) × (Q ÷ 2) ÷ 256 )
```

The `$20` is a fixed eye-height offset; the `Q ÷ 2` turns an altitude difference into screen rows at the same scale as the width. For a level object at distance 640, `Q` = 51, the offset is three rows, and the base sits at row 99. If the product is still negative after the 96 is added, the object is above the top of the view and the painter skips it.

The shape comes from the profile table. The pointer table at `$2942` gives the address of each type's profile, and the length table at `$C3E4` gives its number of rows. Each profile byte encodes two things:

| Bits | Meaning |
| --- | --- |
| 0–5 | Radius of the cylinder at this row, in profile units |
| 6–7 | Blink phase: which frame counter bit makes this row flash |

The radius is the half-width. The renderer walks the profile from the base row upwards:

```text
row    = base row
index  = 0                 ; 16-bit fixed point
repeat:
    radius = profile[index >> 8] & $3F
    half   = radius × Q ÷ 256
    draw a span from column $F6 − half to column $F6 + half
    row   = row − 1
    index = index + 2 × distance
until (index >> 8) ≥ profile length, or row < 0
```

The index is a fixed-point accumulator: its high byte selects the profile row, and each screen row adds `2 × distance` to it. That is the vertical scale — *L* profile rows occupy `128 × L ÷ distance` screen rows. The same factor scales the radius: `128 × r ÷ distance`. Height and width use the same constant, so a building never stretches.

![Silhouettes of the 37 object types](../assets/diagrams/profiles.svg)

*All 37 profiles, drawn from the radius bytes at the addresses in `$2942`. The number under each silhouette is the type and its profile length in rows. Ringed types are dockable. The horizontal scale is the same for every type: a large radius is a wide building, not a tall one.*

There is one more trick: if the base row is at or below the bottom of the buffer, the game walks the profile upwards without drawing until the row reaches `$7F` at `$2F60`. That is how a building you are flying through is clipped at the bottom of the screen instead of being skipped altogether.

The spans themselves are written at `$305D`. Two ramps are built first at `$2FD4`:

- `$0D80[n]` is the high byte of `(n + 1) × min(Q, $FF)`, the half-width in columns for radius *n*. The loop uses `$FF` when the high byte of `Q` is nonzero.
- `$0DC0[n]` is the high byte of `2 × (n + 1) × $F8` — where the light boundary falls across that width.

The span is then `left = $F6 − width` to `right = $F6 + width`, with the boundary between the two fills at `left + $0DC0[width]`. The ends are cut in with the byte masks at `$3305` and `$330A`, because a span rarely begins or ends on a whole byte boundary.

![A building profile projected as two-tone spans](../assets/diagrams/lathe.svg)

*Type 23 at a distance of 640, level with the ship. Left: the profile at its true proportions. Middle: one span per few screen rows, showing how the width comes from the radius and the terminator moves across it. Right: the same structure as the buffer holds it, with the fixed horizon at row 96 and the base at row 99.*

## Where the light comes from

The two fills are not shades chosen per building. They are two values in the buffer, and the split between them is the game's entire lighting model. The renderer writes only four byte values, and the VIC's multicolour-bitmap rules turn each into a colour:

| Buffer byte | Bit pairs | Colour shown |
| --- | --- | --- |
| `$00` | `00 00 00 00` | `$D021`, black |
| `$55` | `01 01 01 01` | high nibble of the cell's matrix byte |
| `$AA` | `10 10 10 10` | low nibble of the cell's matrix byte |
| `$FF` | `11 11 11 11` | low nibble of colour RAM |

That is why the scene is built from two-bit patterns: the span fill chooses *which* of the two body colours a face gets, while the palette byte at `$C298` decides what those colours are.

The scene setup at `$29EE` chooses the left and right fills by the sun's bearing. In the normal case:

| Sun bearing (`$D9:$D8`) | Left fill | Right fill |
| --- | --- | --- |
| `$0000`–`$0001`, `$0180`–`$01FF` | `$00` | `$00` |
| `$0002`–`$001F`, `$0160`–`$017F` | `$55` | `$00` |
| `$0020`–`$003F`, `$0140`–`$015F` | `$AA` | `$00` |
| `$0040`–`$013F` | `$AA` | `$55` |

`$AA` is the low-nibble tone, `$55` the high-nibble tone, and `$00` black. The four combinations step around the circle with the sun, so the city passes through a dark phase, a one-tone phase and a two-tone phase as the day turns. In the dark phase a silhouette is solid `$00`: above the horizon it merges with the black sky, and the part below is a black cut-out against the ground. Only its blinking rows remain visible. While IR is active, or while the `$0356` event timer is running, both fills are `$AA`; the palette lookup is also bypassed and every cell gets `$44`, whose low nibble is 4 — a flat purple silhouette.

The terminator is computed per object at `$2FA6`:

```text
$F8 = low byte of (object bearing − sun bearing − 2)
$F9 = ninth bit of the same difference
```

`$F8` scales the boundary ramp `$0DC0`, so the light line sweeps across the span as the sun moves; `$F9` swaps the two fills when the sun is on the other side. With `$F8 = $78` the boundary falls near the centre of the span — the moment shown in the lathe figure.

The visible shadow is the dark side of the cylinder. The code turns the sun angle into one boundary lookup per shaded row. It writes the interiors of the two spans a byte at a time, painting four multicolour pixels per store, and uses masks where an edge or the light boundary cuts through a byte. This keeps the lighting in the same pass as the shape. The ground fill carries no cast shadows. When buildings overlap in the view, the painter draws the nearer one over the farther one.

### Blinking rows

Not every row is a plain span. The top two bits of a profile byte select a blink phase. At `$3072` the game tests

```text
((profile flags) + frame counter) & $20
```

where *profile flags* is the top two bits of the profile byte shifted down to 0–3, and the frame counter is `$12`. When the test is set both fills become `$FF`. `$FF` is pair `11`, which in a multicolour bitmap takes its colour from the low nibble of **colour RAM**. The palette routine writes 3 into every viewport cell, so blinking rows are always colour 3. Pair `11` is the third per-cell colour, reserved here for lights: the stars and debris are drawn with the same pair.

### The matrix palette

The two body colours come from a 64-byte table at `$C298`. It is indexed at `$2753` as

```text
(city & 3) × 16 + (sun bearing >> 5)
```

so there is one row of sixteen palette bytes for each of four city groups, and the row advances through sixteen phases as the sun turns. Each byte holds both body tones: the high nibble is the `$55` face, the low nibble the `$AA` face. In IR the lookup is skipped and every cell gets the fixed byte `$44`. The bytes are written over the viewport's sixteen rows of sixteen cells at `$277E` — the matrix at `$CC29`, and, in the same loop, 3 into colour RAM at `$D829`. The refresh is not per frame: `$039C` is set when the sun crosses a phase boundary, roughly every 64 seconds, and the palette is rewritten then.

![The 16 sun phases and the four city palettes](../assets/diagrams/sun.svg)

*Four groups of sixteen palette bytes, one per sun phase. The high nibble is the pair-`01` tone — the `$55` fill; the low nibble is the pair-`10` tone — the `$AA` fill. Pair `11`, used for blinking rows, stars, debris and the aperture, is the colour-RAM nibble, written as 3.*

## Doors, windows and debris

Two kinds of object do not use the ordinary profile fill.

**Dockable structures.** A type with flag bit 7 at `$C39A` and a non-zero byte 8 goes through `$3000`. Byte 8 is the aperture — the same animated value the docking test reads. The door occupies profile rows `$5C − a` to `$5C + a`, where `$5C` is 92 and *a* is the aperture. Its half-width is the radius ramp for `a ÷ 2`, so the opening widens as the door opens.

Those rows are filled not with the two body tones but with a byte from the pattern table at `$C2D8`:

```text
pattern = $C2D8[$038F]
$038F = ($038F + 1) mod 8 rows
```

`$C2D8` is 64 bytes — eight groups of eight. The first group is `CC CC 33 33 CC CC 33 33`; `$CC` is pairs `11 00 11 00` and `$33` is the complement. The pattern is therefore a stripe of colour 3 and background, and the row counter advances the byte, so the door shimmers. At the end of each frame `$43FF` adds 8 to `$038F`, moving to the next group; the whole table cycles every eight frames.

**Debris.** A record whose byte 0 has bits 6–7 equal to `$40` is dying. Instead of the lathe, `$3225` draws an explosion: a scatter of up to 128 points (64 for types with flag bit 0) whose offsets come from the two-byte table at `$C500` or `$C600`, with radii from `$C700`. The points are plotted with the same two-bit masks as the stars, each mask setting one pair `11`, so every point of light in the view — star, debris, window, open door — is colour 3. There is no profile and no terminator; an explosion is a cloud of dots whose frame index `$EA` advances every frame.

## The copy out

The buffer cannot be shown directly. The VIC reads a cell-major bitmap, where one cell's eight scanlines are eight consecutive bytes. The buffer is scanline-major. The blit at `$223E` joins the two.

It runs from the display handler at `$49BA`. The main loop signals that the buffer is ready by storing `$80` in `$0348`. The handler claims the request with `$FF`, waits for the low raster register to reach at least `$40` at `$49C9`, then copies. It clears `$0348` when the copy finishes.

The copy transposes sixteen viewport cell rows using groups of unrolled loads and stores:

- Destination block *b* begins at `$E148 + 320b`; 320 is one cell row of the bitmap.
- Each cell row has sixteen columns, indexed by *X* in a full copy.
- Each iteration reads eight bytes with a stride of `$10` — the eight scanlines at column *X* — and writes them to the eight bytes of one bitmap cell.

```asm
LDA $0400,X     ; buffer row 0, column X
STA $E148,Y     ; cell scanline 0
LDA $0420,X     ; row 2
STA $E14A,Y     ; scanline 2
LDA $0440,X     ; row 4
STA $E14C,Y     ; scanline 4
LDA $0460,X     ; row 6
STA $E14E,Y     ; scanline 6
; and, on a full refresh, rows 1, 3, 5, 7 into scanlines 1, 3, 5, 7
INX
TYA
CLC
ADC #$08        ; next cell: eight bytes
TAY
```

`X` runs 0–15 and `Y` 0–120: sixteen columns and sixteen cells. Sixteen blocks of sixteen cells is the whole 128 × 128 view.

### IR and the alternate refresh

When `$0396` is clear and infrared is active, `$2249` toggles `$0334` between `$80` and `$81` and saves the result in scratch byte `$17`. Both values are nonzero, so the branch at `$2278` and its counterparts skip the second group of stores on **every** infrared pass. Bit 0 chooses which rows the remaining stores update.

| IR state after the toggle | Starting indices | Rows copied |
| --- | --- | --- |
| `$81` | `X = $10`, `Y = 1` | Odd. The source is shifted by one 16-byte row and the destination by one scanline within the cell. |
| `$80` | `X = 0`, `Y = 0` | Even. The same instructions use their original offsets. |

Each infrared pass updates 64 of the 128 rows. The other rows retain the preceding pass's image, so a moving edge can show a slight comb. A nonzero dock state bypasses the infrared path and makes a full copy.

## What it costs

The renderer's data is small enough to hold in the space one modern texture would occupy:

| Data | Bytes |
| --- | --- |
| Row buffer at `$0400` | 2,048 |
| Bitmap at `$E000` | 8,192 |
| Character matrix at `$CC00` | 1,000 |
| Record table at `$0E00` | 768 |
| Display list at `$0D00` | 128 |
| Width and terminator ramps at `$0D80` | 128 |
| Profiles and their two tables | 7,356 |

The bitmap and matrix are fixed VIC furniture. The renderer's own working set is the 2 KB buffer plus 128 bytes of list plus 128 bytes of ramps. The drawing code from the record pass at `$2A4D` to the byte masks at `$3305` is `$8B8` bytes — under two and a quarter kilobytes. A full blit writes 2,048 bytes to the bitmap; an IR half-pass writes half that.

The economy is the profile format. Ninety-six bytes of city sheet become thirty-two buildings; each building's shape is a pointer and a length into a table of one-byte radii; and each radius becomes a span, not a polygon. The renderer never multiplies a 3D vertex or divides by a depth. It divides once per object to get `Q`, then adds and shifts.

### CPU cycles and viewport updates

The table gives isolated instruction timings from py65 using the original listing bytes. For the copy, the trace starts at `$223E` and counts through its `RTS`, with `$0396` clear and `$0334` set to `$00`, `$80` or `$81`. The measurements exclude interrupt time and VIC-II bus contention.

| Work | CPU cycles | When it runs |
| --- | ---: | --- |
| Clear and fill the row buffer, `$21DF` | About 11,850 | At the start of an ordinary view |
| Build both 64-entry ramps, `$2FD4`–`$2FFD` | 3,967–4,031 | Once per object on the span-drawing path |
| Full bitmap copy | 20,601 | 2,048 bytes |
| Infrared copy, odd rows | 11,545 | 1,024 bytes |
| Infrared copy, even rows | 11,542 | 1,024 bytes |

A PAL VIC-II refresh spans 19,656 clock cycles, so the full bitmap copy alone takes longer than one refresh. Clearing and copying use about 32,450 cycles together. At the PAL clock rate of 985,248 cycles per second, that puts a theoretical ceiling of about 30 fresh full viewport images per second on the ordinary flight loop, before scene drawing, game logic and waiting for the raster. The number of objects that reach the painter and the number of spans they cover determine much of the additional work. [VICE PAL timing constants](https://github.com/VICE-Team/svn-mirror/blob/main/vice/src/c64/c64.h)

The VIC-II continues scanning the bitmap at about 50 Hz while the game prepares and copies new views. [The raster schedule](one-frame-in-the-skimmer.md#what-the-interrupt-is-doing) gives the controls, clock and SID their own slots. The actual viewport FPS depends on the scene and would need a running-game trace of completed copy requests.

## Next steps

[From scanner blip to missile lock](from-scanner-blip-to-missile-lock.md) follows the bearings that the scanner plots and the target pointers that the painter publishes. [One frame in the skimmer](one-frame-in-the-skimmer.md) puts both routines on the main loop's timeline.

[Back to Deep Dives](index.md)
