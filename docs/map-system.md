# Map System

The MAP command, and the honest state of what is known about the planet data.

---

This is the shortest chapter in the guide, because the map is the subsystem I have been able to
establish least about. Rather than describe a data structure that may not exist, it records what is
verified, what follows from it, and what is still open.

## What is verified

- The 32 city names are a contiguous table at $8D02 in the `8900-CC00` file, encoded as index + $20
  and separated by $C0. See [World and Cities](world-and-cities.md).
- The current city number lives at $0354, and $280B uses it to locate a per-city object list and
  build the 48 object records at $0E00.
- Every string the game prints, including any the map would print, goes through the queue at $4127.

## What is not verified

- **A table of 32 city positions.** Earlier versions of this chapter put it at file offset $14BE4 as
  32 four-byte X/Y/Z/W records. The bytes at the equivalent place in memory are a decaying curve
  (`FE FC F4 E8 D7 C3 AC 93 ...`), which is a scaling table, not a set of coordinates. No such table
  has been found elsewhere.
- **The MAP command's rendering code.** I have not identified the routine that draws the planet
  view, so I cannot say what it reads.
- **Jump-pad pairings.** The manual says the pads are non-programmable "Super Traveller" pads at the
  N/S/E/W edges of a city; nothing in the data I have located encodes the pairing.

## Where to look next

If the city positions exist as data, the most likely places are:

1. **The per-city object list** that $280B reads. That list has to know where each building is, and
   the city's own origin is probably in its header.
2. **The `8900-CC00` file** beyond the name table. It also holds the glyph banks and the demo
   script, so it is a mixed data file rather than a clean map.
3. **The scale factor curve** mentioned above. A table of diminishing values next to the city names
   is exactly what a projection routine would want, which suggests the map maths is nearby even if
   the coordinates are not.

The pragmatic way to answer the question is to break on the routine that runs when MAP is typed, and
watch which addresses it reads. I have not done that.

---

[Back to the overview](../README.md)
