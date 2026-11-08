# Board Computer

The console: a nine-key FIFO, a line editor, a prefix parser with twenty-five commands, the redefinable
key table, and a save file that is a picture of the machine's own memory.

---

The board computer is the interface you use when you are not flying, and it is the most conventional
code in the game: a queue of key numbers, a line editor, a parser that dispatches on the first word,
and handlers that mostly paint a screen or push a message. It is also where the game keeps its save
file and its key bindings, so it is worth reading in order - from the key press to the file on disk.

## Two queues, not one

The console has a keyboard queue of its own, separate from the KERNAL's.

`$4ABF` pushes a key number into a nine-byte FIFO at `$0277`, with the length at `$C6` and the last
key at `$C5`. The key goes in **`Y`**, not `A`, and the routine drops it if the queue is full. `$4ACE`
pops: it takes the byte at `$0277`, shifts the rest down one place, decrements `$C6` and returns the
key in `A` with the carry clear - or with the carry set if there was nothing to pop.

Nine entries is the game's own limit, not the KERNAL's ten, and it does not matter in practice
because the line editor drains the queue faster than a person types.

Then there is the *output* side, which is a pair of ring buffers:

| Routine | Ring | Entry | Pointer |
|---|---|---|---|
| `$4127` | `$0C00` | two bytes: a string address | `$0384` write, `$0383` read |
| `$413B` | `$0C80` | four bytes | `$0391` |

Nothing draws itself in this game. A handler that wants to say something pushes the address of a
string and returns; the raster side drains the ring at `$41F7`, and `$6444` - the frame's
synchronisation point - spins until the read and write pointers match again. A burst of messages
therefore holds the frame up rather than losing any of them, which is why several events at once make
the game stutter.

## The line editor

`$4E4C` is entered with the maximum line length in `A`: `$0C` from the computer prompt, `$0D` from
SAVE and NAME. It blanks 32 bytes at `$0200` to spaces, draws a cursor block, and then loops:

```text
$4E7A  wait for the next frame ($11 to change)
$4E82  pop a key with $4ACE
$4E88  A = $4AEA,key            key number -> glyph
$4EA0  if the glyph < $70: store at $0200,X, $0385 += 8, echo it
$4EB1  if the key is $7E (RETURN): return, with X = the line length
$4EB6  if the key is $7F (DEL): backspace
```

Two bounds live here and they are different numbers. The editor itself refuses to go past 18
characters (`CPX #$12`), but the caller's maximum is normally 12 or 13, so the practical limit for a
command is 12 and for a filename 13. The 18 is a backstop that nothing in the shipped game reaches.

It is worth knowing that the echo of each character goes through the raster wait, so the editor cannot
be run headless: it cannot be bracketed in a 6502 core with no display. What can be done, and was, is
to drive it - turn a command into the key numbers that would produce it, push them, and check that the
line at `$0200` and the glyphs on screen are what the machine would produce.

## The parser

`$4DB7` compares the typed line against a name table at `$4BAC`, left to right, and dispatches through
a parallel table of **handler-minus-one** words at `$4E0B`:

```text
$4DB7  X = 0, $67 = 0                   $67 = the command index
$4DBD  A = $4BAC,X / bit 7 clear: CMP $0200,Y / BEQ next
$4DCC  bit 7 set: A &= $7F / CMP $0200,Y / BEQ found
$4DD5  mismatch: skip to the next name, $67 += 1
$4DE3  ran out: push $4DFA "Not Understood!", return to the prompt
$4DED  found: push the word at $4E0B + 2*$67, RTS into it
```

The comparison is a **prefix** match, and nothing requires the line to end where the name does:
`LAUNCHX` dispatches LAUNCH. The dispatch is a `PHA/PHA/RTS` pair, so the table holds `handler-1` and
the return pops the real address - the same trick the raster dispatch table uses.

## The twenty-five commands

| # | Name | Handler | What it does |
|---|---|---|---|
| 0 | HELP | `$50A3` | the command screen |
| 1 | LAUNCH | `$4EDA` | fuel gate, re-seat the ship, `$0396 = 0` |
| 2 | MAP | `$7D59` | the star chart |
| 3 | RODS | `$6D0E` | the rod tray |
| 4 | REACTOR | `$770B` | the reactor core |
| 5 | LOOK | `$6145` | the view screen |
| 6 | WAIT | `$505B` | pass time, and lose ground position |
| 7 | STATUS | `$54CA` | six lines of system state |
| 8 | EQUIP | `$5C18` | fuel, repair, rearming |
| 9 | NAME | `$4FC4` | name the skimmer |
| 10 | PAD | `$58B6` | the pad screen |
| 11 | NEW PAD | `$509D` | replace the pad |
| 12 | SAVE | `$6C55` | write the game state |
| 13 | LOAD | `$69BA` | read it back |
| 14 | KEYS | `$539B` | redefine the controls |
| 15 | QUIT | `$4FEB` | abandon the mission |
| 16 | SCORE | `$5AA3` | the four counters |
| 17 | PAUSE | `$4FDE` | stop |
| 18 | SIGHTS ON | `$4FB4` | crosshair on |
| 19 | SIGHTS OFF | `$4FBC` | crosshair off |
| 20-23 | FUCK / PISS OFF / CUNT / BASTARD | `$602A` | four of the five joke commands |
| 24 | COKE | `$522C` | the fifth |

Twenty-five names, all of them in one table, and the dispatch is real. What is *not* uniform is how
much of each handler runs without a display: `$5372` (blit and wait for the raster) and `$6444` (wait
for the log to drain) both spin on hardware, so any handler that calls one can only be read, not
executed. That is why the parser is understood for all twenty-five and only a handful of handlers are
verified byte for byte.

## The four screens that are only text

Two command screens turned out to be nothing but pushes into the message ring, which is worth knowing
before looking for a drawing routine.

**STATUS** builds six lines, each with a `DAM`/`OK` word chosen by a state byte:

```text
\nLaser    + ($0370 ? " DAM" : " OK ")
 Fuel      + ($039E ? " DAM" : " OK ")
\nScanr    + ($036F ? " DAM" : " OK ")
 Comp      + ($0371 ? " DAM" : " OK ")
\nInfra Red + ($0372 ? " DAM" : " OK ")
\nDD:DD until Sunset | Sunrise
```

The last line is the only arithmetic. `$5526` negates the nine-bit value at `$0336:$0335`, shifts it
left once with bit 0 of `($0341 ^ 1)` as the carry in, and divides it down into four bytes at `$55BF`
to `$55C3`. Those four bytes are **inside the message text** - `$55C1` is the colon - so the routine
rewrites the sentence it is about to print, and the sign of the negate picks "until Sunset" or "until
Sunrise".

**SCORE** is four counters, each multiplied by a constant and added into its own five-digit field:

| Field | Value | Multiplier |
|---|---|---|
| Robots Killed | `$03A6:$03A5` | 5 |
| Parts Found | `$03A7` | 75 |
| Rods Assembled | `$03A8` | 250 |
| Rods Inserted | `$03A9` | 500 |

`$5BB8` is the multiplier, and it starts with `SED`: every add is decimal, so a digit sum of 15 leaves
5 and carries 1. That is not a detail to smooth over - the first version of this analysis used
`& $0F` and `>> 4` and stored `$0E` where the machine stores 4. `$5B27` then sums the four fields
column by column with decimal mode on. The handler ends at `$4ACE`, waiting for a key, so it is not a
pure routine: it must be given a key to return.

## The key table, and why a rebind is real

The flight controls are sixteen bindings at **$0100**, seeded from seventeen bytes at **$3D30** and
backed up at **$03EF**. The shipped table, decoded through the name table at `$4B2A`:

```text
;  /  Z  X  :  .  SPACE  I  F  M  A  L  R  V  S  J
```

Slots 0-6 are the continuous controls - increase and decrease thrust, turn, change height, fire -
read by `$3968` and `$33F9`, whose indexed reads run over `$0100-$010A`. Slots 7-15 are the discrete
commands, polled by `$334C`, which scans **ten** entries starting at `$0107` into latches at
`$035A-$0363` and timers at `$0364-$036D`; the tenth of those is the pause key, and it is the one that
stops the band by setting `$0395 = $FF`. Between the two scans every entry in the table is read.

That answers the question the manual raises and an earlier version of this chapter got wrong. The
claim used to be that only seven of the sixteen bindings were read anywhere, on the evidence of a
search for absolute references to `$0100-$010F` - but `$334C` reaches the second half through an
indexed read at `$0107,X`, which no byte-for-byte search for `$0100` would find. The commands are in
the table; they are just polled by the other scan.

`KEYS` at `$539B` is both a screen and an editor. The screen blanks the 16x16 window, fills the arena
with `$55`, gives it the `$47` dither in colour 7, and then blits sixteen function names from `$543D`
at column 8 while `$5491` draws each key's name at columns 2-7 from `$4B2A` - 67 names, one per key
code, each terminated with bit 7 set, the longest eight characters. Neither routine clears the
display, so the flight panel stays visible behind it.

The editor asks for a key, rejects any code an earlier slot already holds (`CMP $0100,Y`), and writes
the accepted code to the live entry **and** to the backup at `$03EF`. That is why the rebind is real
and not cosmetic: the same table the flight code polls is the one being rewritten.

> [!NOTE]
> **What this corrects.** The previous version of this chapter said the table was sixteen bytes seeded
> from seventeen, that seven entries were read, and that the rest of the panel's single-key commands
> were picked up somewhere else. The scan at `$334C` covers them, and the KEYS screen is a live editor
> for a table the game actually reads. The same chapter also listed `PRESS 3 TO EXIT` at `$653E`; the
> string is `Press SPACE to exit.` at `$653F`.

## SAVE and LOAD

The save format is not a data structure with named fields. It is a **picture of the machine's memory**:
a fixed list of copies into `$0400-$0C80`, handed to the KERNAL as a program file.

```text
2 bytes   00 04        the load address $FFD8 prepends
2177       $0400-$0C80 the image
```

`$6A77` builds the image from six sources, in this order, and the overlapping is the machine's:

| Image | Source | Bytes |
|---|---|---|
| `$0400` | the packed object store at `$9400`: 12 passes of 86 bytes at a stride of 3 | 1,032 |
| `$0800-$0A6F` | `$1100`, `$11D0`, `$12A0` - the three text rows | 3 x 208 |
| `$0A70` | `$0200` - the command line | 96 |
| `$0AD0` | `$02A8` - the rod table and page 2 state | 96 |
| `$0B30` | `$0334-$03FF` - page 3, including the key backup | 204 |
| `$0BFC` | `$BC50` - the forty rod halves | 48 |
| `$0C2C` | `$7440` - the per-city rod counts | 32 |

What is deliberately **not** in the image is `$0308-$0333`: that is where the KERNAL's RAM vectors live
(`$0314` for IRQ, `$0326` for CHROUT, `$0332` for SAVE), and including them would make the file
unloadable into a running machine.

`$6C73` gives the KERNAL its arguments: `$FB/$FC = $0400` as the zero-page pointer to the start
address, `A = $FB`, and `X = $80, Y = $0C` as the end address $0C80. The device byte at `$BA` comes
from a prompt - `$12` for disk, `$16` for tape - and the filename comes from the console:

```text
$6B7A  push " DISK OR TAPE ", pop a key from the queue
$6BAD  push " ENTER FILENAME ", call the line editor with A = $0D
       $B7 = the length the editor returned
       $BB/$BC = $0200          the KERNAL's file-name pointer, written directly
$6BC3  convert $0200[0..$B7-1] from screen codes to PETSCII, in place
$6C1F  if tape: push "PRESS RECORD & PLAY ON TAPE" and wait for the button
$6C6D  prologue: SEI, I/O in, $D01A = 0, CHROUT and STOP vectors stubbed
$6A77  build the image
$6C81  JSR $FFD8               the KERNAL SAVE
$6CEE  epilogue: restore $01, $D011, the IRQ, CLI
```

The screen-code to PETSCII conversion is three rules: `$00-$09` become `$30-$39` (digits), `$20-$3A`
become `$40-$5A` (letters), everything else becomes a space. That is the same encoding problem as
[Character Set and Text System](charset.md), one layer down: the console holds glyphs, the disk wants
PETSCII, and the conversion is a range shift.

LOAD is the mirror. `$69D5` calls `$FFD5` with `A = 0` - "load to the address in the file's header" -
and `X/Y = $00/$04` as the end address in case the file has none. `$6AF2` then unpacks the image back
into `$1100`, `$0200`, `$0300`, `$BC50` and `$7440`, and its last act is `$280B`, which rebuilds the
32 object records from three bytes each and recreates the four pads from `$C4BE`. On a KERNAL error
the handler pushes `$6A31` and returns to the prompt rather than dying.

The file is 2,179 bytes and it is byte-identical to a real one written by the KERNAL in an emulator -
which is the only test that matters here, because the format *is* the machine's memory layout:

| Check | Result |
|---|---|
| `$6A77` image `$0400-$0C4C` against the machine's own output | 0 bytes differ |
| file, load address included | 2,179 bytes, 0 differences |
| round trip: save, load, compare the live bytes | 0 of 1,348 differ |
| `$280B` rebuild after a load | 24 of 24 object records byte-exact |

Two details are easy to get wrong and both were found the hard way. The name in the directory entry is
the first `$B7` bytes at `($BB)`, copied verbatim - a run that skipped the name prompt, leaving
`$BB/$BC` pointing at the boot buffer, produced a file called `E000-`, the first five bytes of the
`E000-FFFF` filename. And the KERNAL leaves the directory entry **unclosed** (`type $02`, `blocks 0`)
until it closes the file, so an emulator has to be left running after `$FFD8` returns or the saved
image has a zero-length entry.

> [!NOTE]
> **What this corrects.** The old chapter said no save-game format had been identified and that the
> "magic number" and field list it printed were fabricated. That was honest and it is now out of date:
> the format exists, it is the memory image above, and it was verified by writing a file with the real
> KERNAL and comparing. The old chapter's advice - start from the message queue if you want to
> understand this area - was also right, and it is how the parser was found.

## What is still open

- **PAD and NEW PAD.** `$58B6` and `$509D` are routed, and the pad data at `$8900` is known (four
  direction bytes per city), but neither screen has been taken apart.
- **NAME.** `$4FC4` runs the line editor and stores a name; where the name lives afterwards and
  whether anything prints it has not been traced.
- **The other four joke commands.** `$602A` is shared by FUCK, PISS OFF, CUNT and BASTARD, and it
  paints a screen rather than pushing the two-line reply COKE gets. What it paints has not been read.
- **EQUIP.** The two text branches ($0396 = 1, and the reactor types) are understood; the screen past
  `$5C3E` is not.

---

[Back to the overview](../README.md)
