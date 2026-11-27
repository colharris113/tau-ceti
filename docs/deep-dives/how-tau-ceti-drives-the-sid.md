# How Tau Ceti drives the SID

The engine noise follows the throttle. A laser shot has a brief pitch sweep of its own. The C64 keeps these jobs apart by assigning the engine to SID voice 3 and running the sound effects through the other two voices.

## Voice 3 follows speed

The sound update at `$86F8` checks the dock state at `$0396` and the flag at `$0395`. If either is set, the routine writes zero to the engine voice's control register at `$D412` and goes on to the effects. Otherwise it reads speed from `$0353`.

At speed zero it writes `$80` to the control register, selecting the noise waveform with the gate clear. Positive speed writes `$81`, which selects noise and opens the gate. At `$8724` three shifts multiply speed by eight. The shifted-out bits enter the high byte, and the code adds two to that byte before writing it to `$D40F`. [Commodore 64 Programmer’s Reference Guide, SID register map](https://www.commodore.ca/manuals/c64_programmers_reference/c64-programmers_reference_guide-05-basic_to_machine_language.pdf)

| Speed | Frequency word | Gate |
| --- | --- | --- |
| 0 | `$0200` | Clear |
| 64 | `$0400` | Set |
| 191 | `$07F8` | Set |

The low byte goes to `$D40E` and the high byte to `$D40F`. These are frequency-register values, so the engine routine can update the pitch with three shifts and two writes. The flight interrupt calls the driver through the handler at `$4A1F`. See [One frame in the skimmer](one-frame-in-the-skimmer.md) for its place in the raster schedule.

## A laser shot starts with one byte

The [laser fire routine](../source/routines/laser-fire.md) writes effect number `$0E` to `$03C4`. At `$873E`, the sound driver reads it and selects the first voice. A second call reads `$03C5` for voice 2, using SID register offsets seven bytes higher.

A new effect number is multiplied by twelve at `$8763`. The result indexes the parameter table at `$8812`, so laser effect `$0E` starts at `$88BA`. The twelve bytes are copied into RAM at `$0111` for voice 1. Seven supply the SID registers and five control the effect's progression.

| Laser row bytes | Use |
| --- | --- |
| `C0 30` | Initial frequency word `$30C0` |
| `00 04` | Pulse-width register bytes |
| `81` | Noise waveform with the gate set |
| `14 40` | Attack/decay and sustain/release registers |
| `01 FF FC 10 10` | Pitch step every update, a step of `$FCFF`, and gate-off and stop counts of sixteen |

## How the sweep ends

The effect update at `$87BE` increments a divider and waits until it reaches the effect's step interval. On a step it adds the two pitch-delta bytes to the frequency word and writes the result back to SID. For the laser, the first step takes `$30C0` to `$2DBF`. As a signed sixteen-bit delta, `$FCFF` is −769, so each step lowers the noise frequency.

At the gate-off count, the routine clears bit 0 of the saved control byte. At the stop count it writes zero to that control register and returns `$FF` as the effect state. A negative state exits the effect routine immediately. While a sound is running, the driver returns the effect number with bit 6 set, so on the next update it continues the sweep without reloading the table row.

That gives gameplay a compact interface to sound. A laser or a collision can write an effect number and carry on. The raster-driven sound code keeps the engine responsive while it steps through the effects in the background.

[Back to Deep Dives](index.md)
