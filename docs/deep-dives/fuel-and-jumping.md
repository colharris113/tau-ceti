# Fuel, jumping and LAUNCH

<p class="lede">Fuel in Tau Ceti does not power the ship. It is a clock that decides whether you may leave the ground. Jumping costs nothing at all: it is a graph traversal, and the edge you take is chosen by which side of the city you landed on.</p>

Both systems are small, and both are worth reading closely because they explain two of the game's most distinctive rules: you can run dry in the air and still fly, and you cannot choose a jump destination from a menu.

## The tank

Fuel is a sixteen-bit value in two zero-page bytes:

| Address | Half |
| --- | --- |
| <code class="addr">$0345</code> | Low byte |
| <code class="addr">$0346</code> | High byte |

A new game sets <code class="addr">$0346</code> to `$BF` and <code class="addr">$0345</code> to `$FF` at <code class="addr">$57F5</code>–<code class="addr">$57FF</code>: 49,151 units, or 191 and 255/256.

The instrument panel does not show all sixteen bits. The gauge routine at <code class="addr">$373F</code> passes only the high byte to the bar-drawing code at <code class="addr">$3766</code>, so each visible step of the fuel bar is 256 units of the real tank. That is why the bar can sit still for several seconds and then drop.

## One tick a second

The burn hangs off the game's master clock at <code class="addr">$25D3</code>. That routine runs once a frame and keeps a BCD counter at <code class="addr">$0340</code>; when the counter reaches `$50` it wraps and the second's work happens:

- the mission clock advances (`$0341` seconds, `$0342` minutes, `$0343` hours, all BCD);
- the shield level at <code class="addr">$0377</code> goes up by one, to a maximum of `$BF`;
- and the fuel burn runs at <code class="addr">$2637</code>.

The first test in the burn path is <code class="addr">$0396</code>. If it is non-zero — docked at `$80`, grounded at `1` — the burn and the shield regeneration are both skipped entirely. **Docked time is free.** Sitting on a pad to trade, repair or plan never costs a drop.

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

so the burn is

```text
speed >> 3  +  16    (+ 96 if the tank is ruptured)
```

with the whole speed term dropped at altitude zero. Speed is capped at `$BF`, so the burn runs from 16 a second at a standstill in the air to 39 a second at full throttle. A ruptured tank adds 96 to both ends: 112 to 135 a second.

<figure>
--8<-- "assets/diagrams/fuel.svg"
<figcaption>Left: the burn per second, which is linear in speed but with a large fixed floor. Right: endurance in minutes from the 49,151-unit tank. At full throttle that is 21 minutes intact and 6.1 minutes ruptured; at a standstill in the air, 51 and 7.3.</figcaption>
</figure>

The subtraction itself is a genuine sixteen-bit subtraction through the low byte at <code class="addr">$2653</code> and the high byte at <code class="addr">$265B</code>. If the high byte borrows below zero it is clamped to zero and <code class="addr">$03A3</code> is incremented — the "no fuel" latch. If the high byte lands exactly on `$20` (8,192 units left, about a sixth of a tank) and <code class="addr">$03A2</code> is still zero, that flag is set — the "low fuel" latch. Each latch is turned into a message exactly once by the routine at <code class="addr">$586C</code>:

| Latch | Message |
| --- | --- |
| <code class="addr">$03A2</code> = 1 | "Low Fuel" at <code class="addr">$58A3</code> |
| <code class="addr">$03A3</code> = 1 | "No Fuel" at <code class="addr">$58AD</code> |

A tank rupture is a separate event. The routine at <code class="addr">$4C3E</code> sets <code class="addr">$039E</code> once and prints "Fuel Tank Ruptured" from <code class="addr">$4CC8</code>. The flag persists until the repair service clears it; there is no in-flight fix.

## Running dry

An empty tank is not the end of the flight. The flight model never reads <code class="addr">$0346</code>: the only code that looks at it is the gauge, the LAUNCH gate, and the skimmer refuelling loop. With zero fuel you can still climb, dive, shoot and dock.

What you cannot do is *leave*. If the ship is on the ground with the tank empty — <code class="addr">$03A3</code> set, altitude zero, speed zero — the routine at <code class="addr">$589D</code> sets <code class="addr">$0396</code> to `1`, the grounded state. From there LAUNCH refuses, because LAUNCH checks fuel before it checks anything else.

## LAUNCH

The LAUNCH routine at <code class="addr">$4EDA</code> opens with three instructions:

```asm
LDA $0346        ; fuel high byte
BNE ok
; ... queue "Not Enough Fuel" ...
JMP $4dab        ; back to the docked screens
```

The test is on the high byte only. Any value from 1 to `$BF` passes, so a tank reading `$01:anything` is enough to lift off. Zero refuses with the message at <code class="addr">$4FA3</code>.

Past the gate, <code class="addr">$0396</code> selects the kind of take-off:

- **Docked at a pad** (`$80`): the ship is turned around. The heading at <code class="addr">$0338</code>/<code class="addr">$0339</code> has `$20` added and its low bit flipped, and the pad's cell at <code class="addr">$0398</code>/<code class="addr">$0399</code> is copied to the ship's cell at <code class="addr">$033C</code>/<code class="addr">$033F</code>. You leave facing away from the pad you landed on.
- **Grounded** (`1`): <code class="addr">$4F7F</code> handles a take-off from the surface, with no pad to turn away from.

Launch costs nothing. The routine never writes to <code class="addr">$0345</code> or <code class="addr">$0346</code>.

## Refuelling and repair

Two services refill the ship, and both are free. The refuel loop at <code class="addr">$5E4D</code> is disarmingly simple:

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

The delay at <code class="addr">$5FAC</code> waits for the frame counter, so the high byte climbs one point per frame: about 191 frames, or four seconds, from empty to full. The low byte is never touched. The tank ends at `$BF:something` rather than exactly `$BF:$FF`, which is invisible on the gauge and irrelevant to the burn.

The repair loop at <code class="addr">$5E7C</code> uses the same frame-by-frame pattern. It raises the shield at <code class="addr">$0377</code> to `$BF` and clears <code class="addr">$039E</code> along with several damage counters, then prints "All Systems Repaired" at <code class="addr">$5EAA</code>. This is the only way to seal a ruptured tank.

## The jump pad

A jump is a docking, not a command. The proximity scan tests byte 0 of every live record against `$10` before it tests flags, altitude or aperture; a match sets <code class="addr">$039B</code> to `$FF` and skips the rest of the record. The main loop, at the end of the same frame, ORs the flags at <code class="addr">$208C</code> and jumps to <code class="addr">$511E</code> when <code class="addr">$039B</code> is set.

The jump routine at <code class="addr">$511E</code> prints the banner "Super Traveller Mk. IV Jump-pad Engaging Destination" (stored at <code class="addr">$52F6</code> in three-character groups with a control byte), builds the destination name at <code class="addr">$0220</code> from the table at <code class="addr">$8D02</code>, and runs the warp animation at <code class="addr">$67BB</code>.

### The side you docked on picks the destination

There is no destination menu, and no player choice at the jump itself. The choice was made when you flew to a particular pad. At <code class="addr">$512F</code> the game reads the ship's cell and reduces it to one of four sides:

| Test | Side | Link slot |
| --- | --- | --- |
| x ≥ `$90` | East | 2 |
| x < `$70` | West | 3 |
| otherwise, y < `$70` | South | 1 |
| otherwise | North | 0 |

With the city centre at (128,128) and the pads 32 cells out on each axis, these four windows are exactly the four pad sites. The city index at <code class="addr">$0354</code> is shifted left twice and ORed with the side at <code class="addr">$5149</code>, giving an index into the four-bytes-per-city table at <code class="addr">$8900</code>:

```text
destination = $8900[ city * 4 + side ]
```

A byte of `$FF` means there is no pad on that side. The destination index is stored in <code class="addr">$0354</code> and becomes your current city.

### Arrival is on the side that leads back

After the warp, the game finds the city you came from in the destination's own four link bytes — but it compares only the first three, at <code class="addr">$51E7</code>, <code class="addr">$51EE</code> and <code class="addr">$51F5</code>, and falls back to `$18` (the fourth slot) otherwise. That index is then used as an offset into the arrival table at <code class="addr">$C4BF</code>/<code class="addr">$C4C0</code>:

| Arrival slot | Cell x | Cell y | Point |
| --- | --- | --- | --- |
| 0 | `$80` (128) | `$A0` (160) | North |
| 8 | `$80` (128) | `$60` (96) | South |
| 16 | `$A0` (160) | `$80` (128) | East |
| 24 | `$60` (96) | `$80` (128) | West |

The sub-cell bytes <code class="addr">$033B</code> and <code class="addr">$033E</code> are zeroed, so you arrive exactly on the cell centre. The jump flag is cleared at <code class="addr">$5215</code> and the game returns to the main loop with the new city already generated.

Because the arrival side is the side of the destination whose pad points back at your origin, every jump leaves you on the pad you would need to take to go home. In this game's data the relation is symmetric anyway: all 72 pad entries form 36 two-way links.

**No fuel is burned by any of this.** The jump routine never touches <code class="addr">$0345</code> or <code class="addr">$0346</code>. You can jump on an empty tank, and the long-range strategy of the game is built on that: the tank limits how long you can stay out, not how far you can travel.

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

- **Fuel is a timer, not a throttle.** Because the engines ignore it, running dry is a change of plan rather than a crash. Because LAUNCH reads it, an empty tank strands you exactly when you are safe on the ground — a soft failure that the player can see coming from the low-fuel warning and the falling gauge.
- **The burn formula has a floor.** `speed >> 3` changes the burn by only 23 points across the whole speed range, against a fixed 16 (or 96). Slowing down helps, but a ruptured tank overwhelms the saving. The repair service is the real fix, and the damage that causes a rupture is worth avoiding for its own sake.
- **The jump map is spatial.** Four pads on four sides, four destination bytes in a fixed order, and an arrival point on the same side of the destination. The player learns the network as a set of compass directions rather than a list of names, and the arrival rule guarantees that the pad under the ship on arrival is the one that goes back.

It is also a good example of [the record table's](the-record-table.md) economy: a pad is just a record with byte 0 equal to `$10`, the jump needs no new state beyond one flag byte, and the whole 32-city network fits in 128 bytes at <code class="addr">$8900</code>. The docking side is in [the previous article](docking-and-the-aperture.md).

The routine listings are on the [docking test](../source/routines/docking-test.md), [aperture](../source/routines/aperture.md) and [record scan](../source/routines/record-scan.md) pages; the type tables give the pad type's row in [the type tables](../reference/type-tables.md).
