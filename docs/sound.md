# Sound System

Three voices, sixteen twelve-byte records, a state machine carried in a register, and no music.

---

Everything audible in Tau Ceti comes out of one routine and its two helpers. There is no music
player, no filter sweep and no sound queue: an effect is a record of twelve bytes, and the game
decides what the SID does by carrying a state around in the accumulator.

That last part is the design worth knowing. `$8759` is entered with the effect number in `A`, and the
*value* of `A` is the whole state machine:

| `A` | meaning |
|---|---|
| `$00-$3F` | start effect `A` now |
| `$40-$7F` | effect `A & $3F` is running: advance it one frame |
| `$80-$FF` | do nothing, return `A` |

and the caller writes the return value straight back into the slot variable. So `$03C4` and `$03C5`
each hold either "start this effect", "this effect is running" or `$FF` for idle, and the player has
no other memory of what it was doing.

## Who owns which voice

| SID | base | owner | state |
|---|---|---|---|
| voice 0 | `$D400` | effect slot `$03C4` | `$0111-$011E` |
| voice 1 | `$D407` | effect slot `$03C5` | `$0121-$012E` |
| voice 2 | `$D40E` | **engine noise**, no slot | none: driven from `$0353` |

`$86F8` is the frame tick, and it is called from the raster handlers at `$4A0C`, `$4A50` and `$4A87`

- all three end `JMP $86F8` - so the SID is updated exactly once per frame, at 50 Hz, whatever else
the game is doing.

```text
$86F8  if ($0396 | $0395) != 0:          landed, docked or waiting for a key
$8702      $D412 = 0                     voice 2 off
$8705      goto $873E                    skip the engine, do the effects
$8708  $D413 = 0, $D414 = $1C            voice 2 envelope
$8712  A = $0353                         the altitude track
$8715  $D412 = $81 if A != 0 else $80    gate plus noise
$8724  $D40E = (A << 3) & $FF            frequency low, overflow into $03C3
$8733  $D40F = ($03C3 & 7) + 2
$873E  $03C4 = $8759($03C4, X=0,  Y=0)   voice 0
$874B  $03C5 = $8759($03C5, X=$10, Y=7)  voice 1
```

Voice 2 is the engine, and its pitch is not a separate variable at all: it is `$0353`, the same byte
that feeds gauge 5 on the instrument panel. The number that draws the fifth bar is the number the SID
turns into engine noise, which is why the engine rises when the gauge rises and why there is nothing
to model separately.

When the ship is landed or docked - `$0396` non-zero, or `$0395` holding a wait-for-key - voice 2 gets
`$D412 = 0` and **no frequency writes at all**. The effects keep running.

## The silence routine

`$86DB` is called on reset, from `$582E`, and it is where the attract mode gets its silence:

```text
$86DB  for X = $17..0: $D400,X = 0        all 24 registers
$86E5  X = $0394 ; if X == 0: A = $0F     volume
$86EC  $D418 = A                          X != 0 -> volume 0
$86EF  $03C4 = $03C5 = $FF                both slots idle
```

The volume is written from `$0394`, so with the attract flag set the machine has no master volume
whatsoever. The demo is silent because the game decided it should be; a port that plays effects in the
attract mode is wrong in a way the original never was. (The zero comes from the clear loop's `A`, not
from `$0394` itself - a transcription that writes `$80` there gets a completely different sound.)

## The twelve-byte record

Sixteen of them sit at **$8812**, `$8812 + 12*effect`. Starting an effect copies the record into the
voice's state block and writes seven of the twelve bytes to the SID:

| byte | state | SID register | meaning |
|---|---|---|---|
| 0 | `$0111` | `$D400` | frequency low |
| 1 | `$0112` | `$D401` | frequency high |
| 2 | `$0113` | `$D402` | pulse width low |
| 3 | `$0114` | `$D403` | pulse width high |
| 4 | `$0115` | `$D404` | control: waveform and gate |
| 5 | `$0116` | `$D405` | attack / decay |
| 6 | `$0117` | `$D406` | sustain / release |
| 7 | `$0118` | - | frames between pitch steps |
| 8 | `$0119` | - | frequency delta low |
| 9 | `$011A` | - | frequency delta high |
| 10 | `$011B` | - | frame to drop the gate |
| 11 | `$011C` | - | frame to write control 0 |

The remaining state is two counters. `$011D` counts frames since the last pitch step and `$011E`
counts frames since the effect started:

```text
$87BE  $011D += 1
$87C4  if $011D < $0118: return A|$40        the only early exit
$87C9  $011D = 0
$87CE  $0111/$0112 += $0119/$011A            a 16-bit add, written to $D400/1
$87E7  $011E += 1
$87ED  if $011E >= $011B: control &= $FE      gate off
$87FD  if $011E >= $011C: control = 0, return $FF
```

Two consequences follow and both are easy to get wrong.

**The gate and the kill are only tested on a frame where the pitch steps.** The two counters share
the step rate: with a long step (`$0118` large), an effect whose gate frame passes between steps
never gates off - it runs straight to its kill frame. That is not a bug in a port; it is what the
machine does, and an effect list that sounds slightly different is usually this.

**The frequency is an accumulator.** There is no bound: the last step of an effect is clamped by
16-bit wrap, not by anything the effect knows about.

## The sixteen effects

The bytes are read from the image; what they sound like is inferred from the register values, and the
event column comes from a byte scan of every store to `$03C4`/`$03C5`.

| # | wave | per / delta | gate / kill | what it is | pushed by |
|---|---|---|---|---|---|
| `$00` | noise | 1 / 0 | `80` / `80` | a 30 Hz thud | every impact, and a touchdown |
| `$01` | noise | 1 / `+$0980` | `40` / `80` | rising noise | the flare |
| `$02` | pulse | 1 / `+$4080` | `40` / `80` | fast rising pulse | anti-missile detonation |
| `$03` | triangle | 1 / 0 | `50` / `80` | short 1.2 kHz blip | key press on the KEYS screen |
| `$04` | noise | 1 / 0 | `50` / `80` | 75 Hz noise | an object destroyed |
| `$05` | noise | 1 / `-$0080` | `50` / `80` | falling noise from 481 Hz | the missile |
| `$06` | noise | 1 / `-$0080` | `50` / `80` | the same an octave up | a robot projectile |
| `$07` | noise | 4 / `+$0080` | `10` / `FF` | slow rise | jump acceleration |
| `$08` | noise | 2 / `-$0080` | `10` / `E0` | fast fall | jump deceleration |
| `$09` | noise | 4 / 0 | `20` / `60` | 1.2 kHz noise | the reactor room |
| `$0A` | noise | 4 / `+$0004` | `80` / `80` | 37 Hz slow rise | touchdown |
| `$0B` | noise | 1 / 0 | `50` / `80` | 120 Hz noise | a hit that does not kill |
| `$0C` | triangle | 1 / 0 | `FF` / `FF` | 56 Hz knock | entering RODS |
| `$0D` | triangle | 1 / 0 | `FF` / `FF` | the same, 8 units up | entering REACTOR |
| `$0E` | noise | 1 / `-$0301` | `10` / `10` | 733 Hz falling fast | **the laser** |
| `$0F` | - | - | - | designed silence | muting a voice |

Ten of the sixteen are used in play, and two of those - `$00` and `$04`, impact and explosion - are
the workhorses. `$0F` is not an effect at all: it is the record you push when you want a voice quiet,
which is what LOAD does to both slots.

The laser is worth a line, because the manual and the box art both suggest something grander. It is
effect `$0E`: noise, a fixed falling step of `-$0301` per frame, gate off after 16 frames and control
zero after 16, started by the fire path at `$3423` which also sets `$036E = $80` and `$03BF = $80`.
A short fall of noise. The "photon" is a word on the inlay.

## Where the sounds come from

| effect | site | event |
|---|---|---|
| `$00` + `$04` | `$2C9E`/`$2CA3` | touchdown on a pad |
| `$00` + `$0B` | `$460A`/`$460F` | the ship hits an object |
| `$0B` | `$461A` | an object is damaged and survives |
| `$04` | `$4967` | an object is destroyed |
| `$0E` | `$3423` | the laser |
| `$01` | `$3B4C` | the flare |
| `$05` | `$48A3` | missile launch |
| `$02` + `$0B` | `$483F`/`$4862` | anti-missile detonation |
| `$0A` | `$382B` | touchdown with the altitude at zero |
| `$03` | `$53F4`, `$5422` | KEYS: cursor move, and a rebind |
| `$07`, `$08` | `$67D6`, `$67F8` | the jump screen |
| `$0C`, `$0D`, `$09` | `$768F`, `$76C0`, `$76B1` | RODS and REACTOR screens |
| `$0F` | `$69F5` | LOAD: silence both voices |
| `$06` | `$8310` | a robot fires |
| `$00`, `$04` | `$8236`, `$823B` | the mine |

Each effect replaces whatever the slot was playing. There is no queue and no priority: starting a
second effect on the same voice cuts the first one off mid-fall, which is why a burst of hits sounds
like one hit.

## The music player that is not one

There is a routine at **$35F6** that looks, in a listing, exactly like a music sequencer. It has a
tempo byte (`$0397`, copied from `$0378`), eight per-channel countdown timers at `$FF66-$FF75` with
their toggling flags at `$FF76`, a reload on the rising edge and a fire on a threshold, a stream of
records with a "continue" form and an "urgent" bit, and an inner loop that renders three eight-byte
glyphs into a 64-byte block per channel at `$CA00 + channel*64`. Its note bytes are multiplied by
eight and read from the font at `$9000`.

It is not a music player, and the proof is a scan of the whole image:

- every write to `$D400-$D418` in the program is inside `$86DF-$8807`. Nothing else touches the SID.
- nothing in the image reads `$CA00` through an indirect pointer: `LDA ($20),Y` occurs zero times,
  and the only absolute references to `$CA00`/`$CB00` are the two initialising stores.

So the routine interprets a stream, times it, and paints glyphs into a buffer that the CPU never
reads. That is what a *dead* music engine looks like - and it is also exactly what a scrolling banner
looks like, because the buffer it writes is eight 64-byte sprite blocks and the VIC reads them through
the sprite pointers at `$CFF8` without the CPU's help.

It is the banner. The "notes" are characters, the "chords" are three glyphs side by side in one
double-width sprite, the eight "channels" are the eight sprites, and the "tempo" is the scroll step.
[The Border Banner](border-banner.md) has the routine from the other side: the same `$35F6` is what
refills a sprite that has just left the screen, three characters at a time. Reading the picture back
confirms it - the blocks in a captured frame hold `ste`, `m h`, `ad `, `tak`, `en `, `ove`, `r. `,
the tail of `...system had taken over.`, which is paragraph 5 of the ticker text at `$C143`.

The lesson for a port is not "the sequencer is dead" but "there is no music": the game's only SID
writes are the effect player and the engine, and the routine that looks like a soundtrack is drawing
the crawl.

## What else is not there

- **The filter.** Nothing writes the cutoff and resonance at `$D415-$D417`, and `$D418` is written only
  for its volume nibble - bits 4-7, which would switch the filter and its voices on, are never set. The
  "low-pass filter for atmosphere" that an earlier version of this chapter described is not in the code.
- **Music.** See above. The game has no tune, and the attract mode has no sound at all.
- **Per-voice envelope shapes.** Attack/decay and sustain/release are copied straight from the record;
  the SID applies its own exponential rates from there.

> [!NOTE]
> **What this corrects.** The previous version of this chapter was a set of invented parameter sheets:
> a laser on voice 1 with a triangle sweep, a missile on voice 2 with a sawtooth, a flare and an
> explosion on a "voice 3" that the SID does not have. Every row was wrong, including the voice
> numbers. The real thing is a table of sixteen records, two effect slots and an engine, and the
> effects that most sound like the manual's descriptions - laser, flare, missile - are all noise with
> a frequency step, not sweeps of a triangle.

---

[Back to the overview](../README.md)
