# Board Computer

The text console, the messages it prints, and the equipment panel.

---

The board computer is the interface you use when you are not flying. Its visible behaviour is well
documented in the manual; its *code* is the part of the game I have explored least, so this chapter
is deliberately shorter than the one it replaces. What follows is what the disassembly supports, and
the rest is marked as unexamined rather than guessed at.

## Messages are queued, not printed

The most useful thing to understand about the console is that nothing draws itself. When the game
wants to say something, it calls $4127 with a pointer to a string, and the routine appends the two
address bytes to a ring buffer at $0C00. A second queue at $0C80, filled by $413B, takes four-byte
entries.

The raster side drains those queues: the interpreter at $41F7 walks the entries, prints them with
the glyph blitter and scrolls the log with the row copies at $40E4. The frame routine at $4D80 waits
for the queues to empty before it ends the frame - the wait at $6444 compares the read and write
pointers at $0383 and $0384 and spins until they match.

That design has one visible consequence: messages appear in the order they were queued, and a burst
of them can hold the frame up. It is why the message log is the last thing to settle when several
events fire at once.

## Known messages

| Address | Text |
|---|---|
| $6503 | `PRESS 3 TO TRY ANOTHER MISSION` |
| $6528 | `DEMO MODE INITIATED` |
| $653E | `PRESS 3 TO EXIT` |
| $6555 | `     DEMO MODE` |
| $6001 | `NOT AVAILABLE HERE` |
| $6015 | `SKIMMER ISN'T DOCKED` |
| $5E6A | `SKIMMER REFUELED` |
| $3C4E | `NO FLARES LEFT` |
| $3C5E | `NO MISSILES LEFT` |
| $3CA4 | `NO AMMS AVAILABLE` |

The strings sit inline in the code, in the glyph encoding described in
[Character Set and Text System](charset.md).

## The equipment panel

The one command interior I have disassembled is the equipment/install panel at $5DAA. It is a small
form with two adjustable quantities and a toggle:

| Variable | Range | Adjusted by |
|---|---|---|
| $03AB | 14 to 118 | the left/right controls, at $5DBC and $5DD5 |
| $03AC | 12 to 120 | the up/down controls, at $5DEE and $5E07 |
| $03AE | 0 or $FF | a separate key at $5E11, toggled each press |

The panel is drawn by $5D82, which computes a destination in the video matrix at $CC29 and stamps
sixteen bytes - a two-cell-wide block - which is how the panel's fields are painted without using
the glyph blitter.

The two numbers are almost certainly quantities of equipment, but the code at $5DAA only adjusts and
displays them; the routine that takes the money, or that turns them into missiles, is elsewhere and
I have not traced it. The `INSTALL FLARES`, `INSTALL MISSILES` and `INSTALL AMM` strings at
$5FD1-$5FFF belong to this panel.

## What is not established

Three things the old version of this chapter described in detail, and which I have not verified:

- **The command list.** Commands such as MAP, LOOK, RODS, REACTOR and KEYS do appear in the manual,
  and RODS/REACTOR appear in the game's text, but there is no dispatch table at $1B900 and no
  per-command handler offsets. The table in the old chapter was invented wholesale.
- **The PAD text editor.** No storage layout at $F000-$F7FF has been found; that page is not used
  as a note buffer as far as I can see.
- **Save and load.** No save-game format has been identified. The "magic number" and the field list
  in the old chapter were fabricated.

If you want to work on this area, the message queue is the right entry point: every command that
prints something goes through $4127, so tracing calls to it from the keyboard handler would find the
parser quickly.

---

[Back to the overview](../README.md)
