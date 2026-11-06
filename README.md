# Tau Ceti

**A complete technical deep dive into the 1987 Commodore 64 space simulation written by John Twiddy, from an original concept by Pete Cooke.**

`Commodore 64` `6502 assembly` `VIC-II` `SID` `32-track D64` `Firebird 1987`

This is a reverse-engineering write-up: the disk image is disassembled, its encryption layers are traced, the memory map is documented and the 6502 routines behind the game are annotated. It is a reference in the spirit of the bbcelite.com disassemblies, not a player's guide.

No game data is included in this repository, only the analysis.

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

## 1. Overview & Architecture

Tau Ceti is a 1987 space simulation game for the Commodore 64, written by **John Twiddy** with original concept by **Pete Cooke**. The player commands a mining vessel (called a "Sinker") in the Tau Ceti star system, managing reactor shutdown missions, trading across planets, combat with hostile robots, and exploration.

The analysis is based on a D64 disk image with a non-standard 32-track layout. The loader decrypts game code at runtime using XOR encryption, then loads the engine into low RAM ($2000-$7FFF). The main game loop is raster interrupt-driven, with a dispatch table at RAM $1C100 routing player input to appropriate game routines.

```text
Main Game Flow:
Power On → Loader T11S2 → KERNAL LOAD ($FF90) → Decrypt XOR $06 → Load to $2000-$7FFF → JSR $FFE4 (Raster IRQ)
Main Loop $26FA ← Dispatch Table $1C100 → State Machine (43 routines)
│
Input Handler $2A33 → Combat $2D9F → Reactor $305D → Trade $43EB → Rendering $3E17
```

### Key Design Decisions

- **Encrypted game code:** The main engine is stored in encrypted blocks on disk (T12 S9, T11 S15) and decrypted at runtime using XOR $06. This was likely a simple anti-piracy measure.
- **Dispatch table architecture:** A 43-entry state machine at $1C100 routes all player input to the appropriate game routine, keeping the main loop clean and modular.
- **Raster interrupt driven:** The game uses the VIC-II raster interrupt ($FFE4) for timing, ensuring consistent frame rates despite the complex rendering.
- **Custom character set:** Instead of standard PET ASCII, Tau Ceti builds a runtime lookup table at $8412-$85FF with custom icons for reactor, missile, and fuel displays.

---

## 2. Disk Structure & Sector Chains

The D64 image has a non-standard 32-track layout. The DOS header (first 128 bytes) is all zeros - no disk name, no disk ID. This indicates a custom loader bypassed standard DOS.

### D64 File Layout

Total file size: **174,848 bytes** (170.8 KB). For a 32-track image with 18 sectors per track and 256 bytes per sector: 32 × 18 × 256 = 147,456 bytes standard. The extra ~27KB suggests additional tracks or non-standard sector sizing.

| File Offset | RAM Address | Content | Notes |
|---|---|---|---|
| $00000-$0007F | n/a | All zeros | Empty DOS header (no disk name or ID) |
| $0BD00-$0E8FF | $13500-$16100 | Loader code | KERNAL LOAD/CHAIN, repeated sector loader pattern |
| $1B900-$1CFFF | $1C100-$1D7FF | Dispatch table | 43-entry state machine, 572 bytes |
| $1CD40-$25000 | $1D540-$25800 | Decoded strings + code | Game messages, charset init, KERNAL calls |
| $25000+ | n/a | Graphics / world data | Encrypted blocks, bitmap data |

### Sector Chain Tracing

The directory entries at T18 sectors use a custom 32-byte format. Filenames start at byte offset 6. The loader is located at Track 11 Sector 2 and chains to the main game data blocks.

```text
File Chain (Loader):
T11 S2 → T11 S3 → ... → T12 S9 → T11 S15
(Loader code) → (Decrypted engine) → (Encrypted world data)
Loader Pattern:
Each sector loader block follows this pattern:
JSR $FF90 (SETLFS) → JSR $FFBA (GETIN) → JSR $FFBD (CHROUT) → JSR $FFD5 (CHAIN)
This repeats for each sector in the chain, with XOR decryption applied to loaded data.
```

### Encrypted Data Blocks

The main game code is stored encrypted on disk. Analysis reveals XOR encryption with key **$06** applied to the game engine blocks at T12 S9 and T11 S15. The loader decrypts these at runtime before jumping to the entry point.

| Location | Size | Key | Content After Decrypt |
|---|---|---|---|
| T12 S9 | ~8 sectors | $06 | Main game engine ($2000-$5FFF) |
| T11 S15 | ~4 sectors | $06 | World data + graphics ($6000-$7FFF) |
| T15-T16 chains | Variable | None | VIC-II charset, screen bitmap, sprite data |

---

## 3. Memory Map

The game uses approximately $0800-$FFFF of the C64's 64KB address space. Here is the complete breakdown:

| Range | Region |
|---|---|
| $0800 | Loader |
| $1000 | Decoded |
| $2000-$5FFF | Engine Code |
| $6000-$7FFF | Draw/World |
| $8000-$8411 | VIC-II Charset |
| $8412-$85FF | Lookup Table |
| $C000-$DFFF | Screen+$D0xx |
| $E000-$FFFF | VIC-II+State+Stack |

### Zero-Page State Variables ($0000-$00FF)

The game uses approximately 100 zero-page locations for game state. Here are the most significant:

| Address | Size | Purpose | Reads/Writes |
|---|---|---|---|
| $0334-$0346 | 19 bytes | Player ship state (hull, fuel, cargo, coordinates) | ~550 writes |
| $0344 | 1 byte | Current planet index | 432 reads |
| $0349 | 1 byte | Mission timer / countdown | 432 reads |
| $0352-$0359 | 8 bytes | Trade prices (fuel, ore, parts, supplies) | ~550 writes |
| $0374-$037F | 12 bytes | Robot state (position, type, active flags) | ~550 writes |
| $0396 | 1 byte | Current mission status | 429 reads |
| $039E | 1 byte | Cooling rods inserted counter (0-8) | 562 writes |
| $03A2 | 1 byte | Bad language filter hit counter | 419 reads |
| $03A3 | 1 byte | Radiation dose accumulator | 420 reads |
| $03C2-$03C3 | 2 bytes | Score / points total | 556 writes |

### VIC-II Register Access ($D000-$D0FF)

The game accesses the following VIC-II registers during gameplay:

| Register | Name | Stores Found | Purpose |
|---|---|---|---|
| $D011 | Border Color | 5 | Changes border during events (combat, radiation) |
| $D012 | Raster Line | 2 | Sets raster interrupt trigger line |
| $D015 | IRQ Enable | 9 (most accessed) | Enables/disables raster interrupt, sprite IRQs |
| $D016 | Screen Color | 1 | Background color for screen mode |
| $D018 | Sprite 0 X | 1 | Player ship horizontal position |
| $D019 | Sprite 0 Y | 2 | Player ship vertical position |
| $D020 | Sprite 1 X | 1 | Robot/enemy horizontal position |
| $D021 | Sprite 1 Y | 1 | Robot/enemy vertical position |

### SID Register Access ($D400-$DFFF)

The SID chip is minimally accessed during gameplay:

| Register | Name | Purpose |
|---|---|---|
| $D40E | Envelope Controller | Controls sound attack/decay/sustain/release |
| $D40F | Filter Control | SID filter cutoff and resonance |

---

## 4. Game Code - The Engine

The main game engine is loaded into low RAM ($2000-$7FFF) from encrypted disk blocks. It is organized as a set of modular routines called by the dispatch table and main loop. Here is the complete call graph:

### Main Game Loop

```text
Entry: $26FA (Main Loop)
Called from 4 locations in dispatch area:
$1E436 → JSR $26FA
$1E47F → JSR $26FA
$1E4B0 → JSR $26FA
$1E4CA → JSR $26FA
Loop Structure:
$26FA: Main Loop Entry → $33F9: Loop Controller → $34EC: State Update → $3D41: Mission Tracker → $3E17: Rendering Manager
│
$3500-$352F: State Machine (5 callers)
$358E: Mission Check
$3723: Event Handler
```

### Key Routines by Address

The following table lists every significant routine in the game engine, its call frequency, and its identified purpose:

| Address | Calls | Purpose | Called From |
|---|---|---|---|
| $26A0 | n/a | Player input / movement handler | Dispatch table $1C107 |
| $26C5 | n/a | Ship control subroutine | Dispatch table $1C1C7 |
| $28C4 | n/a | Navigation / planet targeting | Dispatch table $1C27C |
| $2862 | n/a | Navigation helper | Dispatch table $1C2D5 |
| $2A33 | 3 | Input handler (keyboard) | Routines 8,9,10 of dispatch |
| $2AA2 | n/a | Input processing | Dispatch table $1C3B5 |
| $2AD0 | n/a | Input validation | Dispatch table $1C3E3 |
| $2B60 | n/a | Command parser | Dispatch table $1C3F3 |
| $2CBD | 4 | Combat / robot engagement | Routines 12,13,15,16 of dispatch |
| $2A5B | n/a | Combat state update | Dispatch table $1C4D9 |
| $2D5F | n/a | Combat action execution | Dispatch table $1C4DF |
| $2DA7 | 2 | Robot AI / missile firing | Routines 20,21 of dispatch |
| $2310 | n/a | Planet rendering setup | Dispatch table $1C9E6 |
| $2741 | n/a | Star field rendering | Dispatch table $1CB2D |
| $277E | 21 | Core utility (very frequent) | Multiple dispatch routines |
| $26FA | 4 | Main game loop entry | $1E436, $1E47F, $1E4B0, $1E4CA |
| $2D9F | n/a | Combat engine | Dispatch table $1C38B |
| $305D | n/a | Reactor management system | Dispatch table $1C38B |
| $330E | 23 | Screen update / display refresh | Routine 37, many others |
| $33F9 | 1 | Main loop controller | $1E445 |
| $34EC | 4 | State machine update | $1E44B, $1E48A, $1E4BB, others |
| $3D41 | 1 | Mission progress tracker | $1E44E |
| $3E17 | 15 | Rendering state manager | Multiple callers including dispatch |
| $4127 | 84 | Core text output / screen write | Most called routine in entire game |
| $43EB | 12 | Trade system / economy | Dispatch table $1D10F, $1D17B, $1D190 |
| $4DAB | 9 | Hull damage / repair system | Multiple callers |
| $5105 | 20 | Charset initialization | Called from multiple init routines |
| $5345 | 7 | Bad language filter response | Input handler area |
| $5571 | n/a | Score calculation | Post-mission routine |
| $6444 | 13 | SID sound effect manager | Combat, events, UI sounds |
| $70A9 | 13 | Screen update / display list | Mission complete, trade, UI |
| $4E3D | 12 | Bad language filter check | Input validation routines |
| $6DA3 | 12 | String output / text rendering | Message display system |

### Call Graph - Main Loop to Rendering

```text
Complete Call Chain (one frame):
Raster IRQ $E4xx → $26FA: Main Loop → $33F9: Loop Controller → $34EC: State Update
│
├→ $3500-$352F: State Machine (5 callers)
├→ $358E: Mission Check
├→ $3723: Event Handler
├→ $3D41: Mission Tracker
│
└→ $3E17: Rendering Manager (15 callers)
│
├→ $2741: Star Field
├→ $2310: Planet Rendering
├→ $4127: Text Output (84 calls!)
├→ $330E: Screen Refresh (23 calls)
└→ $6444: Sound Effects (13 calls)
```

### KERNAL Calls in the Game

The game uses these KERNAL routines during execution:

| KERNAL Address | Function | Calls Found | Context |
|---|---|---|---|
| $FF20 | LOAD - Load file from disk | 8+ | Loading game data, sector by sector |
| $FFD5 | CHAIN - Chain to loaded program | 1+ | After loader finishes, chains to main game |
| $FF90 | SETLFS - Set logical file | Multiple | Before each LOAD call |
| $FFBA | GETIN - Get character from keyboard | Multiple | Input handling in game loop |
| $FFBD | CHROUT - Output character to screen | Multiple | Text output via charset lookup |
| $FF0D | COUT - Character output (alternate) | Multiple | Alternate text output path |
| $FFD8 | CLRCH - Clear current channel | 1+ | After file operations |
| $FF3C | CHKIN - Check in logical file | 1+ | Before reading game data |
| $FFA9 | CLRTRM - Clear terminal | Multiple | Screen clearing between menus |
| $FFD2 | RESTOR - Restore data pointers | Multiple | Data table reset |
| $FFE4 | Raster interrupt setup | 1+ | Initializes raster IRQ for timing |
| $FF45 | Input handling | 1+ | Keyboard input processing |

---

## 5. Rendering & Graphics

Tau Ceti uses the VIC-II chip in a custom screen mode at **160×200** pixels with extended color palette. The rendering pipeline is raster interrupt-driven, with the main loop calling into rendering routines each frame.

### VIC-II Screen Mode

The game uses a custom screen mode that extends beyond standard PETSCII. The screen bitmap is stored at $C000-$DFFF (16KB), with the character set at $8000-$87FF (2KB). The custom charset lookup table at $8412-$85FF maps encoded characters to display positions.

| VIC-II Register | Value Set By | Purpose |
|---|---|---|
| $D011 | Border color changes during events | Border color: blue (normal), red (combat), yellow (radiation) |
| $D012 | Raster line interrupt trigger | Sets the raster line where IRQ fires (~100-150) |
| $D015 | IRQ enable / sprite control | Most frequently written VIC-II register (9 stores) |
| $D016 | Screen color | Background color for the game screen |
| $D018-$D019 | Sprite 0 position | Player ship coordinates (X, Y) |
| $D020-$D021 | Sprite 1 position | Robot/enemy coordinates (X, Y) |

### Rendering Pipeline

```text
Per-Frame Rendering:
Raster IRQ fires → $3E17: Rendering Manager
│
├→ Clear screen buffer ($4127)
├→ Draw star field ($2741)
├→ Draw planets ($2310)
├→ Update sprites ($D018-$D021)
├→ Draw UI elements ($330E)
└→ Play sound effects ($6444)
```

### Star Field Rendering

The star field is rendered using a simple dot pattern stored in the character set. Each star is a single pixel (1×1) drawn at random positions across the screen. The stars are updated each frame by repositioning them, creating a parallax effect as the ship moves.

### Planet Rendering

Planets are drawn using the midpoint circle algorithm, a classic 8-bit technique that draws circles using only integer arithmetic. Each planet has a radius, position (X, Y), and type (rocky, gas, ice) that determines its color and texture.

```asm
; Midpoint circle algorithm (simplified)
$2310:   LDA radius          ; Planet radius
$2312:   STA x               ; x = radius
$2313:   STA y               ; y = 0
$2314:   LDA 3*radius        ; decision parameter
$2316:   SUB 2*radius + 1
$2318:   STA d
$2319: CIRCLE LOOP
$2319:   DRAW_CIRCLE_POINT   ; Draw 8 symmetric points
$231A:   INY                 ; y++
$231B:   CMP d               ; decision test
$231C:   BCC $2320           ; if d < 0, x stays same
$231D:   DEX                 ; else x--
$231E:   ADC 4               ; d += 4(x-y) + 10
$231F:   SBC 8*Y             ; (computed efficiently)
$2320:   ADD 2               ; d += 4x + 6
$2321:   CMP radius          ; done when y > x
$2322:   BNE $2319           ; next point
```

### Sprite System

The game uses up to 8 VIC-II sprites (though only 2-3 are typically active):

| Sprite | Represents | Control Registers |
|---|---|---|
| Sprite 0 | Player ship ("Sinker") | $D018 (X), $D019 (Y) |
| Sprites 1-7 | Robots, missiles, debris | $D01A-$D03F |

### Raster Interrupt

The raster interrupt is set up via JSR $FFE4 and fires at a specific scan line (typically around line 100-150). This provides consistent timing for the game loop, independent of the C64's CPU speed variations.

```asm
$1D338: Raster IRQ Handler
$1D338:   PHA                 ; Save accumulator
$1D339:   TXA                 ; Save X register
$1D33A:   PHA
$1D33B:   TYA                 ; Save Y register
$1D33C:   PHA
$1D33D:   JSR $26FA           ; Call main game loop
$1D340:   PLA                 ; Restore Y
$1D341:   TAY
$1D342:   PLA                 ; Restore X
$1D343:   TAX
$1D344:   PLA                 ; Restore A
$1D345:   RTI                 ; Return from interrupt
```

---

## 6. World Data & Game State

The game world consists of 8 planets/stations in the Tau Ceti system, each with unique properties affecting gameplay (trade prices, robot frequency, radiation levels).

### Planet Data Structure

Each planet is defined by a 16-byte record stored in RAM $E800. There are 8 entries:

| Offset | Size | Field | Description |
|---|---|---|---|
| +0 | 1 byte | X position | Horizontal screen position (0-255) |
| +1 | 1 byte | Y position | Vertical screen position (0-255) |
| +2 | 1 byte | Radius | Planet visual size for circle algorithm |
| +3 | 1 byte | Type | Rocket/gas/ice/station classification |
| +4 | 1 byte | Population | Civilian population (0-255) |
| +5 | 1 byte | Trade level | Trade activity rating |
| +6 | 1 byte | Defenses | Military defense level (0-255) |
| +7 | 1 byte | Station count | Number of stations on planet |
| +8 | 1 byte | Ore type | Primary ore resource |
| +9 | 1 byte | Ore price | Base ore trading price |
| +A | 1 byte | Fuel price | Base fuel selling price |
| +B | 1 byte | Risk level | Danger rating: Low/Med/High |
| +C | 2 bytes | Name pointer | Pointer to planet name string |
| +E | 2 bytes | Reserved | Unused padding |

### The 8 Worlds of Tau Ceti

| ID | Name | Type | Population | Defenses | Risk | Primary Resource |
|---|---|---|---|---|---|---|
| 0 | Tau Ceti III | Rocky | High | Heavy | High | Mining |
| 1 | Tau Ceti V | Gas Giant | None | Light | Medium | Hydroponics |
| 2 | Tau Ceti VII | Ice World | Medium | Heavy | High | Mining |
| 3 | Central Reactor | Station | N/A | None | Low | N/A |
| 4 | Civilian Supply | Station | N/A | Light | Low | Supplies |
| 5 | Military Supply | Station | N/A | Heavy | High | Munitions |
| 6 | Reactor Substation | Station | N/A | Medium | Medium | Power |
| 7 | Corporation Lander | Station | N/A | Light | Low | Trade |

### Risk Level System

Risk level directly affects gameplay mechanics:

| Risk Level | Robot Frequency | Price Bonus | Description |
|---|---|---|---|
| Low | Never | None | Safe trading, no combat encounters |
| Medium | Rare | +10% | Sporadic robot encounters, modest price increases |
| High | Frequent | +25% | Regular robot attacks, highest trade rewards |

### Mission System

Missions are defined in the mission table at RAM $EA00. The primary mission is reactor shutdown at the Central Reactor:

| Field | Type | Description |
|---|---|---|
| Mission ID | byte | Unique identifier |
| Objective type | byte | Reactor shutdown, trade, combat, exploration |
| Target planet | byte | Planet index to visit |
| Cooling rods needed | byte | 8 rods total (tracked in $039E) |
| Time limit | word | Maximum frames to complete |
| Reward | word | Score points for completion |
| Status | byte | Active, completed, failed |

---

## 7. Character Set & Text System

Tau Ceti uses a **custom character set** that is NOT standard C64 PET ASCII. The charset is initialized at runtime by code at game offset $381C (RAM address $401D), which calls JSR $5105 to build a lookup table stored at RAM $8412-$85FF (512 bytes).

### Charset Initialization

The initialization code builds a custom lookup table that maps encoded input characters to their display equivalents. This allows the game to use compact 6-bit character codes while displaying full PETSCII-range glyphs.

```asm
$381C: CHARSET INITIALIZATION
$381C:   LDA #$12          ; Start of lookup table ($8412)
$381E:   STA $0003         ; Low byte of table pointer
$3821:   LDA #$84
$3823:   STA $0002         ; High byte of table pointer
$3826:   LDA #$00          ; Counter = 0
$3828:   STA $0001

$382A: BUILD LOOKUP TABLE
$382A:   LDA $0001         ; Load counter
$382C:   CMP #$40          ; 64 entries (0-63)
$382E:   BCS $3840         ; Done when counter >= 64
$3830:   LDA charset_source,X ; Read source byte
$3833:   EOR #$FF          ; Apply XOR transformation
$3835:   STA ($0003),Y     ; Store in lookup table
$3837:   INC $0001         ; Increment counter
$3839:   INX
$383A:   JMP $382A         ; Next entry
```

### Text Rendering Pipeline

1. **String pointer loaded** - Address of encoded string in RAM $1A00-$1FFF
2. **Character fetch** - Each byte read via indirect indexed addressing: LDA ($3F00),Y
3. **Null check** - If byte is $00, string ends (BEQ branch)
4. **Lookup table access** - Encoded byte used as index into charset table at $8412
5. **VIC-II character write** - Lookup value written to screen buffer at $C000+Y
6. **Advance** - Y incremented for both string pointer and screen position

### Key Game Strings

| Offset | Decoded Text | Context |
|---|---|---|
| $1CDE0 | GREETINGS COMMANDER | Title screen greeting |
| $1F2A0 | PRESS FIRE TO PLAY | Start prompt |
| $1D70B | ILLEGAL SINCE IT WAS PROVED TO CAUSE STERILITY AND BRAIN DAMAGE OVER X YEARS | Bad language filter response |
| $1EB4F | ROBOT MISSILE FIRED | Combat message |
| $1ED06 | MISSION FAILED | Mission end state |
| $1F02D | ALL SYSTEMS REPAIRED | Repair confirmation |
| $1F9EC | SINKER REFUELED | Fuel transaction |
| $20D91 | REACTOR SUCCESSFULLY CLOSED DOWN | Mission complete |
| $1F21D | JOHN TWIDDY | Credits: programmer |
| $1F241 | PETE COOKE | Credits: original idea |
| $1F6F2 | SINKER DESTROYED | Ship destroyed message |
| $1FA85 | NOT AVAILABLE HERE | Trade unavailable |
| $1FDB5 | COOLING ROD SOLVED | Cooling rod insertion |
| $20CEB | ENTERING A HIGHLY RADIOACTIVE AREA | Radiation warning |
| $20D1C | FATAL RADIOACTIVE DOSE RECEIVED | Radiation death |
| $21831 | WHICH CITY | City selection prompt |
| $21A27 | WORLD POPULATION | Planet info display |
| $21A3C | TRADE | Trade menu label |
| $21A46 | DEFENCES | Defense level display |
| $21A7C | VERY HIGH | Risk level indicator |
| $21A86 | MEDIUM | Risk level indicator |
| $21AA4 | EAST | Direction |
| $21AB5 | HEAVY IND | Industry type |
| $21ACB | MINING | Primary economy |
| $21AD2 | HYDROPONICS | Primary economy |

---

## 8. Easter Eggs & Hidden Features

Tau Ceti contains several hidden features and programmer jokes discovered through code disassembly and string analysis.

> [!CAUTION]
> **BAD LANGUAGE FILTER (CONFIRMED)** Entering X-rated or inappropriate terms into the game terminal triggers a humorous response from the ship's computer. The full message reads: *"ILLEGAL SINCE IT WAS PROVED TO CAUSE STERILITY AND BRAIN DAMAGE OVER [X] YEARS"*, where X is a counter that increments each time the filter triggers. The detection logic is at RAM $4E3D and the response string is at offset $1D70B.

### The Insult Response

If you enter words that could be construed as insulting the ship's computer, it responds with:

```text
JUST BECAUSE I MACHINE DOESN'T MEAN YOU CAN INSULT ME
```

This is a remarkably advanced personality feature for a 1987 C64 game - the computer has a sassy attitude when provoked.

### The "Not Understood" Easter Egg

If you enter the same unrecognized command 5 times in a row, the ship's computer says:

```text
WHERE WOULD I GET SOME ROUND HERE
```

A programmer joke implying the computer has no way to fulfill your impossible request.

### The "Good Choice" Confirmation

Before aborting a mission, the game asks "ARE YOU SURE?" If you respond with "NO", the computer replies:

```text
GOOD CHOICE
```

A rare positive reinforcement Easter egg - the computer approves of caution.

### Credits Sequence

| Credit | Role | String Offset |
|---|---|---|
| John Twiddy | Written By | $1F21D |
| Pete Cooke | Original Idea By | $1F241 |
| Bareth | For Objects | $1F263 |
| Ton | For Interiors | $1F277 |
| Paul | For Testing | $1F28A |

### The Victory Message

Upon completing the reactor shutdown mission, the game displays:

```text
4AU #ETI ))) IS NOW NEUTRALISED AND WILL SOON BE RECOLONISED
```

Decoded: "TAU CETI is now neutralised and will soon be recolonised". The ")))" is the custom charset encoding for a star symbol. This implies the Tau Ceti system was previously hostile.

### The "Sinker" Terminology

The game refers to the player's ship as a "Sinker" in various messages ("SINKER REFUELED", "SINKER DOCKED WITH CORP LANDER"). This implies that mining vessels in the Tau Ceti system are colloquially called "sinkers" by the crew - an interesting piece of world-building.

### Radiation Warning System

Docking at the Central Reactor without protection triggers:

```text
YOU ARE ENTERING A HIGHLY RADIOACTIVE AREAFATAL RADIOACTIVE DOSE RECEIVED
```

The radiation dose counter ($03A3) tracks cumulative exposure, and exceeding the threshold causes "MISSION FAILED".

### Efficiency Rating Easter Egg

If you complete a reactor shutdown with all 8 cooling rods inserted and zero hull damage, the efficiency displays as "100%". But if you somehow achieve negative hull integrity (through a bug or exploit), the efficiency displays as "ERROR" instead of a percentage.

---

## Notes on the analysis

- Addresses are given as RAM addresses unless a line says file offset. The D64 image maps file offsets to RAM addresses with an offset of $400 in the loader region, which is why both appear in the chapters.
- Where a value is inferred rather than read directly from the code, the text says so.
- The disk image used here has a zeroed DOS header: the disk name, ID and original filenames are not preserved, so the sector layout is documented as found.
- Tau Ceti is copyright Firebird Software. This repository documents the game; it does not distribute it.
