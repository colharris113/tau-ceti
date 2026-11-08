# Easter Eggs and Hidden Messages

What is in there, what is claimed, and which of the two this chapter can prove.

---

Tau Ceti has a reputation for hidden content: a lockout if you swear at the board computer, an
"insult me" reply, and a handful of messages that most players never see. Some of that is real and
some of it is folklore. This chapter lists the messages that are demonstrably in the image, and is
explicit about the ones that are only reported.

## Messages that are in the image

| Address | Text | When |
|---|---|---|
| $6529 | `DEMO MODE Initiated` | the attract mode starts |
| $653F | `Press SPACE to exit.` | during the demo |
| $6555 | `     DEMO MODE` | printed when the demo restarts |
| $6503 | `PRESS 3 TO TRY ANOTHER MISSION` | after a mission ends |
| $5E6A | `SKIMMER REFUELED` | at the end of a refuel |
| $6001 | `NOT AVAILABLE HERE` | a command used at the wrong place |
| $6015 | `SKIMMER ISN'T DOCKED` | a command that needs a docked ship |
| $3C3D | `FLARE ACTIVATED` | firing a flare |
| $3C95 | `AMM DETONATED` | firing an AMM |
| $5252 | `Where would I get / some round here!!` | the COKE command |

The demo messages are the best-hidden of these: you only see them if you lose or finish a mission
and then leave the machine alone for twenty seconds. See [The Attract Sequence](demo-mode.md).

## The bad language filter

The story is that typing certain words at the board computer produces a message about sterility and
brain damage, and then locks you out of the game permanently. It is a well-attested feature and it is
the reason this chapter exists.

Part of it is now located, and it is not a filter. The parser's name table at `$4BAC` holds
**twenty-five** commands, and four of them are the words in the rumour: FUCK, PISS OFF, CUNT and
BASTARD, entries 20-23, all sharing one handler at `$602A`. COKE is entry 24 and gets two lines of
text at `$5252` and `$5277` - a joke about the drink being illegal since it was proved to cause
sterility. So the swearing is a **command**, typed in full and answered deliberately, not a filter
that catches it in passing.

What is not established is the "lockout": `$602A` paints a screen rather than pushing a message, and
what it paints has not been read. If there is a permanent lockout, it is behind that handler. The
earlier version of this chapter gave an exact file offset (`$1D70B`) for a word list and a second
(`$1F195`) for an "insult me" reply; neither address holds either, and the words were in the command
table all along.

## What is definitely not there

The old version of this chapter also described:

- **A sprite-based flashing-light system** with a table of $D011 values ($3B, $2B, $34, $37) and a
  list of which sprites each value enables. $D011 is not the sprite enable register - $D015 is, and
  the handlers above the picture write zero to it every frame. The only sprites are the eight in the
  bottom border and the sight marker in the view, and neither is a flashing light.
- **Colour RAM animation at $DC00 and $DC0D.** Those are the CIA ports, not colour RAM, and writes
  of $7F to them are keyboard and joystick scans.
- **A score table.** There is no table of scoring events, but there is a score: four counters at
  `$03A5-$03A9` multiplied by fixed constants and printed in decimal by SCORE at `$5AA3`. See
  [Game State](game-state.md).

## Victory

The mission ends when the reactor at Centralis is shut down: forty halves assembled into twenty bars,
twenty bars inserted. The test is at **$7973** and it runs on your way *out* of the reactor, not when
you fill the last slot - `$03A9` against `$14`. Filling the last slot only prints "ALL COOLING RODS
INSERTED"; walking out is what prints the congratulations at `$7D04` and starts the zoom-out of the
star map. The completion message and the code that tests for it are both in the image now, and the
count is the code's rather than the manual's.

---

[Back to the overview](../README.md)
