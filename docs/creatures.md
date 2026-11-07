# Sand Hoppers

The small things on the ground at the jump pads: which record they are, where the city data puts
them, and the short routine that makes them hop.

---

Every city has at least one jump pad, and in seventeen of them a pad has company. Sit still near one
for a few seconds and you notice small objects on the ground, bobbing. They do not shoot, they do not
chase you, and they do not seem to do anything at all - until you fly into one.

The manual gives them a name and a warning in the same sentence, and that sentence is the only
description of them anywhere:

> Gal-corp recommends caution on exit from a jump as reports indicate that small 'sand hoppers', a
> native life-form, tend to cluster around the feeder pipes of jump pads and lives have been lost in
> the past due to collisions.

Two claims, and the code backs both of them: they cluster around the pads, and they are solid enough
to hurt you. What follows is where that lives in the machine.

## Which record they are

Everything on the ground in a city is one of the forty-eight records at $0E00, and byte 0 of the
record is a type index into the table at $C39A. There are thirty-seven types in use, $00 to $24, and
the hoppers are **type $24**.

The identification is not a guess from the name. The routine at $80C3 opens by testing the record's
type byte against two values:

```text
$80C8  CPX #$24
$80CC  CMP #$15
```

The type byte is almost always reduced to its class byte before anything is decided; this routine is
one of the few places that tests the type number itself, and the jump pad's $10 at $2BDE is another.
Type $24 has class $20 and parameter $10, and bit 5 of that class byte is rare: only types $27, $28
and $2B share it.

The **47 hopper records on the disk**, spread over 17 of the 32 cities, come from the city object
lists. Each city owns 32 slots of three bytes at $9400 + city × 96: type, X, Y. A slot whose type
byte is $C0 is unused, and the builder at $280B stops at the first one. Most cities have all 32 slots
filled; the emptiest, REEMA, stops at 23. The hopper count varies the same way: ROON has five,
ENTROLA, ERMA and KRILL four, TSULA, SCARTH and PREEMA one, and fifteen cities have none at all.

## Where they sit

The pads themselves are easy to find in the same data. Four bytes per city at $8900 + city × 4 say
which of the four directions have a pad - bit 7 set means no pad - and the coordinates come from four
fixed eight-byte groups at $C4BE. Every pad in the game is at one of four places:

| Group | Pad at |
|---|---|
| 0 | $80, $A0 |
| 1 | $80, $60 |
| 2 | $A0, $80 |
| 3 | $60, $80 |

Two are on the vertical centre line with the other axis at its limit, two on the horizontal one, so
these are the four edge midpoints the manual calls north, south, east and west. Which of the two
vertical ones is which I cannot tell you - the map has no compass rose in the data.

Each pad is built as two records: type $10 on the pad itself, and a type $0F marker two units further
out. The hoppers are not part of that pair. They are ordinary entries in the city's own list, placed
by hand around the pad slots:

| City | Hopper | Pad slot | Offset |
|---|---|---|---|
| CENTRALIS | $9C,$80 | $A0,$80 | -4, 0 |
| CENTRALIS | $9E,$82 | $A0,$80 | -2, +2 |
| HAME | $62,$7C | $60,$80 | +2, -4 |
| ROON | $7C,$9E | $80,$A0 | -4, -2 |
| KRILL | $9C,$7A | $A0,$80 | -4, -6 |

The offsets are small, and all 47 are nearer the city centre than the pad they stand beside: a hopper
at $9E,$82 sits just inside the pad at $A0,$80, never beyond it. Across all 47:

| Within N of a pad centre | Hopper records | All objects |
|---|---|---|
| 4 units | 49% | 3% |
| 8 units | 81% | 12% |
| 16 units | 98% | 48% |

Objects in general are spread over the map; hoppers are not. They arrive in little groups of one to
five, one group per city, and the group is always at a pad - usually at a pad that city actually has,
sometimes at a slot where a pad would be if the city had one. In PREEMA the group sits at the
$A0,$80 slot; in REYES it is the outlier, three records sixteen to eighteen units from the nearest
slot, halfway into the street.

## What they do

The per-frame object update is at $43CF, called from the main loop at $2057. It walks all forty-eight
records, reads the class byte, and dispatches. Type $24's class ($20) sends it to the handler at
$80C3, which does this:

- reads bit 0 of record byte 3 and turns it into a step of +8 or -8;
- adds that step to **byte 6**, the record's height, every frame;
- flips bit 0 of byte 3 - and so reverses the step - when the height runs past $F8 at the top or
  wraps to nought at the bottom.

That is the whole of it. Byte 6 climbs by 8 a frame for thirty-one frames, reverses, falls back, and
reverses again: a full hop every sixty-two frames, a little over a second. The type-$15 branch at
$80FF shows how deliberately small this is - type $15 takes the same hop and then carries on into a
long walk routine at $8104 that picks a random target near your ship and steps toward it. Type $24
returns at $80FF and does nothing else. It hops where it stands.

Because the record keeps its own phase, a hopper you fly away from and come back to is still mid-hop.
And because the builder at $280B zeroes bytes 3 to 15 of every record before writing the type's
parameter byte into byte 7, every hopper in a city starts each visit from the ground, on the way up:
jump into a city and the group at the pad is at the bottom of its first hop.

They are also solid. The collision scanner that finds the object under your ship runs from $2A45: it
projects each record against the ship's position, keeps the ones inside a narrow window, and at
$2B60 decides what contact means. A jump pad (type $10) triggers the jump. Anything else is compared
by height - your altitude at $0344 against the record's byte 6, adjusted by the per-type table at
$C3E4 - and if the two overlap, the contact runs into the hit routine at $3E65, which banks the
damage and sets the "you have been hit" flag at $0381 when it overflows. Type $24 has no exemption.
Fly into one and you are charged for it, which is the manual's "lives have been lost in the past due
to collisions" with an address on it.

What they never do is fight. There is no attack code for them, and no flag set for them in $03B0, the
byte the object handlers use to report things like "something is close" or "you have been seen".

## How they are drawn

They are not sprites and they are not glyphs. The world has no sprite hardware at all - the only
sprites in the game are the bottom-border banner and the row of instrument sprites that $3436 sets up
each frame - and the glyph blitter at $3E17 exists to put text in the bitmap. Objects get painted.

The painter at $3F93 walks the record table, skips anything not flagged as drawn in byte 3, converts
each record's X and depth into a canvas offset, and writes two bits per pixel into the canvas at
$0400. Two blitters then move that canvas into the bitmap: $3F29 for eight bands, $223E for the
wider strips. Both run every frame.

What a record contributes to that canvas is decided by its class byte, in three cases:

| Class bit 7 | Byte 3 bit 3 | Fill |
|---|---|---|
| set | - | nothing (the object is left out of the fill pass) |
| clear | set | solid, $FF |
| clear | clear | stipple, $AA |

Type $24 is the third row: class $20 has bit 7 clear, and nothing sets bit 3 of a hopper's byte 3. So
it is drawn as a stippled mark - a two-bit checkerboard rather than a solid block - sized and placed
by its distance from the ship.

Where the hop goes on screen I could not pin down. The painter reads the record's X and depth from
bytes 10 to 13, and the flags in byte 3, but it never touches byte 6, so the vertical motion the
height implies has to be applied by something I have not found. What can be shown is that the height
is used: the collision test compares byte 6 with your altitude, and the radar blip routine at $2EC9
subtracts it from your altitude to place the blip on the scope. A hopper that is hopping has a blip
that slides up and down its column, whether or not the mark in the view moves with it.

There is no picture of a sand hopper anywhere in the image. The per-type data I could find is a class
byte at $C39A, a parameter byte at $C3BF, a height tolerance at $C3E4, and three tables used by the
walkers at $C409, $C42E and $C43E. None of them is graphics. Whatever a hopper looks like comes out
of the painter's geometry, not out of a stored shape.

> [!NOTE]
> **What I could not establish.** I could not decode the painter far enough to predict a record's
> outline from its numbers, and I could not find where a record's height byte is folded into the view
> - the painter does not read it, and the routine that fills in the projected X and depth at bytes 10
> to 13 is still unidentified. What is solid is the mechanism: record, painter, canvas, blitter, two
> bits per pixel, and a fill pattern chosen by the class byte. The rest of the geometry is a gap this
> chapter leaves open rather than fills.

## The name

"Sand hopper" is the manual's word and nothing else's. No name for type $24 appears anywhere in the
program: the game's text names weapons, commands, cities and messages, never a creature. Type $24 is
a number, and the only thing in the machine that singles it out is a `CPX #$24` in a hop routine.

So the name is a manual label attached to a record by evidence rather than by a string: by where the
records sit (at the pads), by what they do (hop on the spot), and by the fact that they hurt when you
hit them, which is exactly the manual's warning. The previous version of this guide said sand hoppers
were "ground vehicles near jump pads, VIC-II sprite, moves slowly". All three clauses are wrong: they
are not vehicles, they do not travel, and there is no sprite.

## What this corrects

[Moveable Elements](movables.md) carried a note saying that the old list of robots, hoppers, crawlers
and mines was invented and that only missile type $0A had been mapped. That note was right about the
list, and it is now out of date about the hoppers. The rest of it still stands: the robot marks,
guardian crawlers and proximity mines named in the manual have not been tied to type indices here,
and I am not going to guess which is which.

[Buildings and Interiors](buildings.md) mentioned sand hoppers only inside a table cell describing
the jump pad interior bitmap. The creatures in the city are records, and they have their own chapter
now.

---

[Back to the overview](../README.md)
