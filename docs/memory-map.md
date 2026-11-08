# Memory Map

The full 64KB map: what lives where, and which VIC-II and SID registers the game touches.

---

Tau Ceti fills the machine. The game code sits at $2000 and runs to $88FF, the data files occupy
$8900-$CCFF and $D000-$DFFF, and the screen hardware points into the top of memory: bitmap at
$E000, video matrix at $CC00, colour RAM at $D800. The loader in the bottom quarter is overwritten
almost as soon as the game starts.

## Complete Memory Map

| Range | Contents |
|---|---|
| $0000-$00FF | zero page: pointers, counters, the raster stage byte |
| $0100-$010F | the sixteen rebindable key codes |
| $0111-$012E | the two sound-effect state blocks, in the stack page |
| $0200-$03FF | game variables (page 3 holds the flight state, gauges, mission counters and ammo) |
| $0277-$027F | the console's nine-key FIFO |
| $02B0-$02FF | the forty rod halves, two bytes each |
| $0400-$0BFF | flight-view canvas: 16 rows of 128 bytes, and the camera arena |
| $0C00-$0CFF | loader, then the two message-queue ring buffers |
| $0D00-$0DFF | the render queue, four bytes per entry; also the star map's scratch |
| $0E00-$10FF | 48 object records, 16 bytes each |
| $2000-$88FF | game code |
| $8900-$8FFF | city data: pad table, city coordinates at $89A0/$89C0, names at $8D02 |
| $8A00/$8B00 | the two reciprocal tables used for object half-widths |
| $8C00/$8C81 | the projection tables, 129 bytes each |
| $8E00/$8F00 | the 64-glyph UI font |
| $9000-$92FF | the 96-glyph log font, three pages |
| $9300-$93FF | demo script: one delay byte per entry |
| $BD00-$BDFF | demo script: 256 key-event bytes |
| $BC50-$BC7E | the rod tray, one byte per cell |
| $C000-$C291 | the border ticker text, four bytes per three characters |
| $C39A-$C3FF | object type table and per-type data |
| $CA00-$CBFF | the border ticker's eight sprite blocks |
| $CC00-$CFFF | video matrix (1000 bytes used), sprite pointers at $CFF8 |
| $D000-$DFFF | replacement I/O routines (loaded from `I/O 4K`) |
| $D800-$DBFF | colour RAM (1000 bytes used) |
| $E000-$FF3F | the bitmap, with the character canvas in $E000-$EFFF |
| $FFFE-$FFFF | hardware IRQ vector, holding $3903 |

![The 64KB address space, block by block](../assets/memory-map-viz-1.svg)

## Region Breakdown

### $0000-$00FF: Zero Page

The zero page holds the working state the code touches most often:

| Address | Use |
|---|---|
| $01 | CPU port; the loader switches RAM in and out with it |
| $11 | a frame counter, incremented once per frame at $25D3 |
| $26-$27 | scratch for the 8-bit multiply in the object code |
| $61-$62 | general pointer, used by the record scanner and the sound code |
| $67-$69 | counters and saved indices inside drawing routines |
| $6F | the current raster stage, 0-3 |
| $C6 | KERNAL keyboard buffer length, cleared each frame at $4DA9 |
| $DA-$DB | projected position used by the drawing code |

### $0100-$010F: The Key Map

Sixteen bytes of key codes, plus one spare at $0110, read through the decode routine at $3D18. The
buffer is not a second variable: it is the *only* flight input, restored from a saved copy at $03EF
with the routine at $6403, and seeded from the seventeen defaults at $3D30. The two scans that read it
are described in [Board Computer](board-computer.md); the short version is that `$3968`/`$33F9` poll
the continuous controls and `$334C` polls the discrete ones, so all sixteen slots are live.

Above it, in what is nominally the stack page, sit the two sound-effect state blocks at `$0111-$011E`
and `$0121-$012E`. That is the game using `$0100-$01FF` as ordinary variable space; a port has to keep
these as variables and not model a stack there.

### $0200-$03FF: Game Variables

Almost everything the game tracks lives here, at absolute addresses rather than in the zero page:

| Address | Variable |
|---|---|
| $0277-$027F | the console's nine-key FIFO; `$C6` is the length, `$C5` the last key |
| $02B0-$02FF | the forty rod halves, two bytes each (see [The Rod Puzzle](rod-puzzle.md)) |
| $0334 | sight/flag byte toggled at $3B20 |
| $0335/$0336 | the ground position WAIT advances by $5A |
| $033B-$033F | sight position, computed each frame by the projection helpers |
| $0342/$0343 | BCD seconds and minutes on the clock |
| $0344 | height |
| $0346 | fuel |
| $0347 | a slowly decaying gauge |
| $034A-$0351 | joystick and keyboard shadow: the eight input bytes the flight model reads |
| $0352 | turn rate |
| $0353 | speed - and the engine pitch |
| $0355 | flares |
| $0356 | flare timer |
| $0357 | AMM |
| $0358 | missiles |
| $0359 | AMM flash flag |
| $035A-$0363 | the ten key latches filled by $334C |
| $0364-$036D | their ten timers; the tenth is the pause |
| $0365-$0367 | weapon cooldown timers: flare, missile, AMM |
| $0370-$0372 | laser, scanner and infra-red damage flags for STATUS |
| $0377 | a gauge that fills to $BF |
| $0379 | general-purpose timer |
| $0383/$0384 | message queue read and write pointers |
| $0385 | the log's write offset, eight per glyph |
| $0394 | attract flag: `$00` playing, `$80` attract, `$FF` leave |
| $0395 | pause / wait-for-key |
| $0396 | flight state: 0 launched, 1 landed, $80 docked |
| $0398/$0399, $03A4 | the docked building's X, Y and type |
| $039D | display mode, ORed into the raster dispatch index |
| $03A5/$03A6 | robots killed, a 16-bit counter |
| $03A7 | rod halves on the surface, to `$28` |
| $03A8 | halves solved, to `$14` |
| $03A9 | bars inserted, to `$14` |
| $03AB/$03AC | the cursor on the RODS and REACTOR screens |
| $03B1/$03BB | the demo script's index and delay counter |
| $03BA | "the recording has ended" |
| $03BC | the last rod touched |
| $03BD | the rod drop point |
| $03BE | the radiation dose, to `$3D` |
| $03C0/$03C1 | the star map's cursor |
| $03C2 | the star map's zoom, clamped at `$1F` |
| $03C4/$03C5 | the two sound-effect slots |
| $03DB-$03EE | the reactor's twenty slots |
| $03EF-$03FF | the saved key map |

### $0400-$0BFF: The Flight View

The view is drawn into a 2KB arena at $0400: sixteen rows of 128 bytes, two bits per pixel. The
renderer at $29B6 walks the 48 records, projects the ones that pass its gate, and paints them into
the arena through a back-to-front queue; $223E then blits the arena into the bitmap at $E148, $E288,
$E3C8 and onwards, interleaving even and odd source bytes into the eight bytes of each destination
cell. The scanner window is a separate, smaller blit: $3F2D takes the first 512 bytes of the same
arena and transposes them into eight bands at $E870, $E9B0 and onward.

The arena is scratch, not state. It is cleared to `$55` and repainted every frame, and the star map
reuses it - and the queue at $0D00 - for its own picture. [Moveable Elements](movables.md) has the
gate and the queue.

### $0C00-$0CFF: Loader, Then Message Queue

When the disk boots, this is JEFF. Once the game is running, it is two ring buffers: $4127 appends
two-byte entries at $0C00 and $413B appends four-byte entries at $0C80. The loader does not survive
the first message the game prints.

### $0E00-$10FF: The Object Table

Forty-eight records of sixteen bytes. Byte 0 is a type index into the table at $C39A, byte 3 holds
flags ($40 drawn, $08 variant), bytes 10-11 are a 16-bit X position and bytes 12-13 the depth.

The table is built at run time by $280B from per-city object lists, pointed to by the city number
at $0354, which is why the bytes on the original disk do not match the table in a running game.

### $2000-$88FF: Game Code

The main body of the program, loaded from `2000-8900`. Entry is at $2000 with `LDX #$FE / TXS` and
five `JSR`s into the start-up routines; the frame loop begins at $4D80 and the hardware IRQ handler
at $3903.

### $8900-$92FF: City Data and Glyphs

The city name table is at **$8D02**, thirty-two names separated by $C0. Below it, $8900 holds four
bytes per city saying which of the four directions has a jump pad. Above the names, $89A0 and $89C0
are the 32 city X and Y coordinates on the star map, and $9000-$92FF holds the three pages of the log
font: digits and punctuation, capitals, lower case.

### $CC00-$CFFF: Video Matrix

The VIC-II is pointed here by $D018 = $38 (`$3D` while the loader owns the screen), giving 1000
bytes of matrix for a 40x25 screen in multicolour bitmap mode.

### $D000-$DFFF: Replacement I/O

`I/O 4K` is loaded at $4000 and copied down here under the I/O bank. This is the game's own screen
and input code, running where the KERNAL's I/O normally lives.

### $E000-$FF3F: Bitmap

8000 bytes, one 320x200 multicolour bitmap, displayed from VIC-II bank 3. The top 4,096 bytes,
$E000-$EFFF, double as the character canvas - 32 columns by 16 rows of 8x8 cells, filled by $3E17 -
which is why a 16x16 window is exactly a quarter of it. The last 192 bytes of the bank are not part of
the picture: $FFFE holds the IRQ vector, which is $3903.

## Tables the code leans on

Not all of the data is in a range with a name. These are the tables the routines above actually index,
collected in one place because most of them are short and most of them are load-bearing:

| Address | Size | What |
|---|---|---|
| $3D28 | 8 | the row-bit masks `01 02 04 08 10 20 40 80` |
| $3D30 | 17 | the default key codes |
| $4B2A | 67 | key names, one per code, bit 7 on the last character |
| $4B9C | 22 pairs | the KEYS screen's string pool |
| $4BAC | 25 | the command names, bit-7 terminated |
| $4E0B | 25 words | the command handlers, stored as `handler-1` |
| $7173 | 8 | the rod class table `06 05 02 09 02 09 05 06` |
| $7269 | 18 | the RODS screen's hit rectangles |
| $72B2 | 22 | the REACTOR screen's hit rectangles |
| $7440 | 32 | rod halves per city, bit 7 = already stripped |
| $7DAA | 6 pairs | the star map's menu boxes |
| $86BB | 32 | the star map's zoom scale, 8 at zoom 0 to 245 at 30, then `$FF` |
| $8812 | 16 x 12 | the sound-effect records; everything above $88D1 is code |
| $8A00 / $8B00 | 256 each | the reciprocals that turn a depth into a half width |
| $8C00 / $8C81 | 129 each | the projection tables, tangent-like |
| $C39A / $C3BF / $C3E4 / $C409 | 37-64 | the four per-type tables |
| $C4BE | 4 x 8 | the four pad slots: each is an airlock and its marker |

## VIC-II Register Access

The game uses a normal multicolour bitmap screen and raster splits. The registers it actually
writes:

| Register | Address | Purpose |
|---|---|---|
| $D011 | $D011 | screen control: bitmap mode, display enable, vertical scroll |
| $D012 | $D012 | raster compare - which line the next split fires on |
| $D016 | $D016 | horizontal scroll and multicolour enable |
| $D018 | $D018 | video matrix and bitmap base pointers |
| $D019 | $D019 | interrupt status, acknowledged every frame |
| $D01A | $D01A | interrupt enable |
| $D01B-$D01D | $D01B-$D01D | sprite priority, multicolour and size, used only for the border banner |
| $D020/$D021 | $D020/$D021 | border and background |
| $D027-$D02E | $D027-$D02E | sprite colours, one per banner character group |
| $DD00 | $DD00 | VIC bank select; bits 0-1 = %00 selects bank 3, $C000-$FFFF |

Nothing in the bitmap is a sprite. The eight sprites at $D000-$D01D belong to the scrolling line in
the bottom border, which is enabled for the bottom band of the frame and switched off again above
it; see [The Border Banner](border-banner.md).

## SID Register Access

Sound is small and direct. Three voices, no music player, no filter sweep:

| Register | Address | Purpose |
|---|---|---|
| $D400-$D406 | voice 0 | effect slot `$03C4`: frequency, pulse width, control, envelope - seven bytes copied as a block |
| $D407-$D40D | voice 1 | effect slot `$03C5`: the same seven bytes, from the same routine |
| $D40E/$D40F | voice 2 frequency | the engine, derived from `$0353` |
| $D412-$D414 | voice 2 gate and envelope | engine waveform and ADSR |
| $D418 | volume | `$0F` playing, 0 in attract mode |

Both effect voices are written the same way, from the twelve-byte records at $8812, by the player at
$8759; the engine voice is poked directly by the frame tick at $86F8. Nothing writes the filter at
$D415-$D417 and nothing writes the filter-mode bits of $D418, so the "filter sweep" of earlier
versions of this guide is not there.

> [!NOTE]
> The old version of this chapter listed the SID at $C000-$C01F. The SID is at $D400-$D41C; $C000
> is the start of the border ticker's text.

---

[Back to the overview](../README.md)
