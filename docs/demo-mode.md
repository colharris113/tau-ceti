# The Demo

The attract mode: what it is, how it gets started, what it flies and what stops it.

---

The status line at the top of the flight screen has four possible readings. Three of them describe
where you are - LAUNCHED, LANDED, DOCKED - and the fourth is DEMO. That fourth one is not a menu
label or a leftover: Tau Ceti has a working attract mode that flies the ship for you, and if you
leave the game alone after a mission ends, this is what you get.

## The status line itself

The line is written by the routine at $4906, which picks one of four eight-character entries from
a table at $4931 and blits it into the screen at row 3, starting at column $1E. The table is stored
in the same glyph encoding as every other string in the game, so each letter is its index plus $20:

| Entry | Address | Reads as | When |
|---|---|---|---|
| 0 | $4931 | `DEMO    ` | demo flag set |
| 1 | $4939 | `LAUNCHED` | flying |
| 2 | $4941 | `LANDED  ` | on the ground |
| 3 | $4949 | `DOCKED  ` | at a building |

Which entry is used is decided by two variables before the glyphs are copied. $0394 is the demo
flag: if it is non-zero, the line reads DEMO and nothing else is considered. Otherwise $0396 picks
between the flight states - zero is LAUNCHED, one is LANDED, and anything else is DOCKED.

That single test is why the demo is easy to miss: it is the only place the flag is displayed, and
it is displayed in eight characters at the top of the screen.

## How the demo starts

It does not start at boot. The path runs through the end of a mission: the mission-over routine at
$4D60 sets up its messages and jumps to $6473, which prints `PRESS 3 TO TRY ANOTHER MISSION` and
begins to wait.

The wait is a nested counter - 20 outer passes of 50 inner passes, 1000 frames, about twenty
seconds at the C64's frame rate. Each pass samples two keys and, if either is down, leaves the loop
with the demo flag clear, so pressing a key gets you a new game straight away. If the counters run
out first, the game prints `DEMO MODE INITIATED`, waits for a raster frame, and falls into the same
restart path with $0394 set to $80.

So the demo is the game's answer to an idle player: not a separate program, but the ordinary game
started again with a flag set.

## What it flies

This is the interesting part, and it is much simpler than an autopilot would be.

Every frame the game reads the joystick in a routine at $26FA. Its first instruction loads $0394
and branches on the top bit: in normal play it goes on to read the hardware ports, and in demo mode
it jumps to $6392 instead.

$6392 is not a flight controller. It is a *tape player*. Two tables hold the recording: a list of
hold counts at $9300 and a list of joystick actions at $BD00, both indexed by a byte counter at
$03B1, with a countdown at $03BB pacing the playback. Each entry in the action table is a bit
mask, and the routine translates it into the same eight shadow bytes at $034A that the real
joystick handler writes - bits 0-2 pick which of the eight bits, bits 3-5 pick which byte, and bit
6 says whether the bit is pressed or released.

The consequence is worth stating plainly: the demo has no special flying code at all. The ship in
the attract mode is flown by exactly the flight model you fly, driven by a recording of somebody
pressing and releasing buttons. Everything the demo appears to decide - turning, climbing, firing -
is the ordinary game responding to input that happens to come from a table instead of a port.

The tables are 256 entries long, and the index is a single byte, so the recording is finite: while
it plays, the counter at $03BB divides the frame count so that one entry lasts as long as its hold
count says.

## What it flies over

Nothing in the demo path chooses a city. The restart it uses is the same one a new game uses:
$64F0 calls $5766 to reset the flight variables, calls $280B to rebuild the 48 sixteen-byte object
records that make up the world, and jumps into the frame loop at $4D7D. $280B takes its object
list from the city number at $0354.

Since the demo is entered from the end of a mission and nothing in that path writes a new city
number, the demo flies the city the finished mission ended in.

## How it ends

Two ways.

If the recording runs out, the index wraps and the code sets a flag at $03BA. The frame loop sees
it, and $645A prints `DEMO MODE` and `PRESS 3 TO EXIT`, resets the script counters and restarts
the flight. So an untouched machine loops the demo indefinitely.

If you press a key, the input routine at $6392 notices and stores $FF in $0394 - a request rather
than a state. On the next pass through the main loop, $207A tests for exactly that value, clears
the flag, restores the key map from the copy at $03EF with the routine at $6403, and jumps to
$64F0 to start a real game. The demo hands over by starting over.

> [!NOTE]
> The test at $6392 is narrower than "any key". It selects keyboard row 7 with $DC00 = $7F and
> accepts either bit in mask $90, which on the C64 matrix is SPACE (bit 4) and RUN/STOP (bit 7).
> The message on screen says `PRESS 3 TO EXIT`, so the prompt and the actual test disagree - worth
> knowing if you are trying to get out of the demo and the obvious key does nothing.

---

[Back to the overview](../README.md)
