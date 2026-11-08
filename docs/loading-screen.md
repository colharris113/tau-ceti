# The Loading Screen

The boot path: a 252-byte stub, a 508-byte loader called JEFF, seven files and one picture.

---

Tau Ceti does not load in one go. The disk carries a small boot program, a loader, and seven
files that the loader installs one at a time, and the picture you look at while this happens is
not a decoration loaded for the occasion - it is the game's own screen hardware showing you the
files arriving in memory.

## The boot stub

The first file in the directory is `TAU CETI` (one block, track 17 sector 0). It is a normal
PRG that loads at $0302: 252 bytes that do very little.

It sets the VIC-II up, loads a second file called `JEFF` to $0C00 with the KERNAL LOAD routine,
and jumps to it. That is all. Everything else in the boot sequence lives in JEFF.

## JEFF, the loader at $0C00

JEFF is 508 bytes - two blocks - and begins with the instructions you would expect of a loader
written in 1987: `SEI`, then a KERNAL call to silence the error channel, then straight into
setting up the screen before a single byte of the game is on disk-read.

The screen setup is at $0CC6 and it is worth walking through, because it explains the picture:

| Register | Value | Effect |
|---|---|---|
| $DD00 | $94 | VIC-II bank 3, the $C000-$FFFF bank |
| $D011 | $2B | bitmap mode, 25 rows, display **off** |
| $D018 | $3D | video matrix at $CC00 |
| $D016 | $D8 | 40 columns, multicolour on |
| $D020/$D021 | $00 | black border, black background |

It then clears four pages of video matrix at $CC00, four pages of colour RAM at $D800, and fills
the 8K bitmap at $E000-$FFFF with $FF. On a screen that is entirely colour 0, that is a black
screen - but it is a *bitmap* screen, and the bitmap it is displaying is the one the game will
use, at $E000.

That is the trick of the loading screen. The seven files are loaded into the addresses they will
occupy when the game runs, and some of those addresses are inside the visible bitmap. The VIC is
pointing at memory that is being overwritten, so the loading display is literally the file data
being written into screen memory. Large parts of it look like static; the regular bands are the
structure of the data.

## The seven files

JEFF loads seven files in a fixed order. Each name in its table is nine bytes long and the short
names use a `*` wildcard, because the loader hands the name straight to the KERNAL:

| File | Track/Sector | Blocks | Loads at | What it is |
|---|---|---|---|---|
| `PIC B*` | 13/0 | 40 | $4000 | the picture |
| `I/O 4K*` | 19/0 | 17 | $4000, then copied to $D000 | replacement I/O routines |
| `0E00-2000` | 17/1 | 19 | $0E00 | object records and tables |
| `2000-8900` | 21/6 | 106 | $2000 | the game itself |
| `8900-CC00` | 17/20 | 68 | $8900 | data: glyphs, city names, demo script |
| `CC00-D000` | 19/9 | 5 | $CC00 | character and screen tables |
| `E000-FFFF` | 20/0 | 33 | $E000 | the main bitmap |

Two details in that table are worth pausing on. `I/O 4K` is loaded at $4000, not at its final
address: you cannot load into $D000 with the I/O bank switched in, so JEFF's hook for that file
copies sixteen pages down to $D000 after switching $01 to $34 and back. And `CC00-D000` is five
blocks, not the 4K its name suggests - the name is the range it belongs to, not the size it is.

## The per-file hooks

After each LOAD, JEFF patches the operand of a `JSR` at $0C52 with an address from a table at
$0CB8, and calls it. Each file therefore gets its own small follow-up routine:

- `PIC B*` gets $0D1F, the picture installer, described below.
- `I/O 4K` gets $0D63, the copy to $D000.
- `8900-CC00` gets $0D19, which blanks the display by writing $2B to $D011.
- The other four get $0D18, which is a bare `RTS`.

The blanking is not decoration. `E000-FFFF` loads over the visible bitmap, so the display has to
be off while that happens or the screen would show the load as a mess of half-written bytes.

## The picture

`PIC B TAUCETI+` is the largest non-code file: forty blocks, 10160 bytes, loaded at $4000. Its
contents are laid out as three consecutive blocks of data:

| Offset | Size | Purpose |
|---|---|---|
| 0 | 8000 | bitmap, exactly one 320x200 multicolour screen |
| 8000 | 1000 | video matrix |
| 9000 | 1000 | colour RAM nibbles |

The installer at $0D1F does three things with it. It copies the 1000 matrix bytes from $5F40 to
the video matrix at $CC00, copies the 1000 colour bytes from $6328 into colour RAM at $D800, and
copies part of the bitmap into the screen area at $E000 in a strided pass - 64 bytes out of every
256-byte page, 32 pages in all. Then it writes $3B to $D011, which turns the display on, and
waits.

> [!NOTE]
> The strided copy is the one part of this sequence I have not fully explained. It moves 2K of
> the 8K bitmap, not all of it, so the code as read does not by itself put a complete picture on
> screen. The file at $4000 is the title image - decoding its first 8000 bytes with the matrix and
> colour block beside them gives the title screen - but whether the full image is visible at the
> prompt, or is completed later by the game, I could not confirm from a memory dump.

## The SPACE prompt

The wait at $0D83 is a KERNAL `GETIN` loop that exits only when the key returned is $20, the space
bar:

```
$0D83  STA $D011      ; display on
$0D87  JSR $FFE4      ; GETIN
$0D8A  CMP #$20       ; space?
$0D8C  BNE $0D87
$0D8E  SEI
$0D8F  RTS
```

This is the only interactive moment in the boot. The version of the disk used for the traces in
this repository has these instructions NOPed out, so the emulator runs the loader unattended.

When the loop finishes, JEFF restores $01 to $FF and jumps to $2000: the first instruction of the
game, `LDX #$FE / TXS`, which resets the stack and begins the start-up sequence that ends in the
frame loop. What it does first is the credits screen: a message, an unpacked picture, and a thousand
frames of waiting before it hands over to the attract mode. [The Attract Sequence](demo-mode.md) has
that path.

## The line in the border

One thing on the loading screen is not the loader's doing. Once the game's own code starts running,
a line of text begins to scroll in the bottom border, and it is still there when the credits screen
appears. It is not drawn by JEFF - the loader contains no sprite code at all - and it is not a
border trick either. [The Border Banner](border-banner.md) explains what it is.

## One last detail

JEFF's own memory does not go to waste. The message queue that the game uses for its on-screen
text is written at $0C00 and $0C80 - the two ring buffers the loader leaves behind when it jumps
to $2000. The loader is overwritten by the first message the game prints.

---

[Back to the overview](../README.md)
