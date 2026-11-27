# The 32 cities

Tau Ceti has no city generator. All thirty-two cities, with every building in them, are written down in advance: one 96-byte sheet per city at `$9400`, each a list of three-byte records. This article recovers all of them from the listing, follows the loader that turns one sheet into the game's record table, and draws every city side by side.

The cities feel varied because they were placed by hand, not because the code varies. There is one loader, one record format and one set of type tables; what changes from city to city is a short list of positions. Reading that list is enough to map the whole game.

## A city is a list of three-byte records

Each city owns a 96-byte block, and each building in it is three bytes:

| Byte | Meaning |
| --- | --- |
| 0 | Type. The low six bits index the game's type tables |
| 1 | x position, 0–255 |
| 2 | y position, 0–255 |

That is the entire sheet. There is no hit point value, no size, no shape, no behaviour and no state — everything else about a building comes from its type, and everything that changes during play starts at zero.

A sheet has room for 32 records, and ends early with a type byte of `$C0`. The real cities use between 23 and 32 slots — most fill 30 or more — and across all thirty-two sheets there are **1,005 records**. The sparsest city is REEMA with 23.

## Finding a city's sheet

The current city is a single byte at `$0354`. The pointer builder at `$27EC` turns that index into the address of its sheet with a multiply and a divide:

- `ASL A` then `ADC $0354` gives the index × 3.
- Three `LSR A` / `ROR $61` pairs shift that right three times, collecting the bits that fall off the end in the low byte of the pointer.
- `ADC #$94` sets the high byte, ``$63`` is set to zero for the destination, and the result is a pointer to the sheet.

The arithmetic is a stride of 96 disguised as a stride of 3: 96 is 3 × 32, so the game multiplies by three and divides by eight. For city 1 the shift leaves nothing in the high byte, and the low byte becomes 3 × 32 = `$60`:

```text
1 × 3        = 3
3 >> 3       = 0        high = $94 + 0      = $94
3 & 7        = 3        low  = 3 × 32       = $60
pointer      = $9460    = $9400 + 1 × $60
```

The same instruction pair builds the destination pointer: `$63`/`$64` is set to `$0E00`, the start of the 48-record table.

## The loader, step by step

`$280B` rebuilds the record table for the city in `$0354`. It is not a per-frame routine: it runs when the game switches city — at jump arrival in `$51DB`, and in two other places that rebuild the current city (`$64F3` and `$6B72`).

| Step | Address | What it does |
| --- | --- | --- |
| 1 | `$27EC` | Turn the city index into a sheet pointer |
| 2 | `$280E` | Set the slot counter to 32 |
| 3 | `$2812` | Read a type byte; `$C0` ends the sheet |
| 4 | `$2818` | Copy type, x and y into the record |
| 5 | `$2823` | Zero bytes 3–15 |
| 6 | `$2831` | Copy hit points from `$C3BF[type & $3F]` into byte 7 |
| 7 | `$284E` | Advance both pointers and take the next slot |
| 8 | `$2857` | Scan the city's four jump destinations at `$8900` |
| 9 | `$286B` | Append two pad records per destination from `$C4BE` |
| 10 | `$28C4` | Fill the rest of the table with `$C0` |
| 11 | `$28E0` | Clear the provocation latch at `$03BF` |

### The building records

Steps 3 to 7 are the whole of a city. The loader reads the type byte first, because `$C0` is both the sheet's terminator and the value that marks an empty slot in the loaded table: the same byte ends the list and blanks the unused records.

Three bytes are copied to the record's start, then bytes 3 to 15 are zeroed. This clean slate matters. Byte 3 is cleared, so the building begins with no status bits; byte 8, the docking aperture, begins shut and then animates through play; the fire counters, blips and target pointers all begin at zero.

Byte 7 is then filled from the hit point table at `$C3BF`:

```asm
LDA ($63),Y     ; the record's type byte
AND #$3F        ; strip the state bits
TAY
LDA $C3BF,Y     ; 37 hit point values, one per type
LDY #$07
STA ($63),Y     ; record byte 7
```

The type byte is masked first, so the state bits copied from the sheet cannot disturb the lookup. This is why the sheet needs no durability field: hit points belong to the building's type, not to its position. Every substation in the game has the same hit points.

### The jump pads

The sheet does not contain the jump pads. They are added from a second table, which is why the loader keeps counting after the city's last building.

Each city has four bytes at `$8900` + city × 4. Each byte is the index of a destination city; `$FF` (any byte with bit 7 set) means the slot is unused. For each used byte, the loader appends **two** records from a shared table at `$C4BE`:

- the entry is eight bytes: two four-byte groups of type, x, y and hit points;
- the two records are a jump pad (type 16) and a small type-15 structure two cells further out;
- the record counter at `$67` is spent two at a time on these pairs, and one at a time on fillers, so the 48-slot table always ends exactly full.

The four entries are shared by every city. In table order they are north (y = 160), south (y = 96), east (x = 160) and west (x = 96), each with its type-15 marker just outside the pad. A city with three links has three pads. The comparisons at `$5134`–`$5147` select east when x is at least 144, west when x is below 112, south when y is below 112, and north otherwise.

Across the 32 cities there are 72 destination bytes, so the loader appends 144 pad and marker records. With the 1,005 buildings that makes 1,149 live records when every city has been visited. The jump graph itself is the subject of [Fuel, jumping and LAUNCH](fuel-and-jumping.md); here it is enough to note that every link is stored at both ends — each of the 72 entries has a reciprocal in the destination city.

### The empty slots

Whatever the buildings and pads do not use is filled with a record whose type byte is `$C0` and whose other fifteen bytes are zero (step 10). The record scan reads byte 0 and skips anything with bit 7 set, so `$C0` is a record that is already free. The table is never shorter than 48 entries; the end of the city is simply a run of blanks.

Finally the loader clears `$03BF`, the provocation latch. That is what stops a city's static defences firing at you the moment you arrive: they ignore the ship until a laser or a missile sets the latch. Mobile units are not governed by that latch, which is why some cities are hostile the instant you appear.

## The sheets remember

The city sheet is not only read. Before a jump, `$28E6` walks the sheet and the loaded record table together and copies one byte per record — **byte 0** — from the record back into the sheet. The city you leave is written down, and the next visit starts from what you left behind.

Two rules make this work:

- **Death keeps the type.** The dying animation's last act is `type AND $3F`, then `ORA $80`. A destroyed building is marked free without losing what it was: type 19 becomes `$93`, not `$80`.
- **The record scan tests bit 7.** The loader copies byte 0 unmasked, so a sheet slot of `$93` loads as a record with bit 7 set and is skipped. The building is gone, but the slot still says what it was.

The [save routine](../source/routines/city-save.md) deliberately skips the five armed mobile types — 3, 6, 9, 20 and 21, the ones whose flags hold both the mobile and armed bits. Machines are not architecture: they always come back, however many you shoot down.

The reverse happens at the start of a new game. `$2921` ([city restore](../source/routines/city-restore.md)), called by the new-game reset, walks all twelve pages of the sheet area and masks every byte that is not `$C0` with `$3F`. The `$80` falls away and the original building returns, which is exactly why the type had to be preserved. This also explains the filler value: an empty slot marked `$80` would be masked to type 0 and come back as a building, so the fillers are `$C0`, the one value the restore leaves alone.

The sheet is therefore a small save file as well as a layout: 96 bytes per city hold exactly what you have destroyed there. It is one of the few places in Tau Ceti where the game remembers something between visits.

## What the numbers mean

The type byte's low six bits select a row in nine parallel tables that begin at `$C39A`: flags, hit points, profile length, behaviour, class range, class speed, fire masks, fire ticks and the missile threshold. The [type tables](../reference/type-tables.md) reproduce all of them. Three flag bits do most of the work in a city:

| Flag | Bit | Meaning in a city |
| --- | --- | --- |
| `$80` | 7 | Dockable — a special building with an aperture |
| `$40` | 6 | Armed — a static defence |
| `$20` | 5 | Mobile — a hunter, sand hopper or other machine |

The x and y bytes are city cells, from 0 to 255, with the city centre at 128. Every record lies between **96 and 160** on both axes, so the whole city fits inside a 64-cell square. Increasing x goes east and increasing y goes north. The diagrams draw larger y values higher on the page.

## The special buildings

Five types carry the dockable flag, and they are the only ones that do:

| Type | Building | Where it appears |
| --- | --- | --- |
| 27 | Gal-Corp lander | REEMA only |
| 28 | Central reactor | CENTRALIS only |
| 29 | Reactor substation | 31 cities — every city except CENTRALIS |
| 30 | Civilian supply centre | 21 cities |
| 31 | Military supply centre | 10 cities |

The placement is exact. Every city has two dockable buildings except two: CENTRALIS has one, the reactor, and no substation or supply centre at all; REEMA has three — the lander, a substation and a civilian supply centre. Every other city pairs one substation with one supply centre, and the supply centre is either civilian or military, never both.

That layout is the campaign in miniature. The only lander is at REEMA, so that is where the mission starts; the only reactor is at CENTRALIS, in the most crowded city in the game; and every other city offers a substation to sabotage and a supply centre to dock at.

## The maps

![The layouts of all 32 cities](../assets/diagrams/cities.svg)

*All 32 city sheets, drawn from the game's own table at `$9400`. Each panel is an 80-cell window around the city centre; every mark is one three-byte record. The jump pads and their markers are absent because they are not in the sheet: the loader appends them from four shared templates at `$C4BE`, always at the same four edge positions.*

The figure is generated directly from the sheet, not traced from screenshots, so it can be checked against the extraction script. A few things stand out:

- **CENTRALIS is the exception.** It uses all 32 slots; 20 records carry the armed flag and 18 the mobile flag, and twenty-two records are armed or mobile — more than in any other city. It also has a single ringed mark: the reactor at (140,116).
- **REEMA is the quietest.** At 23 records it has the fewest buildings, one mobile machine and five armed structures. Its three rings sit far apart, which is a kindness on the first landing.
- **KRILL has no armed structures at all**, and **JADE has no mobile machines**. The maps show this immediately: KRILL has no ochre squares, JADE has no blue diamonds. Both facts come straight from the type flags, not from the map.
- **Every city is compact.** No building lies outside the central square, so the approach to any city crosses empty ground before the defences begin.

## The names

The city names live at `$8D02`, one after another in the same order as the sheets. Each character is one byte and each name ends with a byte that has bit 7 set — in practice `$C0`. CENTRALIS begins:

```text
$23 $25 $2E $34 $32 $21 $2C $29 $33 $C0
 C   E   N   T   R   A   L   I   S  end
```

Those bytes are not text codes in the usual sense: they are **glyph numbers** into the message font at `$9000`. The font's first glyphs are the digits, and the alphabet starts at 33, so `A` is `$21` and `C` is `$23`. The bytes are copied straight to the screen buffer by the printer at `$5149`, which finds the name it wants by walking the table from the beginning and counting terminators until it has passed the right number of names. There is no index and no fixed record size.

That is the whole string system in about 200 bytes: variable-length names, a one-byte terminator, and a linear scan. The [message renderer](../source/routines/message-printer.md) uses the same font and the same trick.

## Why it works

The city data is remarkably small:

| Data | Bytes |
| --- | --- |
| 32 city sheets at `$9400` | 3,072 |
| 32 × 4 jump destinations at `$8900` | 128 |
| 4 shared pad templates at `$C4BE` | 32 |
| Names at `$8D02` | about 200 |

Under four kilobytes holds the architecture of the entire game. The saving comes from putting everything that is shared into the type tables — a building is a type number and a place, nothing more — and from accepting a hard limit of 32 structures per city. Within that budget the designer filled the sheets by hand, and the variety that results is the variety of 1,005 deliberate positions rather than of a random seed.

## Next steps

The next question is how those three-byte records become buildings on screen: the profiles that give each type its shape, the lathe that draws it, and the two-colour light that falls across it. [The viewport in flight](the-viewport-in-flight.md) follows a record from this table to the raster. The storage side is documented in full on the [city loader](../source/routines/city-loader.md) page, and the record format it produces is the subject of [The record table](the-record-table.md).

[Back to Deep Dives](index.md)
