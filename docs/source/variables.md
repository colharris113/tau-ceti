# Variables

<p class="lede">The game keeps almost everything in the zero page and the first few pages of RAM. These are the values the routines in this guide read and write; names are ours, addresses are the game's.</p>

## Flight

| Address | Name | Notes |
| --- | --- | --- |
| <code class="addr">$0338</code> | **Launch heading (low)** | Low eight bits of the ship's heading. LAUNCH adds <code class="addr">$20</code> - 32 steps of 512, or 22.5 degrees - and carries into <code class="addr">$0339</code>. |
| <code class="addr">$0339</code> | **Launch heading (high)** | Ninth bit of the heading; toggled on launch so the 22.5-degree step wraps correctly. |
| <code class="addr">$0340</code> | **Frame counter** | BCD counter of frames within the second, 0-<code class="addr">$49</code>. At <code class="addr">$50</code> the clock ticks. |
| <code class="addr">$0341</code> | **Seconds** | BCD seconds, 0-<code class="addr">$59</code>. |
| <code class="addr">$0342</code> | **Minutes** | BCD minutes, 0-<code class="addr">$59</code>. |
| <code class="addr">$0343</code> | **Hours** | BCD hours, 0-<code class="addr">$23</code>. |
| <code class="addr">$0344</code> | **Altitude** | 0-<code class="addr">$BF</code>. Zero is the ground; docking altitude is 28 (<code class="addr">$1C</code>). |
| <code class="addr">$0345</code> | **Fuel (low byte)** | Low byte of the 16-bit fuel value. The pair is decremented directly by the burn amount. |
| <code class="addr">$0346</code> | **Fuel (whole units)** | High byte of the fuel value. Full is <code class="addr">$BF</code>, just under 192 units; LAUNCH refuses at zero. |
| <code class="addr">$0353</code> | **Speed** | 0-<code class="addr">$BF</code>. Divided by 8 to get the fuel burn, and tested for zero when deciding the ship is at rest. |
| <code class="addr">$0377</code> | **Shield** | 0-<code class="addr">$BF</code>, full at the start of a game. Regenerates one point a second while airborne and not docked. |
| <code class="addr">$039E</code> | **Tank ruptured** | Non-zero adds 96 to the per-second fuel burn. |
| <code class="addr">$03A2</code> | **LOW FUEL flag** | Set once when the fuel high byte reaches <code class="addr">$20</code>; the watch routine prints the message for value 1 and then increments it. |
| <code class="addr">$03A3</code> | **NO FUEL flag** | Set when fuel underflows. Also drives the stranded state on the ground. |

## Docking

| Address | Name | Notes |
| --- | --- | --- |
| <code class="addr">$0381</code> | **Dock refused** | Set to <code class="addr">$FF</code> when a docking attempt fails the altitude or aim test. |
| <code class="addr">$0396</code> | **Dock state** | 0 in flight, <code class="addr">$80</code> after a normal dock, 1 when stranded with an empty tank on the ground. |
| <code class="addr">$0398</code> | **Docked cell (low)** | Low byte of the docked building's cell, copied on docking and used as the ship's position on launch. |
| <code class="addr">$0399</code> | **Docked cell (high)** | High byte of the docked building's cell. |
| <code class="addr">$039B</code> | **Jump pad docked** | Set to <code class="addr">$FF</code> when the docked building is type 16, the jump pad. |
| <code class="addr">$03A4</code> | **Docked type** | Record byte 0 of the docked building, copied at <code class="addr">$2C4E</code>. |

## Combat

| Address | Name | Notes |
| --- | --- | --- |
| <code class="addr">$0347</code> | **Laser heat** | 0-<code class="addr">$BF</code>. Each shot adds <code class="addr">$0C</code>; at <code class="addr">$B0</code> or above the laser will not fire. |
| <code class="addr">$034A</code> | **Flag mask** | Eight bytes, 64 bits, tested by the helper at <code class="addr">$3D18</code>. |
| <code class="addr">$0358</code> | **Missiles** | Missile count, eight at the start of a game; decremented by a launch. |
| <code class="addr">$036E</code> | **Bolt timer** | Zero when the laser is ready. Firing sets <code class="addr">$80</code>; the low seven bits then count the bolt's 22-frame flight. |
| <code class="addr">$0370</code> | **Laser lockout** | While non-zero the laser cannot fire. |
| <code class="addr">$0386</code> | **Last on-screen target** | Pointer to the record most recently drawn or seen on the main view. |
| <code class="addr">$0388</code> | **Missile target** | Pointer the missile launch routine reads. Zero means no lock; cleared on a new game and after a jump. |
| <code class="addr">$038A</code> | **Scanner target** | Pointer to the record selected on the scanner. |
| <code class="addr">$038C</code> | **Laser target** | Pointer resolved when the bolt lands; the hit goes to this record and no other. |
| <code class="addr">$03A5</code> | **Kill count (low)** | Incremented by the damage routine for every armed type destroyed. |
| <code class="addr">$03A6</code> | **Kill count (high)** | High byte of the kill count. |
| <code class="addr">$03BF</code> | **Provocation latch** | Set by a laser (<code class="addr">$341E</code>) or a missile launch (<code class="addr">$48F6</code>) and cleared when a city loads. Static defences ignore the ship until it is set. |

## Messages

| Address | Name | Notes |
| --- | --- | --- |
| <code class="addr">$0383</code> | **Message read cursor** | Next slot in the <code class="addr">$0C00</code> ring buffer to print. |
| <code class="addr">$0384</code> | **Message write cursor** | Next slot in the <code class="addr">$0C00</code> ring buffer to fill. |

*Generated by `tools/build_source.py`.*
