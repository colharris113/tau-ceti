# Map System

The MAP command: 64 projected points, a table of links, a zoom scale, and one routine still unread.

---

The map is the one screen in the game that is *drawn* rather than composed from a stored picture, and
it is also the screen the ending reuses: the win sequence zooms it out 31 times. For a long time this
was the shortest chapter in the guide because the chart's renderer had not been located. It has now,
and the reconstruction below is mostly measured - with one specific, named gap where it is not.

## What MAP does

`$7D59` is the handler, and it is short:

```text
$7D59  $277E(0,0)         blank the 16x16 window
       $5365              fill the arena $0400-$0BFF with $55, then wait for the blit
       $277E($01,$0D)     the window texture in colour 13
       the menu: six boxes, and the cursor
       $85BB              draw the chart
```

The six boxes are at `$7DAA` - zoom in, zoom out, next city, previous city, centre, exit - and they
are hit-tested through the same rectangle routine the RODS and REACTOR screens use, `$7075`. The
cursor is `$03C0/$03C1`, and it is seated by `$8422`, which is nine bytes:

```text
$8422  LDA $89A0,X -> $03C0
$8428  LDA $89C0,X -> $03C1
```

Call it with `X = 0` and the cursor lands on `$80/$80`, the centre of the map and the position of
Centralis. Call it with `X = 1` and it lands on `$8C/$94`, which is REEMA, the city a new game starts
in. That is how the game knows where you are without a separate "current city" coordinate: the city
number *is* the index into the coordinate table.

## The chart

`$85BB` is the drawing routine, and it is four stages in a row:

```text
$85BB  fill the whole 8K bitmap ($0400-$0BFF) with $55
$85C0  $848F      project the points
$85C3  if $03C2 >= $18: $858A      draw the city names
$85CD  $5372      wait for the raster stage to blit
```

`$848F` is where the data is:

1. **four source tables become 64 records.** For each `i` in 0-31 it copies `$89A0+i` and `$89C0+i`,
   then `$89E0+i` and `$8DE0+i`, into the four-byte records at `$0D00-$0DFF`. That is 64 points:
   two sets of 32, the first of which is the city list in name-table order.
2. **each point is projected.** The cursor is subtracted, `$40` added, and the result scaled by the
   zoom through the 8x8 multiply at `$424C`, with a sign fix-up. The scale is the table at `$86BB`,
   indexed by `$03C2`.
3. **the links are drawn.** `$85D0` clips a line and `$7F87` steps it out; one line per link, walked
   from a table at `$8900` - the same four-bytes-per-city table that records which directions have a
   jump pad.
4. **the names are drawn** when the zoom reaches `$18`: `$8648` blits an 8x8 glyph block into the
   bitmap for each point whose depth bytes say it is near.

## The zoom scale

`$86BB` is 32 bytes and it is used, in one place, at `$84E1`:

```text
08 0A 0C 0F 13 17 1C 22 28 2F 36 3E 46 4E 57 60
69 72 7C 86 90 9A A4 AE B8 C2 CC D6 E1 EB F5 FF
```

Thirty-one strictly ascending values, 8 at zoom 0 to 245 at zoom 30, and then a `$FF` - the last byte
before `$86DB`, which is the silence routine's first instruction. `$03C2` is clamped at `$1F`, so a
lookup at the clamp reads that `$FF` and the multiply does whatever `$FF` does. The machine's own
arithmetic; a port should not smooth it over.

This table is also the answer to a question the previous version of this chapter asked in the wrong
place: the "monotonically decaying curve" next to the city names that looked like a scale is a
projection table, and the map's actual scale is here, going up rather than down.

## The coordinates

The planet's coordinate system is a `$80`-based grid. The 32 city positions are two plain 32-byte
arrays, `$89A0` for X and `$89C0` for Y, in the same order as the names at `$8D02`. The second set of
32 points, at `$89E0` and `$8DE0`, is projected with the same code, which is why the chart has 64
points for a planet of 32 cities - two rings, or a near set and a far set.

Nothing here is inferred from a picture. `$8422` reads the first pair to place a cursor and `$848F`
reads all four to build the record table; both were read off the listing and both have been checked
against a capture of the screen.

## The win sequence

The ending is a zoom-out of this screen, and it reuses the chart rather than drawing anything new:

```text
$7987  $8422(0)                     centre the cursor on Centralis
$798C  $277E(0,0), $5365, $277E(1,1)
$799D  $03C2 = $1F
$79A2  loop: $85BB, DEC $03C2, BPL   31 passes
$79AA  $03C2 += 1, $7689, $537D($55), $76BA, wait for a key, $5AA9
       JMP $6473                     the "mission failed" exit, reused
```

Thirty-one passes from zoom 30 down to 0, each one redrawing the whole chart at the next scale. The
win therefore ends on the same exit path as a failure - the congratulations, then the map zooming out,
then the shared exit - which is either economy or a joke, and the code does not say which.

## What is not established

**How the plotter is reached.** `$7F87` is the Bresenham stepper and, read as a listing, it has no
store in `$7F87-$8030` at all. The pixel write is at `$8031` - `ORA $21D7,X`, the 2-bit pixel mask
table - and **no `JSR $8031` exists anywhere in the image**. Something reaches that write that is not
a call, most likely a fall-through from a branch inside the stepper, and until that is settled the
chart's drawing cannot be transcribed with confidence. This is a matter of the 6502, not of the
measurements: a captured picture of the screen exists, so a port can be checked when it is done.

**Whether the links are the jump-pad pairings.** `$85BB` walks `$8900`, and `$8900` is the
four-bytes-per-city pad table. That is consistent with the manual's "the pad takes you where it is
paired", and it is not proof: the same four bytes could be read as four link slots without telling
you which city is at the other end.

**The second ring.** `$89E0`/`$8DE0` are projected and drawn exactly like the first, but what the
second 32 points *are* - a second set of cities, the same cities at a different scale, or stars - has
not been established. The label pass at `$858A` draws names only for points whose depth bytes say they
are near, which suggests the second ring is background.

> [!NOTE]
> **What this corrects.** The previous version of this chapter said the MAP command's rendering code
> had not been identified and that no table of 32 city positions existed. Both were true when written
> and are now out of date: the chart is `$85BB`, the renderer is `$848F`, and the coordinates are at
> `$89A0`/`$89C0`. What has *not* moved is the plotter - `$7F87`'s pixel write is still reached by a
> path no call instruction explains.

---

[Back to the overview](../README.md)
