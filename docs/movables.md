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

## The canvas and the painter

Drawing happens in two steps, through a small off-screen canvas.

**The canvas** is at $0400: eight rows of 64 bytes, two bits per pixel, cleared to $55 by the
routine at $40AC. Small, and not a screen - it is a working buffer for one band of the view.

**The painter** at $3F93 walks all forty-eight records and plots them into that canvas. It is the
routine that reads the type index, the flags, the X position and the depth, and decides what each
record looks like at its distance.

**The blitters** move the canvas into the bitmap. One at $3F29 copies the canvas into eight bands at
$E870, $E9B0, $EAF0, $EC30, $ED70, $EEB0, $EFF0 and $F130. A second at $223E reads a wider area,
$0400-$0BFF, and writes strips into $E148, $E288, $E3C8 and onwards, separating even and odd
destination bytes as it goes. The first is called from the raster stage 0 handler; the second is
gated by the flag at $0348 and waits for raster line $40 before it runs.

That split - paint the canvas, then blit it during a raster stage - is how the game gets a whole
screen redrawn without the display showing the work in progress.

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
