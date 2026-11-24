# Type tables

<p class="lede">Every object in the game is one of 37 types. Four parallel per-type tables in the $C39A-$C408 block say what each type is; five sixteen-byte class tables below them decide how it fights. The record table copies the values it needs when an object spawns.</p>

These tables were extracted mechanically from the game image by `tools/extract_tables.py`. The interpretations below come from the routines that read them.

## The per-type tables

`$C39A` flags, `$C3BF` starting hit points (record byte 7), `$C3E4` the altitude allowance used when aiming a missile, and `$C409` the behaviour byte. A type index is the low six bits of record byte 0.

| Type | Flags | Bits | Hit points | Altitude allowance | Behaviour | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| $00 (0) | $00 | none | 20 | 254 | $FF — unused ($FF) |  |
| $01 (1) | $00 | none | 16 | 252 | $FF — unused ($FF) |  |
| $02 (2) | $40 | armed | 48 | 255 ($FF) | $C5 — missile, AMM; class 5 |  |
| $03 (3) | $61 | quick death, mobile, armed | 32 | 70 | $02 — class 2 | mobile armed unit |
| $04 (4) | $00 | none | 64 | 249 | $FF — unused ($FF) |  |
| $05 (5) | $00 | none | 12 | 241 | $FF — unused ($FF) |  |
| $06 (6) | $61 | quick death, mobile, armed | 40 | 58 | $03 — class 3 |  |
| $07 (7) | $02 | sensor | 24 | 254 | $FF — unused ($FF) | sensor |
| $08 (8) | $02 | sensor | 24 | 254 | $FF — unused ($FF) | sensor |
| $09 (9) | $61 | quick death, mobile, armed | 52 | 75 | $44 — AMM; class 4 |  |
| $0A (10) | $09 | quick death, player missile | 1 | 74 | $FF — unused ($FF) | player missile |
| $0B (11) | $05 | quick death, robot missile | 1 | 76 | $FF — unused ($FF) | robot missile |
| $0C (12) | $40 | armed | 24 | 255 ($FF) | $06 — class 6 |  |
| $0D (13) | $00 | none | 16 | 255 ($FF) | $FF — unused ($FF) |  |
| $0E (14) | $00 | none | 8 | 255 ($FF) | $FF — unused ($FF) |  |
| $0F (15) | $00 | none | 16 | 255 ($FF) | $FF — unused ($FF) |  |
| $10 (16) | $01 | quick death | 255 ($FF) | 28 | $FF — unused ($FF) | jump pad (handled before the dockable flag test at $2BE0) |
| $11 (17) | $40 | armed | 20 | 255 ($FF) | $07 — class 7 |  |
| $12 (18) | $00 | none | 16 | 255 ($FF) | $FF — unused ($FF) |  |
| $13 (19) | $00 | none | 20 | 255 ($FF) | $FF — unused ($FF) |  |
| $14 (20) | $61 | quick death, mobile, armed | 24 | 71 | $01 — class 1 |  |
| $15 (21) | $61 | quick death, mobile, armed | 28 | 159 | $00 — class 0 | mobile unit |
| $16 (22) | $40 | armed | 8 | 184 | $C8 — missile, AMM; class 8 |  |
| $17 (23) | $00 | none | 96 | 255 ($FF) | $FF — unused ($FF) |  |
| $18 (24) | $41 | quick death, armed | 32 | 168 | $29 — type-24 gate; class 9 | type-24 gun (behaviour bit 5 gate at $82B1) |
| $19 (25) | $02 | sensor | 24 | 171 | $FF — unused ($FF) | sensor |
| $1A (26) | $41 | quick death, armed | 1 | 72 | $0A — class 10 | special early path at $8202 |
| $1B (27) | $80 | dockable | 255 ($FF) | 255 ($FF) | $FF — unused ($FF) | Gal-Corp lander |
| $1C (28) | $80 | dockable | 255 ($FF) | 255 ($FF) | $FF — unused ($FF) | Central reactor |
| $1D (29) | $80 | dockable | 255 ($FF) | 205 | $FF — unused ($FF) | reactor substation |
| $1E (30) | $80 | dockable | 255 ($FF) | 205 | $FF — unused ($FF) | civilian supply centre |
| $1F (31) | $80 | dockable | 255 ($FF) | 255 ($FF) | $FF — unused ($FF) | military supply centre |
| $20 (32) | $00 | none | 20 | 200 | $FF — unused ($FF) |  |
| $21 (33) | $00 | none | 127 | 253 | $FF — unused ($FF) |  |
| $22 (34) | $00 | none | 127 | 253 | $FF — unused ($FF) |  |
| $23 (35) | $00 | none | 20 | 200 | $FF — unused ($FF) |  |
| $24 (36) | $20 | mobile | 16 | 159 | $FF — unused ($FF) | mobile unit |

A hit-point or altitude allowance of 255 is usually a marker that the type is not a target in the ordinary sense; the dockable structures all sit at $FF.

## Flag bits

| Bit | Value | Meaning | Read by |
| --- | --- | --- | --- |
| 0 | $01 | Quick death: the record is freed at $78 after 15 frames | $4445, $444C |
| 1 | $02 | Sensor record | $44A1 |
| 2 | $04 | Robot missile | $44C4 |
| 3 | $08 | Player missile | $44C4 |
| 5 | $20 | Mobile unit | $4620, $823F |
| 6 | $40 | Armed | $4620, $4975 |
| 7 | $80 | Dockable | $2BFA, $4463 |

Bit 4 is never set in the table. Bit 0 is what produces the 15-frame death animation for missiles and the 31-frame one for most robots.

## Behaviour bits

The behaviour byte at `$C409` is read by both AI routines.

| Bit | Value | Meaning |
| --- | --- | --- |
| 7 | $80 | The unit may launch a missile |
| 6 | $40 | The unit may answer a lock with an AMM |
| 5 | $20 | Fire only when locked or already hit (the type-24 gate at $82B1) |
| 0-3 | $0F | AI class: indexes the five tables below |

## The five class tables

The low nibble of the behaviour byte picks a row from five sixteen-byte tables. Range is in cells, speed is in 1/256 cell a frame, the mask is ANDed with a random byte when the fire counter reloads, the tick table sets the interval, and the threshold is the roll a missile-capable unit must beat.

| Class | Range ($C42E) | Speed ($C43E) | Fire mask ($C44E) | Fire ticks ($C45E) | Missile threshold ($C46E) | Types |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 8 | 14 | 3 | 16 | 0 | $15 |
| 1 | 9 | 11 | 15 | 50 | 0 | $14 |
| 2 | 11 | 14 | 7 | 42 | 0 | $03 |
| 3 | 13 | 17 | 7 | 31 | 0 | $06 |
| 4 | 16 | 20 | 3 | 16 | 0 | $09 |
| 5 | 12 | 0 | 7 | 32 | 240 | $02 |
| 6 | 9 | 0 | 7 | 48 | 0 | $0C |
| 7 | 6 | 0 | 7 | 48 | 0 | $11 |
| 8 | 5 | 0 | 7 | 63 | 128 | $16 |
| 9 | 16 | 0 | 1 | 0 | 0 | $18 |
| 10 | 4 | 0 | 0 | 63 | 0 | $1A |

Only classes 0-10 are used. Class 11-15 are $FF placeholders; type 36 carries a behaviour byte of $FF, so its class is 15 and its range byte is 255 — the type is handled by the mobile AI's own early branch at $80C8 instead.

Class 5 (type $02) fires every 42 frames and has a missile threshold of 240, so it rarely launches. Class 8 (type $16) has a threshold of 128, so it launches a missile on about half its fire opportunities. Class 9 (type $18) has a fire interval of zero, which makes the gun fire whenever its gate opens.

*Generated by `tools/build_type_tables.py` from `sources/data/type_tables.json`.*
