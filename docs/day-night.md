# Day/Night Cycle

The 16-spin clock, sun position, visibility levels and light changes.

---

A complete analysis of the 16 "Spins" per day system, time tracking, and the transition between daylight and infrared modes.

## The 16 Spins System

Each day on Tau Ceti consists of 16 "Spins", with each spin lasting approximately 5 Earth minutes (1/12 of an hour). This means a full day is about 80 Earth minutes (1 hour 20 minutes).

> [!NOTE]
> **From the manual:** "Each spin lasts approximately 5 Earth minutes. The planet completes 16 spins per day." This gives a total day length of about 80 minutes.

### Time Tracking

| Parameter | Value |
|---|---|
| Spins per day | 16 |
| Duration per spin | ~5 Earth minutes (in-game) |
| Total day length | ~80 Earth minutes |
| Day phase | Spins 0-7 (sunrise to sunset) |
| Night phase | Spins 8-15 (sunset to sunrise) |
| Time variable | $11 in zero-page memory (0-15) |

## Sun Position System

The sun's position changes as the planet spins, affecting visibility and shadow casting. The sun is the only celestial body rendered - planets are not shown.

### Sun Rendering

```text
Sun Position Calculation:
  sun_angle = (current_spin * 22.5) degrees
  sun_x = centre_x + cos(sun_angle) * radius
  sun_y = centre_y - sin(sun_angle) * height

The sun is drawn as a bright yellow/orange circle in the sky area of the main viewer.
```

## Day/Night Transition

The transition between day and night affects visibility dramatically. During the day, you can see the landscape clearly. At night, you need infrared mode to navigate.

### Visibility Levels

| Phase | Spins | Visibility | Infrared Required |
|---|---|---|---|
| Dawn | 0-2 | Low | No |
| Day | 3-6 | High | No |
| Dusk | 7-8 | Medium | No |
| Night | 9-14 | Very low | Yes |
| Dawn (again) | 15 | Low | No |

## Infrared Mode Toggle

The I key toggles infrared mode on and off. When infrared is active, the screen takes on a green-tinted appearance with enhanced contrast for night navigation.

| Mode | Key | Screen Effect | Visibility |
|---|---|---|---|
| Daylight | I (off) | Normal colours | Good in day, poor at night |
| Infrared | I (on) | Green tint, high contrast | Poor in day, good at night |

## Time-of-Day Effects on Rendering

The time of day affects several aspects of the rendering:

| Effect | Daytime | Nighttime |
|---|---|---|
| Sky colour | Blue/orange | Black/dark blue |
| Ground colour | Brown/green | Dark grey |
| Building colours | Full palette | Muted, green-tinted |
| Shadows | Long/short depending on sun angle | No shadows (no direct light) |
| Sun visibility | Bright yellow circle | Not visible (below horizon) |
| Infrared indicator | Off | On (if IR activated) |

## Summary

The day/night cycle is a core mechanic in Tau Ceti, with 16 spins per day creating a dynamic environment. The lack of a moon means infrared mode is essential for nighttime play, adding strategic depth to mission planning.

---

[Back to the overview](../README.md)
