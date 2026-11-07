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
| $6528 | `DEMO MODE INITIATED` | the attract mode starts |
| $653E | `PRESS 3 TO EXIT` | during the demo |
| $6555 | `     DEMO MODE` | printed when the demo restarts |
| $6503 | `PRESS 3 TO TRY ANOTHER MISSION` | after a mission ends |
| $5E6A | `SKIMMER REFUELED` | at the end of a refuel |
| $6001 | `NOT AVAILABLE HERE` | a command used at the wrong place |
| $6015 | `SKIMMER ISN'T DOCKED` | a command that needs a docked ship |
| $3C3D | `FLARE ACTIVATED` | firing a flare |
| $3C95 | `AMM DETONATED` | firing an AMM |

The demo messages are the best-hidden of these: you only see them if you lose or finish a mission
and then leave the machine alone for twenty seconds. See [The Demo](demo-mode.md).

## The bad language filter

The story is that typing certain words at the board computer produces a message about sterility and
brain damage, and then locks you out of the game permanently. It is a well-attested feature and it
is the reason this chapter exists.

What I can say about the code is less satisfying: I have not located the filter. There is no
forbidden-word table in the data I have read, and the message text the story quotes is not in the
image at any address I have found. The earlier version of this chapter gave an exact file offset
($1D70B) for the word list and a second one ($1F195) for an "insult me" reply; both addresses are
inside the game's code area, and neither holds a word list or a reply.

So: the behaviour is probably real, the addresses that used to be printed here were not. If you want
to find it, the place to start is the keyboard handler that feeds the board computer, not the text
tables.

## What is definitely not there

The old version of this chapter also described:

- **A sprite-based flashing-light system** with a table of $D011 values ($3B, $2B, $34, $37) and a
  list of which sprites each value enables. There are no sprites in this game, and $D011 is not the
  sprite enable register - $D015 is, and the game writes zero to it every frame.
- **Colour RAM animation at $DC00 and $DC0D.** Those are the CIA ports, not colour RAM, and writes
  of $7F to them are keyboard and joystick scans.
- **A score system.** No score variable or scoring table has been found.

## Victory

The mission ends when the reactor at Centralis is shut down - 40 rod parts assembled into 20 bars
and inserted. The completion message is in the game, but I have not located the code that tests for
it, so the count that ends the mission is taken from the manual rather than from the binary.

---

[Back to the overview](../README.md)
