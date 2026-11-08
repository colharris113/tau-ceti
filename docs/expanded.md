# Tau Ceti: Expanded

A design sketch for a larger colony game built on the same engine.

---

A complete design for transforming Tau Ceti from a single-objective maze game into an open-world colony simulation - the Elite of 1983, but with depth.

## The Backstory (Already in the Code)

> [!NOTE]
> The design below is speculative. An earlier draft of this page quoted a line of text at file
> offset $204D8 - `TAU CETI 3))) IS NOW NEUTRALISED AND WILL SOON BE RECOLONISED` - as if it were in
> the game. It is not: that offset holds ordinary code, and the line was invented to give the design
> a hook. Treat the whole chapter as a proposal, not a description of the original.
> This is the **re-colonisation mission**. You are not just collecting reactor parts - you are the vanguard of a planetary reclamation effort. The three brackets ())) represent the three phases of the operation, or possibly the three original colonisation waves that were destroyed.

The full picture from message strings:

- **"TAU CETI 3))) IS NOW NEUTRALISED"** - The original colonisation was destroyed. Something neutralised it.
- **"WILL SOON BE RECOLONISED"** - Your mission is to rebuild.
- **"CIVILIAN SUPPLY CENTRE"**, **"MILITARY SUPPLY CENTRE"** - The game already has supply infrastructure concepts.
- **"ORP LANDER"** - You arrive in an ORP Lander, not just a glider.
- **"CENTRAL REACTOR"**, **"REACTOR SUBSTATION"** - Power infrastructure is already modelled.
- **"LAND 0PULATION"**, **"TRADE"**, **"DEFENCES"** - The game already tracks population, trade, and defences as stats (at offsets $21A27-$21A4B). These were meant to be meaningful.

## Core Design Philosophy

The rods are the **boss fight**, not the entire game. Think of it like this: you need to shut down the Central Reactor to win, but getting there requires conquering a planet first. The reactor shutdown is the final act after a campaign of expansion.

## Phase 1: The Colony Game (Core Loop)

### The New Objective Structure

| Phase | Goal | Time | Difficulty |
|---|---|---|---|
| 1. Establish Foothold | Secure Reema (starting city), build basic infrastructure | 1-2 hours | Easy |
| 2. Expand Network | Capture 4-6 cities, establish supply lines | 3-5 hours | Medium |
| 3. Industrial Base | Build refineries, shipyards, defence grids | 2-3 hours | Medium |
| 4. Planetary Unification | Take all 32 cities, neutralise hostiles | 3-4 hours | Hard |
| 5. The Reactor | Infiltrate Centralis, shut down the reactor | 1-2 hours | Extreme |

### The Economy System

The game already has strings for "TRADE", "CIVILIAN SUPPLY CENTRE", and "MILITARY SUPPLY CENTRE" - these were half-implemented. Here's the full system:

#### Currency: Credit Units (CR)

Each city generates income based on its type and development level. The player earns CR by:

- **Taxation** - Each controlled city pays daily tax (amount depends on city population and infrastructure)
- **Trade routes** - Transport goods between cities for profit (the glider becomes a cargo ship)
- **Resource extraction** - Mining cities produce raw materials that can be sold
- **Bounties** - Eliminate hostile robot armies for reward

#### Resources

| Resource | Source | Use |
|---|---|---|
| Credits (CR) | Tax, trade, bounties | Everything |
| Steel | Mining cities, military supply centres | Ship upgrades, buildings, defences |
| Food | Civilian supply centres, hydroponics cities | Population growth, city happiness |
| Energy | Reactor substations, solar cities | Powers buildings, ship fuel |
| Cooling Rods | Special buildings (original game) | Final boss key items |

#### City Types (Expanded from 8 to 16)

| Type | Income | Special | Example Cities |
|---|---|---|---|
| Industrial | High steel, med energy | Can build shipyards | Centralis, Botania |
| Mining | Med steel, low income | Rich in raw materials | Krill, Drano |
| Agricultural | High food, low credits | Population growth bonus | Jade, Hame |
| Military | Low income, high defence | Produces weapon parts | Kdapt, Kzinti |
| Scientific | Med credits, unlocks tech | Research speed bonus | Auriga, Preema |
| Commercial | Very high credits | Trade route hubs | Reema, Reyes |
| Hydroponic | High food, med energy | Food surplus for export | Botania, Minstro |
| Energy | High energy, med credits | Power generation bonus | Novia, Rubiya |

## Phase 2: Ship Upgrades

Your glider/lander evolves from a single-purpose vehicle into a multi-role colony ship.

| Upgrade | Cost | Effect |
|---|---|---|
| Shield Generator | 500 CR + 20 Steel | Reduces damage from hostile buildings by 50% |
| Extended Fuel Tank | 300 CR + 10 Steel | Double jump range between cities |
| Cargo Bay | 400 CR + 15 Steel | Carry trade goods between cities (new economy) |
| Weapons Array | 600 CR + 25 Steel | Fire at hostile buildings from orbit (new command) |
| Scanner Suite | 350 CR + 10 Steel | Reveal robot positions on local map |
| Repair Bay | 450 CR + 20 Steel | Auto-repair glider between missions (no fuel cost) |
| Hyperspace Drive | 1000 CR + 50 Steel | Skip to any city instantly (once per day) |
| Population Module | 800 CR + 30 Steel | Transport colonists to new cities (unlocks colonisation) |

## Phase 3: City Capture & Colonisation

### The Conquest System

Each of the 32 cities has a **hostility level** (0-100). Capturing a city is a multi-stage process:

1. **Reconnaissance** - Land at the jump pad, scan for robot density and building types
2. **Weakening** - Destroy military buildings and robot barracks to reduce hostility
3. **Infiltration** - Enter civilian supply centres and hijack their systems
4. **Declaration** - Plant your flag at the city centre (new building type)
5. **Holding** - Defend against counter-attacks for 1 in-game day

### City Development Levels

Once captured, cities can be developed through 4 tiers:

| Tier | Requirement | Effect |
|---|---|---|
| T0: Occupied | Complete capture sequence | City is yours, minimal income |
| T1: Settled | Build civilian supply centre (200 CR) | Population arrives, basic income |
| T2: Developed | Build industrial/agricultural buildings (500 CR) | Resource production begins |
| T3: Metropolis | Build all infrastructure (1500 CR + special items) | Maximum income, produces colonists for new cities |

## Phase 4: Trading & Supply Chains

The glider becomes your trade vessel. This is where the game truly opens up.

### Trade Mechanics

- **Buy low, sell high** - Each city has different supply/demand for each resource. Buy steel in mining cities, sell to industrial ones.
- **Trade routes** - Establish permanent routes between two cities. Your glider automatically makes the trip each day (costs fuel).
- **Cargo capacity** - Limited by cargo bay upgrade. Start with 4 units, max 16.
- **Risk and reward** - Trade routes pass through hostile territory. Pirates (rogue robots) can intercept your cargo.

### Dynamic Prices

Prices fluctuate based on supply and demand, which changes based on:

- How many cities of each type you control
- Recent events (a destroyed mining city spikes steel prices)
- Seasonal cycles (harvest time increases food supply)
- War status (hostile cities disrupt trade routes)

## Phase 5: Alien Visitors

The name "Tau Ceti" and the city names (Kzinti, Krill, Zilogi) reference real science fiction. The Kzinti are from Larry Niven's Known Space universe. This isn't accidental - the game is set in a shared sci-fi landscape.

### Alien Contact System

Random encounters with alien species appear at trade hubs or scientific cities:

| Species | Appearance | Trade Goods | Quest |
|---|---|---|---|
| Kzinti Warriors | Military cities, combat zones | Weapon parts, shield tech | Help them fight a common enemy |
| Theta Bandits | Commercial hubs, trade routes | Smuggled goods, black market items | Protect or raid trade convoys |
| Pak Homids | Scientific cities, research outposts | Advanced tech, energy cells | Research project collaboration |
| Drone Merchants | Any city with supply centre | Rare components, parts | Delivery missions between planets |

### Alien Diplomacy

Each alien faction has a **relationship meter** (0-100). Actions affect it:

- Trading with them increases relationship
- Attacking their ships decreases it
- Completing their quests gives large boosts
- At maximum relationship, they provide unique upgrades and ally in combat
- At minimum, they become hostile and attack your cities

## Phase 6: The Reactor Campaign (The Boss)

The cooling rods are the **final key**. You collect them after conquering most of the planet, when Centralis becomes fully fortified.

### The Final Sequence

1. **Phase A: Weaken Centralis** - Destroy outer defence buildings, reduce robot density to manageable levels. This requires capturing surrounding cities first to cut off reinforcements.
2. **Phase B: Collect the Rods** - The cooling rods are now in heavily defended buildings. Each rod requires a separate infiltration mission. You need 40 parts (20 bars).
3. **Phase C: The Insertion** - Enter the Central Reactor room. The reactor is now fully armed and fires back. This is a multi-stage boss fight.
4. **Phase D: Shutdown** - Insert the 20 cooling bars while defending against waves of robots. The "REACTOR SUCCESSFULLY CLOSED DOWN" message appears when complete.

### Boss Fight Mechanics

| Stage | Threat | Strategy |
|---|---|---|
| 1. Guardian Crawlers | 4-6 crawlers patrol the reactor room | Use infrared to track, missiles to eliminate |
| 2. Fortress Turrets | Fixed buildings fire continuously | Destroy turrets before advancing deeper |
| 3. Hunter-Killer Swarm | Rapid-fire hunter-killers | Shields essential, use cover between buildings |
| 4. The Reactor Core | The reactor itself fires energy blasts | Insert bars one at a time while dodging |

## New Commands (Board Computer Extensions)

Add these commands to the board computer (the parser has not been located, so this is a design
proposal rather than a patch):

| Command | Function |
|---|---|
| TAX | Collect credits from all controlled cities |
| TRADE | Open trading menu (buy/sell resources) |
| BUILD | Construct new buildings in controlled cities |
| UPGRADE | Upgrade ship or city infrastructure |
| COLONISE | Sent colonists to uncontrolled cities |
| DEFEND | Set up defence grid around a city |
| ROUTE | Establish trade route between two cities |
| SCAN | Show city statistics (population, defences, resources) |
| STATUS | Show your empire overview (cities controlled, credits, fleet) |
| DIPLOMACY | View alien faction relationships |

## New Game State Variables

The game already tracks some of this at zero page. Here's the expanded layout:

| Address | Variable | Range | Description |
|---|---|---|---|
| $0041 | Current city index | 0-31 | Already exists |
| $0042 | Building type | 0-7 | Already exists |
| $0043 | Hostility flag | 0-100 | Already exists, expand range |
| $0045 | Credits | 0-9999 | New: player wealth |
| $0047 | Steel | 0-255 | New: construction resource |
| $0048 | Food | 0-255 | New: population resource |
| $0049 | Energy | 0-255 | New: power resource |
| $004A | Cargo capacity | 0-16 | New: trade limit |
| $004B | Cargo contents | 0-16 | New: current cargo |
| $004C | Cities controlled | 0-32 | New: conquest progress |
| $004D | Ship shields | 0-100 | New: shield integrity |
| $004E | Ship fuel | 0-255 | Already exists, repurpose |
| $004F | Kzinti relations | 0-100 | New: alien diplomacy |
| $0050 | Bandit relations | 0-100 | New: alien diplomacy |
| $0051 | Pak relations | 0-100 | New: alien diplomacy |
| $0052 | Day counter | 0-9999 | New: game time |
| $0053 | Total score | 0-99999 | Already exists |
| $0054 | Rods collected | 0-40 | Already exists |
| $0055 | Bars assembled | 0-20 | New: bar assembly counter |

## The Save System (Already Exists)

The game already has the KERNAL SAVE ($FFD8) and LOAD ($FFD5) calls, reached through the handlers at
$6C55 and $69BA. The existing routine writes a raw $0400-$0C80 image - 2,179 bytes with the load
address, no field structure at all - so "extending" it means either replacing the image with a
versioned format or appending a second file. For the expanded version, the second file would hold:

- All new economy variables (credits, resources, cargo)
- City ownership data (which cities are controlled, at what tier)
- Ship upgrade state
- Alien relationship meters
- Trade route definitions
- Day counter and game progress

The disk has **78 free sectors** - more than enough for the expanded save file (estimated 3-4 sectors).

## New Cities (Expansion to 48)

The current 32 cities are a great start. Add 16 more to create a larger galaxy:

| New City | Type | Coordinates | Special Feature |
|---|---|---|---|
| ALTAIR | Scientific | New | Alien embassy, trade hub |
| VEGA | Commercial | New | Largest market, black market |
| SIRIUS | Military | New | Fortress city, weapon factory |
| PROCYON | Industrial | New | Shipyard, steel production |
| ARCTURUS | Agricultural | New | Food basket of Tau Ceti |
| SPICA | Energy | New | Solar array complex |
| RIGEL | Mining | New | Deep mine shafts, rare minerals |
| BETELGEUSE | Hydroponic | New | Massive greenhouse facilities |
| ANTARES | Military | New | Orbital defence platform |
| CAPPELLA | Commercial | New | Trade nexus, banking centre |
| ALDEBARAN | Scientific | New | Research station, alien contact |
| POLLUX | Industrial | New | Manufacturing hub |
| CASTOR | Energy | New | Nuclear fusion plant |
| ACHERNAR | Mining | New | Rare element extraction |
| CANOPUS | Agricultural | New | Fertile plains, population centre |
| REGULUS | Military | New | Command centre for fleet operations |

## The World Map (Visual Progression)

As you conquer cities, the world map on the board computer updates:

- **T0:** All cities shown as red (hostile) with question marks
- **T1-T3:** Cities turn yellow (contested) then green (controlled)
- **Trade routes:** Lines appear between connected cities
- **Alien outposts:** Blue dots appear when you make first contact
- **Centralis:** Pulses red until the reactor is shut down, then turns gold (victory)

## The Endgame & Replayability

### Victory Conditions

There are now **three ways to win**:

1. **The Purist** - Shut down the reactor with minimal city conquest (hard mode, high score)
2. **The Conqueror** - Take all 32 cities, then shut down the reactor (standard mode)
3. **The Diplomat** - Make peace with alien factions and negotiate reactor shutdown (new ending)

### New Game Plus

After winning, start a new game with:

- Your ship upgrades carry over
- Alien factions start with higher relationship
- Some cities are pre-controlled
- New challenge: the reactor is now fully armed and harder to infiltrate

## Implementation Priority

| Priority | Feature | Est. Effort |
|---|---|---|
| 1 | Extended save system (economy data) | 200 bytes |
| 2 | Credits and resource variables | 50 bytes |
| 3 | New board computer commands (TAX, TRADE, STATUS) | 150 bytes |
| 4 | City ownership tracking | 100 bytes |
| 5 | Ship upgrade system | 300 bytes |
| 6 | Trade route mechanics | 250 bytes |
| 7 | Alien contact encounters | 400 bytes |
| 8 | New cities (16) with coordinates | 300 bytes |
| 9 | Reactor boss fight redesign | 500 bytes |
| 10 | World map visual progression | 200 bytes |

> [!NOTE]
> **Total estimated code addition: ~2,500 bytes.** The largest free block on the D64 is 3,745 bytes at $1695F. Even without expanding the disk image, there's room for everything. The 78 free sectors provide massive headroom for new data (city definitions, alien encounters, trade tables).

> [!NOTE]
> **The vision:** Tau Ceti becomes a game where you wake up on an alien planet, find a broken glider and a mission brief about reactor parts, then realise the real game is building an empire. The rods are the final key - but getting there means turning a hostile world into your colony, one city at a time. It's Elite's open-world freedom meets the colonial sci-fi backdrop that was always there in the code.

---

[Back to the overview](../README.md)
