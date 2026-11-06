# Disk Structure

D64 layout, directory format, sector chains and the encryption layers.

---

The Tau Ceti D64 image is a 32-track, non-standard Commodore 64 disk image. Unlike standard 35-track D64 images, this uses all 32 tracks of the 1541 disk drive's usable surface area (tracks 0-31), providing approximately 174,848 bytes of storage.

### Header Analysis

The D64 header is non-standard: the first 128 bytes are all zeros, so the original disk name and ID are not preserved in this image. Standard D64 headers contain:

- Bytes 0-32: Disk ID and name
- Bytes 33-34: Track 0, Sector 0 pointer
- Bytes 35-36: Track 18, Sector 0 pointer (directory start)
- Bytes 37-127: Unused padding

In Tau Ceti's case, all these bytes are zero. The directory must be found by scanning for known sector chain patterns.

### Directory Structure

The directory entries use a custom 32-byte format rather than the standard 32-byte PETSCII directory entry. The key differences:

| Offset | Standard D64 | Tau Ceti Format |
|---|---|---|
| 0-1 | Next track/sector pointer | Padding / flags |
| 2-3 | File length (low/high) | Sector count / metadata |
| 4-5 | Starting track/sector | Track/sector pair |
| 6+ | Filename (16 bytes PETSCII) | Filename starts at byte 6 |

### Sector Chain Tracing

File contents are reconstructed by following sector chains. Each file's data begins at its starting track/sector, and subsequent sectors are linked via [track][sector] pairs stored within the data itself.

| File | Start Location | Chain Length | Content Type |
|---|---|---|---|
| TAUCETI (PRG) | T11 S2 | ~8 sectors | Main loader + decryption routine |
| Encoded Data 1 | T12 S9 | ~16 sectors | XOR encrypted game engine |
| Encoded Data 2 | T11 S15 | ~12 sectors | XOR encrypted graphics/world data |
| Graphics Block A | T15 S0-S3 | ~4 sectors | VIC-II character set + sprite data |
| Graphics Block B | T16 S0-S4 | ~5 sectors | Screen bitmap + tile data |
| World Data | Scattered T8-T10 | Variable | Planet maps, station layouts |

### Loader Analysis (T11 S2)

The main loader at Track 11 Sector 2 performs the following sequence:

1. Loads data to RAM address $0801 using KERNAL LOAD ($FF90)
2. Performs XOR decryption on encoded data blocks
3. Sets up raster interrupt via VIC-II $D01A register
4. Initializes custom charset by calling JSR $5105
5. Jumps to game entry point at RAM $26A0

### Encryption Scheme

The game data uses XOR encryption with multiple key bytes:

| Data Region | XOR Key | Decrypted Content |
|---|---|---|
| T12 S9 (game code) | $06 | 6502 assembly routines ($2xxx-$7xxx) |
| T11 S15 (graphics) | $FF | VIC-II bitmap data |
| World data blocks | Multi-byte ($06,$FF,$3C) | Planet/station definitions |

### Disk Layout Map

```text
Track  0: [unused - boot sector area]
Track  8: World data (planet definitions)
Track  9: World data (station layouts)
Track 10: World data (object definitions)
Track 11: S2=Loader, S15=Encrypted graphics
Track 12: S9=Encrypted game code
Tracks 13-14: [unused or system data]
Tracks 15-16: Graphics (character set, bitmaps)
Track 17: [unused]
Track 18: Directory entries (custom format)
Tracks 19-31: [extended track area - may contain additional data]
```

### File Reconstruction

To reconstruct any file from the D64:

1. Find the starting [track][sector] pair in the directory
2. Read 256 bytes from that sector position (track * 256 + sector * 256 + base_offset)
3. Check first 2 bytes for next-sector pointer
4. If non-zero, follow the chain until a null pair is encountered
5. XOR decrypt each sector with the appropriate key

> [!WARNING]
> The D64 image used for this analysis has a zeroed header, so its original track allocation and file names are not preserved.

---

[Back to the overview](../README.md)
