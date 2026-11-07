# Character Set and Text System

How text is stored, and how it reaches the screen when there is no character mode.

---

Tau Ceti has no character set in the usual sense. The screen is a bitmap, so there is nothing for
the VIC-II to fetch glyphs from: every letter on screen has been copied into the bitmap by the
game. What looks like a custom charset is a set of 8x8 patterns in RAM, a blitter that copies them
into the picture, and a simple encoding that turns string bytes into pattern numbers.

## The encoding

Every string in the game - the status line, the message log, the city names - uses the same
encoding. A letter is stored as its index in the alphabet plus $20, with A as 1:

| Byte | Character | Byte | Character |
|---|---|---|---|
| $21 | A | $2C | L |
| $22 | B | $2D | M |
| $23 | C | $2E | N |
| $24 | D | $2F | O |
| $25 | E | $30 | P |
| $26 | F | $31 | Q |
| $27 | G | $32 | R |
| $28 | H | $33 | S |
| $29 | I | $34 | T |
| $2A | J | $35 | U |
| $2B | K | $36 | V |
| | | $37-$3A | W X Y Z |

Two conventions sit on top of that:

- **$C0 separates items in a list.** The city names at $8D02 are one long run of letters with $C0
  between them, terminated by $FF.
- **$80 ends a line and $FF ends a message.** The message interpreter stops a line at $80 and the
  whole list at $FF, so a single message can be several lines long.

Bit 6 of a byte is used as a flag rather than part of the letter. In the message `PRESS 3 TO TRY
ANOTHER MISSION` the R is stored as $52 rather than $32, and the decoder ignores the top bit; the
same byte appears with and without it in neighbouring strings.

## Worked example: CENTRALIS

```text
C = $23   E = $25   N = $2E   T = $34   R = $32
A = $21   L = $2C   I = $29   S = $33

CENTRALIS  ->  $23 $25 $2E $34 $32 $21 $2C $29 $33
```

That sequence is at $8D02, the start of the city name table, and decoding it gives the first of the
32 names.

## The glyph blitter at $3E17

One routine draws every character in the game. It takes three arguments: the glyph number in A, the
screen column in X and the character row in Y. It then:

1. adds $C34A[X] to the row offset $C318[Y] to get the low byte of the destination;
2. adds $C372[X] to $C331[Y] and then $E0 to get the high byte - the $E0 is the top of the bitmap,
   so the cell lands inside $E000-$FF3F;
3. multiplies the glyph number by 8 to get a byte offset, and copies eight bytes from a font to the
   bitmap.

The font is chosen by the carry out of that multiply: glyphs 0-31 come from $8E00, glyphs 32-63
from $8F00. Two banks of 32 patterns each, 512 bytes in total, is the whole character set for
on-screen text.

Because the destination is a bitmap and not a screen matrix, the blitter writes *pixels*. The
glyphs sit in a band of the display whose mode is set by one of the raster stages, which is why
small text can be sharp while the playfield around it is multicolour.

## The message log's own fonts

The scrolling message log does not use the same font. Its interpreter at $41F7 reads glyph numbers
from a display list and multiplies each by 8 to index one of three banks:

| Bank | Address | Contents |
|---|---|---|
| 0 | $9000 | digits and punctuation |
| 1 | $9100 | A-Z, blank first |
| 2 | $9200 | not identified |

The byte's value also selects the bank, so the same number means different things depending on
where it lands - the display list encodes which bank it wants, not just which pattern.

## The display list

The log is driven by a pointer at $1C. Bytes below $80 are glyph numbers; $80 ends the current
line and triggers the scroll at $40E4; anything above $80 ends the list.

The scroll is a straight copy of eight rows, 80 bytes at a time: $F908 to $F7C8, $F958 to $F818,
$FA48 to $F908, $FA98 to $F958, $FB88 to $FA48, $FBD8 to $FA98, $FCC8 to $FB88 and $FD18 to
$FBD8. The log is a fixed-size buffer that is shuffled upwards, not a text window with a cursor.

## Messages worth knowing

The strings in this game are short and mostly functional. A sample, with the address each is
queued from:

| Address | Text |
|---|---|
| $4931 | `DEMO` / `LAUNCHED` / `LANDED` / `DOCKED` (status line) |
| $3C3D | `FLARE ACTIVATED` |
| $3C4E | `NO FLARES LEFT` |
| $3C5E | `NO MISSILES LEFT` |
| $3C95 | `AMM DETONATED` |
| $3CA4 | `NO AMMS AVAILABLE` |
| $5E6A | `SKIMMER REFUELED` |
| $6001 | `NOT AVAILABLE HERE` |
| $6015 | `SKIMMER ISN'T DOCKED` |
| $6503 | `PRESS 3 TO TRY ANOTHER MISSION` |
| $6528 | `DEMO MODE INITIATED` |
| $653E | `PRESS 3 TO EXIT` |

> [!NOTE]
> The old version of this chapter described a 512-byte lookup table at $8412-$85FF and a list of
> decoded strings at file offsets like $1CDE0. Neither exists: $8412 holds ordinary game data, the
> strings are scattered through the code at the addresses above, and there is no lookup table
> because there is no character mode to feed. The encoding table further up, though, was right, and
> it is the one part of the old chapter that survives intact.

---

[Back to the overview](../README.md)
