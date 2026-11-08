# Moveable Elements

There are no sprites in the world. Everything you see moving is a record and a painter.

---

Tau Ceti draws its whole world, including everything that moves, into a bitmap. The VIC-II sprite
registers are not used for the objects - the raster handlers write zero to $D015 at the top of
almost every stage, which is as explicit as the code can be about it. So the question "how are the
moving objects rendered" has a different answer than the one this chapter used to give: they are
entries in a table, and the table is painted every frame.

There is one exception, and it is not in the world: the scrolling line in the bottom border is eight
hardware sprites. [The Border Banner](border-banner.md) covers it.

## The object table

The world is forty-eight records of sixteen bytes, at $0E00-$10FF. Each record describes one thing
in the city:

| Byte | Contents |
|---|---|
| 0 | type index, into the table at $C39A |
| 3 | flags: $40 drawn, $08 variant |
| 10-11 | X position, 16-bit |
| 12-13 | depth |

Byte 7 of each record is filled from a per-type table at $C3BF, indexed by `byte0 AND $3F`, which is
where the type-specific parameters live.

The table is not static. It is rebuilt at run time by the routine at $280B, from a per-city object
list that is located using the city number at $0354. That is why the bytes on the original disk do
not match the records in a running game: the disk holds the source lists, and the table at $0E00 is
assembled from them when you arrive in a city.

## The canvas and the two blitters

Drawing happens in two steps, through an off-screen canvas.

**The canvas** is 16 rows of 128 bytes at `$0400-$0BFF`, two bits per pixel, cleared to `$55` by
`$40AC` before anything is painted. The scanner window uses only the first 512 bytes of it; the main
view uses all 2,048.

**The renderer** at `$29B6` walks all forty-eight records and paints the ones that pass a gate into
that canvas. It reads the type index, the flags and the two 16-bit positions, and decides what each
record looks like at its distance. It is the routine that draws the world, and it is proven:
run from a captured state it reproduces the captured arena **2,048 bytes of 2,048**, and the span
writer it ends in is the only thing in the game that puts a record's pixels down.

**The blitters** move the canvas into the bitmap. One at `$3F2D` copies 512 bytes into eight bands at
`$E870`, `$E9B0`, `$EAF0`, `$EC30`, `$ED70`, `$EEB0`, `$EFF0` and `$F130` - the scanner window, and it
does it as a byte transpose, so the destination index is `8*(X&7) + (X>>3)`. The other at `$223E`
reads the full 2,048 bytes and writes strips into `$E148`, `$E288`, `$E3C8` and onwards, interleaving
even and odd source bytes into the eight bytes of each destination cell. Both are exact: driven from
a known arena they reproduce the bitmap with **0 of 8,000 bytes differing**.

That split - paint the canvas, then blit it during a raster stage - is how the game gets a whole
screen redrawn without showing the work in progress.

## The gate: why planting a record changes nothing

The renderer draws only a fraction of the 48 records on any given frame, and the tests that decide it
are worth writing down, because they are the difference between "the object is in the world" and "the
object is on the screen". In order:

```text
$2A4D  clear bit 6 of record[3]                  "drawn this frame"
$2A55  record[0] bit 7 set -> skip               a free slot draws nothing
$2A7C  depth   = (record[1]:record[4]) - ($033C:$033B)     16-bit
$2AA2  |depth| high byte >= $10 -> skip
$2AAA  lateral = (record[2]:record[5]) - ($033F:$033E)     16-bit
$2AD0  |lateral| high byte >= $10 -> skip
$2B60  project: scale from the depth, screen X from record[10]/[11]
$2BB3  projected row >= $10 -> skip              the arena is 16 rows
$2BBE  record[13] = row, record[12] = column
$2BC8  record[3] |= $40                          "on screen this frame"
$2BD3  row bit 7 set or column >= $80 -> the NEAR path $2CC0
       else                              the FAR path $2BD6
```

The window test is on the **high byte** of a 16-bit difference, so it is a window of `+/-$1000` world
units and the low byte only reaches it through the sign. Twelve of the 27 live records in a captured
frame are inside the window, and fewer than that survive the row and half-width culls.

Then there are two paths, and only one of them draws immediately:

- **the near path**, `$2CC0`, taken when the projected row has bit 7 set or the column is `$80` or
  more: `$2CC6` takes a half width from the reciprocal tables at `$8A00`/`$8B00` - no divide - and
  jumps straight to the queue append. A record at depth 0 gets half width `$7F` and is culled as
  off-screen before it is ever queued.
- **the far path**, `$2BD6` on: type `$10` is the landing pad and is special-cased, everything else
  goes through the footprint test at `$2BF9`, then `$2E60` culls sideways and `$305D` writes spans.

Both end in the same place. `$2D5F` appends a four-byte entry to the queue at `$0D00` - pointer low,
pointer high, the record's column and row - and `$2D9F` repeatedly finds the entry with the largest
column:row key, zeroes it and draws it. **The queue is drawn back to front**, which is what makes the
near path work: near objects are not drawn by a different routine, they are queued and drawn later by
the same span writer, in depth order.

One more filter sits in the append, and it is easy to miss: `$2D76` tests the parity of the projected
X value and **drops the entry if it is odd**. In a measured frame ten records reach `$2D5F` and only
eight are queued; the two that vanish are not culled, they are filtered. The dropped pair depends on
the projection, so it is not a fixed set of records.

## The scanner draws the complement

`$3F93` is not a second world renderer. It walks the same 48 records and paints the ones with
`record[0] & $C0 == 0` **and `record[3] & $40 == 0`** - exactly the records the world view did not mark
as on screen this frame. The scanner shows what is not in front of you.

That makes bit 6 of `record[3]` a byte with three meanings at three moments, and they have to be kept
apart: `$2BC8` sets it for records the world view projected, `$4622` reads it to decide whether a robot
thinks, and `$3F93` uses it to skip those records on the scanner. It is cleared at the top of the
renderer and rebuilt every frame, so it is not state - it is a note to the rest of the frame.


## What the moving things are

| Thing | How it exists in the game |
|---|---|
| Player missiles | a record of type $0A, created by $4878 at the sight position |
| Hostile missiles | records of a type whose $C39A entry has the $0C class bits set |
| AMM | not an object; it rewrites records in place (see [weapons](weapons.md)) |
| Flares | not an object; a timer that changes how the view is painted |
| Sand hoppers | records of type $24, grouped at the jump pads (see [Sand Hoppers](creatures.md)) |
| Ground units | records whose class byte has bit 5 set, handed to $80C3 - hoppers and walkers both |
| Proximity mines | records of type $1A, special-cased by name at $8204 |
| Buildings, robots, turrets | records, distinguished only by their type index |

The type table at $C39A is the switchboard for all of it. Some entries are types the painter treats
as structures, some as vehicles, and the $0C mask used by the AMM routine marks the ones that count
as missiles.

## The ground units

The armed robots are the one family that can be put in order, because the second per-type table at
$C409 carries a handler class in its low nibble and two flags above it. Bit 6 marks the types that arm
the alarm: once one of them has been in sight long enough - the counter in record byte 9 runs to $18 at
$8285 - the game prints `ROBOT ALL ACTIVATED` and $4838 marks every missile-class record hostile.

Classes 0 to 4 are the walkers, dispatched through $8106 and $81F5. Each steps its own X position and
depth toward the ship by the amount in $C43E, and stops once it is further away than the engagement
range in $C42E:

| Type | Class | Parameter ($C3BF) | Engages within ($C42E) | Step ($C43E) |
|---|---|---|---|---|
| $15 | 0 | $1C | 8 | $0E |
| $14 | 1 | $18 | 9 | $0B |
| $03 | 2 | $20 | $0B | $0E |
| $06 | 3 | $28 | $0D | $11 |
| $09 | 4 | $34 | $10 | $14 |

Type $15 is the odd one: it shares the hopper's hop before it walks, which is why
[Sand Hoppers](creatures.md) meets it there. The other four are one machine in four strengths, and if
the publisher's "marks I, II and III" are in this table at all, they are $03, $06 and $09 - three types
whose parameter, range and step all climb together, and the last of which is the only walker carrying
the alarm flag. That is the best fit the data offers and it is still an inference: nothing in the
program prints a mark number, so the manual's marks cannot be attached to types with certainty.

The proximity mine is easier. Type $1A is tested by name at $8204, ahead of the general dispatch: if
you are between four and six units from it, $821D prints `MINE DETONATED`, puts $30 damage through
$3E65 and removes the record. So the inlay's line about radar detecting proximity mines is describing
something the code really has, and it is a number after all.

> [!NOTE]
> Beyond the missile type $0A, the hopper type $24, the mine at $1A, the five walkers above and the
> class bits themselves, I have not mapped individual type indices to individual kinds of building. An
> earlier version of this chapter listed MK1, MK2 and MK3 robots, sand hoppers, guardian crawlers and
> proximity mines with AI behaviours and sprite numbers - all of it invented. The hoppers, the mine and
> the walker ladder now have evidence behind them; the fortress, the turret and the crawler are still
> names from the manual with nothing in the code to attach them to.

---

[Back to the overview](../README.md)
