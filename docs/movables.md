# Moveable Elements

Missiles, robots, turrets, flares and sprite management.

---

A complete analysis of how missiles, robots, turret lasers, and flares are rendered, animated, and controlled.

## Moveable Element Types

| Type | AI Behaviour | Rendering |
|---|---|---|
| Missiles (hostile) | Heat-seeking, tracks player position | VIC-II sprite, moves toward player |
| Missiles (player) | Straight line, no guidance | VIC-II sprite, moves forward |
| AMMs (player) | Intercepts hostile missiles | VIC-II sprite, tracks nearest missile |
| Flares | Falls downward, distracts missiles | VIC-II sprite, moves down |
| Robots (MK1) | Patrols area, fires at player if close | VIC-II sprite, moves in pattern |
| Robots (MK2) | More aggressive, faster movement | VIC-II sprite, larger sprite |
| Robots (MK3) | Hunter-killer, tracks player position | VIC-II sprite, largest sprite |
| Turret lasers | Fires at player when in range | Line drawing on screen bitmap |
| Sand hoppers | Ground vehicles near jump pads | VIC-II sprite, moves slowly |
| Proximity mines | Stationary, explodes when player passes | Static sprite, triggers on proximity |

## Missile AI

Hostile missiles use heat-seeking AI to track the player's skimmer:

```text
Missile AI Algorithm:
  1. Detect player within range (radar lock)
  2. Calculate bearing to player's current position
  3. Adjust missile heading toward player
  4. Move missile forward along new heading
  5. If player fires flare: chance to lose lock
  6. If player fires AMM: intercept check
  7. If collision with player: explosion
```

## Robot Movement Patterns

Different robot types have different movement patterns:

| Type | Pattern | Speed |
|---|---|---|
| MK1 | Patrols in a fixed pattern | Slow |
| MK2 | Chases player if in range | Medium |
| MK3 | Hunter-killer, tracks player position | Fast |
| Guardian crawler | Slow but powerful, moves toward player | Very slow |

## Turret Laser Rendering

Turret lasers are rendered as lines on the screen bitmap. The line algorithm calculates the start point (turret position) and end point (player position) and draws a bright line between them.

```text
Turret Laser Drawing:
  1. Get turret position (x1, y1)
  2. Get player position (x2, y2)
  3. Calculate line using Bresenham's algorithm
  4. Draw line in bright red colour
  5. Fade out over several frames
```

## Flare Mechanics

Flares are deployed to distract heat-seeking missiles. When a flare is active, hostile missiles have a chance to lose their lock and drift away.

| Parameter | Value |
|---|---|
| Max flares | 8 |
| Key | F |
| Duration | ~3 seconds per flare |
| Effectiveness | 50% chance to break missile lock |
| Rendering | Bright yellow sprite, falls downward |

## Sprite Management

Tau Ceti uses VIC-II sprites for all moveable elements. The sprite system has 8 sprites available, which are dynamically assigned to the most relevant objects.

| Spr# | Purpose | Priority |
|---|---|---|
| 0 | Infrared indicator | Always on |
| 1 | Target tracking square | When locked |
| 2-3 | Hostile robots | High |
| 4-5 | Missiles | High |
| 6-7 | Turret lasers / flares | Medium |

## Summary

Tau Ceti's moveable elements system combines sprite-based rendering with simple AI for robots and missiles. The turret laser uses line drawing on the screen bitmap, while flares provide a counter-measure against heat-seeking missiles.

---

[Back to the overview](../README.md)
