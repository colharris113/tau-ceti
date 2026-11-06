# Rendering Pipeline

The custom VIC-II mode, the twelve-screen UI and the sprite and raster tricks.

---

A deep technical analysis of how Tau Ceti renders its quasi-3D cityscapes, the 12-screen UI system, and the VIC-II hardware tricks that make it all work.

## The Custom Screen Mode

Tau Ceti uses a custom VIC-II screen mode that extends beyond the standard C64 text or bitmap modes. The game manipulates the VIC-II's color and border registers to create a pseudo-3D effect with 25 colours on a 160x200 grid.

> [!NOTE]
> **Key insight:** The screen mode is set up during initialization by writing directly to VIC-II registers. The game uses hardware scrolling for smooth panning across the city landscape.

### VIC-II Registers Accessed

| Register | Address | Purpose |
|---|---|---|
| $D011 | BORDER COLOR | Controls border colour (used for sky/terrain differentiation) |
| $D016 | SPRITE ENABLE | Enables/disables sprites for UI elements |
| $D018-$D019 | SPRITE X/Y EXPAND | Scale sprites for distance effects |
| $D01A | SPRITE MULTICOLOR | Multicolor mode for richer graphics |
| $D020 | SPRITE PRIORITY | Sprite vs background priority |
| $D012 | RASTER | Raster interrupt line position |
| $D015 | IRQ ENABLE | Enable raster interrupts for frame sync |
| $D025-$D026 | H/V SCROLL | Hardware scrolling for smooth panning |

## The 12 UI Components - Detailed Breakdown

The main flight screen is divided into 12 distinct regions. Here's how each is rendered:

### 1. Main Viewer (Quasi-3D Landscape)

This is the largest region, occupying the upper-left portion of the screen. It renders a perspective view of the city/landscape with buildings and objects that grow progressively larger as you approach them - the classic "quasi-3D" technique.

The rendering pipeline works as follows:

1. Calculate perspective scale factor based on distance (Z coordinate)
2. Apply the perspective lookup table at $14D00 to convert depth to screen coordinates
3. Draw building outlines using line algorithms that account for perspective
4. Fill building interiors with solid colours from the palette
5. Apply shadow calculations based on sun position (time of day)
6. Overlay moving elements (robots, missiles) using VIC-II sprites

### 2. Infrared Indicator

A small icon in the centre of the screen that shows whether infrared mode is active. This is a static sprite that toggles visibility based on the IR flag in zero-page memory.

### 3. Target Tracking (White Square)

When a hostile target is locked, a white square appears in the centre. This is rendered by writing directly to the screen bitmap at a fixed position, with the colour byte set to white ($01).

### 4. Radar Sensor

A circular radar display that shows nearby targets. The radar is drawn using a circle algorithm that plots points around a centre coordinate. Targets appear as bright dots on the radar when they're within range.

### 5. Compass

A compass needle in the board instruments area that points toward the city centre. The needle direction is calculated from the difference between your current heading and the city centre bearing. When you're at the city centre, the needle swings quickly (unstable).

### 6. Status Field (Green)

The upper-right green field shows real-time information: clock, view direction, city name, and ship status. This is rendered using the custom charset at RAM $8412-$85FF, with each character drawn as an 8x8 bitmap from the charset lookup table.

### 7. Radar Screen

The left-side radar shows buildings, hostile robots, and proximity mines. It switches between close and distant scan modes (key "S"). The radar uses a separate bitmap area in RAM for its display.

### 8. View Direction Indicator

Shows the current viewing angle: forward, right, backward, or left. This is a small icon that changes based on the view direction variable in zero-page memory.

### 9. ADF (Lower)

The lower ADF (Automatic Direction Finder) always points toward the closest jump pad. The bearing is calculated from your current position to the nearest jump pad's coordinates.

### 10. ADF (Upper)

The upper ADF always points to the centre of the current city. Similar to the compass but specifically targets the city centre rather than a general heading.

### 11. Supply Display (Red Field)

Below the radar screen, the red field shows missile count, anti-missile missile count, and flare count. These are rendered as small bar graphs or numeric displays using the custom charset.

### 12. Flying Info Window (Yellow)

Next to the supply display, the yellow window shows flying height, shield status, fuel supply, laser temperature, and speed. Each value is updated every frame based on the ship's state variables.

## Quasi-3D Rendering Algorithm

Tau Ceti uses a "quasi-3D" technique where objects get progressively bigger as you approach them. This is achieved through perspective projection:

```text
Quasi-3D Perspective Formula:
  screen_x = (object_x - camera_x) * scale_factor + centre_x
  screen_y = (object_y - camera_y) * scale_factor + centre_y
  screen_size = object_base_size / distance

Where:
  scale_factor = perspective_table[depth_index]
  distance = sqrt((x-x0)^2 + (y-y0)^2 + (z-z0)^2)
```

The perspective lookup table at file offset $14D00 contains pre-calculated scale factors for different depths. This avoids expensive division operations on the 6502 processor.

### Perspective Lookup Table

The table at $14D00 is 768 bytes long and contains values that map depth to screen scale. The values decrease exponentially as depth increases, creating the illusion of perspective:

```text
Depth Index    Scale Factor    Screen Size
0 (nearest)    $FF             100%
1              $E0             88%
2              $C0             75%
...            ...             ...
16 (farthest)  $08             5%
```

## Raster Interrupt System

The game uses VIC-II raster interrupts to synchronize the main game loop with the display refresh. The raster interrupt fires at a specific scanline each frame, triggering the main update routine.

```asm
Raster Interrupt Setup:
  LDA #$xx        ; Raster line number
  STA $D012       ; Set raster compare
  LDA #%00100000  ; Enable raster IRQ
  STA $D01A       ; VIC-II IRQ enable
  CLI             ; Enable interrupts
```

## Sprite System

Tau Ceti uses VIC-II sprites for UI elements and moving objects. Each sprite is defined by its X/Y position, colour, size (double-width/double-height), and multicolor mode settings.

| Spr# | Purpose | Position |
|---|---|---|
| 0 | Infrared indicator | Centre screen |
| 1 | Target tracking square | Centre instruments |
| 2-3 | Moving robots | Landscape area |
| 4-5 | Missiles | Landscape area |
| 6-7 | Turret lasers | Landscape area |

## Shadow Rendering

Buildings cast shadows based on the sun position (time of day). The shadow algorithm works as follows:

1. Calculate sun angle from the current spin (time of day)
2. For each building, calculate the shadow direction and length
3. Draw the shadow as a dark polygon extending from the building base
4. The shadow length is proportional to the building height and inversely proportional to the sun elevation

> [!NOTE]
> **From the manual:** "The sun's position changes as the planet spins, affecting how buildings cast shadows. This is an important visual cue for determining time of day." The shadow system adds depth and realism to the quasi-3D cityscapes.

## Summary

Tau Ceti's rendering pipeline combines custom VIC-II screen modes, sprite-based UI elements, perspective lookup tables, and raster interrupts to create a convincing quasi-3D experience on the limited hardware. The 12-screen UI system provides comprehensive situational awareness while maintaining performance through careful use of hardware features.

---

[Back to the overview](../README.md)
