# From scanner blip to missile lock

A hunter can appear on the scanner while the missile launcher still has no target. The scanner plots nearby records. The viewport selects a record under the horizontal aiming window and publishes a separate pointer for the launcher.

## An active record carries its own bearing

The proximity pass at `$2A4D` starts by clearing bit 6 of each record's status byte. Records that pass the range tests re-acquire that bit at `$2BC8`. When the processing path reaches `$2CC0`, the bearing routine computes a nine-bit angle. The code at `$2D5F` stores it in bytes 10 and 11. Bytes 12 and 13 already carry the distance.

The same bearing is useful in two places. At `$2D69` a heading-relative test decides whether to append the record to the painter's list. The entry in that list is four bytes, holding the record pointer and its distance. Later, when the scanner walks the record table, it can use the bearing stored in the record independently of the painter's list.

## How a bearing becomes a blip

The main loop calls the scanner at `$2071`. In the ordinary display path, the scan at `$3F90` visits the same forty-eight records as the proximity pass. It requires live state in byte 0 and the active bit in byte 3.

1. At `$3FDE`, it subtracts the ship's heading and an alignment offset of `$20` from the cached bearing.
2. At `$3FF9`, it reads distance and chooses a scale using bit 7 of `$038E`. The path for the set bit spreads nearby contacts farther apart. The limit at `$4014` clips contacts whose scaled distance is `$20` or more.
3. The table lookups at `$401E` and `$403D` turn angle and scaled distance into displacements. The signs put the mark in the right quadrant. The plotting code can use type and status to vary the mark in close view.

The scanner can plot a contact to the side or behind the ship. The painter's forward window and centre tests have a different purpose.

## How the viewport picks a target

Before the proximity pass the code at `$2A37` clears the high bytes of two candidate pointers. The painter walks the list farthest first. At `$2E99` it checks whether the object's apparent width reaches the centre columns. A live candidate other than the player's own missile goes to `$0386`/`$0387`. A later candidate can replace it, so a nearer eligible object takes precedence.

The code at `$30F2` applies a tighter raster test near the sight. Its result goes to `$038A`/`$038B`. At the end of the painter's pass, `$2DD9` copies that candidate to the laser hit pointer at `$038C/$038D`. A few instructions later it copies the horizontal candidate to the missile pointer at `$0388/$0389`.

| A contact is… | Effect |
| --- | --- |
| In scanner range and off to the side | It can appear as a blip while contributing no missile candidate. |
| Crossing the viewport centre horizontally | It can become the missile candidate even when the rendered spans miss the laser sight. |
| Crossing the tighter raster window | It can become the target that receives damage when a laser bolt finishes. |

## What the launcher keeps

At `$4878`, a zero high byte in the missile pointer sends the routine to the refusal message. With a target, it searches the sixteen records in page `$10` for a free slot. Only after it finds one does it spend a missile and create a type-10 record. At `$48DF` it copies the target pointer into missile bytes 14 and 15, then sets bit 4 in the target's status byte. The pointer in the missile record gives the guided-object handler its target after the next frame's painter has chosen a new one.

For example, take a frame whose horizontal candidate is `$0E30` and whose raster candidate is `$0E40`. The painter publishes those to the missile and laser pointers, respectively. If the next missile takes the first free slot at `$1000`, the bytes at `$100E/$100F` become `$30/$0E` and `$0E33` receives the lock bit. The laser hit routine still reads `$0E40` from its own pointer for that frame.

See [Player missile launch](../source/routines/player-missile.md) for the record writes, [Guided-object handling](../source/routines/guided-objects.md) for what happens in flight, and [Why the city starts shooting](why-the-city-starts-shooting.md) for how a defence can answer the lock.

[Back to Deep Dives](index.md)
