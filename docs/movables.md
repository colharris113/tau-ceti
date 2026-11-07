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
| Buildings, robots, turrets | records, distinguished only by their type index |

The type table at $C39A is the switchboard for all of it. Some entries are types the painter treats
as structures, some as vehicles, and the $0C mask used by the AMM routine marks the ones that count
as missiles.

> [!NOTE]
> Beyond the missile type $0A and the class bits themselves, I have not mapped individual type
> indices to individual kinds of building or robot. An earlier version of this chapter listed MK1,
> MK2 and MK3 robots, sand hoppers, guardian crawlers and proximity mines with AI behaviours and
> sprite numbers - all of it invented. The names may well be right, since they come from the manual,
> but nothing in this chapter's old table was read from the code.

---

[Back to the overview](../README.md)
