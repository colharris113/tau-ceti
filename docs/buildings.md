# Buildings and Interiors

What a building is in this game: a numbered record, three tables that describe it, an airlock, and a
view inside.

---

Cities are assembled from a small vocabulary of structures, and the game's word for one is a number.
Byte 0 of a sixteen-byte record at $0E00 is a type index, and the builder at $280B copies it straight
out of the city's own object list at $9400. There are thirty-seven of those numbers, $00 to $24,
thirty of which appear in the shipped data: 1,005 records across the 32 cities, so the ground of a
city is largely this one table rearranged. The hoppers at $24 and the pad pair at $0F and $10 are
accounted for elsewhere; what follows is the rest of the vocabulary.

## Three tables, not one

Each type is described by three parallel tables, all indexed by the type byte:

| Address | Contents | Read by |
|---|---|---|
| $C39A | class byte | the missile marker at $4855, the kill path at $4977, the update loop at $4462, the painter at $4079 |
| $C3BF | parameter byte, copied into record byte 7 | the builder, at $2833 |
| $C409 | behaviour class in the low nibble, two flags in the top bits | the ground-unit dispatcher at $81F5 |

The class byte does the work, because four parts of the game ask it four different questions:

| Bit | Meaning | Evidence |
|---|---|---|
| $0C | this type is a missile | $4855 marks the record hostile and $44CE fires it |
| $40 | this type scores when destroyed | $4977 adds one to the counter at $03A5-$03A6 |
| $20 | this type has a ground handler | $4645 hands the record to the routine at $80C3 |
| $80 | never draw this type | $4079 gives the painter a fill of zero |

The scoring bit deserves its own line, because it is the only place in the game where destruction is
counted. When a record dies, $4957 takes its remaining strength out of byte 7; when that runs out it
marks the record $40 and, if the type's class byte has bit 6 set, adds one to a sixteen-bit counter at
$03A5. That counter is printed by the routine at $5AD4. Eleven of the thirty types carry the bit, so
the city has a price list whether or not the player ever sees one.

## What the twelve drawings describe

The Spectrum inlay draws twelve silhouettes - tall cone, low cone, dome, dome with a mast, stepped
block, angular tower with a crossbar, half-sphere, sphere, three finned hulls, and a mast on a stepped
platform - each filled with its own dot or hatch pattern. It is an attractive way to present a
building set, and none of it is in the Commodore version.

Here the painter at $3F93 reduces every record in the table to the same mark. It takes the record's X
position and depth, projects them into the canvas at $0400, and writes the same two bytes for a reactor
as for a hunter: a fill of $AA for the stipple, $FF when record byte 3 has bit 3 set, and zero when the
type's class byte has bit 7 set. There is no per-type shape in the drawing code, no outline table and
no silhouette bank. The earlier version of this chapter claimed the game renders each type "as a unique
bitmap pattern", and it does not: on the C64 a reactor and a supply dome are distinguished by where
they stand, by how far away they are, and by what they do when you arrive.

That changes how the publisher's names read. MAIN CENTRAL REACTOR, REACTOR SUBSTATION, SUPPLY CENTRE
(CIVILIAN), SUPPLY CENTRE (MILITARY), FORTRESS, CONTROL TOWER, DOME, SPHERE and JUMP PAD COMPLEX are
the publisher's names for a different machine's artwork. Five numbers in this one can be tied to a
name with evidence behind it: $0A is a missile, $0F and $10 are the two records that make a jump pad,
$1A is the proximity mine ([Moveable Elements](movables.md)), and $24 is the sand hopper
([Sand Hoppers](creatures.md)). Everything else is a number. The old table in this chapter -
"Main, Reactor, Military, Civil, Gal-Corp Lander, Jump Pad, Fortress, Control Tower, Turret" - mixed
manual names with guesses, and the turret is not in the manual either.

## Interiors

Interiors use the same machinery as the rest of the screen: glyph patterns through the blitter at
$3E17, into the same 320x200 bitmap. The equipment panel is the one interior that has been
disassembled ([Board Computer](board-computer.md)), and it is a small form of two adjustable numbers
and a toggle rather than a picture. The old version of this chapter described interiors as ~200-byte
pre-drawn bitmaps scattered across tracks, with labelled rows such as "DRINKS MACHINE"; that layout was
not read from the disk and should not be relied on.

What matters in play is the same for all of them: you dock, you get whatever the building offers, and
the offerings are fuel, repair and rearming.

## DFP airlocks

Every building's airlock is a DFP energy screen, and it flickers. That much the publisher and the
screen agree on: the inlay tells you to recognise the characteristic flickering pattern, wait for the
aperture to open fully and fly in slowly.

The guide used to give the flicker as a timer crossing a threshold - open for about two seconds,
closed for about one - and used to call docking a test of speed, aperture and alignment. Neither
should be taken as established. What the code does say about arriving is in
[Game State](game-state.md): landing is speed zero and height zero at $3BEB, and the flight state at
$0396 holds 0 for launched, 1 for landed and 2 upwards for docked. The routine that decides which
building you docked with, and whether the aperture was open when you did it, has not been located.

## Shadows

The earlier version of this chapter gave a shadow algorithm - sun angle, a tangent for length, a dark
version of the building colour. There is no tangent in this game and no shadow code in the painter.
The painter does not even read the record's height byte; the collision test at $2B60 and the radar blip
at $2EC9 are the two routines that do. Treat the shadows in the view as unexplained.

---

[Back to the overview](../README.md)
