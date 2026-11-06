# Infrared Blur

The infrared scanner and its blur algorithm.

---

A complete analysis of the infrared viewing system and its blur effect algorithm.

## The Infrared Scanner

Since Tau Ceti III has no moon, nighttime visibility is extremely poor. The infrared scanner (activated with the I key) provides night vision by enhancing contrast and adding a green tint to the display.

> [!NOTE]
> **From the manual:** "At night the only way to see is through the infrared scanner." This makes the IR toggle essential for nighttime navigation and combat.

## Infrared Blur Algorithm

The infrared mode applies a blur effect to the screen to simulate the low-resolution nature of infrared imaging. This is achieved by:

1. **Downscale:** Reduce the screen resolution by sampling every other pixel
2. **Blur:** Average adjacent pixels to create a soft, blurred effect
3. **Upscale:** Scale the blurred image back to full resolution
4. **Tint:** Apply a green colour overlay to simulate infrared imaging

### Implementation Details

```text
Infrared Blur Algorithm:
  1. Copy screen bitmap to working buffer
  2. For each pixel in the buffer:
     a. Read 2x2 block of pixels
     b. Average their colours
     c. Write averaged value back to buffer
  3. Apply green tint by modifying colour registers
  4. Copy blurred buffer back to screen
```

## Infrared Indicator

A small icon in the centre of the screen shows whether infrared mode is active. This is a static sprite that toggles visibility based on the IR flag in zero-page memory.

## Performance Considerations

The blur effect is computationally expensive on the 6502 processor. The game optimizes this by:

| Optimization | Description |
|---|---|
| Block processing | Process 4x4 pixel blocks instead of individual pixels |
| Lookup tables | Pre-calculate blur weights for common patterns |
| Skip frames | Only apply blur every other frame to maintain performance |
| Partial update | Only blur the landscape area, not the UI elements |

## Summary

The infrared blur effect is a clever simulation of infrared imaging that adds realism to nighttime gameplay. While computationally expensive on the 6502, the game uses several optimizations to maintain acceptable performance.

---

[Back to the overview](../README.md)
