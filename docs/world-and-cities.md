# World and Cities

The 32 cities, their name table, the jump-pad network, reactors and cooling rods.

---

Tau Ceti (III) is a rocky world with 32 named cities. What the disk can tell us for certain is the
city list and how it is encoded; what it can tell us about how the cities are laid out on the planet
is much less, and this chapter is careful to separate the two.

## The city name table

The 32 names are stored as one contiguous run at **$8D02**, in the file `8900-CC00`, 0x402 bytes
from the start of that file. The format is simple:

```text
$8D02:  $23 $25 $2E $34 $32 $21 $2C $29 $33  $C0  $32 $25 $25 $2D $21  $C0 ...
        C   E   N   T   R   A   L   I   S   sep  R   E   E   M   A    sep
```

- Each letter is its alphabet index plus $20, so A is $21, B is $22, and so on.
- **$C0** separates one name from the next.
- **$FF** ends the list.

There is no XOR key and no lookup table: the names are readable straight out of the image once you
know the offset. (An earlier version of this chapter said the names were XOR-encoded with $60 and
that $23 decodes to C by XOR. $23 XOR $60 is $43, which is not C; the +$20 rule is what the code
and the data both use.)

## The 32 cities

In table order, which is the order the game indexes them:

| # | City | # | City | # | City | # | City |
|---|---|---|---|---|---|---|---|
| 0 | CENTRALIS | 8 | QUILBA | 16 | KRILL | 24 | MINSTRO |
| 1 | REEMA | 9 | ERMA | 17 | DRANO | 25 | FROME |
| 2 | HAME | 10 | CORUK | 18 | KDAPT | 26 | ILEA |
| 3 | AURIGA | 11 | RILENY | 19 | KZINTI | 27 | LEESTRA |
| 4 | ENTROLA | 12 | GOBORINDI | 20 | HEYROL | 28 | PREEMA |
| 5 | CERITI | 13 | ZILOGI | 21 | SCARTH | 29 | REYES |
| 6 | ZOON | 14 | KULA | 22 | JADE | 30 | NOVIA |
| 7 | ROON | 15 | TSULA | 23 | BOTANIA | 31 | RUBIYA |

> [!NOTE]
> The run is 210 bytes long and ends with $FF, with 31 separators between the names - so 32 names,
> CENTRALIS at index 0 and RUBIYA at index 31. The spellings most often mangled in transcriptions
> are ENTROLA (not Entroia), ERMA (not Erna) and HEYROL (not Keyrol); KDAPT and KZINTI keep their K
> prefixes.

## City positions: the map's own table

The obvious next question is where each city sits on the planet, and the answer is a table that has
been in front of me since the first pass: **$89A0 holds 32 bytes of X and $89C0 holds 32 of Y**, one
per city in name-table order, just above the names.

Two routines use them, and neither is a guess:

- `$8422` is nine bytes long and seats the star map's cursor from them. Called with `X = 0` it gives
  `$03C0/$03C1 = $80/$80`, the centre of the map and the position of Centralis; called with `X = 1` it
  gives `$8C/$94`, which is REEMA, the city a new game starts in. [Map System](map-system.md) has the
  rest of that screen.
- `$848F` builds the 64 four-byte star records at `$0D00` from four tables - `$89A0` and `$89C0` for
  the first 32, `$89E0` and `$8DE0` for the second - and projects them through the zoom scale at
  `$86BB`.

So the planet's coordinate system is a `$80`-based grid, the cities have integer positions on it, and
the "not established" of earlier versions of this chapter was a matter of looking next to the names
rather than three hundred bytes above them.

The table that follows the name list is still what it looked like - a monotonically decaying curve:

```text
FE FC F4 E8 D7 C3 AC 93 7A 61 49 33 20 11 07 02 ...
```

- but it is a projection scale, not a list of positions, and it is not the map's. What is still not
established is something different: the **ground origin** of a city in the flight view. That is not a
coordinate pair in a table; it is the per-city object list, and `$280B` builds the 48 records from it
without ever needing a separate origin.

What the code does show is how the *content* of a city is found. The current city number lives at
$0354. The routine at $280B uses it to derive a pointer - with a high byte near $94 - into a list of
objects for that city, and builds the 48 sixteen-byte records at $0E00 from it. So the per-city
data is a list of objects with their own positions, and if the city coordinates exist as data, that
list is the most likely place for them.

> [!WARNING]
> Earlier versions of this chapter printed a table of X/Y/Z/W coordinates for all 32 cities. Those
> numbers were not read from the disk; the address they were attributed to holds the curve above.
> That table was removed rather than corrected, and it should stay removed: the real coordinate table
> is not a 128-byte block of four-byte records, it is two plain 32-byte arrays at `$89A0` and `$89C0`,
> and any table with four numbers per city is describing something else.

## Jump pads

The manual describes the transport network: each city has jump pads at its north, south, east and
west edges, of the non-programmable "Super Traveller" type - you cannot choose a destination, the
pad takes you where it is paired. The lower of the two direction finders on the instrument panel
points at the nearest pad, and the upper one at the centre of the current city.

That much is manual text, not disassembly, and it is the level of detail I can stand behind. The
pairing map between cities is not documented anywhere I have found, in the code or in the data.

Where the pads are, though, is in the data, and so is what is standing next to them. Each city has
four bytes at $8900 + city × 4 saying which of the four directions has a pad, and the pad coordinates
come from four fixed groups at $C4BE - the four edge midpoints. The small creatures the manual calls
sand hoppers are ordinary objects in the city list, placed within a few units of those midpoints.
[Sand Hoppers](creatures.md) has the counts and the code.

## Buildings

Cities are made of buildings, and the buildings are the game. The manual's list is the best guide to
what you will meet:

| Type | What it is |
|---|---|
| Reactor stations | hold cooling rod parts; the objective |
| Military bases and fortresses | defended; turrets, robots, mines |
| Civil bases | resupply; where EQUIP works |
| The Gal-Corp lander | your starting base |
| Jump pads | transport between cities |
| Control towers | navigation and intelligence |

Every building has a DFP energy-screened airlock that opens and closes in a flickering pattern. You
dock by waiting for the opening and flying in slowly - the airlock is a timing problem, not a
collision problem.

In the code, a building is one of the 48 records at $0E00: byte 0 is a type index into the table at
$C39A, byte 3 carries flags ($40 drawn, $08 variant), bytes 10-11 are the X position and bytes 12-13
the depth. The records are rebuilt from the city's list each time you change city.

## The mission chain

The manual's description of the mission is accurate but flat: collect 40 cooling rod parts from
reactors across the cities, assemble them into 20 bars, insert the bars into the main reactor at
Centralis. The code adds the conditions, the counters and the way it can kill you.

```text
land on a type $1C or $1D building     $2C45   $0396 = $80, $03A4 = the type
  the console loop, once per frame    $4DA1
    $73C4  that city's rods appear     only if the type is $1C/$1D and the city is unvisited
RODS    $6D0E  pair the halves         $03A8 counts solved pairs, to $14
REACTOR $770B  insert the bars         $03A9 counts inserted bars, to $14
              $03BE counts the dose   61 ticks -> $7B5E, mission failed
walk out of the reactor               $7973   $03A9 = $14 -> the win
```

Four counters and one flag carry all of it:

| Variable | Meaning | Range |
|---|---|---|
| `$03A7` | rod halves on the surface, world total | 0 to `$28` (40) |
| `$03A8` | halves solved into bars | 0 to `$14` (20) |
| `$03A9` | bars inserted | 0 to `$14` (20) |
| `$03BE` | radiation dose | 0 to `$3D` (61) |
| `$7440 + city` | halves that city drops | 0-3, bit 7 set once visited |
| `$BC50-$BC7E` | the tray, one byte per cell | a rod index, or `$FF` |
| `$03DB-$03EE` | the reactor's 20 slots | 0 empty, `$FF` filled |

`$7440` is the per-city distribution, and it is worth printing because the numbers are not uniform:
`03 00 01 02 01 02 01 00 01 01 01 02 02 01 01 02 01 02 01 01 01 01 01 00 02 01 02 01 01 02 01 01`.
City 0 drops three, three cities drop none, nineteen drop one and nine drop two, and the total is
exactly the world cap of 40.

**The rods appear when you land.** `$73C4` runs from the console loop, once per frame, while you are
docked. It tests `$03A4` for the two reactor types, looks up the city's count, and **sets bit 7 of the
flag before it places anything**. That ordering is not a detail: a city whose rods cannot be placed -
because the world total is already at 40 - is still marked stripped, and can never drop them later.
The message in that case says "0 ROD SECTION S FOUND", which is the game telling the truth.

The count in that message is not a formatted number. `$742A` is a byte inside the sentence, written by
the routine that just counted what it placed. [Character Set and Text System](charset.md) has the same
trick in the reactor's own message.

**The reactor room is only at Centralis.** `$770B` refuses unless `$03A4` = `$1C` - the Central
reactor - and says so in as many words. A substation (`$1D`) will give you rods and will not take them
back. The type byte is the same one the landing path wrote, which is how the game knows which building
you are standing in without a separate flag.

**Insertion is two actions.** The screen arms with one menu box and confirms on the cell, and the arm
refuses when `$03A9` has caught up with `$03A8`: you cannot insert more bars than you have assembled.
Filling the twentieth slot pushes "ALL COOLING RODS INSERTED / REACTOR SUCCESSFULLY CLOSED DOWN", which
is not the win. **The win is `$7973`, in the leave path**: it runs when you walk out of the reactor,
tests `$03A9` against `$14`, and only then prints `$7D04` and starts the ending - the map cursor
centred, and 31 zoom-out passes of the star chart from `$1F` down to 0.

**The dose clock is the only way the mission fails on its own.** `$03BE` is incremented once per slow
tick while you are in the reactor room - the `$11 & $7F == 0` tick, so once per 128 frames - and
nothing else in the image writes it. At `$28`, `$34` and `$39` it queues a warning into the border
banner, each one faster than the last. At **61** it pushes `$7B5E` and jumps to `$6473`, the shared
mission-failed sequence, which is also what QUIT uses. Standing in the reactor thinking about it for
two and a half minutes ends the game, and the counter is only cleared when a new mission starts.
That room, its gauge and its three warnings have their own chapter: [The Radiation Clock](radiation.md).

## The puzzle in the tray

The halves are not interchangeable, and the RODS screen is a real puzzle with a rule that the game
never states: the profiles are complementary pairs, the hand bits must differ, and the classes must
agree through a table that folds eight classes into four. The deal you are given rolls about half of
the second halves, so nothing fits as it lies and one of the three buttons is mandatory.

That is worth its own chapter, and it has one: [The Rod Puzzle](rod-puzzle.md). What matters here is
the shape of the chain - a city gives you halves, the tray turns halves into bars, the reactor turns
bars into progress, and the two counters at `$03A8` and `$03A9` are the only record of either.


---

[Back to the overview](../README.md)
