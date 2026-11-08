# Call Graph

How the frame routine, the raster stages and the message path call each other.

---

Tau Ceti's call graph is shallow. There are two entry points that matter - the frame routine and the
raster interrupt - and both call a flat list of workers rather than a deep tree of functions. This
chapter is the map of that flat structure.

## Per frame: $4D80

```text
$4D80  frame
 ├─ $3436   prepare the view
 ├─ $3723   draw the five gauge bars
 ├─ $37F5   gauges, second stage
 ├─ $4906   status line (DEMO/LAUNCHED/LANDED/DOCKED)
 ├─ $615F   context message
 ├─ $7689   bar animation            (skipped when $0396 = 1, i.e. landed)
 ├─ $6185   animation, second half
 ├─ $76BA   instrument update
 ├─ $73C4   the rod drop: docked at a reactor, scatter that city's halves
 ├─ $6444   wait for the message queues to drain
 └─ $46F3   tail call into the next frame
```

The routine is at $4D73 in running memory; $4D80 is thirteen bytes into it.

## Per frame: the raster handler at $3903

The hardware IRQ vector at $FFFE points here. It runs four times a frame, once per stage, and
dispatches through the 16-entry table at $498A:

```text
$3903  irq
 ├─ save A/X/Y, switch RAM in at $01
 ├─ acknowledge $D019
 ├─ set $D016/$D012/$D011 from the stage tables
 ├─ stage = (stage + 1) AND 3
 └─ jmp through $498A[(stage | $039D) * 2]     (target stored as address-1)

stage 0  $49BA ── wait for line $40, then $223E (canvas blit)
stage 1  $49D9 ── $D015=0, $26FA (input), $33F9, $334C, $34EC, $3D41, $35F6
stage 2  $49FD ── $33B7, $3803 (weapons), $25D3 (frame counter, flare timer)
stage 3  $4A0C ── $D015=0, $4690, $3968 (flight controls), $3436, jmp $86F8
```

The other three display modes substitute different handlers for stages 1-3, but stage 0 is the same
routine in all four.

## The message path

```text
$4127  queue a string address      -> ring buffer at $0C00, pointer $0384
$413B  queue a four-byte entry     -> ring buffer at $0C80, pointer $0391
$41F7  interpret the display list  -> glyph blitter, line ends at $80
$40E4  scroll the log              -> eight 80-byte row copies
$3E17  blit one glyph              -> 8 bytes into the bitmap
$6444  frame waits for $0383 = $0384
```

That is the whole text system: a producer ($4127), a ring buffer, a consumer ($41F7) and a
synchronisation point ($6444).

## The weapons path

```text
fire                 -> $3B13 block, one timer per weapon
missile              -> $4878 fills a free record at $0E00 with type $0A
AMM                  -> $4838 rewrites records whose type class has the $0C bits
flare                -> $0356 timer, read by the view painter
```

## The object path

```text
$280B  build the 48 records at $0E00 from the city's list ($0354)
$29B6  the renderer: gate, project, queue at $0D00, draw back to front
$305D  the span writer - the only routine that puts a record's pixels down
$3F93  the scanner painter: the records the world view did NOT mark on screen
$3F2D  transpose the scanner canvas into eight bitmap bands
$223E  blit the 2KB view canvas into $E148 and onward
```

and the attract path, which replaces input rather than drawing:

```text
$26FA  reads $0394: bit 7 clear -> scan the matrix, set -> JMP $6392
$6392  the script driver: delays at $9300, key events at $BD00
          writes $034A-$0351, the same shadow the joystick writes
$03B1  the index; $03BB the delay counter; $03BA "recording ended"
```

## What was here before

This chapter used to show four SVG diagrams and a 43-entry "dispatch table" at $1C100, with routine
sizes, first instructions and purposes. That table does not exist: $1C100 is inside the game's code
but it is not a table of entry points, and the sizes and descriptions were fabricated. The diagrams
were drawn from it, so they have been removed rather than redrawn.

The genuine dispatch table in this program is the 16-entry raster table at $498A, and it is
described in [Game Code](game-code.md).

---

[Back to the overview](../README.md)
