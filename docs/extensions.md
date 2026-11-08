# Extensions and Improvements

What could be added within the original hardware limits, ranked by difficulty.

---

A technical analysis of what could be added or changed, based on the actual code structure, available RAM, and C64 hardware capabilities.

## The Constraints

| Resource | Status | Available |
|---|---|---|
| Screen RAM | In use (Mode 4 TED) | $0400-$07FF + $1800-$1BFF |
| Color RAM | In use | $DC00-$DFFF (partial) |
| VIC-II Sprites | Sprites 0-5 used | Sprites 6-13 free |
| SID Channels | All three in use (two effects, one engine) | Nothing free at the voice level |
| Disk I/O | KERNAL LOAD/CHAIN used | All KERNAL calls available |
| Free RAM blocks | Scattered | Largest: 3,745 bytes at $1695F |

## Category 1: Visual Improvements (Easy)

### 1.1 Additional Sprite Lights (Easy)

**What:** The game uses sprites 0-5 for building rendering and lighting. Sprites 6-13 are completely unused throughout the entire codebase.

**How:** Write to $D015 (sprite X) and $D014 (sprite Y) for sprites 6-13, then enable them via $D011. Each sprite is only 24x21 pixels in Mode 4, so they work best as small indicators.

**Idea:** Add orbiting debris or satellite indicators around the sun. Each sprite could represent a different celestial body or space station, positioned at calculated angles using the existing trigonometry tables.

### 1.2 Expanded Color Palette (Easy)

**What:** The game currently uses a limited set of color RAM values ($7F and $FF for buildings). Mode 4 supports 16 colors per row with hardware color RAM.

**How:** The color RAM is at $DC00-$DFFF. Currently only $DC00 and $DC0D are written during rendering. The rest of the color RAM is available for custom building colors.

**Idea:** Assign different color codes to building types (dockable = green, hostile = red, special = yellow) instead of the current monochrome approach. This would make city interiors much easier to navigate visually.

### 1.3 Animated Building Shapes (Easy)

**What:** The 8 building types (A-H) are rendered as static bitmap patterns. The game already knows how to draw its building types from the object records at $0E00, whose type byte indexes the table at $C39A.

**How:** Modify the rendering routine at $1E2D5 to shift the bitmap pattern by one column every N frames, creating a scrolling/rippling effect. The existing sprite 5 flashing mechanism can be repurposed for this.

**Idea:** Make hostile buildings pulse red (via color RAM changes) and dockable buildings have a gentle green glow. The DFP airlocks already flicker - extend this to all building entrances.

## Category 2: Gameplay Extensions (Medium)

### 2.1 Additional Commands (Easy)

**What:** The board computer parses commands somewhere in the $5xxx-$6xxx range (its messages are queued from there), but the parser itself has not been disassembled.

**How:** Add new CMP entries to the dispatch table. Each command needs: CMP #$xx, then BEQ/BNE branching to the handler routine in low RAM ($2xxx-$7xxx).

**Idea:** Add "SCAN" (scan for robots), "MAP" (show local city map on screen), or "FIRE" (fire at a building). The board computer already parses input - just extend the dispatch table.

### 2.2 Robot AI Enhancement (Medium)

**What:** Robots move on fixed paths with predictable patterns. The game tracks MK I, II, III, hunter-killers, guardian crawlers, and fortresses - but their behavior is hardcoded.

**How:** The robot movement code uses zero-page variables. A new routine could read a movement table (stored in the free space at $1695F) and make robots respond to player position or building status.

**Idea:** Make hunter-killers chase the player when they detect a cooling rod being carried. Guardian crawlers could patrol building perimeters instead of standing still. This would add genuine tactical depth.

### 2.3 City Interaction Depth (Medium)

**What:** The game has 32 cities with full coordinate data, but the only interaction is finding cooling rods and dodging robots. There's no city-to-city variation beyond coordinates.

**How:** Each city already has a per-city object list, located through the city number at $0354. The object records could be extended with additional bytes for city-specific properties (hostility level, robot density, rod locations).

**Idea:** Some cities could have hidden shortcuts between buildings, others could have civilian robots that don't attack. The coordinate system already supports this - just add a "city flags" byte to each entry.

### 2.4 Extended Mission Objectives (Medium)

**What:** The sole objective is collecting 40 rod parts for 20 bars. There's no secondary goal, no time pressure, and no branching paths.

**How:** The game already tracks score, cooling rod count, and mission state in zero page ($0056 is the frame counter). New variables could track bonus objectives.

**Idea:** Add "rescue prisoners" or "disable defense grids" as secondary objectives. Each city could have a prisoner that reduces robot density when freed. This would make every city worth visiting, not just the ones with rods.

## Category 3: Audio Enhancements (Medium)

### 3.1 Multi-Channel Music (Medium)

**What:** The SID chip has 3 voices and the game uses all three: voice 0 and voice 1 play the twelve-byte
effect records at $8812 through $8759, and voice 2 is the engine, driven from the speed byte at $0353.
There is no music player anywhere in the image - the routine at $35F6 that looks like one is the border
banner's text engine (see [Sound System](sound.md)).

**How:** Freeing a voice for music means taking one away from the effects, which is why the original did
not. A music player would have to share: run the engine and one effect voice, and let the second effect
voice drop out under the tune. The pitch registers are the same ones $8812 already writes.

**Idea:** Add a background music loop using channels 1-2 (bass + melody) with channel 3 for sound effects. A simple arpeggiated bass line on channel 1 would fill the cities with atmosphere without overwhelming gameplay audio.

### 3.2 Dynamic Sound Effects (Easy)

**What:** The game has basic sound effects but they're all the same tone. No variation based on situation.

**How:** Modify the existing SID writes to use different frequency values ($D402-$D403) based on context. The frame counter at $0056 can drive pitch modulation.

**Idea:** Robot detection = rising pitch, cooling rod pickup = descending tone, building fire = noise burst. All achievable with 10-20 bytes of new code each.

## Category 4: Technical Overhauls (Hard)

### 4.1 Procedural City Generation (Hard)

**What:** Cities are hand-designed with fixed building layouts. A randomizer would create unique city layouts each playthrough.

**How:** The type table at $C39A defines the building classes and the painter at $3F93 draws them. A procedural generator could rearrange these, add new building combinations, and place robots/rods in different configurations.

**Space needed:** ~500 bytes for a PRNG + layout generator. The existing per-city object lists would need to be extended with new layout tables.

### 4.2 Multi-City Map Display (Hard)

**What:** The glider viewer shows one city at a time. A mini-map showing all 32 cities on screen would be invaluable for navigation.

**How:** This would require significant screen RAM manipulation. The game uses Mode 4 TED mode with character-based rendering. A map display would need to draw the city network using screen RAM at $0400-$07FF.

**Challenge:** The existing rendering loop at $1E2D5 is tightly coupled to the glider viewer. A map overlay would need its own rendering path, possibly using sprites 6-13 for city dots on a dark background.

## Category 5: Quality of Life (Easy)

### 5.1 Player Position Indicator (Easy)

**What:** Inside buildings, the player has no visual indicator of their position. The screen shows building interiors but not where you are relative to exits.

**How:** Use one of the free sprites (6-13) as a player cursor arrow. Position it based on the player's coordinates within the building, updated each frame via $D014/$D015 writes.

### 5.2 Robot Proximity Warning (Easy)

**What:** Robots appear suddenly with no warning. A proximity indicator would give players time to react.

**How:** Compare player coordinates against robot positions each frame ($0056 increments every frame). If within a threshold, flash a sprite or change border color via $D020.

### 5.3 Cooling Rod Counter (Easy)

**What:** The player must track rod collection mentally. A persistent on-screen counter would help.

**How:** Use the existing glyph blitter at $3E17 to draw digits in a corner of the screen. The game already renders text - just add a counter display routine that blits into the bitmap.

### 5.4 Hostility Status Indicator (Easy)

**What:** Cities can become hostile (by natural state or after firing), but there's no clear indicator of the current status.

**How:** Add a single-byte flag in zero page ($00xx unused). When the city is hostile, display a warning symbol using a free sprite or color RAM write to the screen border.

## Category 6: The "What If" Projects (Extreme)

### 6.1 Full Remake with Expanded Content (Extreme)

**Concept:** Use Tau Ceti's engine as a foundation for a significantly expanded game. Keep the glider viewer rendering, the city coordinate system, and the building types, but add:

- Multiple mission types (rescue, sabotage, reconnaissance)
- Player upgrades (shield, speed, weapon systems)
- City-specific events and NPCs
- A branching storyline with multiple endings
- Expanded SID music and sound effects
- Save/load with full game state persistence

### 6.2 Networked Multiplayer (Extreme)

**Concept:** Two C64s connected via a serial cable, each controlling a different glider in the same city. This would require a custom protocol over the IEC serial bus (KERNAL $FFC6 is available).

**Feasibility:** Technically possible but would consume most of the available free RAM and require significant re-architecture of the rendering loop.

### 6.3 Demoscene Intro (Extreme)

**Concept:** A Tau Ceti-themed demoscene intro using the game's own assets - building bitmaps, city coordinates, and charset - but presented as a rotating 3D cityscape with SID music.

**Why it fits:** The game already has 3D projection math (used for the glider viewer), trigonometry tables, and custom rendering. A demoscene intro would push these systems to their absolute limits.

## Summary: What's Actually Feasible Right Now

| Priority | Change | Effort | Impact |
|---|---|---|---|
| 1 | Expanded color palette for buildings | Low | High - instant visual improvement |
| 2 | Additional sprite lights (6-13) | Low | Medium - more visual depth |
| 3 | Multi-channel SID music | Medium | High - atmosphere |
| 4 | New commands via dispatch table | Low | Medium - gameplay depth |
| 5 | Robot AI enhancement | Medium | High - tactical depth |
| 6 | Procedural city generation | Hard | Very high - replayability |
| 7 | Multi-city map display | Hard | Medium - navigation aid |

> [!NOTE]
> **Bottom line:** Tau Ceti's code is remarkably extensible. The dispatch table architecture, the sprite-based rendering, and the free VIC-II resources (sprites 6-13, SID channels 1-2) provide clear pathways for improvement without requiring a complete rewrite. The largest constraint is free RAM - the biggest contiguous block is only 3,745 bytes at $1695F. But for visual enhancements and gameplay tweaks, that's plenty.

---

[Back to the overview](../README.md)
