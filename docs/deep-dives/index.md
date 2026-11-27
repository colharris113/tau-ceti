# Deep dives

Follow Tau Ceti's C64 code from one pass through the flight loop to a complete trip through the reactor room. Start with the frame if you want to see how the routines fit together, or pick a question from the sections below.

## The flight loop and its data

- [One frame in the skimmer](one-frame-in-the-skimmer.md) follows the foreground loop and the raster handlers from scene setup to the next mode.
- [The record table](the-record-table.md) explains how forty-eight records hold buildings, robots, missiles and dying objects.
- [The 32 cities](the-32-cities.md) shows how three-byte entries, shared pad templates and write-back rules give each city its layout and memory.

## The mission

- [How the cooling rods work](the-cooling-rods.md) follows two halves from the shuffled pile to a filled socket at Centralis.
- [Docking and the aperture](docking-and-the-aperture.md) shows how the opening in a building sets the permitted height and bearing.
- [Fuel, jumping and LAUNCH](fuel-and-jumping.md) explains what the fuel gauge controls and how the game selects a destination and arrival pad.

## The cockpit and combat

- [The viewport in flight](the-viewport-in-flight.md) traces a structure from its radius profile to a finished bitmap.
- [From scanner blip to missile lock](from-scanner-blip-to-missile-lock.md) follows the bearings, target pointers and missile record.
- [Why the city starts shooting](why-the-city-starts-shooting.md) compares fixed defences and mobile hunters.
- [How Tau Ceti drives the SID](how-tau-ceti-drives-the-sid.md) follows engine noise and a laser effect from game state to the sound chip.

[Back to the guide](../index.md)
