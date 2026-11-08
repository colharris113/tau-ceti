# Game State

Where the game keeps its variables, and what the flight model actually does with them.

---

The flight state does not live in the zero page. Almost everything that matters to the ship - its
height, its speed, its fuel, its ammunition - sits in page 3, at absolute addresses in the
$0330-$03FF range, and the zero page is used for pointers and scratch. That is the first correction
this chapter has to make: the old version printed a tidy zero-page table from $00 to $1A, and none
of those variables exist where it said they did.

## The variables that matter

| Address | Meaning | Evidence |
|---|---|---|
| $0344 | height | raised and lowered with two keys at $3A14-$3A3D, capped at $BF |
| $0346 | fuel | refuelling loop at $5E4D fills it to $BF then prints `SKIMMER REFUELED` |
| $0347 | a gauge that decays | decremented once every other frame at $34EC |
| $0352 | turn | adjusted between $E1 and $1F, so it is a signed heading offset |
| $0353 | speed - and the SID voice 2 pitch, which is the same byte |
| $0355/$0357/$0358 | flares / AMM / missiles | see [Flares, Missiles and AMM](weapons.md) |
| $0356 | flare timer | counts down once per sixteen frames at $25EA |
| $0365-$0367 | weapon cooldowns | cleared by the start-up wipe at $56D8 |
| $0377 | a gauge that fills to $BF | filled by the loop at $5E7C |
| $0394 | attract flag | `$00` playing, `$80` attract, `$FF` leave attract |
| $0395 | pause | set while a handler waits for a key |
| $0396 | flight state | 0 launched, 1 landed, `$80` docked |
| $039D | display mode | ORed into the raster dispatch index |
| $034A-$0351 | input shadow bytes | written by the input code, read by the flight model |

One of those is worth a second line because it explains two things at once. `$0353` is not just the
speed: `$86F8` shifts it left three times and writes the result to the SID's voice 2 frequency, so the
number that drives the fifth gauge is the number you hear as engine noise. Gauge 5 and the engine are
the same variable read by two different pieces of hardware.

Two of the five gauges on the panel are still unidentified. $0346 is fuel and $0344 is height, and
$0353 clearly behaves like speed, but $0347 and $0377 are only known by their behaviour - one
decays slowly, the other fills to the top and then clears a set of timers. They are probably
shields, hull or laser temperature, and the honest answer is that I have not proven which.

## The flight model

The controls are simple and the model is smaller than it looks.

**Throttle.** $3968 checks the up control against a joystick bit and a key map entry. If either is
active, the speed at $0353 is incremented, to a ceiling of $BF. The down control decrements it,
floored at zero. There is no acceleration curve to the input itself: press up, speed rises.

**Turning.** $0352 is adjusted in the same routine, between limits of $E1 and $1F. The asymmetry is
deliberate - $E1 is -31 and $1F is +31, so the value is a signed turn rate that saturates at about
thirty either way.

**Landing.** At $3BEB the code checks two things: speed is zero, and height is zero. When both are
true it writes 1 to $0396, which is the value the status line reads as LANDED. That is the whole
landing test - no attitude, no vertical speed, just "stopped and on the ground".

**Height and speed interact.** At $381A, if height is zero and speed is not, the code takes two off
the speed and starts a short timer. The skimmer is being dragged down by contact: height has to come
first, and a moving ship on the deck loses speed until it stops.

**Fuel** is not burned by flying. It is filled by a loop at $5E4D that increments $0346 until it
reaches $BF and then prints `SKIMMER REFUELED` - which is a station routine, not a flight one.

## The gauges

The five bar gauges in the instrument panel are all drawn by one routine, $3769, called five times
with a different value and a different destination:

| Bar | Bitmap offset | Variable |
|---|---|---|
| 1 | $F8A0 | $0344 |
| 2 | $F9E0 | $0377 |
| 3 | $FB20 | $0346 (+3 before scaling) |
| 4 | $FC60 | $0347 |
| 5 | $FDA0 | $0353 (+3 before scaling) |

Each value is shifted right twice, capped at $2D, and then turned into a bar width: widths 0-8 come
from a ramp table at $379F (`00 80 C0 E0 F0 F8 FC FE FF`) and anything wider is a solid byte of
$FF. The routine writes four bytes per row for six rows, stepping nine bytes per row, which is why
the bars are short four-byte-wide strips in the bitmap rather than long lines.

The two bars with +3 added before scaling are the two that floor at zero in gameplay - fuel and
speed - so the offset is there to keep their minimum visible.

## Mission progress

The mission counters are in the block after all, and there are three of them plus a dose clock:

| Address | Meaning | Range |
|---|---|---|
| `$03A7` | rod halves on the surface, world total | 0-40 |
| `$03A8` | halves solved into bars | 0-20 |
| `$03A9` | bars inserted in the reactor | 0-20 |
| `$03BE` | radiation dose, while in the reactor room | 0-61 |

All three rod counters are zeroed in the new-game tail (`$57B1-$57B7`), and the win is `$7973`
testing `$03A9` against 20 on your way out of the reactor - not on filling the last slot. The dose
clock is the one countdown that kills you: incremented once per 128 frames while you are in the
reactor, fatal at 61.

There is a score, too, but it is not what the old chapter meant by one. `$03A5/$03A6` is a 16-bit
count of destroyed objects whose class byte carries bit 6, and SCORE at `$5AA3` prints four
multiplied fields - robots killed x5, parts found x75, bars assembled x250, bars inserted x500 - in
decimal through `SED`. The points table is real, and it is four constants rather than a list of
scoring events.

The manual's other rules - 40 parts, 20 bars - are correct, but "8 per reactor" is not a rule the
code has: a city drops zero, one, two or three halves according to the table at `$7440`, and the
world total is capped at 40. [World and Cities](world-and-cities.md) has the chain and
[The Rod Puzzle](rod-puzzle.md) has the pairing rule.

> [!WARNING]
> Two things in the old version of this chapter were wrong rather than merely unfound. The state is
> not in the zero page, and there is no physics model with per-frame acceleration and an inertia
> term - the throttle is a clamped increment, and the only "inertia" in the flight code is the
> speed loss when the skimmer is on the ground.

---

[Back to the overview](../README.md)
