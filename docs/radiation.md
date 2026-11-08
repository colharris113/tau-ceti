# The Radiation Clock

The dose counter in the reactor room: the gauge you watch, the three warnings in the border, and
the two and a half minutes you have.

---

The reactor room at Centralis is the one place in Tau Ceti where standing still kills you. Not the
robots, not the defences, not the fuel: the room itself, on a timer that starts the moment the screen
opens and that nothing you can do inside it will stop.

## Going in

The room has one door and one condition. `$770B` refuses to open it unless `$03A4` holds `$1C`, the
Central reactor, and says so in as many words: the reactor room is only available at Centralis. When
the condition is met, before anything is drawn, `$771C` queues the string at `$7A0E` through the
message queue at `$4127`, and `$7723` then waits for the log to drain, so the text is on the screen
before the room is:

```
WARNING: YOU ARE
ENTERING A HIGHLY
RADIOACTIVE AREA.
```

`$80` in that string is the line break, `$0A` is the font's full stop and `$FF` ends it. This is the
whole of the game's explicit warning, and the only text you are given until it is far too late. The
room does not repeat it, does not count anything down on the screen in numerals, and does not beep.

## The counter

`$03BE` is the dose, one byte. `$790E` increments it, but not every frame. The reactor screen's own
loop is at `$785B`: it calls `$5DAA` for input, which waits a frame (`$5FAC` reads `$11` and compares
it with itself until it changes), so the loop turns over once per frame. The increment sits behind a
test of `$11 & $7F` at `$7908`, so it fires on one frame in 128. On a PAL machine that is one tick
every **2.56 seconds**.

`$11` is the game's frame counter, incremented at `$25D3` out of the stage-2 raster handler (`$49FD`,
and its twin in the other display mode at `$4A39`/`$4A44`). It is incremented *before* the mission
clock at `$03AF` is tested, so the drum beats whether or not the mission clock is running.

Only four places in the image touch `$03BE`: `$57BA` zeroes it, `$790E` increments it, `$7911` tests
it, and `$7CB6` reads it to draw. Nothing subtracts from it, nothing else writes it, and there is no
cure, syringe or safe room anywhere in the game.

## What you actually see

Not a number. `$7CB4` draws the reading, and it is called from `$7955` on the 32-frame tick, so the
picture refreshes about one and a half times a second while the number underneath changes about once
every two and a half.

`$7CB4` calls `$7CC3` twice, and each call is one vertical ribbon:

| call | value | starts at | meaning |
|---|---|---|---|
| `$7CB6` | `$03BE` | `$EBB0` | your dose |
| `$7CBE` | `$26` | `$EBC0` | the reactor's remaining output |

`$7CC3` takes its pick from the two bytes at `$EBB0` and `$EBC0` — sixteen bytes apart, two character
cells — and walks *up* the bitmap a scanline at a time, one byte of a cell per scanline, 62 scanlines
in all. Each scanline is masked to leave only the leftmost multicolour pixel of the byte, so the
ribbon is one multicolour pixel wide, two screen pixels, and sixty-two pixels tall. For the first *n*
scanlines from the bottom the pixel is set to `%10` of the cell byte; above that, to `%11`. The
boundary is the value.

The cells behind the ribbons are tinted at `$77C4`: `$2D` is written to columns 14 and 16 of rows 2
to 9, which is exactly the eight-row span the ribbon walks. So `%10` is colour `$D`, light green, and
`%11` is colour `$2`, red. **The dose fills the left-hand ribbon from the bottom up in green, with
the red above it giving way**; the ribbon is 62 scanlines and the fatal dose is 61, so the tube is
never quite full when the mission ends. One thin line of red stays at the top.

The right-hand ribbon is the reactor. `$26` starts at zero at `$77E0` and is then pulled one unit at
a time towards three times the bars still to fit — `$78EF` computes `3 * ($14 - $03A9)` and creeps
`$26` toward it on the same 32-frame tick, 0.64 seconds a unit. With nothing inserted that is a
target of 60, reached in about 38 seconds; every bar you insert drops the target by three and the
ribbon visibly falls. The screen is therefore a race between two columns: yours climbing on the
left, the reactor's output falling on the right.

**The twenty-one rectangles are not the meter.** The screen's set-up loop at `$7732` runs `$7C06`
twenty-one times, and an earlier reading took that for a bar graph. `$7C06` reads its rectangles from
the hit table at `$72B2` and draws twenty rod slots plus the insert box — it is the grid you are
filling, not a gauge. The only dose display in the room is the thin ribbon at `$EBB0`.

## The three warnings

All three are silent. `$413B` is not the sound engine; it is the queue at `$0C80` that feeds the
border banner, four bytes per entry: a string pointer and a flag. The low seven bits of the flag
become the ticker's scroll step at `$0378`/`$0397`, which normally holds 2. So each threshold hands
the banner a new line and a new speed.

| dose | reaches it at | string | colour | step |
|---|---|---|---|---|
| `$28` = 40 | 1:42 | `$7A45` | 1, white | 2 |
| `$34` = 52 | 2:13 | `$7A9C` | 7, yellow | 4 |
| `$39` = 57 | 2:26 | `$7AE7` | 10, light red | 8 |

The strings themselves, stored in the ticker's four-byte groups of one colour byte and three
characters, read:

```
RADIATION DOSE NOW APPROACHING GAL-CORP RECOMMENDED MAXIMUM.
WARNING: RADIATION NOW EXCEEDS THE MAXIMUM SAFE DOSE.
DANGER   CRITICAL RADIATION LEVEL   LEAVE THE REACTOR CHAMBER IMMEDIATELY
```

So the escalation is not in the wording only. At step 2 the text advances a pixel a frame, one
character every eight frames, which is the pace the story paragraphs scroll at: the first warning is
a normal message, and you have to read it. At step 4 it crosses twice as fast; at step 8, four times,
one character every two frames. The last warning is a flash rather than a sentence — by then the game
has stopped trying to be polite.

Each string ends with `$FF` and a two-byte pointer, and all three point at `$35EF`, which is the
four-blank string at the head of the ticker routine and points at itself. A warning plays once, the
banner falls idle, and the queue hands it the next one when it arrives. The gaps work out: at these
lengths and speeds the first warning takes about nine seconds to pass, the second about four and the
third about three, and the thresholds are thirty-one, thirteen and ten seconds apart — so each one
finishes scrolling before the next arrives.

## The death

`$793F`, on the tick that carries `$03BE` to `$3D` = 61:

- pushes `$7B5E` into the message log, which prints as

  ```
  FATAL RADIOACTIVE
  DOSE RECEIVED.
  MISSION FAILED.
  ```

- pushes `$35EF` at step 8, which blanks whatever is left of the banner;
- and jumps to `$6473`.

`$6473` is the shared mission-failed sequence, the same one QUIT uses. It queues `$6503` — two blank
lines and `PRESS 3 TO TRY ANOTHER MISSION` — sets `$03AF` to `$FF` so the mission clock stops,
waits for the log to drain, then polls keys `$3C` and `$3F` fifty frames apart, twenty times over
(`$68` = `$14`, `$67` = `$32`). Press 3 and you get a new mission; let the countdown run out and the
game falls through to the attract mode's `DEMO MODE Initiated` instead.

Nothing in that path queues a sound effect, and the radiation code never writes the effect slots at
`$03C4`/`$03C5`. Death in the reactor is silent apart from whatever the room was already playing.

## What resets it

One routine, and the important part is where it is not called from. `$5766` resets the flight
variables, and `$57BA` inside it is the write that clears the dose. `$5766` is called from exactly
two places in the image: `$2009`, the boot, and `$64F0`, the tail of the mission-failed sequence
before a new mission starts.

There is no landing code that touches `$03BE`. **The dose is per mission, not per landing.** Taking
off, flying to another city, doing something useful and coming back does not clear it: sixty ticks
spent in the room, an hour elsewhere, and one more tick is a dead mission. The only two ways to see
the counter at zero again are to die and start over or to begin a new mission.

> [!NOTE]
> **What this corrects.** Earlier notes in the port, and a paragraph in
> [World and Cities](world-and-cities.md), had the dose reset at every landing, credited the three
> thresholds with playing sounds at `$7A45`/`$7A9C`/`$7AE7`, and read the twenty-one passes at
> `$7732` as a bar graph. None of the three holds. `$57A2`-`$57BA` is the new-mission reset, reached
> from `$64F0` and from boot and from nowhere else; `$7A45` and its neighbours are border-banner
> strings queued through the four-byte queue at `$0C80`, whose flag byte is a scroll step; and
> `$7732` is the set-up for the rod grid.

## How long you have

| dose | event | ticks | frames | time |
|---|---|---|---|---|
| 0 | the room opens | 0 | 0 | 0:00 |
| `$28` = 40 | white warning, banner at normal speed | 40 | 5,120 | 1:42 |
| `$34` = 52 | yellow warning, twice speed | 52 | 6,656 | 2:13 |
| `$39` = 57 | light red warning, four times speed | 57 | 7,296 | 2:26 |
| `$3D` = 61 | mission failed | 61 | 7,808 | 2:36 |

Frames are ticks times 128; the times assume 50 Hz. On an NTSC machine at 60 Hz the same counts run
about a fifth quicker — two minutes and ten seconds to the end — which is why the allowance is worth
quoting in ticks as well as in seconds.

The shape of it matters more than the total. The first warning arrives a third of the way in and the
gauge has barely started; two of the three warnings, and the whole final rush, are inside the last
thirty seconds. A player who walks in, works steadily and does not think about the clock will hear
nothing for a minute and a half, then be told three times in a minute that it is time to leave.

## Where else it applies

`$03BE` is the reactor room's own variable and nothing on the flight side reads it. The increment is
inside the loop at `$785B`, which only exists while the reactor screen is up, so the radiation is a
hazard of that room and of nothing else: no dose accrues while you fly, while you dock, or while you
stand outside the building at Centralis. There is no "near the reactor" exposure to model, and a port
that adds one would be inventing a mechanic.

What a port does have to carry is the pacing and the reset rule: 128 frames per tick, death at 61,
zeroed only at the start of a mission.

## What is still open

- **The look of the ribbons off the machine.** The geometry in `$7CC3` is exact — 62 scanlines, one
  multicolour pixel wide, green under red, filled from the bottom — but I have described it from the
  code and not from a captured frame. Whether two pixels read on screen as a filling tube or as a
  thin line, and how the ribbon sits against the room's artwork, is not established here.
- **Why the columns are where they are.** `$EBB0` and `$EBC0` fix them to columns 14 and 16 of rows 2
  to 9, and `$77C4` tints exactly those cells, but nothing in the code says what the picture around
  them is meant to be.
- **The meaning of `$26`.** That it is `3 * (20 - bars inserted)` is arithmetic; that it is best read
  as the reactor's output, and that the "EFFICIENCY" figure in the message at `$7B93` is half of it,
  is inference from the numbers, not a statement the game makes.
- **Whether the timer ever pauses.** The gate is the frame counter, and the frame counter is
  incremented from the raster handler before any state test, so I have assumed nothing pauses it.
  No pause facility is documented for the game, and none turned up in the path.

---

[Back to the overview](../README.md)
