# Why the city starts shooting

A fixed gun can sit within range and do nothing until you open fire. A mobile hunter can close on you before you fire a shot. The two share a firing routine, and the distinction fits into one type flag and one city-wide byte.

## The city-wide latch

The city loader clears `$03BF` at `$28E2`. A successful laser trigger writes `$80` to it at `$341E`, and launching a player missile writes `$FF` at `$48F8`. The laser writes the latch as it starts the bolt, before the later damage test. A shot that misses can still alert the city.

The common defence path at `$823F` masks the type flags with `$20`, the mobile bit. At `$8244` it ORs that result with `$03BF`. A zero result returns immediately. A fixed gun needs a nonzero city latch, while the mobile bit can carry a hunter through the same gate even with the latch clear.

## A fixed gun and a hunter

The [record dispatcher](../source/routines/ai-dispatch.md) checks the record's active status. The fixed defence path at `$81F3` and the mobile path at `$8104` both use the low nibble of the behaviour byte to index the class tables.

| Example type | Flags | Behaviour | Class range | Fire threshold | Counter reload mask |
| --- | --- | --- | --- | --- | --- |
| Fixed defence, type 12 | `$40` | `$06` | 9 cells | 48 | `$07` |
| Armed hunter, type 3 | `$61` | `$02` | 11 cells | 42 | `$07` |

The range check uses record byte 13, the whole-cell part of the cached distance, and requires it to be strictly below the class limit. A type-12 defence eight cells away can fire once provoked. At nine whole cells it takes the out-of-range return. A type-3 hunter can enter the common path with the latch clear, and its mobile routine can also move it using the class speed. The ranges, thresholds and masks are in [the type tables](../reference/type-tables.md).

## Counting up to a shot

The ordinary firing path at `$82C0` increments record byte 9 and masks the value with `$3F`. If the latched sensor count at `$0374` is nonzero, the code doubles the comparison value at `$82D0`. With a counter starting at zero, the type-12 example reaches 48 after 48 eligible updates on its ordinary path, or 24 with a sensor. The stored counter still advances by one.

On reaching the threshold, `$82D7` reloads the counter from a random byte ANDed with the class mask. For a `$07` mask that starts the next count somewhere from 0 to 7. The firing path then either reaches the direct-damage routine at `$8347` or, for behaviour bytes with bit 7 set, tests another random byte against the class missile threshold. A high enough roll and a free slot on page `$10` let it create a type-11 robot missile.

## When a defence answers a missile

Behaviour bit 6 enables a separate response. If the player has already set the record's missile-lock bit, the code at `$8272` diverts to the counter check against `$18`. That path reuses byte 9, so the time to respond depends on the counter value the record had when the lock arrived. On reaching the threshold it clears the lock and calls the AMM routine at `$4838`.

The AMM sweep marks live missile records of both sides as dying. A defender can therefore remove the player's incoming missile and other missiles already in play. See [From scanner blip to missile lock](from-scanner-blip-to-missile-lock.md) for the write that starts the response, and [Clear all missiles](../source/routines/clear-missiles.md) for the sweep.

[Back to Deep Dives](index.md)
