# Game Code

Entry, frame loop, the four-stage raster interrupt, and the message system.

---

Tau Ceti's code is not one loop. It is a main routine that runs frame by frame, plus a raster
interrupt that fires four times per frame and does a different job each time. Understanding which
of the two owns which task explains most of the game's structure.

## Entry

The loader finishes with `JMP $2000`, and the first instructions there are:

```asm
$2000  A2 FE     LDX #$FE
$2002  9A        TXS           ; reset the stack
$2003  20 FE 56  JSR $56FE     ; hardware and screen setup
$2006  20 64 56  JSR $5664
$2009  20 66 57  JSR $5766     ; reset the flight variables
$200C  20 D8 56  JSR $56D8     ; clear timers, key map, joystick shadows
$200F  20 50 62  JSR $6250
```

Then the main loop starts and never returns to the loader.

## The frame routine at $4D80

Once a frame, the main code runs a fixed sequence of calls. The order is the design:

| Call | What it does |
|---|---|
| $3436 | prepares the view |
| $3723 | draws the five gauge bars |
| $37F5 | draws the gauges' second stage |
| $4906 | writes the status line (DEMO / LAUNCHED / LANDED / DOCKED) |
| $615F | context message for the current state |
| $7689 | bar animation, skipped when landed |
| $6185 | second half of that animation |
| $76BA | instrument update |
| $73C4 | the rod drop: if you are docked at a reactor, scatter that city's halves |
| $6444 | waits for the frame's work to finish |
| $46F3 | tail call into the next frame |

The routine runs at **$4D73** in memory; $4D80, which this chapter used to print, is thirteen bytes
into it, and the disk image's bytes at that address are part of a message table rather than this
routine. Read the code from a RAM dump in this region, not from the file.

Two details are worth noting because they show how the machine is being paced. $6444 is a
busy-wait: it compares two bytes at $0383 and $0384 - the message queue's read and write pointers -
and returns only when they match, which means every queued message has been printed. And $4DA9
clears the KERNAL keyboard buffer length at $C6 before the tail call, so a key press cannot leak
into the next frame twice.

## The raster interrupt at $3903

The hardware vector at $FFFE points at $3903, not at the KERNAL's $0314. On entry the handler saves
A, X, Y and the CPU port byte, switches RAM back in at $01, acknowledges the VIC's interrupt by
writing $D019 back to itself, and then does the interesting part:

- reads the stage number from $6F (0-3);
- writes a new $D016, $D012 and $D011 from three four-byte tables at $395C, $3960 and $3964;
- rotates the stage number for next time;
- re-enables interrupts and dispatches into a 16-entry table at $498A.

The tables are the screen split. Each stage sets the mode, the line the *next* stage fires on, and
the control register, so the screen is divided into four bands with different VIC settings:

| Stage | $D016 | Next line ($D012) | $D011 |
|---|---|---|---|
| 0 | $18 (multicolour) | $CA (202) | $38 |
| 1 | $08 (hires) | $F8 (248) | $38 |
| 2 | $08 (hires) | $14 (20) | $B0 |
| 3 | $08 (hires) | $30 (48) | $30 |

The effect is a multicolour playfield band with hires bands above and below it - the standard C64
way to get sharp small text over a soft-coloured picture.

### The dispatch table

The table at $498A holds sixteen addresses, laid out as four display modes times four stages. The
mode comes from $039D, which the game changes as the screen changes (0, 4, 8 and 12 are the values
seen); the index is `(stage | mode) * 2`.

The entries are stored as target-minus-one, because the trampoline at $3953 does not jump. It
pushes the target address onto the stack and executes `RTS`, which pops it and continues one byte
later - so the table has to point one short of the real handler.

What the handlers do, in the mode-0 layout:

| Stage | Handler | Work |
|---|---|---|
| 0 | $49BA | waits for line $40, then blits the flight canvas to the bitmap with $223E |
| 1 | $49D9 | disables sprites, reads input with $26FA, updates the instruments |
| 2 | $49FD | runs the slow timers: $3803 (weapons), $25D3 (frame counter, flare timer) |
| 3 | $4A0C | reads the flight controls with $3968 and $3436, then falls into $86F8 |

Most handlers begin with `STA $D015` of zero. There are no sprites in this game; the register is
cleared every frame to be certain of it.

### Why the split matters

Because the interrupt owns input, the weapons and the playfield blit, the main routine at $4D80 can
spend its whole frame budget on drawing gauges and text. The two halves communicate through flags:
$0348 gates the blit, $0395 pauses the update, $039D selects the display mode and so chooses a
whole different set of stage handlers.

## The stage machine

There is no separate "game mode" structure. The whole of Tau Ceti's outer state is one byte, `$0394`,
and the code tests its top bit:

| `$0394` | state | who sets it |
|---|---|---|
| `$00` | playing | `$6495` (credits skipped), `$207A` (leaving attract) |
| `$80` | attract | `$64CF` (credits timed out) |
| `$FF` | a key was pressed in attract | `$63A5` |

and two more bytes finish the job: `$0396` for flight state (0 launched, 1 landed, `$80` docked) and
`$03BA` for "the demo recording has ended". The boot is a walk through the same bytes:

```text
$2000  start-up, credits screen
$648D  1000-frame wait, SPACE or RUN/STOP breaks out
$64BB  timeout: key table restored, messages pushed, $0394 = $80
$64D8  reset the script counters, rebuild the city, JMP $4D7D
$207A  a key in attract: $0394 = 0, key table restored, new game
```

So the credits, the attract mode and the game itself are three states of one flag rather than three
programs, and the hand-over from attract to play is a write of `$00` followed by the new-game tail.

## The message system

Text is not printed directly. Messages are queued and printed by the raster side.

- $4127 queues a two-byte entry - low and high byte of a string address - into a ring buffer at
  $0C00, using a write pointer at $0384.
- $413B queues a four-byte entry at $0C80 for the second kind of message.
- $41F7 is the interpreter: it walks the queued list with a pointer at $1C, treats bytes below $80
  as glyph indices (multiply by 8, carry selects bank $9000/$9100/$9200, copy 8 bytes to $FCC8,Y),
  $80 as end-of-line, and anything above $80 as end-of-list.

When a line ends, $40E4 scrolls the log up by copying whole rows: $F908 to $F7C8, $F958 to $F818,
$FA48 to $F908, $FA98 to $F958, $FB88 to $FA48, $FBD8 to $FA98, $FCC8 to $FB88 and $FD18 to
$FBD8. That is a straight memory move of eight 80-byte rows - the log is a fixed-size display
buffer, not a text window with scrolling hardware.

> [!NOTE]
> This chapter replaces an earlier version that described a game-state machine at $E009 and a set
> of rendering routines at $28C4-$2B5A. Those addresses are not code in this image: the state is
> held in $0394 and $0396, and the frame work is the sequence of calls above. The old listings
> were reconstructions rather than disassembly.

---

[Back to the overview](../README.md)
