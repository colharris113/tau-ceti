# Memory Map

The full 64KB map: what lives where, and which VIC-II and SID registers the game touches.

---

Tau Ceti uses approximately $E00-$FFFF of the C64's 64KB address space, leaving $000-$DFF unused or used only transiently by KERNAL calls. The game was clearly designed for a cartridge-style memory layout rather than a standard disk load.

## Complete Memory Map

| Range | Region |
|---|---|
| $0800 | Loader |
| $1000 | Decoded |
| $2000-5FFF | Engine Code |
| $6000-7FFF | Draw Tables |
| $8000-BFFF | Graphics |
| $C000-DFFF | Screen+Charset |
| $E000-FFFF | VIC-II+State |

![The 64KB address space, block by block](../assets/memory-map-viz-1.svg)

## Region Breakdown

### $0800-$0FFF: Loader / KERNAL Workspace

The loader PRG is loaded at $0801 (standard C64 PRG start). This region contains:

- Loader code (decryptor, KERNAL call wrappers)
- KERNAL workspace and I/O buffers
- Stack space ($0100-$01FF also used)

### $1000-$1FFF: Decoded Data Area

The XOR-decoded game data resides here, including:

| Range | Content |
|---|---|
| $1000-$19FF | Decrypted game code (JSR targets) |
| $1A00-$1FFF | Game strings, message tables, credits |

The decoded area starts at offset $1CD40 in the D64 file (RAM $1D540). Key strings found here include "GREETINGS COMMANDER" at $1CDE0 and "PRESS FIRE TO PLAY" at $1F2A0.

### $2000-$5FFF: Game Engine Code

The main game engine occupies this large region. Disassembly reveals these key routines:

| Address | Routine | Description |
|---|---|---|
| $26A0 | Main Loop | Raster interrupt handler, game state machine |
| $28C4 | Renderer | VIC-II screen update, sprite positioning |
| $2A33 | Input Handler | Joystick/keyboard input processing |
| $2B51 | World Builder | Planet/station rendering, object placement |
| $2D47/$2D52 | Drawing Tables | 3D projection math, polygon drawing |
| $2DA7 | Combat Logic | Missile firing, collision detection |
| $2EF7 | Trading System | Fuel/ore pricing, station transactions |
| $305D | Reactor Management | Cooling rods, reactor shutdown sequences |
| $3225 | Mission System | Mission state tracking, success/failure |
| $34AD | Navigation | Jump calculations |
| $3660 | Text Display | Custom charset text rendering |
| $3810/$3848 | Charset Init | Runtime character set table initialization |
| $39A2/$39EE | String Processing | Input parsing, command interpretation |
| $3B0A/$3A4B | UI Display | Status bar, HUD elements |
| $3B5E/$3B94/$3BBC | Screen Effects | Color cycling, screen panning |
| $3E17 | Sound Manager | SID register writes, music control |
| $3F29/$3F90/$3FAB | Audio Effects | Explosions, engine sounds, beeps |
| $4037/$4054 | Math Routines | Fixed-point arithmetic, trig tables |
| $40E4 | Random Number | RNG for combat and events |
| $4127/$4149 | Data Loading | World data access, planet lookups |
| $4241 | Ship State | Fuel, hull integrity, cargo tracking |
| $4348/$43EB | Object Rendering | 3D object drawing, perspective projection |
| $451F/$4547/$4560/$4584/$45AD | Polygon Drawing | Filled polygon rasterization |
| $4620/$4645 | Collision Detection | Sphere/box intersection tests |
| $4745 | Camera Control | View angle, zoom level |
| $4D73/$4DAB/$4DA4/$4DBD | Text Output | Custom charset string printing |
| $4E3D/$4E41/$4E45/$4E49/$4E4F | Input Parsing | Command parsing, number entry |
| $4F62/$4F7F | Menu System | Dialog boxes, option selection |
| $5241/$5245 | Mission Messages | Status messages, notifications |
| $5320/$5345/$5349/$5372/$5441/$5449 | Combat Messages | Firing, hit, damage reports |
| $5571/$5585 | Reactor Messages | Cooling rod status, shutdown alerts |

### $6000-$7FFF: Drawing Tables

This region contains lookup tables used by the rendering engine:

- Sine/cosine lookup tables for 3D rotation ($6xxx)
- Polygon vertex tables ($7xxx)
- Color palette tables
- Projection matrix constants

### $8000-$BFFF: Graphics Data

All game graphics are stored here:

| Range | Content |
|---|---|
| $8000-$8FFF | VIC-II character set (custom charset) |
| $9000-$9FFF | Sprite data (player ship, enemies, stations) |
| $A000-$AFFF | Planet/star bitmap tiles |
| $B000-$BFFF | Station building sprites, UI icons |

### $C000-$DFFF: Screen Buffer + Charset RAM

| Range | Content |
|---|---|
| $C000-$C7FF | Screen bitmap (160x200, 4-color) |
| $C800-$CFFF | Color RAM (background/border colors per character) |
| $D000-$D7FF | Extended screen buffer (double buffering) |
| $D800-$DFFF | Charset lookup table ($8412-$85FF in game RAM, mapped here) |

### $E000-$FFFF: VIC-II Registers + Game State

| Range | Content |
|---|---|
| $E000-$E7FF | Game state variables (ship position, fuel, cargo) |
| $E800-$EFFF | World data (planet positions, station layouts) |
| $F000-$F7FF | Mission state, scoring, game flags |
| $F800-$FFFF | SID sound registers, raster interrupt vectors |

## VIC-II Register Access

The game actively accesses these VIC-II registers:

| Register | Address | Purpose |
|---|---|---|
| $D011 | $D011 | Screen mode (custom 160x200 extended) |
| $D016 | $D016 | Raster interrupt enable ($02 bit) |
| $D018 | $D018 | Raster register (line number for interrupt) |
| $D019 | $D019 | Sprite enable registers |
| $D01A-$D01F | $D01A-$D01F | Sprite position, shape, color registers |
| $D020-$D027 | $D020-$D027 | Sprite multi-color mode |
| $D025 | $D025 | Hblank sprite expand / hardware scroll |
| $D030-$D031 | $D030-$D031 | Border/background color |

## SID Register Access

The SID ($C011-$C01F) is accessed for sound:

| Register Range | Purpose |
|---|---|
| $C011-$C013 | Voice 1: frequency, volume, waveform |
| $C014-$C016 | Voice 2: frequency, volume, waveform |
| $C017-$C019 | Voice 3: frequency, volume, waveform |
| $C01A | Filter: cutoff, resonance, filter mode |
| $C01B | Attack/decay, sustain/release (voice 1) |
| $C01C | Attack/decay, sustain/release (voice 2) |
| $C01D | Attack/decay, sustain/release (voice 3) |
| $C01E | Modulation, SID model select |
| $C01F | Voice mix, external input, output select |

## Key Game State Variables (RAM $E000+)

Disassembly reveals these state variables:

| RAM Address | Variable | Description |
|---|---|---|
| $E000 | Ship X position | Current 3D coordinates |
| $E001 | Ship Y position | Vertical position |
| $E002 | Ship Z position | Depth coordinate |
| $E003 | Fuel level | 0-255 (percentage) |
| $E004 | Hull integrity | Ship health |
| $E005 | Cargo type | Ore, fuel, supplies |
| $E006 | Cargo amount | Quantity on board |
| $E007 | Current target | Target index |
| $E008 | Current station | Station index at docked planet |
| $E009 | Game state | Menu, flying, docked, combat |
| $E00A | Mission ID | Current active mission |
| $E00B | Cooling rods | Number inserted in reactor |
| $E00C | Reactor temperature | Heat level (danger threshold) |
| $E00D | Missile count | Remaining missiles |
| $E00E | Score | Game score total |
| $E00F | Efficiency | Mission efficiency rating |

---

[Back to the overview](../README.md)
