# Tau Ceti

**A complete technical deep dive into the 1987 Commodore 64 space simulation written by John Twiddy, from an original concept by Pete Cooke.**

`Commodore 64` `6502 assembly` `VIC-II` `SID` `32-track D64` `Firebird 1987`

## About This Deep Dive

Tau Ceti is a 1987 space simulation game for the Commodore 64, written by John Twiddy with original concept by Pete Cooke. The game tasks you as commander of a mining vessel on the planet Tau Ceti (III), collecting 40 cooling rod parts from reactors across 32 cities to assemble 20 cooling bars for the main reactor in Centralis. There is no trading - only exploration, combat, and mission completion.

This analysis disassembles the D64 disk image, traces encryption layers, maps memory usage, documents the 6502 code routines, and decodes the custom character set - providing a reference as thorough as [elite.bbcelite.com](https://elite.bbcelite.com/) and [thesentinel.bbcelite.com](https://thesentinel.bbcelite.com/).

## Quick Reference

- **32 Cities** - 32 named cities on the planet surface, stored at file offset $14B0E in custom charset encoding ($C0-separated). Each city has 4-byte coordinates at $14BE4. *(No trading - only cooling rod collection)*
- **Cooling Rods** - 40 parts from reactors → 20 bars (RODS command) → insert into Centralis reactor. The goal is 20 bars, not 8 or 16. *(Mission: shut down the defence system)*
- **Custom Charset** - Custom charset initialized at runtime via lookup table at RAM $8412-$85FF. Code at offset $381C ($401D RAM). NOT standard PET ASCII. *(512 bytes of lookup data)*
- **Main Game Loop** - Raster interrupt driven. Dispatch table at file offset $1B900 (RAM $1C100). Core routines at $26A0 (state), $28C4 (render), $305D (world), $3225 (input). *(~15+ dispatch routines)*
- **Screen Mode** - VIC-II custom mode at 160x200 with extended color palette. Hardware scrolling for panning. Only the sun is rendered - planets are not shown. *($D011, $D025 registers accessed)*
- **SID Sound** - SID registers $C000-$C01F accessed for effects only. No music - only laser fire, missile launch, flare deployment, and explosion sounds. *(Minimal sound design)*

## Disk Structure Overview

The D64 image uses a non-standard 32-track layout with a zeroed DOS header. The directory entries use a custom 32-byte format where filenames start at byte offset 6. Sector chains are traced across tracks to reconstruct file contents.

| File | Location | Type | Description |
|---|---|---|---|
| TAUCETI (PRG) | T11 S2 + chain | Loader | KERNAL LOAD/CHAIN, loads to $0801, decrypts game data |
| Encoded Data Block 1 | T12 S9 | Encrypted | XOR encrypted game code + data |
| Encoded Data Block 2 | T11 S15 | Encrypted | XOR encrypted graphics + world data |
| Graphics Data | T15-T16 chains | Bitmap/Sprite | VIC-II character set, screen bitmap, sprite data |
| World Data | Scattered tracks | Binary | Planet maps, station layouts, object definitions |

## Memory Map Summary

The game uses approximately $E00-$FFFF of the C64's 64KB address space:

| Range | Region |
|---|---|
| $0800 | Loader |
| $1000 | Decoded |
| $2000-5FFF | Engine Code |
| $6000-7FFF | Engine+Draw |
| $8000-BFFF | Graphics |
| $C000-DFFF | Screen+Charset |
| $E000-FFFF | VIC-II+State |

## Key Game Strings (Decoded)

The decoded data area starting at offset $1CD46 contains hundreds of game strings. Here are the most significant:

| Offset | Decoded Meaning |
|---|---|
| $1CDE0 | "GREETINGS COMMANDER" - Title screen greeting |
| $1F2A0 | "PRESS FIRE TO PLAY" - Start prompt |
| $1D70B | "ILLEGAL SINCE IT WAS..." - Bad language filter |
| $1EB4F | "ROBOT MISSILE FIRED" - Combat message |
| $1ED06 | "MISSION FAILED" - Mission end state |
| $1F02D | "ALL SYSTEMS REPAIRED" - Repair confirmation |
| $1F9EC | "SINKER REFUELED" - Fuel transaction |
| $20D91 | "REACTOR SUCCESSFULLY CLOSED DOWN" - Mission complete |
| $1F21D | "JOHN TWIDDY" - Credits: programmer |
| $1F241 | "PETE COOKE" - Credits: original idea |

## Character Set Decoding

Tau Ceti uses a custom character set that is NOT standard C64 PET ASCII. The charset is initialized at runtime by code at game offset $381C (RAM address $401D), which calls into the decoded data area via JSR $5105.

The lookup table occupies RAM addresses $8412-$85FF (512 bytes). Each entry maps a 6-bit input character to its display equivalent. The charset supports uppercase letters A-Z, digits 0-9, punctuation and symbols, plus custom game-specific icons for reactor, missile, and fuel gauge displays.

## Easter Eggs & Hidden Features

> [!WARNING]
> **BAD LANGUAGE LOCKOUT** Entering X-rated or inappropriate terms into the game terminal triggers a lockout - you are permanently locked out of the game and must restart. The response: "ILLEGAL SINCE IT WAS PROVED TO CAUSE STERILITY AND BRAIN DAMAGE OVER [X] YEARS". Located at offset $1D70B in the decoded data area.

## Chapters

| Chapter | What it covers |
|---|---|
| [Disk Structure](docs/disk-structure.md) | D64 layout, directory format, sector chains and the encryption layers. |
| [Memory Map](docs/memory-map.md) | The full 64KB map: what lives where, and which VIC-II and SID registers the game touches. |
| [Game Code](docs/game-code.md) | Main loop, state machine and the key routines by address. |
| [Call Graph and Rendering Pipeline](docs/call-graph.md) | Call graphs for the main loop, rendering, input, combat and the raster handler. |
| [Rendering Pipeline](docs/rendering.md) | The custom VIC-II mode, the twelve-screen UI and the sprite and raster tricks. |
| [World and Cities](docs/world-and-cities.md) | The 32 cities, their coordinates, the jump pad network, reactors and cooling rods. |
| [Buildings and Interiors](docs/buildings.md) | Building types, interior graphics, energy-screened airlocks, shadows and docking. |
| [Game State](docs/game-state.md) | Zero-page variables, ship physics, combat mechanics and mission progress. |
| [Board Computer](docs/board-computer.md) | The command parser, the PAD text editor and the save/load system. |
| [Map System](docs/map-system.md) | The MAP command, city map generation and the planet map data structure. |
| [Day/Night Cycle](docs/day-night.md) | The 16-spin clock, sun position, visibility levels and light changes. |
| [Infrared Blur](docs/infrared.md) | The infrared scanner and its blur algorithm. |
| [Moveable Elements](docs/movables.md) | Missiles, robots, turrets, flares and sprite management. |
| [Sound System](docs/sound.md) | SID usage and a breakdown of every effect in the game. |
| [Character Set and Text System](docs/charset.md) | The runtime charset, its encoding scheme, the string tables and text rendering. |
| [Easter Eggs](docs/easter-eggs.md) | The swear filter, the insult response, hidden messages and the victory message. |
| [Extensions and Improvements](docs/extensions.md) | What could be added within the original hardware limits, ranked by difficulty. |
| [Tau Ceti: Expanded](docs/expanded.md) | A design sketch for a larger colony game built on the same engine. |

---

## Notes on the analysis

- Addresses are given as RAM addresses unless a line says file offset. The D64 image maps file offsets to RAM addresses with an offset of $400 in the loader region, which is why both appear in the chapters.
- Where a value is inferred rather than read directly from the code, the text says so.
- The disk image used here has a zeroed DOS header: the disk name, ID and original filenames are not preserved, so the sector layout is documented as found.
- Tau Ceti is copyright Firebird Software. This repository documents the game; it does not distribute it.
