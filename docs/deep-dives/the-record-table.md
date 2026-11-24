# The record table

<p class="lede">Everything that can move, fight, be shot at or be docked with lives in one array of forty-eight sixteen-byte records. There are no objects in Tau Ceti, only rows — and almost every interesting thing in the game is a loop over those rows.</p>

The table occupies <code class="addr">$0E00</code>–<code class="addr">$10FF</code>: three pages, forty-eight records, sixteen bytes each. It never moves. Records are not created and destroyed; they are marked free and overwritten in place. A record does not even have a fixed meaning per byte — the same offset is an altitude while a unit is alive and a falling body once it is dying.

Understanding the game at all starts here.

## Two walks a frame

Two separate routines walk the whole table on every frame, each with the same pointer convention. The address of the current record is held in zero page at <code class="addr">$61</code>/<code class="addr">$62</code>, and bytes are reached through the indirect indexed form `($61),Y`, with `Y` a constant 0–15. Advancing to the next record is a sixteen-byte add, not a pointer table:

```asm
LDA $61
CLC
ADC #$10
STA $61
BCC next
INC $62
```

The first walk is the dispatcher at <code class="addr">$43CF</code>. It loads the pointer with <code class="addr">$0E00</code>, processes every record through the state machine below, and after the third page advances a rotation counter at <code class="addr">$038F</code> by eight and clears its high bits (`AND #$3F`), adds <code class="addr">$4D</code> to <code class="addr">$EA</code>, and copies the frame's target counters. That counter is the game's round-robin for "which contact gets attention next".

The second walk is the proximity scan at <code class="addr">$2A4D</code>. It clears the top two bits of byte 3 on every record — the per-frame status bits — then tests each live record against the ship's cell. If the record is within sixteen cells on both axes it gets a proper 16-bit distance calculation (<code class="addr">$2ADE</code>) and is handed to the docking test at <code class="addr">$2B60</code>. That is the only route into docking, and it is also what makes a record "active" for the AI later in the same frame.

<figure>
--8<-- "assets/diagrams/record-table.svg"
<figcaption>The forty-eight records in their three pages, and one record expanded to all sixteen bytes. Byte 0 is tinted because it is the only byte every routine agrees on.</figcaption>
</figure>

## Byte 0 is the life cycle

The top two bits of byte 0 decide what the dispatcher does, and the low six bits are the type index:

| Byte 0 | Meaning | Dispatcher |
| --- | --- | --- |
| `$00`–`$3F` | Live; low bits are the type | `$445D`, the live dispatch |
| `$40`–`$7F` | Dying | `$441E`, the death animation |
| `$80`–`$BF` | Free, with the old type retained | Skipped |
| `$C0`–`$FF` | Also skipped | Skipped |

The test is literally three instructions at <code class="addr">$43E1</code>:

```asm
LDA ($61),Y      ; Y = 0
AND #$C0
CMP #$40
BCC live         ; $00-$3F
BEQ dying        ; $40-$7F
```

When a dying record finishes its animation, it is freed with `(byte0 & $3F) | $80` at <code class="addr">$4454</code>. That is why free records remember their type: the type bits survive, only the two state bits change.

Type is always the low six bits — `AND #$3F` — and indexes the parallel tables at <code class="addr">$C39A</code> (flags and hit points), <code class="addr">$C409</code> (behaviour) and the rest. Type numbers above 36 do not occur. See [the type tables](../reference/type-tables.md).

## Dying is two animations

The death animation at <code class="addr">$441E</code> reuses bytes 6 and 8 with new meanings:

1. Byte 6 falls by 8 a frame until it reaches zero. While it is falling, byte 8 is untouched. This is the body dropping out of the air.
2. Once byte 6 is zero, byte 8 rises by 8 a frame. This is the expanding flash, drawn from the same byte that is the docking aperture on a live building.
3. When byte 8 reaches `$F8` — thirty-one frames — the record is freed.

Types with bit 0 set in the flags table at <code class="addr">$C39A</code> are freed at `$78` instead, after fifteen frames. That is the "quick death" bit, and it is set for both missile types: a missile is gone in half the time of a robot. There is a special case in the middle of the loop that also frees a quick-death record as soon as byte 8 passes `$78`.

<figure>
--8<-- "assets/diagrams/dying.svg"
<figcaption>The same two bytes run two different animations. Thirty-one frames for most records, fifteen for anything with the quick-death flag.</figcaption>
</figure>

## The sixteen bytes

The names below are the conventions the code actually uses. Several are state-dependent, and a few bits are still unaccounted for; where a meaning is inferred rather than proved, the wording says so.

| Byte | Role | Evidence |
| --- | --- | --- |
| 0 | State (top two bits) and type (low six) | `$43E1` |
| 1, 2 | Cell x and y | Subtracted from ship cell at `$2A86`, `$2AB4` |
| 3 | Status bits, rebuilt each frame | See below |
| 4, 5 | Sub-cell x and y (1/256 cell) | Subtracted at `$2A7E`, `$2AAC` |
| 6 | Altitude for a unit; height for a structure; falling body when dying | `$2C66`, `$4420`, `$82EF` |
| 7 | Hit points | `$4951` subtracts damage here |
| 8 | Aperture for a dockable; flash for a dying record | `$4465`, `$4430` |
| 9 | Fire counter | `$82C0` |
| 10, 11 | Scanner blip position | Written by the scan code |
| 12, 13 | Distance to the ship, set by the docking scan | `$2BBE` |
| 14, 15 | Target pointer | `$48DF` |

Byte 3 is the busiest:

| Bit | Value | Meaning | Set by | Cleared by |
| --- | --- | --- | --- | --- |
| 5 | `$20` | Hit | `$3D83` when a player bolt lands | Record free |
| 4 | `$10` | Missile locked on | `$48F2` when a player missile launches | Record free |
| 6 | `$40` | Active / in range this frame | Proximity scan `$2BC8` | Scan `$2A51` and dispatch `$462A` |
| 2 | `$04` | Fired or attacked this frame | AI fire path `$834E` | Not seen cleared |
| 0, 1 | — | Per-frame mobile flags | AI movement | Dispatch `$462A` |

The `$40` bit is the hinge of the whole design. The proximity scan clears it at the start of the frame and sets it only for records close enough to matter. Everything downstream — AI, sensors, the aperture — runs only when that bit is set. An enemy on the far side of the city costs nothing because its bit is clear.

## The live dispatch

A live record goes through a short decision tree at <code class="addr">$445D</code>. It loads the per-type flags byte and tests one bit at a time:

| Flags bit | Meaning | Handler |
| --- | --- | --- |
| 7 (`$80`) | Dockable | Aperture animation, `$4465` |
| 1 (`$02`) | Sensor | Sensor counter, `$44A1` |
| 2 or 3 (`$04`, `$08`) | Robot or player missile | Guided-object logic, `$44C4` |
| otherwise | Mobile or static unit | AI dispatch, `$4620` |

The AI dispatch tests byte 3 bit 6 first. If the record is not active, it clears byte 3's bits 0 and 1, zeroes bytes 8 and 9, and moves on. If it is active, bit 6 of the flags byte calls the static-defence brain at <code class="addr">$81F3</code> and bit 5 calls the mobile-unit brain at <code class="addr">$80C3</code>. Type `$03`, for example, carries both flags, so it runs both brains in the same frame.

The tree is worth following on the routine pages: [record scan](../source/routines/record-scan.md), [live dispatch](../source/routines/live-dispatch.md), [aperture](../source/routines/aperture.md), [sensors](../source/routines/sensors.md), [guided objects](../source/routines/guided-objects.md), [AI dispatch](../source/routines/ai-dispatch.md).

## Damage and death

Damage arrives through <code class="addr">$4951</code>. It subtracts the damage value from byte 7 and, on underflow, performs the whole death sequence in one place:

- byte 8 is zeroed,
- the sound or effect code <code class="addr">$03C5</code> is set to 4,
- byte 0 is ORed with `$40`, putting the record straight into the dying animation,
- if the type's flags have bit 6 set (armed), the kill counters at <code class="addr">$03A5</code>/<code class="addr">$03A6</code> are incremented,
- <code class="addr">$0359</code> is set to `$FF`.

A player laser bolt does four points of damage when it resolves (<code class="addr">$3D89</code>) and sets the hit bit at <code class="addr">$3D83</code> before calling the damage routine. The hit bit is what tells an AI that it has been attacked — and, as [docking](docking-and-the-aperture.md) explains, what tells a dockable building to close its door.

## Where the 48 slots come from

The table is a fixed budget, and the game spends it unevenly:

- Most slots hold the city: buildings, sensors, the reactor, the lander.
- Mobile units occupy records that are already there when you arrive.
- Missiles are spawned into the **last page only**. The AI's allocation routine at <code class="addr">$82ED</code> sets the pointer to <code class="addr">$1000</code> and scans in sixteen-byte steps, stopping when the low byte of `Y` wraps to zero. It searches sixteen records and no more.

So every missile in a firefight — yours and theirs — comes out of the same sixteen-record page at <code class="addr">$1000</code>–<code class="addr">$10FF</code>. If the page is full, the launch simply does not happen; the shooter still goes through the firing motions and still sets its fired bit. That is a hard ceiling on how much ordnance can be in the air, and it is a direct consequence of the table being a fixed array.

The spawned missile is written at <code class="addr">$8315</code>:

```asm
LDA #$0B          ; type 11, the robot missile
STA ($63),Y       ; byte 0
; bytes 1 and 2 copied from the shooter's cell
LDA #$48
STA ($63),Y       ; byte 3 = active + ? (see below)
; bytes 4 and 5 zeroed
LDA ($61),Y       ; shooter's byte 6
CLC
ADC #$80
STA ($63),Y       ; byte 6 = shooter + $80, saturated
; byte 7 zeroed, then bytes 8..15
```

Byte 3 of a fresh missile is `$48`: bit 6 active, plus bit 3. Since the scan clears bits 6 and 7 every frame, the missile is active immediately and the `$08` bit presumably marks it as a missile rather than a placed object. The altitude byte starts 128 above the shooter's value, saturated at `$FF` — the missile appears overhead rather than inside its parent.

## Why this design

A record table buys the game several things at once:

- **Addressable everything.** The scanner, the AI, the docking test and the renderer can all agree on a contact because a contact is just `$0E00 + 16n`.
- **No allocator.** Spawning is "write into a record whose top bits are set", and freeing is two bit operations.
- **Cheap iteration.** The 16-byte stride and page-aligned base mean the page register only changes once every sixteen records.
- **Fifteen bytes per record of slack.** The table's meanings can be reused per state — altitude becomes death fall, aperture becomes flash — because nothing enforces a schema.

The price is that every subsystem has to know what each byte means in each state, and that a record's meaning can be overwritten by a missile spawning in a slot that a building thought it owned. The next two articles take the two places where that convention matters most: [the docking aperture](docking-and-the-aperture.md), where byte 8 is a moving door, and [fuel and jumping](fuel-and-jumping.md), where the table is deliberately left alone.
