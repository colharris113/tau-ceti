# Map System

The MAP command, city map generation and the planet map data structure.

---

A complete analysis of how the city map and planet map are generated, stored, and rendered.

## The MAP Command

Entering MAP on the board computer switches the display to a zoomable map of Tau Ceti showing all 32 cities and their jump pad connections.

## City Map Generation

The city map is generated from the coordinate data stored at file offset $14BE4. Each city's coordinates are scaled to fit the screen display area.

### Map Rendering Process

1. Read city coordinates from the table at $14BE4
2. Apply zoom/pan offsets to each coordinate
3. Scale coordinates to fit the screen area
4. Draw city names using the custom charset
5. Draw jump pad connections between cities
6. Highlight the current city with a different colour

### Zoom/Pan Controls

| Action | Key | Effect |
|---|---|---|
| Zoom in | + | Increase magnification |
| Zoom out | - | Decrease magnification |
| Pan up | Up arrow | Move map view north |
| Pan down | Down arrow | Move map view south |
| Pan left | Left arrow | Move map view west |
| Pan right | Right arrow | Move map view east |

## Planet Map (Board Computer MAP)

The planet map shows all 32 cities connected by jump pad lines. The layout is a top-down view of the planet surface with cities positioned according to their coordinates.

### Planet Map Data Structure

```text
Planet Map Structure:
  City positions: $14BE4-$14D00 (128 bytes)
  Jump pad connections: $14D00-$14E00 (256 bytes)
  Map display buffer: RAM $F800-$FBFF (1024 bytes)
  Zoom level: Zero-page variable
  Pan offset: Two zero-page variables (X, Y)
```

## Walkthrough: Generating a City Map

Let's walk through the process of generating a map for Centralis:

1. **Read coordinates:** LDA city_index, LDX #$14BE4, read X/Y/Z/W bytes
2. **Apply zoom:** Multiply coordinates by zoom factor from lookup table
3. **Apply pan:** Subtract pan offset from each coordinate
4. **Scale to screen:** Convert world coordinates to screen pixels
5. **Draw buildings:** For each building in the city, draw its outline
6. **Draw labels:** Write city name using custom charset
7. **Draw jump pads:** Draw lines from city edges to connected cities

## Jump Pad Network Visualization

The jump pad connections form a network graph that connects all 32 cities. The MAP command displays this as lines between city positions.

```text
Jump Pad Network:
  Each city has 4 jump pads (N/S/E/W)
  Each pad connects to exactly one other pad in another city
  Total connections: ~64 (32 cities x 2 unique connections each)

The network is fully connected - you can reach any city from any other city through a series of jumps.
```

## Summary

The map system uses pre-stored city coordinates and a simple scaling algorithm to generate the planet map. Zoom and pan controls allow exploration of the full network, with jump pad connections drawn as lines between cities.

---

[Back to the overview](../README.md)
