# Source guide

The pages are generated from the original listing bytes and curated code ranges. The labels and summaries explain how the routines fit into the game.

## How to read a listing

Each line is an instruction: its address, its bytes, the mnemonic and operand, and a comment where a routine or variable has a known name. A routine can include additional code blocks at separate addresses.

`Called by` lists direct `JSR` and `JMP` instructions from the curated code ranges that land on an instruction in the routine. Coverage grows as more code ranges are reviewed. Indirect jumps and fall-through paths are outside the scope of this index.

## Routines

### Flight

| Routine | Address | What it does |
| --- | --- | --- |
| [`Frame tick: clock, shield and fuel`](routines/frame-tick.md) | `$25D3` | A BCD counter at `$0340` counts 50 frames to a second, then the BCD clock at `$0341`-`$0343` advances. When `$0396` is zero, the shield regenerates and the routine updates the fuel at `$0345`/`$0346`. In the air it subtracts (speed >> 3) + 16, plus 96 for a ruptured tank. At altitude zero it subtracts 96 for a ruptured tank or 256 for an intact tank because the computed zero burn takes the same carry path. A high byte of `$20` raises the LOW FUEL flag. On underflow the routine clears only the high byte and increments `$03A3`. |
| [`New-game state reset`](routines/new-game-reset.md) | `$5766` | Clears the counters, clock and target pointers, then lays out a fresh ship at `$57F0`: altitude 28, shield and fuel full (`$BF`), eight missiles, flares and AMMs, laser heat zero. |
| [`Low-fuel watch and the stranded state`](routines/low-fuel-watch.md) | `$586C` | Called every frame. Queues LOW FUEL once when `$03A2` is set and NO FUEL once when `$03A3` is set. If the tank is empty, altitude and speed are both zero, it sets `$0396` to 1; LAUNCH treats that stranded state differently from a normal dock (`$0396` = `$80`). |

### Docking

| Routine | Address | What it does |
| --- | --- | --- |
| [`Object distance and the docking test`](routines/docking-test.md) | `$2B60` | Works out the distance to the record in `$61`/`$62`, scales it through the tables at `$C800`/`$C900` and stores the product in bytes 12/13. Only a product under 128 is close enough to dock; anything up to 4,095 is added to the target list, and anything larger is dropped. For a close record, type 16 docks as a jump pad before anything else. A dockable building must pass \|altitude - 28\| + 55 < aperture, then a bearing test of 2 * (\|bearing offset\| + 28) against the same aperture - at the full 72-point opening that is an offset of at most 7 steps of the 512-step circle, about 5 degrees. Passing both sets `$0396` = `$80` and copies the building's type and cell to `$03A4`/`$0398`/`$0399`. |

### Records

| Routine | Address | What it does |
| --- | --- | --- |
| [`City loader: the sheet at $9400 into the record table`](routines/city-loader.md) | `$27EC` | Rebuilds the 48-record table at `$0E00` for the city index in `$0354`. The pointer builder at `$27EC` multiplies the index by three and then shifts right three times, which is exactly a stride of 96 bytes: `$9400` + city × `$60`. The loop copies up to 32 three-byte records (type, x, y) from that sheet, stopping at a type byte of `$C0`, zeroes bytes 3-15 of each record, and copies hit points from `$C3BF`[type & `$3F`] into byte 7. It then scans the city's four bytes at `$8900`, which hold jump destinations (a byte of `$80` or more is empty), and appends a pair of pad records for each one from the four shared templates at `$C4BE` + n × 8. Whatever space is left in the table is filled with type `$C0`, and the provocation latch at `$03BF` is cleared. |
| [`City save: writing damage back to the sheet`](routines/city-save.md) | `$28E6` | Called before a jump (`$51C5`) and from `$6A77`. Walks the city sheet at `$9400` and the loaded record table at `$0E00` in step, copying one byte per record — byte 0 — from the record back into the sheet. Types whose flags at `$C39A` hold both the mobile and armed bits (`$60`: types 3, 6, 9, 20 and 21) are skipped, so the armed mobile units always return. A destroyed building has already been marked type \| `$80` by the dying animation, so it is written back as free and stays destroyed on the next visit. |
| [`City restore: stripping the state bits`](routines/city-restore.md) | `$2921` | Called by the new-game reset at `$5863`. Walks all twelve pages of the city sheet area from `$9400` and masks every byte that is not `$C0` with `$3F`, clearing the `$80` and `$40` state bits from every record. Since a destroyed record keeps its type under the free bit, this restores every city exactly: `$93` becomes `$13` again. The `$C0` fillers are skipped because masking them would create type-0 buildings. |
| [`Record scan`](routines/record-scan.md) | `$43CF` | Walks the 48 sixteen-byte records at `$0E00`-`$10FF`. Byte 0 sorts them: `$80` is free and skipped, `$40` is dying and goes to the death animation, anything else is live and goes to the dispatcher at `$445D`. At the end of the sweep the game rotates the 6-bit round-robin index at `$038F` and advances its frame counters. |
| [`Dying animation`](routines/dying.md) | `$441E` | Byte 6 falls by 8 a frame; when it reaches zero, byte 8 climbs by 8 a frame. At `$F8` the record is freed. Types carrying bit 0 of `$C39A` (including both missile types) are freed at `$78` instead, after 15 frames rather than 31. |
| [`Live-record dispatch`](routines/live-dispatch.md) | `$445D` | Sorts a live record by its per-type flags at `$C39A`. Dockable types (bit 7) go to the aperture and docking path at `$4465`; sensor types (bit 1) are counted when in range at `$44A1`; everything else falls through to the guided-object and robot handlers. |
| [`Aperture animation`](routines/aperture.md) | `$4465` | Dockable buildings only, and only while byte 3 bit 6 says the record is active. A missile lock (bit 4) or a hit (bit 5) shuts the iris two points a frame, except on type 27; otherwise it shuts while the scaled distance byte 13 is 2 or more, and opens two points a frame to `$48` while byte 13 is below 2. The door takes 36 frames to travel from shut to fully open. |
| [`Sensor records`](routines/sensors.md) | `$44A1` | For records whose type flags carry bit 1. An in-range sensor (byte 3 bit 6, distance under 9 cells) is counted at `$0373` and sets bit 7 of `$03B0`, which is what the scanner uses to know a contact is live. |
| [`Guided-object handling`](routines/guided-objects.md) | `$44C4` | Reached from the dispatcher when a live record is neither dockable nor a sensor. Missiles and other guided objects take their target from bytes 14/15, publish their state to the eight-byte block at `$FFC0`, and run the homing and detonation logic that follows. |
| [`Robot dispatch`](routines/ai-dispatch.md) | `$4620` | A live record that is out of range has its moved/aimed bits cleared and is left alone. In range, the type flags choose the brain: bit 6 calls the static defence AI at `$81F3`, bit 5 calls the mobile unit AI at `$80C3`. |

### Combat

| Routine | Address | What it does |
| --- | --- | --- |
| [`Laser fire`](routines/laser-fire.md) | `$33F9` | Checks that no bolt is in flight (`$036E`), heat is below `$B0` and the laser is enabled (`$0370`), then checks the fire input. Firing sets the bolt timer to `$80`, latches provocation in `$03BF`, requests the shot sound and adds `$0C` to the heat at `$0347`, capped at `$BF`. The target is tested later when the bolt finishes. |
| [`Flag-bit test`](routines/bit-test.md) | `$3D18` | Tests one bit of the eight-byte mask at `$034A`-`$0351`. A holds the bit index: X = A >> 3 selects the byte from `$034A`, and the low three bits index the mask table at `$3D28`. Returns with Z set when the bit is clear. |
| [`Laser bolt: timer and hit`](routines/laser-bolt.md) | `$3D41` | Counts the bolt's flight in the low seven bits of `$036E`. At 22 frames it clears the bolt colour, resets `$036E` and resolves the shot against `$038C`/`$038D`: exactly one target, only if still alive, takes 4 points through the damage routine at `$4951` and gets byte 3 bit 5 set. |
| [`Clear all missiles (AMM)`](routines/clear-missiles.md) | `$4838` | Walks the record table and marks every missile record dying - the player's type 10 and the robots' type 11 alike. Nothing else is touched: the selected target in `$0388`/`$0389` survives, as does the target's lock bit. Both missile types are freed after 15 frames. |
| [`Player missile launch`](routines/player-missile.md) | `$4878` | Refuses to fire at `$0389` = 0 (no target). Otherwise finds a free record, makes it type 10, copies the ship's cell and sub-cell, sets byte 6 to altitude + `$40`, points bytes 14/15 at the target, sets the target's lock bit (byte 3 bit 4) and decrements the missile count at `$0358`. |
| [`Damage`](routines/damage.md) | `$4951` | Shared by lasers and everything else. Subtracts the damage in A from byte 7. On underflow it clears byte 8, sets the death sound counter, marks byte 0 dying, and for armed types adds one to the 16-bit kill count at `$03A5`/`$03A6`. Finally it sets `$0359` = `$FF` for the screen flash. A record whose byte 7 is already negative is immune. |
| [`Mobile unit AI`](routines/mobile-ai.md) | `$80C3` | Dispatched from `$4620` for records whose type flags carry bit 5. Types 36 and 21 bob between two altitudes first, flipping byte 3 bit 0; every mobile then runs the class-range test, closes on the ship and fires. Out of range it clears byte 8 and returns. |
| [`Static defence AI`](routines/static-defence-ai.md) | `$81F3` | Static defence AI. Type flags bit 5 (mobile units) always run; everyone else runs only while the provocation latch `$03BF` is set. Out of class range it does nothing. In range it sets byte 3 bit 3, answers a player lock with an AMM after 24 frames (clearing its own lock first), and otherwise counts byte 9 against the fire interval at `$C45E`. A random roll masked by `$C44E` reloads the counter; behaviour bit 7 units also roll against `$C46E` and, on success, take a free record from `$1000` and spawn a missile into it. Type 26 has an early path of its own at `$8202`. Movement ends at `$8347`. |

### Messages

| Routine | Address | What it does |
| --- | --- | --- |
| [`Message queue`](routines/message-queue.md) | `$4127` | Pushes a two-byte text pointer into the ring buffer at `$0C00`: A is the low byte, X the high, and `$0384` is the write cursor. Does not print; the printer drains the queue separately. |
| [`Message text renderer`](routines/message-printer.md) | `$41F7` | Reads one character code at a time from the pointer in `$1C`/`$1D`. Codes under `$80` select an 8-byte glyph from the game's own font at `$9000`-`$92FF` (32 glyphs a page); `$80` is a control code, and `$FF` ends the string. The glyph is copied into the character/sprite buffer at `$FCC8`. |

## Variables

The zero-page and low-memory values these routines share are listed in [Variables](variables.md).

*Generated by `tools/build_source.py`.*

[Back to the guide](../index.md)
