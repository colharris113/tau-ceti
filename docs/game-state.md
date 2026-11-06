# Game State

Zero-page variables, ship physics, combat mechanics and mission progress.

---

A complete analysis of the game's state management, ship physics, combat mechanics, and mission progress tracking.

## Zero-Page State Variables

The game maintains its state in zero-page memory ($00-$FF) for fast access. Key variables include:

| Address | Name | Purpose |
|---|---|---|
| $00-$01 | Frame counter | Counts frames since game start |
| $02 | Current city index | Which city you're in (0-31) |
| $03 | View direction | 0=forward, 1=right, 2=back, 3=left |
| $04 | Ship heading | Current direction (0-255 = 360 degrees) |
| $05 | Ship speed | Current velocity |
| $06 | Ship altitude | Flying height above ground |
| $07 | Missile count | Remaining missiles (max 8) |
| $08 | AMM count | Anti-missile missiles (max 8) |
| $09 | Flare count | Flares (max 8) |
| $0A | Fuel level | Current fuel supply |
| $0B | Shield status | Shield strength |
| $0C | Laser temperature | Laser heat level |
| $0D | Cooling rods collected | Parts count (0-40) |
| $0E | Cooling bars assembled | Bars count (0-20) |
| $0F | Cooling bars inserted | Bars in reactor (0-20) |
| $10 | Day/night flag | 0=day, 1=night |
| $11 | Current spin | Spin count (0-15) |
| $12 | Infrared flag | 0=off, 1=on |
| $13 | Game mode | 0=flying, 1=ground, 2=map |
| $14 | Score | Current score total |
| $15-$16 | Ship position X | 3D X coordinate |
| $17-$18 | Ship position Y | 3D Y coordinate |
| $19-$1A | Ship position Z | Depth/distance |

## Ship Physics

The skimmer has realistic physics with acceleration, deceleration, and turning mechanics:

| Parameter | Value | Description |
|---|---|---|
| Max speed | $FF | Maximum forward velocity |
| Acceleration | $04 | Speed increase per frame (Z key) |
| Deceleration | $02 | Speed decrease per frame (; key) |
| Turn rate | $08 | Heading change per frame (X/Z keys) |
| Rise rate | $03 | Altitude increase (: key) |
| Sink rate | $02 | Altitude decrease (. key) |
| Inertia | $01 | Gradual speed reduction when no input |

### Physics Update Loop

```text
PER FRAME:
  ; Handle input
  IF Z key pressed AND speed < max_speed:
    speed += acceleration
  IF ; key pressed AND speed > 0:
    speed -= deceleration
  IF X key pressed:
    heading -= turn_rate
  IF / key pressed:
    heading += turn_rate
  IF : key pressed:
    altitude += rise_rate
  IF . key pressed:
    altitude -= sink_rate

  ; Apply inertia
  IF no speed input:
    speed -= inertia

  ; Update position
  position_x += sin(heading) * speed
  position_y += cos(heading) * speed
```

## Combat Mechanics

Combat involves lasers, heat-controlled missiles, anti-missile missiles (AMMs), and flares:

| Weapon | Key | Damage | Range | Special |
|---|---|---|---|---|
| Laser | SPACE/C/E | Low | Line of sight | Heats up, needs cooldown |
| Missile | M | High | Long | Heat-seeking, limited ammo |
| AMM | A | Medium | Short | Counter-measure vs missiles |
| Flare | F | None | Short | Distracts heat-seeking missiles |

### Missile AI

Hostile robots fire missiles at your skimmer. The missile AI works as follows:

1. Robot detects your skimmer within range (radar lock)
2. Robot fires missile with initial heading toward your position
3. Missile tracks your position each frame (heat-seeking)
4. Missile adjusts its heading to intercept your trajectory
5. If you fire a flare, the missile may be distracted and lose lock
6. If you fire an AMM, it intercepts the hostile missile

## Mission Progress Tracking

The mission progress is tracked through three counters:

| Counter | Range | Purpose |
|---|---|---|
| Cooling rods collected | 0-40 | Parts found in reactors |
| Cooling bars assembled | 0-20 | Parts paired into bars (RODS command) |
| Cooling bars inserted | 0-20 | Bars placed in Centralis reactor |

> [!NOTE]
> **Win condition:** All 20 cooling bars must be inserted into the main reactor in Centralis. When the counter reaches 20, the mission is complete and the "REACTOR SUCCESSFULLY CLOSED DOWN" message appears.

## Score System

The SCORE command rates your progress. Points are awarded for:

| Achievement | Points |
|---|---|
| Each cooling rod collected | +10 |
| Each cooling bar assembled | +50 |
| Each cooling bar inserted | +100 |
| Enemy destroyed | +25 |
| City visited | +15 |
| Time bonus | Varies |

## Game Modes

The game has three main modes controlled by the game mode variable:

| Mode | Value | Description |
|---|---|---|
| Flying | 0 | Above-ground flight, 3D landscape rendering |
| Ground | 1 | Docked at building, board computer commands available |
| Map | 2 | Planet map display, zoom/pan controls |

## Summary

Tau Ceti's game state management uses a compact zero-page layout with ~$20 bytes of state variables covering ship physics, combat, mission progress, and game mode. The physics model is simple but effective, with acceleration-based movement and realistic turning mechanics.

---

[Back to the overview](../README.md)
