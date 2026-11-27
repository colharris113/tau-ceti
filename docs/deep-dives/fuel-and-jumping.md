# Fuel, jumping and LAUNCH

An empty tank makes the skimmer descend and can strand it on the ground. Jumping uses no fuel. The pad you reach selects an edge in the city's four-slot jump table.

Both rules follow from a handful of state bytes. The fuel code tracks the tank and the no-fuel latch separately, while each city has four bytes for its jump destinations.

## The tank

Fuel is a sixteen-bit value in two bytes on page three of RAM:

| Address | Half |
| --- | --- |
| `$0345` | Low byte |
| `$0346` | High byte |

A new game sets `$0346` to `$BF` and `$0345` to `$FF` at `$57F5`–`$57FF`: 49,151 units, or 191 and 255/256.

The instrument panel does not show all sixteen bits. The gauge routine at `$373F` passes only the high byte to the bar-drawing code at `$3766`, so each visible step of the fuel bar is 256 units of the real tank. That is why the bar can sit still for several seconds and then drop.

## One tick a second

The burn hangs off the game's master clock at `$25D3`. That routine runs once a frame and keeps a BCD counter at `$0340`; when the counter reaches `$50` it wraps and the second's work happens:

- the mission clock advances (`$0341` seconds, `$0342` minutes, `$0343` hours, all BCD);
- the shield level at `$0377` goes up by one, to a maximum of `$BF`;
- and the fuel burn runs at `$2637`.

The first test in the burn path is `$0396`. If it is non-zero — docked at `$80`, grounded at `1` — the burn and the shield regeneration are both skipped entirely. **Docked time is free.** Sitting on a pad to trade, repair or plan never costs a drop.

## The burn

The amount subtracted each second is built in four steps:

```asm
LDA $0344        ; altitude
BEQ ground       ; zero altitude: no speed term at all
LDA $0353        ; speed
LSR A
LSR A
LSR A            ; speed / 8
CLC
ADC #$10         ; + 16
ground:
LDX $039e        ; tank rupture flag
BEQ no_rupture
CLC
ADC #$60         ; + 96
no_rupture:
```

At positive altitude the routine computes

```text
speed >> 3  +  16    (+ 96 if the tank is ruptured)
```

Speed is capped at `$BF`, so the airborne burn runs from 16 a second at a standstill to 39 a second at full throttle. A ruptured tank adds 96 to both ends, for a range of 112 to 135. At altitude zero the `BEQ` skips both the speed term and the fixed 16. The computed amount is then zero with an intact tank or 96 with a ruptured one.

![Airborne fuel burn and endurance by speed](../assets/diagrams/fuel.svg)

*Airborne fuel burn and endurance from the 49,151-unit tank. At full throttle the tank lasts 21 minutes intact or 6.1 minutes ruptured. At a standstill in the air it lasts 51 or 7.3 minutes.*

The routine negates the amount in eight bits, clears carry, and adds the result to the tank's low byte at `$2653`. It then adds `$FF` plus the resulting carry to the high byte at `$265B`. For a nonzero amount this subtracts the computed burn. A zero amount leaves the low byte as it was and produces no carry, so the high byte drops by one. At altitude zero with an intact tank and `$0396` clear, this takes `$BFFF` to `$BEFF` in one tick. A ruptured tank at altitude zero subtracts 96 as computed.

On underflow, the routine clears only the high byte, preserves the low-byte result, and increments `$03A3`, the "no fuel" latch. A resulting high byte of `$20` (`$2000`–`$20FF`, about a sixth of a tank) sets `$03A2`, the "low fuel" latch, if it was clear. The routine at `$586C` queues a message when it sees the corresponding latch at 1:

| Latch | Message |
| --- | --- |
| `$03A2` = 1 | "Low Fuel" at `$58A3` |
| `$03A3` = 1 | "No Fuel" at `$58AD` |

A tank rupture is a separate event. The routine at `$4C3E` sets `$039E` once and prints "Fuel Tank Ruptured" from `$4CC8`. The flag persists until the repair service clears it; there is no in-flight fix.

## Running dry

The skimmer keeps moving after the no-fuel latch sets, but it starts to descend. The control handler tests `$03A3` at `$3A14` and branches directly to the descent code at `$3A33`. Altitude falls by one on each control update until it reaches zero, even with no dive input. Turning and firing remain available. The burn routine, gauge, LAUNCH gate and skimmer refuelling loop read the fuel high byte at `$0346`.

What you cannot do is *leave*. If the ship is on the ground with the tank empty — `$03A3` set, altitude zero, speed zero — the routine at `$589D` sets `$0396` to `1`, the grounded state. From there LAUNCH refuses, because LAUNCH checks fuel before it checks anything else.

## LAUNCH

The LAUNCH routine at `$4EDA` opens with three instructions:

```asm
LDA $0346        ; fuel high byte
BNE ok
; ... queue "Not Enough Fuel" ...
JMP $4dab        ; back to the docked screens
```

The test is on the high byte only. Any value from 1 to `$BF` passes, so a tank reading `$01:anything` is enough to lift off. Zero refuses with the message at `$4FA3`.

Past the gate, `$0396` selects the kind of take-off:

- **Docked at a pad** (`$80`): the ship is turned around. The heading at `$0338`/`$0339` has `$20` added and its low bit flipped, and the pad's cell at `$0398`/`$0399` is copied to the ship's cell at `$033C`/`$033F`. You leave facing away from the pad you landed on.
- **Grounded** (`1`): `$4F7F` handles a take-off from the surface, with no pad to turn away from.

Launch costs nothing. The routine never writes to `$0345` or `$0346`.

## Refuelling and repair

Two services refill the ship, and both are free. The refuel loop at `$5E4D` is disarmingly simple:

```asm
refuel:
LDA $0346
CMP #$BF
BEQ done
INC $0346        ; one point, once a frame
JMP refuel
done:
; queue "Skimmer Refueled" ($5E6A)
```

The delay at `$5FAC` waits for the frame counter, so the high byte climbs one point per frame: about 191 frames, or four seconds, from empty to full. The low byte is never touched. The tank ends at `$BF:something` rather than exactly `$BF:$FF`, which is invisible on the gauge and irrelevant to the burn.

The repair loop at `$5E7C` uses the same frame-by-frame pattern. It raises the shield at `$0377` to `$BF` and clears `$039E` along with several damage counters, then prints "All Systems Repaired" at `$5EAA`. This is the only way to seal a ruptured tank.

## The jump pad

A jump is a docking, not a command. The proximity scan tests byte 0 of every live record against `$10` before it tests flags, altitude or aperture; a match sets `$039B` to `$FF` and skips the rest of the record. The main loop, at the end of the same frame, ORs the flags at `$208C` and jumps to `$511E` when `$039B` is set.

The jump routine at `$511E` prints the banner "Super Traveller Mk. IV Jump-pad Engaging Destination" (stored at `$52F6` in three-character groups with a control byte), builds the destination name at `$0220` from the table at `$8D02`, and runs the warp animation at `$67BB`.

### The side you docked on picks the destination

There is no destination menu, and no player choice at the jump itself. The choice was made when you flew to a particular pad. At `$512F` the game reads the ship's cell and reduces it to one of four sides:

| Test | Side | Link slot |
| --- | --- | --- |
| x ≥ `$90` | East | 2 |
| x < `$70` | West | 3 |
| otherwise, y < `$70` | South | 1 |
| otherwise | North | 0 |

These directions follow the [city maps](the-32-cities.md), with x increasing east and y increasing north. The four tests select the corresponding pad 32 cells from the city centre at (128,128). The city index at `$0354` is shifted left twice and ORed with the side at `$5149`, giving an index into the four-bytes-per-city table at `$8900`:

```text
destination = $8900[ city * 4 + side ]
```

A byte of `$FF` means there is no pad on that side. The destination index is stored in `$0354` and becomes your current city.

### Arrival is on the side that leads back

After the warp, the game finds the city you came from in the destination's own four link bytes — but it compares only the first three, at `$51E7`, `$51EE` and `$51F5`, and falls back to `$18` (the fourth slot) otherwise. That index is then used as an offset into the arrival table at `$C4BF`/`$C4C0`:

| Arrival slot | Cell x | Cell y | Point |
| --- | --- | --- | --- |
| 0 | `$80` (128) | `$A0` (160) | North |
| 8 | `$80` (128) | `$60` (96) | South |
| 16 | `$A0` (160) | `$80` (128) | East |
| 24 | `$60` (96) | `$80` (128) | West |

The sub-cell bytes `$033B` and `$033E` are zeroed, so you arrive exactly on the cell centre. The jump flag is cleared at `$5215` and the game returns to the main loop with the new city already generated.

Because the arrival side is the side of the destination whose pad points back at your origin, every jump leaves you on the pad you would need to take to go home. In this game's data the relation is symmetric anyway: all 72 pad entries form 36 two-way links.

**No fuel is burned by any of this.** The jump routine never touches `$0345` or `$0346`. You can jump on an empty tank, and the long-range strategy of the game is built on that: the tank limits how long you can stay out, not how far you can travel.

## The network

Thirty-two cities, four possible pads each. A dash is `$FF`, no pad on that side. Slots are north, south, east, west.

| # | City | North | South | East | West |
| --- | --- | --- | --- | --- | --- |
| 0 | Centralis | Reema | Zilogi | Tsula | Heyrol |
| 1 | Reema | — | Centralis | — | Hame |
| 2 | Hame | — | Novia | Reema | Auriga |
| 3 | Auriga | — | Entrola | Hame | Ceriti |
| 4 | Entrola | Auriga | — | — | Ceriti |
| 5 | Ceriti | — | Entrola | Auriga | Quilba |
| 6 | Zoon | — | Leestra | Jade | Roon |
| 7 | Roon | Quilba | — | Zoon | — |
| 8 | Quilba | — | Roon | Ceriti | — |
| 9 | Erma | — | Rileny | — | Coruk |
| 10 | Coruk | Scarth | — | Erma | Goborindi |
| 11 | Rileny | Erma | — | Reyes | — |
| 12 | Goborindi | — | — | Coruk | — |
| 13 | Zilogi | Centralis | — | Kula | — |
| 14 | Kula | Tsula | — | — | Zilogi |
| 15 | Tsula | Krill | Kula | — | Centralis |
| 16 | Krill | Drano | Tsula | — | — |
| 17 | Drano | Kdapt | Krill | — | — |
| 18 | Kdapt | — | Drano | — | Kzinti |
| 19 | Kzinti | — | — | Kdapt | — |
| 20 | Heyrol | Novia | Scarth | Centralis | Jade |
| 21 | Scarth | Heyrol | Coruk | Botania | Jade |
| 22 | Jade | — | Scarth | Heyrol | Zoon |
| 23 | Botania | — | — | Minstro | Scarth |
| 24 | Minstro | Frome | — | Ilea | Botania |
| 25 | Frome | — | Minstro | — | — |
| 26 | Ilea | — | — | — | Minstro |
| 27 | Leestra | Zoon | Preema | — | — |
| 28 | Preema | Leestra | — | — | — |
| 29 | Reyes | — | — | — | Rileny |
| 30 | Novia | Hame | Heyrol | — | Rubiya |
| 31 | Rubiya | — | — | Novia | — |

The graph is connected, every link is two-way, and no city has more than four. Centralis, Heyrol and Scarth are the only four-pad junctions: the central hub and two regional crossroads. The fringe cities — Frome, Ilea, Preema, Reyes, Rubiya, Goborindi, Kzinti — are leaf nodes with one pad each, places you visit deliberately rather than pass through.

## Why it works

The two systems reinforce each other:

- **Fuel determines how long the skimmer can stay aloft.** Running dry causes a descent while horizontal motion remains under the pilot's control. After landing, the LAUNCH gate can strand the skimmer until it refuels.
- **The burn formula has a floor.** `speed >> 3` changes the burn by only 23 points across the whole speed range, against a fixed 16 (or 96). Slowing down helps, but a ruptured tank overwhelms the saving. The repair service is the real fix, and the damage that causes a rupture is worth avoiding for its own sake.
- **The jump map is spatial.** Four pads on four sides, four destination bytes in a fixed order, and an arrival point on the same side of the destination. The player learns the network as a set of compass directions rather than a list of names, and the arrival rule guarantees that the pad under the ship on arrival is the one that goes back.

It is also a good example of [the record table's](the-record-table.md) economy: a pad is just a record with byte 0 equal to `$10`, the jump needs no new state beyond one flag byte, and the whole 32-city network fits in 128 bytes at `$8900`. The docking side is in [the previous article](docking-and-the-aperture.md).

The routine listings are on the [docking test](../source/routines/docking-test.md), [aperture](../source/routines/aperture.md) and [record scan](../source/routines/record-scan.md) pages; the type tables give the pad type's row in [the type tables](../reference/type-tables.md).

[Back to Deep Dives](index.md)
