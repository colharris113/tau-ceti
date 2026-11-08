# The Rod Puzzle

Forty half-rods, three buttons, and a deal that is unsolvable until you find the one that looks like a
rotation and is not.

---

The mission is stated in the manual in one line: collect cooling rod parts, assemble them into bars,
shut down the reactor. What the manual does not say is that the parts are a puzzle, that the puzzle
has three operations rather than two, and that the deal you are given at the start of a new game has
been arranged so that no pair fits at all as it lies on the tray.

That last part sounds like a bug. It is not: it is the design. This chapter is the machine's rule,
measured rather than inferred, because the same numbers are what a port needs to reproduce the game
and what a player needs to stop believing the game is broken.

## A rod is ten bits and two attributes

The tray is not per-city and not on the disk. Forty half-rods live in two bytes each in one global
table at **$02B0**, at `$02B0 + 2*i` for `i` = 0 to 39, and the table is generated once per game by
the routine at **$7319**:

```text
$02B0 + 2i   bit 7        handedness ("flipped")
             bits 6,5,4   the class, 0..7
             bits 3,2     always zero: the generator masks with $73
             bits 1,0     the top two bits of a ten-bit profile
$02B1 + 2i   bits 7..0    the low eight bits of that profile
```

So a half-rod is a **ten-bit profile** (`(b0 & 3):b1`) plus a hand bit and a three-bit class. The
grid you work on holds indices, not rods: `$BC50` is one byte per cell holding `0..39`, or `$FF` for
empty. Cell 0 is the hand, cells `$07` to `$2E` are the working area, and a solved pair consumes both
of its cells and increments the counter at `$03A8`.

The drawing code at `$7101` uses bits 1, 0 and bit 7 to pick one of eight four-byte row masks from
`$717B`, then shifts the ten-bit profile two bits per row to build a twenty-row glyph. The class bits
are read by **nothing except the fit test** - they do not change what a rod looks like, only whether
it joins.

## The three buttons

| Box | Handler | Code | What it does |
|---|---|---|---|
| 5 | `$6F8E` ROTATE | `$02B0 ^= $40` | toggles the top class bit, `c -> c ^ 4` |
| 4 | `$6FA6` FLIP | `$02B0 ^= $80` | toggles the hand bit |
| 3 | `$6FDE` ROLL | `$6FF1` | replaces the profile with its end-for-end reverse |

The box numbers are not in address order, which is worth knowing before writing a menu: the dispatch
words at `$6F04` run `$6F13, $6F3E, $6F6D, $6FDD, $6FA5, $6F8D, $6FBD, $6FCD`, so ROLL is box 3 and
ROTATE is box 5. They are stored as `handler-1` and the `PHA/PHA/RTS` at `$6DBD` adds the one back.

`$6FF1` is the interesting one, because of what it is not. It shifts the ten-bit pattern right two
positions, five times, emitting each pair as `(bit, bit ^ other bit)` into a sixteen-bit accumulator;
the low byte goes to `$02B1` and the low two bits of the high byte to bits 1, 0 of `$02B0`, which
leaves the class and the hand bit untouched. **That is an involution, not a rotation**: two presses
are the identity. Checked over all 16,384 combinations of the two bytes - ten profile bits, three
class bits, one hand bit - with zero exceptions and 512 fixed points. A rod therefore has a binary
choice in ROLL - the profile or its reverse - not five rotational states.

Because the three operations touch disjoint bits, they commute, and a rod's whole reachable set is
`2 (roll) x 2 (rotate) x 2 (flip) = 8` states. All three act on the same rod: `$7034` picks the rod
in the hand if the hand is occupied, otherwise the rod under the cursor at `$03BC`, otherwise
nothing.

## Three conditions, tested in this order

The fit test is **$6E1A**. It is entered with the cursor cell in `X`, and it compares the rod in the
hand with the rod under the cursor:

```text
$6E26  $02B1[hand] ^ $02B1[rod]                 CMP #$55   must be equal
$6E3A  ($02B0[hand] ^ $02B0[rod]) & $83         CMP #$81   must be equal
$6E46  ($02B0[hand] >> 4) & 7  -> $7173[] -> $68
$6E55  ($02B0[rod]  >> 4) & 7  -> $7173[]       CMP $68    must be equal
```

In words:

1. **the two profiles are exact ten-bit complements.** `$02B1` XOR `$55`, plus bit 1 equal and bit 0
   different in `$02B0`, is precisely "every bit of one profile is the other's opposite" - `$55` and
   the `1` in `$83`/`$81` are one constant, `$155`, seen in two pieces.
2. **the hand bits differ.** Bit 7 is in `$83`; the comparison wants `$81`, so exactly one of the two
   halves is flipped.
3. **the classes agree through the table at `$7173`**, not directly.

All three failures jump to the same place, `$6E30`, which pushes `$6EB1`. That string is
`80 30 41 52 54 53 20 44 4F 20 4E 4F 54 20 4D 41 54 43 48 0A FF`, which in the encoding described
in [Character Set and Text System](charset.md) reads **"Parts do not match."** The leading `$80` is
the line break; an earlier reading that started one byte later produced "ARTS DO NOT MATCH". Success
pushes `$6EC6`, "Cooling Rods Solved".

## The table that folds eight classes into four

`$7173` is eight entries: `06 05 02 09 02 09 05 06`. It is palindromic - `t[c] == t[c ^ 7]` - and it
holds four distinct values, so it folds the eight class codes into four labels:

```text
label      6     5     2     9
members   0,7   1,6   2,5   3,4
```

ROTATE (`c ^ 4`) always moves a rod to a *different* label, so a rod's reachable labels are the pair

```text
family(c) = { t[c], t[c ^ 4] }
c in {0,7} -> {6,2}     c in {1,6} -> {5,9}
c in {2,5} -> {2,5}     c in {3,4} -> {6,9}
```

Four of the six family pairings meet: `{6,2}` with `{2,5}` at 2, `{6,2}` with `{6,9}` at 6, `{5,9}`
with `{2,5}` at 5, `{5,9}` with `{6,9}` at 9. Two never meet: `{6,2}` against `{5,9}`, and `{2,5}`
against `{6,9}`. So **rotation rescues a class mismatch two times in three**; the other third has to
be paired with a different half entirely. That single asymmetry is the one real constraint in the
puzzle, and it is why the correct pairing of the tray is not simply the deal's own pairs.

## The deal

`$7319` is called once, from `$5860` in the new-game tail. It builds twenty designed pairs and then
shuffles them:

```text
$7319  clear bit 7 of $7440[0..31]           no city stripped yet
$7326  X = 0, 4, 8, ... $4C                  two rods per pass
$7328    A = RND($330E) -> $02B1[X]
$732E    A ^ $55        -> $02B3[X]          the partner's profile
$7333    A = RND & $73  -> $02B0[X]          class + low bits
$733B    bit0 ^ 1, bit1 kept -> $02B2[X]
$734B    A = RND & $F0, retried until (A & $30) != (b0 & $30) ^ $10
$735B    $02B2[X] = (A & $70) | low2
$7364    if A bit 7: ROLL rod X+2            about half of the second halves
$7378  shuffle: 40 times, swap two whole 2-byte rods at random
$73A7  $BC50 = $FF, $03BC = $FF, $03A7 = 0, $03DB-$03EE = 0
```

Two facts fall out of that listing and they decide the whole puzzle.

**Every rod is dealt with bit 7 clear.** Both halves get `AND #$73` or an equivalent mask, and the
hand bit is never set. But condition 2 requires bit 7 to *differ*. So **no pair fits as dealt**, in
any deal, ever, and FLIP is not optional.

**About half the second halves are rolled at deal time.** `$7364` tests bit 7 of the random byte and
calls `$6FF1` on the partner when it is set. Since `$6FF1` does not commute with the `$55`
complement - 0 of 1,024 inputs agree - a rolled partner no longer complements its first half. The
pair is intact in the designer's intent and one button away in the player's hands, but it fails
condition 1 as it lies. In the captured deal, ten of the forty rods have no complement partner at all
until they are rolled back.

## What that costs the player

Measured on the captured deal (`ref/rod_deal.bin`) and on two hundred fresh deals generated by
running the machine's own `$7319` in a 6502 core:

| Question | Answer |
|---|---|
| pairs that fit as dealt, no button pressed | **0** |
| pairs that fit with ROTATE and FLIP only, all 16 combinations per pair | **13** |
| rods that fit nothing at all under ROTATE and FLIP | **14** |
| pairs that fit with ROTATE, FLIP and ROLL, all 8 states per rod | **20 of 20** |
| candidate links in the eight-state graph | 24 - 32 rods have one partner, 8 have two |
| button presses for one complete solution | 44 |
| fresh deals winnable with ROTATE and FLIP alone | **0 of 200** |
| fresh deals winnable once ROLL is allowed | **200 of 200** |
| fitting pairs per fresh deal without ROLL | 6 to 15 |

The three conditions are not equally responsive to the buttons, and that is the whole trick:

| Condition | ROTATE `^$40` | FLIP `^$80` | ROLL `$6FF1` |
|---|---|---|---|
| the profiles are complements | no effect | no effect | **rewrites the profile** |
| the hand bits differ | no effect | **toggles the bit-7 term** | no effect |
| the classes agree through `$7173` | **moves the label by `^4`** | no effect | no effect |

So the class test is a property of the deal, the hand bit is a property of FLIP, and the complement
is only reachable - once the deal has rolled a half - through ROLL. Nothing else in the game exposes
that: ROLL is one of eight boxes on the RODS screen, the game never says what the three buttons do,
and the message when you get it wrong says only "Parts do not match."

## Why this is a design and not an accident

Put the three facts together and the shape of the puzzle is explicit.

Every pair needs a FLIP, because the deal leaves every hand bit clear. Every deal contains pairs that
need a ROLL, because the deal rolls about half of the second halves. And every pairing has to respect
the class fold, which fails for one family pair out of six and therefore cannot be solved by simply
joining the halves the deal made. A player who treats ROTATE and FLIP as the puzzle - which is what
the screen invites, since ROLL sits one box away and has the least obvious effect - will find thirteen
fitting pairs, fourteen rods that match nothing, and no way to finish.

Found the right way, the deal is always solvable. The structure guarantees it (each designed pair is
complementary up to one roll), and the search confirms it: 200 of 200 deals reach a perfect matching
of all forty halves. A plain greedy pass - take the rods in index order, pair each with the first
unused rod that fits - found all twenty pairs on the captured deal and on one hundred fresh ones.
Whether a *particular* greedy order could strand a rod is not proven either way; a solved pair is
consumed irreversibly, so in principle it could, and no deal in the sample did.

## The two counters

`$03A8` counts **solved pairs** (`$6E6D`), from zero to `$14` = 20, and one solved pair consumes two
halves and yields one finished bar. `$6E7D` renders it: below ten, one digit plus a space; from ten,
a `1` and the remainder; at `$14` the digits are skipped entirely and `$6EDA` pushes "All 20 rods now
solved".

`$03A9` counts bars **inserted**, on the reactor screen, and `$7973` tests it against `$14` for the
win. `$784A` compares `$03A9 + $29` with `$03A8` before arming an insert, so the reactor will not let
you insert more bars than you have assembled. The two counters are the mission's only progress
record, and neither is a score.

## What is still open

- **The meaning of the four class labels.** The table is measured and its arithmetic is exact, but
  nothing in the game prints or otherwise exposes what a class *is*. It behaves like a fit family and
  that is all that can be said.
- **Whether the class fold was designed or inherited.** The game is a conversion of an Atari 800
  title, and a palindromic eight-entry table that folds into four is the kind of thing that survives
  a port because the original had eight classes and this one has four. There is no evidence either
  way in the image.
- **Whether a bad pairing order can strand rods.** Not observed in 101 deals, not proven impossible.

> [!NOTE]
> **What this corrects.** Earlier versions of this guide, and one earlier reading of the same table,
> said the deal was broken: thirteen fitting pairs, fourteen rods that fit nothing, and a fit test
> that looked inconsistent with the data. The numbers were right and the conclusion was wrong. The
> thirteen is what you get when ROLL is excluded, and the fourteen dead rods are the halves the deal
> rolled. A port that computes "8 to 13 fitting pairs" has measured its own missing button.

---

[Back to the overview](../README.md)
