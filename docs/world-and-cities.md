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

## City positions: what is not established

The obvious next question is where each city sits on the planet, and this is where the trail goes
cold. There is no table of 32 four-byte coordinate records following the names: the bytes that
follow the name list are a monotonically decaying curve -

```text
FE FC F4 E8 D7 C3 AC 93 7A 61 49 33 20 11 07 02 ...
```

- which is the signature of a projection or scaling table, not a list of positions. Whatever holds
  the city coordinates, it is not a simple array next to the names, and I have not located it.

What the code does show is how the *content* of a city is found. The current city number lives at
$0354. The routine at $280B uses it to derive a pointer - with a high byte near $94 - into a list of
objects for that city, and builds the 48 sixteen-byte records at $0E00 from it. So the per-city
data is a list of objects with their own positions, and if the city coordinates exist as data, that
list is the most likely place for them.

> [!WARNING]
> Earlier versions of this chapter printed a table of X/Y/Z/W coordinates for all 32 cities. Those
> numbers were not read from the disk; the address they were attributed to holds the curve above.
> The table has been removed rather than corrected, because there is nothing to correct it to.

## Jump pads

The manual describes the transport network: each city has jump pads at its north, south, east and
west edges, of the non-programmable "Super Traveller" type - you cannot choose a destination, the
pad takes you where it is paired. The lower of the two direction finders on the instrument panel
points at the nearest pad, and the upper one at the centre of the current city.

That much is manual text, not disassembly, and it is the level of detail I can stand behind. The
pairing map between cities is not documented anywhere I have found, in the code or in the data.

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

## Cooling rods

The mission, as the manual states it: collect 40 cooling rod parts from reactors across the cities,
assemble them into 20 bars, and insert the bars into the main reactor at Centralis.

| Step | Action |
|---|---|
| 1 | fly to a reactor station and dock |
| 2 | use LOOK to go inside |
| 3 | find and collect the rod parts |
| 4 | use RODS to assemble parts into bars |
| 5 | fly to Centralis |
| 6 | use REACTOR to insert the bars |
| 7 | repeat until the reactor is shut down |

The commands are real - RODS and REACTOR appear in the game's text - but the counting rules (40
parts, 20 bars, 8 per reactor) come from the manual rather than from anything I have disassembled,
and should be treated as description rather than reverse engineering.

---

[Back to the overview](../README.md)
