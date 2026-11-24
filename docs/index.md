# Tau Ceti: a guide to the C64 code

<p class="lede">Tau Ceti is a 1986 Commodore 64 game by Pete Cooke, converted by John Twiddy and published by CRL. This site explains how it works, address by address: the record table that holds every object, the docking aperture, the fuel clock, the jump network, the AI and the rest.</p>

It is a guide to the machine, not a walkthrough. The aim is to answer the question "why did the game do that?" with a routine and a byte, and to make the answers readable without a background in 6502 assembly.

## Start here

<div class="grid cards" markdown>

-   **[The record table](deep-dives/the-record-table.md)**

    Forty-eight records of sixteen bytes, walked twice a frame. Everything else in the game is a loop over this array.

-   **[Docking and the aperture](deep-dives/docking-and-the-aperture.md)**

    Two inequalities sharing one animated byte: the altitude window, the bearing window, and the door that opens only while you are close.

-   **[Fuel, jumping and LAUNCH](deep-dives/fuel-and-jumping.md)**

    A sixteen-bit tank drained once a second, a LAUNCH gate that reads only the high byte, and a 32-city jump graph where the side you land on chooses where you go.

</div>

## What is covered

The guide is built around the parts of the code that reward close reading:

| Area | The questions it answers |
| --- | --- |
| Records | How objects exist, move, die and share the table with missiles |
| Docking | What the aperture really tests, and why the door shuts when you shoot |
| Fuel | What the tank gates, and what it does not |
| Jumping | How a pad selects a destination and an arrival side |
| Types | What the 37 type rows say about flags, hit points and behaviour |
| AI | How static defences and mobile units decide to fire, lock and launch |
| Combat | Lasers, heat, missiles, lock-ons and damage |

The [source guide](source/index.md) holds a generated page for each routine: the real instruction stream, the variables it touches, and who calls it. The [type tables](reference/type-tables.md) reproduce the game's nine parallel tables.

## How the site is organised

- **Deep dives** are written explanations of one mechanism at a time, with diagrams generated from the game's own constants.
- **Source guide** pages are regenerated from the disassembly, so addresses, bytes and call sites are never retyped by hand.
- **Reference** pages are mechanical dumps with interpretation: type flags, class tables, zero-page variables.

## Provenance

Every address on this site was read in a disassembly of the original disk image, and the behaviour was checked against the running game where a check was possible. The C64 code is the single source of truth. Where a mechanism is also present in the Spectrum, DOS or Amiga ports, those ports are interesting comparisons — not evidence.

Where a meaning is inferred rather than proved, the text says so. The [method](about/method.md) page describes how the listings, tables and figures are produced.

## Status

The three deep dives on this site are complete. The source guide covers the frame tick, docking, the record dispatch, combat, AI and messages. Still to come: the city generator, the reactor and rods, the scanner and target list, and a full address map.

---

*Tau Ceti is © CRL Group PLC. This is an independent, non-commercial work of analysis; the Source guide shows disassembled code for study and commentary.*
