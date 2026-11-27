# Docking and the aperture

Docking is the one manoeuvre in Tau Ceti where the game checks your flying rather than your guns. The test is short, exact and unforgiving: get close, line the ship up in two axes, and be inside a door that opens only while you are close — and shuts if you shoot the building.

The docking code is reachable from exactly one place: the proximity scan at `$2A4D`. Nothing else can dock you, and nothing else can trigger a jump.

## The approach pass

Every frame the scan walks all forty-eight records and rebuilds their status byte. The top two bits of byte 3 are cleared on every record at `$2A51`. Then, for each live record, it compares the record's cell and sub-cell with the ship's:

```asm
LDA ($61),Y      ; Y = 4, sub-cell x
SEC
SBC $dc
TAX
LDA ($61),Y      ; Y = 1, cell x
SBC $dd
...
CMP #$10
BCS next         ; an axis gap of 16 cells or more is out of range
```

The same test runs for y at `$2AAA`–`$2AD2`. A record that survives both axes gets its 16-bit distance worked out by the division at `$2ADE`, and the scan jumps straight to the docking test at `$2B60`.

So the 16-cell box is a *coarse* filter, and it is not the docking range. It decides which records are close enough to be worth examining at all — and, as a side effect, which records are close enough to appear on the scanner. Docking itself happens inside a much tighter radius.

## The test, in order

The docking test at `$2B60` starts with the distance in `$5A`/`$5B` and looks up a scale factor from two 256-byte tables: `$C800` when the high byte is 1, and `$C900` when it is 2–9, packed into an index by the shifts at `$2B6C`. The vector is then multiplied by that scale in a shift-and-add loop at `$2B8C`. The result is a three-byte product in `$26`, `$58`/`$59`, and it is sorted into three bands:

| Product | Treatment |
| --- | --- |
| High byte `$10` or more (4096+) | Ignored entirely — not even added to the target list |
| High byte 1–15, or high byte 0 with low byte `$80`+ | Active, target-listed at `$2CC0`, but too far to dock |
| High byte 0, low byte below `$80` (under 128) | Active and close enough to be examined for docking |

The product is stored in record bytes 12 (low) and 13 (high) and byte 3 bit 6 is set at `$2BC8`, so the record is active for the rest of the frame either way. A final guard at `$2BD6` rejects any record whose byte 0 still has state bits set — only live records get as far as the type tests.

### Jump pads come first

The very first type test is byte 0 against `$10`:

```asm
LDA ($61),Y       ; byte 0
CMP #$10
BNE not_a_pad
...
LDA #$FF
STA $039B         ; jump requested
JMP $2CBD         ; next record
```

A jump pad is not a building you land at. If you are close enough — and a flag test at `$3D18` passes — the pad sets `$039B` and the jump happens on the next pass through the main loop. There is no altitude check, no bearing check and no aperture. Pads are deliberately the easiest thing in the game to touch: `$036C`, the first test in the branch, is cleared at the end of every scan and so is normally zero, leaving only the `$3D18` test between you and the jump.

### Not dockable: collision

Anything without flags bit 7 at `$C39A` is solid, and the collision test at `$2C60` begins by skipping types with flags bits 2 or 3 — the two missile types, which have their own guided logic. For everything else it compares the ship's altitude at `$0344` with byte 6, the structure's base altitude, and the type's profile length at `$C3E4`; the structure's top is byte 6 plus that length. A hit marks the record's byte 0 with `$40` — it is destroyed — zeroes its aperture byte, adds `$40` to its hit points, and sets `$0392`, `$0393` and the effect code `$03C5` for the ship's own damage. Flying into a city building hurts you and kills it.

### The altitude window

For a dockable structure the first geometric test is altitude. The code at `$2BFA` computes

```text
|altitude - $1C| + $37   must be less than   record byte 8 (the aperture)
```

`$1C` is 28, the altitude at which the ship sits when docked. `$37` is 55. The test is a strict comparison, so an aperture of 0–55 can never accept anything: **no altitude docks until the door is at least 56/72 open**. At the full opening of `$48` (72), the window is altitude 12–44.

![Accepted altitude and bearing by aperture opening](../assets/diagrams/docking.svg)

*The altitude gate. The x-axis is the aperture byte; the wedge is the set of altitudes the test accepts. Below an aperture of 55 the wedge is empty.*

### The bearing window

The second test is the one players feel and rarely see. At `$2C1C` the game calls `$2CC6` to compute the bearing to the building as a nine-bit angle — a 512-step circle, so about 0.7° a step. The bearing comes back as a low byte in `A` and its ninth bit in `X`. It subtracts the ship's heading at `$0338`/`$0339`, then subtracts a fixed `$20` (32) — the 22.5° by which the bearing and heading conventions are offset, so that a target dead ahead lands in the middle of the window.

The way the difference is reduced is easy to misread. The 16-bit subtraction leaves a sign in the carry, and `$2C2F` shifts it out of the high byte with `LSR A`. The high byte is only ever 0 or 1, so the shift is not a division: it is the sign extraction. If the shifted-out bit is set, the low byte is negated at `$2C33`. The low byte is therefore the whole angular offset in steps, not a fraction of it. The routine adds `$1C` (28), doubles, and compares with the same aperture byte; a carry at either add is an immediate refusal.

The bearing gate is

```text
2 × (|bearing offset| + 28)   must be less than   the aperture
```

which is the altitude test with a different constant — the `+ 28` is doubled rather than left alone. The door's opening is a shared budget for *both* alignment errors. You must be lined up in height and in heading at the same time, and the same byte 8 decides how much slop you get in each. At the maximum opening of 72 the altitude band is 12–44 and the bearing window is |offset| ≤ 7 steps — a little under ±5°.

One quirk falls out of the integer arithmetic: a target exactly 256 steps (180°) away has a zero low byte with the sign bit set, and negating zero leaves zero, so the exact antipode is accepted. It is the only false positive in the test.

Failing either test sets `$0381` to `$FF`, the "dock refused" flag, and the main loop turns that into a message at `$4D60`.

### Acceptance

Passing both sets the docked state in three instructions and a short copy:

```asm
LDA #$80
STA $0396         ; docked
LDA ($61),Y       ; byte 0
STA $03A4         ; docked type
...               ; bytes 1 and 2
STA $0398         ; docked cell x
STA $0399         ; docked cell y
```

`$0396` = `$80` means "docked". The value 1 is a different state — grounded away from a pad — which [the next article](fuel-and-jumping.md) deals with.

## The aperture is a moving door

Byte 8 of a dockable record is not a fixed tolerance. It is an animation, and the thing that animates it is the aperture routine at `$4465`, which runs from the live dispatch for every dockable record:

- If byte 3 has **bit 4 (missile locked on) or bit 5 (hit)** set, the door closes two points a frame — unless the type is `$1B` (27), the Gal-Corp lander, which ignores this.
- Otherwise, if the record's distance byte 13 is **2 or more**, the door closes two points a frame.
- Only when byte 13 is **less than 2** does the door open, two points a frame, up to a maximum of `$48` (72).

![Aperture opening and closing over time](../assets/diagrams/aperture.svg)

*The iris moves two points a frame and takes thirty-six frames to travel from shut to fully open. Every point below 56 is a door that cannot accept any altitude.*

The practical consequences are sharp:

- **The door is already open before you can dock.** Byte 13 is the high byte of the scaled distance, so "less than 2" means a product below 512 — four times the docking radius of 128. A steady approach enters the opening band well before it enters the docking band, and the 36-frame travel is usually finished by the time you are close enough to touch the pad.
- **Hovering is not enough if you arrive late.** A quick dash into the centre leaves the door part-open, and the altitude and bearing tests simply fail until it finishes opening.
- **Drifting away closes it.** The door starts closing as soon as the product passes 512.
- **Shooting the building shuts it.** A player laser hit sets byte 3 bit 5 at `$3D83`; a locked-on missile sets bit 4 at `$48F2`. Either one drives the door shut at two points a frame, even while you are close enough to dock. The Gal-Corp lander is the exception, which is a small mercy when a fight spills over a landing site.
- **A closed door is not a refusal.** It simply makes the altitude and bearing tests impossible until it opens again.

The full 36-frame travel is why the aperture feels like a mechanism rather than a threshold, and why the docking test reads byte 8 fresh every frame.

## What docking changes

`$0396` is read all over the game:

- The frame tick at `$2627` skips both shield regeneration and fuel burn while it is non-zero. Docked time is free time.
- The main loop at `$2047` uses `BIT $0396`; a negative value (bit 7 set) branches into the docked screens instead of the flight loop.
- LAUNCH at `$4EDA` reads it to distinguish a normal pad undocking from the grounded state.
- `$03A4` holds the type you docked with, which is how the game decides whether you get a service screen, a trade screen or a jump.

Docking does not clear byte 3 or free the record. The building stays in the table, still active, and the door starts closing as soon as the distance test says you are no longer near.

## Why the design works

The two-window test plus a moving door turns docking into a short, legible skill check with a readable failure:

| Mistake | What you see |
| --- | --- |
| Too far (product 128–511) | No docking; the door is opening anyway |
| Wrong altitude | Refusal message; the door is open if you are within 512 |
| Nose not on the building | Refusal message; the door likewise open |
| Shot the building | Refusal; the door is closing |
| Perfect approach | The door opens during the approach, then acceptance |

There is no hidden die roll and no "docking computer". Two inequalities and one animated byte produce the whole mechanic — and because both inequalities share the aperture, improving your alignment pays off in both directions at once.

The listings are on the [docking test](../source/routines/docking-test.md) and [aperture](../source/routines/aperture.md) pages. The records themselves are explained in [the record table](the-record-table.md).

[Back to Deep Dives](index.md)
