# The Attract Sequence

Title, credits, a thousand-frame wait, and then 205 seconds of somebody playing the game.

---

The status line at the top of the flight screen has four possible readings. Three of them describe
where you are - LAUNCHED, LANDED, DOCKED - and the fourth is DEMO. That fourth one is not a menu label
or a leftover: Tau Ceti has a working attract sequence, and the part most games fake with an autopilot
is here a recording. The ship in the attract mode is flown by a script of key presses and releases,
played back into the same input shadow the joystick writes.

That is the interesting claim, and the rest of this chapter is the evidence for it, in the order the
machine does it.

## The status line

The line is written by the routine at $4906, which picks one of four eight-character entries from a
table at $4931 and blits it into the screen at row 3, starting at column $1E. The table is stored in
the game's own glyph encoding, so each letter is its index plus $20:

| Entry | Address | Reads as | When |
|---|---|---|---|
| 0 | $4931 | `DEMO    ` | $0394 non-zero |
| 1 | $4939 | `LAUNCHED` | $0396 = 0 |
| 2 | $4941 | `LANDED  ` | $0396 = 1 |
| 3 | $4949 | `DOCKED  ` | $0396 = $80 (anything else) |

Two variables decide it, and only two. $0394 is the attract flag; if it is non-zero the line reads
DEMO and nothing else is considered. Otherwise $0396 picks among the three flight states. $0394 is
only ever written with three values in the whole image - `$00`, `$80` and `$FF` - and the code tests
nothing but bit 7, so the three mean "playing", "attract" and "a key was pressed, leave attract".

## Boot: a message and a picture

The loader ends with `JMP $2000`, and the first thing the game does is present the credits:

```text
$2000  $56FE  CLD, keyboard shadows to $FF, 32 spaces at $0240
       $5664  $5766  $56D8        reset block: key latches, timers, state bytes
       $6250  push $625C           the credits text
              $46E9                 a two-note sound
       $7689  draw the screen
       $6578  unpack a run-length picture from $0E00 into $0400
       $76BA  $534E                three text rows at $1100/$11D0/$12A0
       JMP $648D
```

`$625C` is 227 bytes: 32 lines and 194 glyphs, all of it landing in the log window. The picture that
`$6578` unpacks is the other half of the credits screen, and it is one of the two things in this
sequence that are **not** reproduced anywhere - see the note at the end.

Twelve snapshots taken through the wait show the screen settling:

| Snapshot | On screen |
|---|---|
| 00, 01 | the cockpit frame, every window empty and black |
| 02, 03 | text appearing; the canvas at $E000 goes from 3,320 to 3,995 non-zero bytes |
| 05 onwards | the TAU CETI logo over a starfield in the left window, `*** TAU CETI ***` and `(C) CRL 198x` in the log, the gauges reading `TAU CETI III` / `REEMA` / `FORWARD` / `DOCKED`, the five bars, and the border banner already crawling |

From snapshot 05 the screen is static and byte-identical to the last one, so the credits are a
picture plus a message plus a moving line, and the wait after that is just a wait.

## The thousand-frame wait

`$648D` is the wait, and it is a nested counter rather than a timer:

```text
$648D  $039D = 8                 the display-mode index for this screen
$6444  wait until the log ring is empty
$6495  $0394 = 0
$649A  $68 = $14, $67 = $32
$64A2  loop: $5FAC waits for $11 to change        (one frame)
              test SPACE  ($3D18 with X=$3C)
              test RUN/STOP ($3D18 with X=$3F)
              either -> $64D3, leave with $0394 = 0
       twenty outer passes of fifty inner passes = 1000 frames
```

Measured by patching the entry point and counting the loop top: **1,000 passes exactly**, and 1,116
ticks of the frame counter $11 between the first and the last. The excess over one tick per pass is
the spin at `$5FAC` occasionally losing a tick to the handler that increments $11; it is not a second
wait inside the loop. Nominally 1,000 frames is 19.95 seconds at 50.125 Hz, and the measured figure is
twenty to twenty-two.

Two keys are tested, not one: SPACE and RUN/STOP, both in matrix column 7, both read through the same
decode routine at $3D18 that the flight controls use. Press either and the credits are skipped and a
real game starts. Press neither and the wait falls through to the attract mode.

## The hand-off to attract

```text
$64BB  $63F7  copy $3D30-$3D40 (17 bytes) to $0100     the shipped key table
       push $6529  "DEMO MODE Initiated"
       push $653F  "Press SPACE to exit."
       $6444       wait for both to be printed
$64CF  $0394 = $80                                     <-- the attract flag
$64D8  $03B1 = $03BB = $03BA = 0
       $034A-$0351 = $FF, $03B2-$03B9 = $FF
       $5766, $280B (build the city's objects), $0E08 = $48, $03AF = 0
       JMP $4D7D                                       the board computer
```

Two details are easy to miss and both matter for a port. The key table is restored to the shipped
defaults **before** the demo runs, so a player's rebinds do not survive into the recording - and the
backup at $03EF is left alone, which is how the player's own keys come back afterwards. And the
restart drops into the board computer, not into the flight view: the demo types its first command
from the console like a player would.

The demo is also **silent by design**. The silence routine at $86DB writes the volume register from
$0394 when it is non-zero, so with the attract flag set $D418 goes to 0 and the machine has no volume
at all. A port that plays sound in the attract mode is audibly wrong, and it is wrong in a way the
original never was. [Sound System](sound.md) has the routine.

## The recording

This is the part that is not an autopilot.

Every frame the game reads its input in a routine at $26FA. The first instruction loads $0394 and
branches on the top bit: in normal play it goes on to scan the keyboard matrix and the joystick port,
and in attract mode it jumps to **$6392** instead. The physical scan never runs, which is the
mechanical reason the script works: nothing overwrites the shadow bytes it writes.

$6392 is a tape player:

```text
$6392  $0349 = $FF                 joystick shadow: nothing pressed
$6397  $DC00 = $7F                 select keyboard column 7
$639C  $DC01 & $90 ?= $90          SPACE or RUN/STOP?
$63A5    no  -> $0394 = $FF, RTS   leave attract
$63AB  Y = $03B1                   script index
$63AE  A = $03BB                   delay counter for this entry
$63B1  A >= $9300,Y ?
$63B6    no  -> $03BB += 1, RTS    spend one frame
$63BA  $03BB = 0
$63BF  A = $BD00,Y                 the entry
$63C2  A == 0 -> no key change
$63C4  column = (A >> 3) & 7
$63CB  row bit = A & 7
$63D0  A & $40 ?
$63D5    set   -> $034A[col] |=  $3D28[row]    key UP
$63E1    clear -> $034A[col] &= ~$3D28[row]    key DOWN
$63EC  $03B1 += 1
$63EF  loop while the index did not wrap
$63F1  wrapped: $03BA = $FF        the recording is over
```

Everything the demo appears to decide - turning, climbing, firing, typing - is the ordinary game
responding to input that happens to come from two tables.

The format is in the entry byte: bits 5-3 pick which of the eight column bytes at $034A to touch, bits
2-0 pick the row bit through the mask table at $3D28 (`01 02 04 08 10 20 40 80`), and **bit 6 says
whether the key goes up or down** - set means release, clear means press, because the matrix is active
low. Bit 7 is dead: all 256 entries have it set and the driver never tests it, which is a good sign
the table was hand-assembled.

The pacing is one byte per entry at $9300, and a delay unit is exactly one frame - measured by
counting 300 hits on $6392 against 300 increments of $11. The compare is `counter >= delay` and both
reset together, so entry *i* is applied on the call that is the sum of delays `0..i` after the first,
and entry 0 is applied on the very first call. Because the loop at $63EF repeats, one call can consume
several entries: `$9300[135]` is 0, so two entries go in one frame there.

The whole table is 256 entries, and the delays add up to **10,285 frames - 205.2 seconds** at the
PAL frame rate. That is the length of the attract mode: three and a half minutes of somebody playing
the game.

## What the recording does

Eighteen distinct keys appear in the script. The first sixteen entries type a word into the console,
at three or four frames per key:

```text
  0 $B6 down UP-ARROW  c6 b6   delay   0
  1 $F6 up   UP-ARROW  c6 b6   delay   4
  2 $AA down L         c5 b2   delay 211     entry 2 lands 215 frames in
  3 $EA up   L         c5 b2   delay   4
  4 $8A down A         c1 b2   delay   3
  5 $CA up   A         c1 b2   delay   3
  6 $9E down U         c3 b6   delay   3
  7 $DE up   U         c3 b6   delay   4
  8 $A7 down N         c4 b7   delay   7
  9 $E7 up   N         c4 b7   delay   4
 10 $94 down C         c2 b4   delay   3
 11 $D4 up   C         c2 b4   delay   3
 12 $9D down H         c3 b5   delay   1
 13 $DD up   H         c3 b5   delay   4
 14 $81 down RETURN    c0 b1   delay  10
 15 $C1 up   RETURN    c0 b1   delay   2
 16 $B2 down ;         c6 b2   delay  94     the rest is flight
 17 $F2 up   ;         c6 b2   delay 193
```

LAUNCH, then RETURN. The captured frame 240, a few entries in, shows the board computer's prompt
reading `>LAU` mid-word, so this is not an inference from the key codes - the picture has the word on
it. After RETURN the script flies, using the same keys the game polls in flight: `;` `X` `Z`
`/` `V` `M` `I` `.` `:` and SPACE, for the remaining ten thousand frames.

## What it flies over

Nothing in the demo path chooses a city. The restart calls $5766 to reset the flight variables and
$280B to rebuild the 48 object records from the city number at $0354, and nothing in the path writes
$0354. The captured demo frames read `REEMA` in the status panel, which is the city a fresh boot
starts in - so at boot the recording flies the starting city, and after an aborted mission it flies
whatever city that mission ended in. The demo is a recording of input, not of a place.

## How it ends

Two ways, and they are different code paths.

**The recording runs out.** `$03B1` wraps past $FF, the driver sets `$03BA = $FF`, and the main loop
picks that up at $208C and jumps to $645A, which pushes two messages, waits, and drops back into
$64D8. The script counters are reset and the recording plays again from the top. An untouched machine
loops it indefinitely.

**A key is pressed.** The test at `$639C` is narrower than "any key", and the narrowness is the
interesting part. It drives PA7 low with `$DC00 = $7F`, so only column 7 is read, and it masks
`$DC01` with `$90`. Column 7 holds `1`, LEFT-ARROW, CTRL, `2`, SPACE (bit 4), C=, Q and RUN/STOP
(bit 7), so:

| `$DC01 & $90` | meaning | result |
|---|---|---|
| `$90` | neither SPACE nor RUN/STOP | the recording plays |
| `$10` | SPACE down | `$0394 = $FF`, return |
| `$80` | RUN/STOP down | `$0394 = $FF`, return |
| anything else | Q, `2`, C= and the rest of column 7 | **no exit** |

Pressing Q inside the demo does nothing at all, and the delay counter still advances. `$0394 = $FF`
is a request rather than a state: on the next pass through the main loop, $207A clears it, $6403
restores the player's key table from the backup at $03EF, and $64F0 starts a new game. The demo hands
over by starting over.

> [!NOTE]
> **What this corrects.** The messages the machine pushes when the credits time out are `$6529`
> "DEMO MODE Initiated" and `$653F` "Press SPACE to exit."; the earlier version of this chapter
> printed a different string at `$653E` and had the demo waiting for a key the exit test does not
> read. The chapter also used to say any key ends the demo. It is two keys, in one column, and the
> mask is `$90`.

## The line under the picture

The credits screen and the demo both show a line of prose crawling along the bottom of the frame, and
it is the same line in both: `From CRL comes TAU CETI.` in the credits capture, and
`...time a cure was found, the planet's defence system had taken over` in the demo. Those are
paragraphs 1 and 5 of the story at $C000.

It is the border banner, it is eight hardware sprites, and it has its own chapter:
[The Border Banner](border-banner.md). The reason it can look like a separate piece of machinery is
that the routine that writes it does not draw pixels into the bitmap - it composes character blocks
for the sprites, which is also why it is the routine that gets mistaken for a music player. That
confusion is dealt with in [Sound System](sound.md).

## What is not reproduced

- **The credits picture.** `$6578` unpacks `(count, value)` runs from $0E00 into $0400, and the stream
  does not decode into 2,048 bytes under the run rule read off the routine: it produces 4,953 bytes
  and overruns the window. Either the entry state differs from the file on disk or the encoding has a
  case this reading misses. **Open**, and worth saying plainly: the credits screen is one picture and
  one message, and the picture is the part that has not been taken apart.
- **The pacing of the credits text.** `$41F7` blits a whole display list in one pass, so on the
  machine the 32 lines scroll through the five-row log window as fast as the raster stage can drain
  them. A reproduction that renders the same list into the same window ends with the same picture and
  different intermediate frames.

---

[Back to the overview](../README.md)
