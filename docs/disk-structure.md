# Disk Structure

A standard 35-track D64: eight files, a normal directory, and nothing hidden.

---

The disk image is 174,848 bytes, the size of a single-sided 35-track C64 disk. It has a normal
Commodore DOS directory at track 18 sector 1, eight files with ordinary names, and no encryption,
no packing and no protection. What made earlier readings of this image look exotic was arithmetic:
a D64 is not a rectangular grid of sectors, and if you index it as one, everything you read back is
garbage.

## The sector formula

A C64 disk is divided into zones, and each zone holds a different number of sectors per track.
Converting a track/sector pair to a byte offset therefore takes three cases:

```text
t <= 17        index = 21 * (t - 1) + s
18 <= t <= 24  index = 357 + 19 * (t - 18) + s
t >= 25        index = 490 + 18 * (t - 25) + s

byte offset = index * 256
```

Tracks 1-17 have 21 sectors, 18-24 have 19, and 25-35 have 18. A reader that uses
`(track * 40 + sector) * 256`, or that assumes every track has the same number of sectors, lands in
the wrong place for most of the disk - and the bytes it finds there look encrypted, because they
belong to a different file.

There is no encryption layer in this image. Every file is plain data and code; the loader reads
each one with the KERNAL LOAD routine and jumps into it.

## The directory

The directory is where DOS puts it, at track 18 sector 1, using the standard 32-byte entry format:

| Offset in entry | Contents |
|---|---|
| 0 | file type ($82 = PRG) |
| 1-2 | first track and sector |
| 3-18 | filename, padded with $A0 |
| 28-29 | size in blocks |

The listing, as read from the disk:

| File | Location | Blocks | Loads at | Role |
|---|---|---|---|---|
| `TAU CETI` | 17/0 | 1 | $0302 | boot stub |
| `JEFF` | 11/4 | 2 | $0C00 | loader |
| `PIC B TAUCETI+` | 13/0 | 40 | $4000 | title picture |
| `0E00-2000` | 17/1 | 19 | $0E00 | object records and tables |
| `8900-CC00` | 17/20 | 68 | $8900 | glyphs, names, demo script |
| `I/O 4K` | 19/0 | 17 | $D000 | replacement I/O |
| `CC00-D000` | 19/9 | 5 | $CC00 | screen tables |
| `E000-FFFF` | 20/0 | 33 | $E000 | main bitmap |
| `2000-8900` | 21/6 | 106 | $2000 | the game |

The filenames are the load ranges, which is why they read like memory addresses. `I/O 4K` is the
exception that proves the rule: it is loaded at $4000 and copied down to $D000 by the loader,
because you cannot LOAD into $D000 with the I/O bank switched in.

## Sector chains

The files are ordinary chained files - each sector begins with the track and sector of the next
one - but they are not contiguous. The chain jumps around within a track: the game file starts at
track 21 sector 6 and its second sector is track 21 sector 16, then track 22 sector 6, then 22/16,
and so on in an interleaved pattern.

That interleaving is the second reason naive readers go wrong. Even with the correct sector
formula, concatenating consecutive sectors produces a plausible-looking but wrong stream: the first
sector of the game file reads correctly, and from the second sector onward every byte is shifted.
Following the chain instead yields code that is byte-identical to a VICE dump taken at the point
the loader hands over to the game.

## First-sector headers

Every file that the loader installs begins with four bytes before its payload: two bytes that look
like a track/sector pair, then the load address, low byte first. JEFF starts `0B 0E 00 0C`, which
is track 11, sector 14, load address $0C00; the game file starts `15 10 00 20`, load address $2000.
The KERNAL LOAD call the loader uses takes its address from that header on the first sector, which
is why the payload proper starts at offset 4.

The boot stub is the exception: `TAU CETI` carries the usual two-byte PRG address and nothing else.

## What is not on the disk

Three things earlier versions of this chapter claimed, and which are not true of this image:

- **It is not a 32-track disk.** It is 35 tracks and 174,848 bytes, the standard size.
- **The header is not zeroed.** Track 18 sector 0 holds a normal BAM and the directory sector has a
  normal link; the filenames above are read straight out of it.
- **There is no XOR layer.** The bytes on disk are the bytes in memory. The files that appeared to
  be encrypted were the result of reading the wrong sectors.

---

[Back to the overview](../README.md)
