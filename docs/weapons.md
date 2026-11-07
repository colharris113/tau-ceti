# Flares, Missiles and AMM

Three counters in the supply box, three completely different mechanisms behind them.

---

The box at the lower right of the flight screen carries three single-character readouts, labelled
MIS, AMM and FLAR. They look like the same kind of thing - a number that goes down when you use it -
and they are the only place in the game where three quite different designs are presented as if
they were a set.

## The counters

All three are ordinary bytes in page 3, and all three start at 8:

| Reading | Variable | HUD cell (column,row) | Drawn by |
|---|---|---|---|
| MIS | $0358 | $23,$0F | $350A |
| AMM | $0357 | $23,$10 | $3514 |
| FLAR | $0355 | $23,$11 | $3500 |

Each is drawn as a *single glyph*: the routine loads the counter and hands it to the glyph blitter
at $3E17 as if it were a character code. That works because the counts only ever run from 8 down
to 0, so one digit is always enough - but it does mean the display has no spare room. Nothing
formats a two-digit number here.

Each also has its own cooldown timer immediately above it in memory - $0366 for missiles, $0367
for AMM, $0365 for flares - and all three are cleared when a new game starts, in the block that
$56D8 wipes.

## Missiles: a thing you put in the world

Firing a missile is the only one of the three that creates something.

The routine at $4878 walks the page at $1000 - the last sixteen of the forty-eight records, sixteen
bytes each, the same table that holds buildings, robots and every other drawing object - looking
for a free slot, which is a record whose first byte has bit 7 set. When it finds one it writes:

- the type byte, $0A, at offset 0;
- the sight coordinates: $033C and $033F in bytes 1-2, $033B and $033E in bytes 4-5;
- the flags byte, $40, at offset 3 - the bit the drawing code treats as "live";
- the ship's height, $0344, plus $40, at offset 6.

Then it decrements $0358, plays the launch effect by setting $03C4, and refreshes the MIS readout.

The important consequence is that a missile is not a sprite or a special effect. It is an entry in
the same list as the buildings, moved and drawn by the same object code, which is why missiles
inherit the game's collision and drawing behaviour for free. It also means the four bytes it takes
from the sight are the four values the projection helpers at $26CC and $26D4 have just calculated
for the gunsight - a missile is spawned exactly where you are aiming.

The ammo message when the counter is empty is `NO MISSILES LEFT` ($3C5E).

## AMM: a thing you do to the world

An anti-missile missile never becomes an object. Firing one runs $4838, which scans the object
table from $1000 and, for every record whose type byte points at a class entry with the $0C bits
set in the table at $C39A, sets bit 6 of the record's type byte and zeroes a byte eight further in.

Two details follow from that, and both are verifiable in the table:

- The test is a *class* test, not a target lock. It does not pick the nearest threat or the missile
  aimed at you; it flags everything of that class in the list.
- The player's own missile type ($0A) is in the class: $C39A[$0A] is $09, and $09 AND $0C is 8 -
  not zero, so it passes the test. Firing an AMM while your own missile is still in the air catches
  that too.

The routine also sets $0359 to $FF, a flag the flight-view painter reads, and $03C5 to $0B for the
effect. The message is `AMM DETONATED` ($3C95), or `NO AMMS AVAILABLE` ($3CA4) when the counter is
empty.

So the AMM is not a projectile that flies out and intercepts. It is an instant edit to the object
table, and what makes it feel like a counter-measure is that it only touches objects the type table
marks as missiles.

## Flares: a thing you do to yourself

A flare creates no object either, and it does not touch the object table at all. The firing code
sets three things:

- $0356 to $90 - the flare timer;
- $03C4 to 1, the effect/sound selector;
- the message `FLARE ACTIVATED` ($3C3D), or `NO FLARES LEFT` ($3C4E) when the counter is empty.

What the timer does is change how *your* view is painted. Two routines read it. The flight-view
painter at $29F2 checks it before choosing its fill pattern, and the canvas clear at $21DF chooses
between $00 and $55 depending on whether the timer is running. In other words, the flare's visible
effect is a different dither pattern across the flight view - a bright, noisy screen that reads as
glare.

The timer is decremented once every sixteen frames (the code at $25EA only takes the decrement when
the low nibble of the frame counter is zero), so $90 is about 2,300 frames, or roughly forty-five
seconds of wall time.

> [!WARNING]
> **What I could not establish.** The manual-style description of a flare is that it decoys
> heat-seeking missiles. I did not find code that supports it: the only two readers of the flare
> timer are both drawing routines, and the missile guidance path does not consult it. Either the
> decoy effect is implemented somewhere I did not identify, or flares in this version are purely a
> defensive-looking light show. I have left it unstated rather than repeat the manual's claim.

## The three side by side

| | MIS | AMM | FLAR |
|---|---|---|---|
| Creates an object | yes, type $0A at the sight | no | no |
| Touches the object table | adds one record | rewrites records in place | never |
| Persistent | until it hits something | one instant | a 45-second view effect |
| Consumed per press | 1 of $0358 | 1 of $0357 | 1 of $0355 |

The clean way to remember the difference: the missile is a thing in the world, the AMM is a thing
you do to the world, and the flare is a thing you do to your own screen.

---

[Back to the overview](../README.md)
