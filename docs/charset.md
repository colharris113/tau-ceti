# Character Set and Text System

There is no character mode, one encoding rather than two, and two glyph banks with different jobs.

---

Tau Ceti has no character set in the usual sense. The screen is a bitmap, so there is nothing for the
VIC-II to fetch glyphs from: every letter on screen has been copied into the picture by the game. What
looks like a custom charset is a set of 8x8 patterns in RAM, a blitter that copies them into the
picture, and an encoding that turns string bytes into pattern numbers.

The encoding is the part that used to be misread. The strings contain bytes like `$4F` and `$54` in the
middle of words, which looks like a second alphabet bolted onto the first. It is not: `$4F` is a
lowercase `o`, and the reason it looks like ASCII is that it *is* ASCII's numbering, deliberately.

## One font, three pages

Text that goes to the message log is drawn by the interpreter at `$41F7`, which hands each byte to
`$4210`:

```text
address = $9000 + ((b >> 5) << 8) + (b & $1F) * 8
eight bytes, one per bitmap row
```

so the font is three pages of 32 glyphs at `$9000`, `$9100` and `$9200`, and the byte's top two bits
choose the page while its low five bits choose the glyph. Three pages of 32 is 96 patterns, which is
what the whole written language of the game fits into:

| Codes | Glyphs |
|---|---|
| `$00-$09` | `0`-`9` |
| `$0A-$0B` | `.` `<` |
| `$0C-$13` | `>` `?` `"` `+` `-` `!` `:` `=` |
| `$14-$1E` | up arrow, `,` `;`, starburst, left arrow, `@`, `/`, `'`, `£`, `(` `)` |
| `$1F-$20` | blank |
| `$21-$3A` | **A-Z** |
| `$3B-$3F` | blank, `/` `(` `)` heavy `-` |
| `$40` | solid block (the bar fill) |
| `$41-$5A` | **a-z** |
| `$60-$7F` | unused; the third page is the last one the arithmetic can reach |

The two ranges that matter are adjacent and that is not a coincidence. `$21-$3A` is A-Z numbered from
1, so `A` is `$21` and `Z` is `$3A`. `$41-$5A` is a-z, and those numbers are *exactly* ASCII's
capitals: `$4F` is `O` in ASCII and `o` here. The designers did not invent a second encoding - they
put the lowercase alphabet at the numbers a programmer already knows, so that mixed-case text in a
hex dump reads partly like ASCII. A string with capitals in the game's encoding and lowercase in
ASCII is not two encodings meeting; it is one font, arranged so that the second half is typable.

The clearest example is the parser's failure message at `$4DFA`:

```text
80 2E 4F 54 20 35 4E 44 45 52 53 54 4F 4F 44 11
   N  o  t     U  n  d  e  r  s  t  o  o  d  !
```

`$2E` is `N` in the game's numbering, `$4F $54` are `o t` in ASCII's, `$35` is `U`, and the rest is
ASCII lowercase. It reads **"Not Understood!"** - title case, with the capitals in the first encoding
and the lower-case in the second, and one font underneath both.

## The control codes

Three byte values are not glyphs:

| Byte | Meaning |
|---|---|
| `$80` | line break: `$41F7` jumps to `$40E4` and scrolls the log up one row |
| `$81-$FF` | end of message: `$03A1` is cleared and the interpreter returns |
| `$C0` | in the city name table only: separates one name from the next |

The city names at `$8D02` are a special case of the same idea - a run of letters with `$C0` between
them and `$FF` at the end - and they are the only place in the game where `$C0` is a separator rather
than an end. See [World and Cities](world-and-cities.md).

## Typed input is the same encoding

Commands are typed into `$0200`, and the line editor at `$4E4C` builds them through a 64-entry table
at `$4AEA` indexed by **key number** (row*8 + bit on the C64 matrix). The three ranges it produces are
the same three it would produce for a string:

| Keys | Byte written | Example |
|---|---|---|
| digits | `$00-$09` | `1` -> `$01`, `0` -> `$00` |
| letters | `$21-$3A` | `A` -> `$21`, `Z` -> `$3A` |
| SPACE | `$20` | |

so a typed line and a string literal are directly comparable, which is what the parser at `$4DB7`
relies on: it compares the line against a name table at `$4BAC` whose entries are in the same
encoding, with bit 7 set on the last letter as a terminator, and the parser strips that bit before
comparing. `STATUS` in `$0200` is `33 34 21 34 35 33`, and the table holds the same six bytes.

There is one place in the command path where the two numberings are easy to confuse: the QUIT handler
at `$4FEB` tests for `$19` and `$27`, which are the **matrix codes** for Y and N, not their glyphs.
The queue carries key numbers, not characters, all the way to the line editor.

## The blitter at $3E17, and the second glyph bank

The screen does not only hold log text. Windows, panels, the status word, the command screens and the
whole 32-column character canvas are drawn through a different routine, `$3E17`, and it uses a
different bank of patterns:

| Bank | Address | Patterns | Used by |
|---|---|---|---|
| UI | `$8E00` and `$8F00` | 64 (32 + 32) | `$3E17`: status word, panels, command screens |
| log | `$9000-$92FF` | 96 (3 x 32) | `$41F7`/`$4210`: the message log |

Both are 8x8, two bits per pixel, and both end up in the same bitmap. The difference is the count and
the encoding: 64 patterns numbered 0-63 with a carry choosing the bank, against 96 numbered 0-95 with
the top two bits choosing the page.

`$3E17` takes the glyph in `A`, the column in `X` and the row in `Y`, and computes:

```text
dest = $E000 + $C34A[X] + $C318[Y] + $C372[X] + $C331[Y]
source = $8E00 + ((A*8) & $FF)  if A < $20, else $8F00 + ((A*8) & $FF)
```

`$C34A` is 0, 8, 16 ... 120 (eight bytes per column), `$C318` steps 0, $40, $80, $C0 and repeats
(four-cell rows), `$C372` adds 1 for columns 16-31, and `$C331` handles the odd row offsets - the
bitmap's cell interleave, expressed as two nibble tables. Eight bytes go straight into the bitmap, so
the blitter writes pixels, not screen codes.

The banner's glyphs come from the log's bank, and the status word's from the UI bank, which is why the
`DEMO` in the corner and the prose in the log do not quite look like the same typeface. They are not:
one is 64 patterns drawn into a 32x16 cell canvas, the other 96 patterns drawn into a five-row window.

## The character canvas

`$5105` is a string plotter built on `$3E17`: it walks a string whose last character has bit 7 set,
plots one glyph per call and advances the column. With `$277E` - which fills a 16x16 cell window with
a texture byte and a colour - it is the whole of the KEYS screen and the text half of MAP.

The canvas it draws into is `$E000-$EFFF`: 32 columns by 16 rows of 8x8 tiles, which is the top 4,096
bytes of the bitmap. That is not a coincidence about layout; it means a 16x16 window is exactly a
quarter of a 32x32 cell area, and a screen can be composed by filling windows with textures and then
plotting strings over them.

## The message log

The log is a display list, not a string buffer. A pointer at `$1C` is walked by `$41F7`: bytes below
`$80` are glyph numbers, `$80` ends the line, anything above ends the list. `$0385` is the write
offset into the line and `$4201` advances it by eight per glyph.

When a line ends, `$40E4` scrolls the window by copying whole rows: `$F908` to `$F7C8`, `$F958` to
`$F818`, `$FA48` to `$F908`, `$FA98` to `$F958`, `$FB88` to `$FA48`, `$FBD8` to `$FA98`, `$FCC8` to
`$FB88`, `$FD18` to `$FBD8`, then clears the two bottom rows for the new line. The sources sit `$50`
bytes apart, so a log row is 80 bytes wide inside the bitmap, and the visible window is five rows.

It is a fixed-size buffer shuffled upwards, which is why text in Tau Ceti appears to rise rather than
scroll, and why a burst of messages pushes everything above it out of existence rather than into a
history.

## Messages worth knowing

The strings are short and mostly functional. A sample, with the address each is pushed from:

| Address | Text |
|---|---|
| `$4931` | `DEMO` / `LAUNCHED` / `LANDED` / `DOCKED` (status word) |
| `$4DFA` | `Not Understood!` |
| `$6EB1` | `Parts do not match.` |
| `$6EC6` | `Cooling Rods Solved` |
| `$6EDA` | `All 20 rods now solved` |
| `$742A` | ` n ROD SECTION S FOUND` - the count is written into the string |
| `$79C9` | `Reactor room is only available in the Central reactor at Centralis` |
| `$7A0E` | `WARNING - You are entering a highly radioactive area` |
| `$7B5E` | `FATAL RADIOACTIVE DOSE RECEIVED / MISSION FAILED` |
| `$7BB8` | `ALL COOLING RODS INSERTED / REACTOR SUCCESSFULLY CLOSED DOWN` |
| `$7D04` | `CONGRATULATIONS / TAU CETI III IS NOW NEUTRALISED ...` |
| `$6C9B` | `Save aborted` |
| `$6A31` | `Load Error` |
| `$6503` | `PRESS 3 TO TRY ANOTHER MISSION` |
| `$6529` | `DEMO MODE Initiated` |
| `$653F` | `Press SPACE to exit.` |

Two of those are worth a second look because they are **self-modifying**. `$742A` is a byte inside the
"ROD SECTION" message, written by the routine that has just counted how many rods it placed, so the
number in the sentence is not a formatted field - it is the string being edited. `$7B93` on the
reactor screen works the same way: `$7BA4` and `$7BA5` are the tens and units digits, rewritten in
place before the message is queued. Any tool that treats these addresses as read-only text will print
whatever the last visit left in them.

> [!NOTE]
> **What this corrects.** An earlier version of this chapter proposed a 512-byte lookup table at
> `$8412-$85FF` and a list of decoded strings at file offsets like `$1CDE0`. Neither exists: `$8412` is
> ordinary game data, and the strings sit inline in the code at the addresses above because there is no
> character mode to feed. The same version described bit 6 as "a flag rather than part of the letter";
> in fact bit 6 is the page selector, and the reason `$52` and `$32` both appear in neighbouring
> strings is that `$52` is `r`, not a flagged `R`. The encoding table itself was right, and it is the
> part that survived.

---

[Back to the overview](../README.md)
