# Tau Ceti

**A technical deep dive into the 1987 Commodore 64 space simulation written by John Twiddy, from an original concept by Pete Cooke.**

`Commodore 64` `6502 assembly` `VIC-II` `SID` `D64` `Firebird 1987`

## About This Deep Dive

Tau Ceti is a 1987 space simulation for the Commodore 64, written by John Twiddy with the original
concept by Pete Cooke. You command a skimmer on the planet Tau Ceti (III), collecting cooling rod
parts from reactors across 32 cities and assembling them into bars for the main reactor at Centralis.

This analysis works from the disk image itself: the files are reconstructed sector by sector, the
code is disassembled, and the results are checked against memory dumps taken from VICE while the game
runs. Where something could not be established, this guide says so rather than filling the gap - a
habit it did not always have, and the notes at the bottom of the chapters record what changed.

## Quick Reference

- **32 Cities** - named in one table at **$8D02**, encoded as letter index + $20 and separated by
  $C0, so `$23 $25 $2E $34 $32 $21 $2C $29 $33` reads CENTRALIS. The run ends with $FF after RUBIYA.
- **The disk** - an ordinary 35-track D64, 174,848 bytes, eight files, no encryption and no packing.
  What looked like encryption was a wrong sector formula.
- **The screen** - one 320x200 multicolour bitmap at $E000, video matrix at $CC00, colour RAM at
  $D800, VIC bank 3. Four raster stages switch the mode partway down the screen so the text bands
  are sharp and the view is soft.
- **The frame** - the routine at $4D80 runs once per frame; the raster interrupt at $3903 runs four
  times and owns input, the playfield blit and the clocks. The interrupt vector is $FFFE, not $0314.
- **The world** - 48 object records of 16 bytes at $0E00, rebuilt for each city by $280B. Buildings,
  robots and missiles are all entries in that table; there are no sprites anywhere in the game.
- **The demo** - a real attract mode, flown by a recorded joystick script, showing `DEMO` in the
  status line. See [The Demo](docs/demo-mode.md).
- **Sound** - two SID voices at $D400-$D418, effects only, no music.

## Disk Structure Overview

| File | Location | Blocks | Loads at | Role |
|---|---|---|---|---|
| `TAU CETI` | 17/0 | 1 | $0302 | boot stub |
| `JEFF` | 11/4 | 2 | $0C00 | loader |
| `PIC B TAUCETI+` | 13/0 | 40 | $4000 | title picture |
| `0E00-2000` | 17/1 | 19 | $0E00 | object records and tables |
| `8900-CC00` | 17/20 | 68 | $8900 | glyphs, names, demo script |
| `I/O 4K` | 19/0 | 17 | $D000 | replacement I/O |
| `CC00-D000` | 19/9 | 5 | $CC00 | screen tables |
| `E000-FFFF` | 20/0 | 33 | $E000 | main bitmap |
| `2000-8900` | 21/6 | 106 | $2000 | the game |

The filenames are load ranges, not descriptions. [Disk Structure](docs/disk-structure.md) has the
sector formula and the chain layout.

## Memory Map Summary

| Range | Contents |
|---|---|
| $0000-$03FF | zero page, stack, and the game's variables in page 3 |
| $0400-$0BFF | flight-view canvas and blitters' source |
| $0C00-$0CFF | loader, later the message queues |
| $0E00-$10FF | 48 object records |
| $2000-$88FF | game code |
| $8900-$92FF | city data and glyph banks |
| $9300 / $BD00 | demo script tables |
| $CC00-$CFFF | video matrix |
| $D000-$DFFF | replacement I/O routines |
| $E000-$FF3F | bitmap |
| $FFFE | IRQ vector, holding $3903 |

## Messages

| Address | Text |
|---|---|
| $4931 | `DEMO` / `LAUNCHED` / `LANDED` / `DOCKED` |
| $3C3D | `FLARE ACTIVATED` |
| $3C5E | `NO MISSILES LEFT` |
| $3C95 | `AMM DETONATED` |
| $5E6A | `SKIMMER REFUELED` |
| $6503 | `PRESS 3 TO TRY ANOTHER MISSION` |
| $6528 | `DEMO MODE INITIATED` |

## Chapters

| Chapter | What it covers |
|---|---|
| [Disk Structure](docs/disk-structure.md) | The sector formula, the directory, and the chain layout. |
| [Memory Map](docs/memory-map.md) | The 64KB map, the variables in page 3, and the VIC-II and SID registers used. |
| [The Loading Screen](docs/loading-screen.md) | Boot stub, JEFF, the seven files, the picture at $4000 and the SPACE prompt. |
| [Game Code](docs/game-code.md) | Entry, the frame routine, the four-stage raster interrupt and the message system. |
| [The Demo](docs/demo-mode.md) | The attract mode: trigger, the recorded joystick script, and how it ends. |
| [Flares, Missiles and AMM](docs/weapons.md) | The three counters in the supply box and the three different mechanisms behind them. |
| [Call Graph](docs/call-graph.md) | How the frame routine, the raster stages and the message path call each other. |
| [Rendering Pipeline](docs/rendering.md) | The bitmap, the four raster bands, the canvas and the blitters. |
| [World and Cities](docs/world-and-cities.md) | The 32 cities, the name table, jump pads, reactors and cooling rods. |
| [Buildings and Interiors](docs/buildings.md) | Building types, interiors, airlocks, shadows and docking. |
| [Game State](docs/game-state.md) | Where the flight variables live and what the flight model does with them. |
| [Board Computer](docs/board-computer.md) | The text console, the message queue and the equipment panel. |
| [Map System](docs/map-system.md) | The MAP command and what is, and is not, known about the planet data. |
| [Day/Night Cycle](docs/day-night.md) | The 16-spin clock, sun position and visibility. |
| [Infrared Blur](docs/infrared.md) | The infrared scanner and its blur. |
| [Moveable Elements](docs/movables.md) | The object table, the painter and the blitters - and why there are no sprites. |
| [Sound System](docs/sound.md) | SID usage and the effects. |
| [Character Set and Text System](docs/charset.md) | The glyph encoding, the blitter at $3E17 and the message interpreter. |
| [Easter Eggs](docs/easter-eggs.md) | Hidden messages, and which rumours the code supports. |
| [Extensions and Improvements](docs/extensions.md) | What could be added within the original hardware limits. |
| [Tau Ceti: Expanded](docs/expanded.md) | A design sketch for a larger colony game on the same engine. |

---

## Notes on the analysis

- Addresses are RAM addresses unless a line says otherwise. On-disk positions are given as
  track/sector, and file offsets only where the file itself is the subject.
- Where a value is inferred rather than read directly, the text says so; where something could not
  be established at all, the text says that too. Several chapters carry a note listing what an
  earlier version of the guide claimed and what is actually there.
- The image was rebuilt with the piecewise sector formula and the sector chains, and the result was
  checked against VICE: the bytes at $2000-$88FF are identical to a memory dump taken at the point
  the loader jumps into the game.
- Each chapter carries the same rule: a claim without an address, a dump or a trace behind it is
  either labelled as coming from the manual or left out.
- Tau Ceti is copyright Firebird Software. This repository documents the game; it does not distribute
  it.
