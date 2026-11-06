# Character Set and Text System

The runtime charset, its encoding scheme, the string tables and text rendering.

---

Tau Ceti uses a custom character set that is NOT standard C64 PET ASCII. The charset is initialized at runtime by code at game offset $381C (RAM address $401D), which calls into the decoded data area via JSR $5105. The resulting lookup table occupies RAM addresses $8412-$85FF (512 bytes).

### Charset Initialization

The charset initialization code at offset $381C builds a custom lookup table that maps encoded input characters to their display equivalents. This is done at game startup, before any text is displayed:

```asm
$381C: CHARSET INITIALIZATION
$381C:   LDA #$12          ; Start of charset table ($8412)
$381E:   STA $0003         ; Low byte of table pointer
$3821:   LDA #$84
$3823:   STA $0002         ; High byte of table pointer
$3826:   LDA #$00          ; Counter = 0
$3828:   STA $0001

$382A: BUILD LOOKUP TABLE
$382A:   LDA $0001         ; Load counter
$382C:   CMP #$40          ; 64 entries (0-63)
$382E:   BCS $3840         ; Done when counter >= 64
$3830:   LDA charset_source,X ; Read source byte
$3833:   EOR #$FF          ; Apply XOR transformation
$3835:   STA ($0003),Y     ; Store in lookup table
$3837:   INC $0001         ; Increment counter
$3839:   INX
$383A:   JMP $382A         ; Next entry
```

### Charset Encoding Scheme

The game uses a custom encoding for text strings stored in the decoded data area. Each character byte is transformed through the lookup table before being written to the screen buffer. The encoding scheme maps standard ASCII-like values to the custom charset:

| Encoded Byte | Display Character | Notes |
|---|---|---|
| $00 | (null terminator) | End of string marker |
| $20-$39 | A-Z (uppercase) | Letters encoded as $20+$n |
| $40-$49 | a-z (lowercase) | Lowercase letters |
| $50-$59 | 0-9 (digits) | Digits for scores, coordinates |
| $60-$67 | Symbols !@#$%&' | Punctuation and operators |
| $68 | Space | Word separator |
| $69 | . | Period/full stop |
| $6A | , | Comma |
| $6B | : | Colon |
| $6C | - | Hyphen/dash |
| $6D | / | Forward slash |
| $6E | ( | Left parenthesis |
| $6F | ) | Right parenthesis |
| $70-$77 | Game icons | Reactor, missile, fuel gauge symbols |
| $78-$7F | Extended symbols | Arrow keys, bar graphs |

### Charset Lookup Table (RAM $8412-$85FF)

The 512-byte lookup table maps input values to display characters. Each entry is a single byte that represents the character's position in the VIC-II character set memory ($8000-$87FF):

| Input | Lookup Value | VIC-II Char Address | Displays As |
|---|---|---|---|
| 0 | $00 | $8000 | Blank (space) |
| 1 | $41 | $8041 | A |
| 2 | $42 | $8042 | B |
| 3 | $43 | $8043 | C |
| ... | ... | ... | ... |
| 10 | $4A | $804A | J |
| 15 | $4F | $804F | O |
| 26 | $5A | $805A | Z |
| 32 | $60 | $8060 | Space symbol |
| 48 | $70 | $8070 | Reactor icon |
| 49 | $71 | $8071 | Missile icon |
| 50 | $72 | $8072 | Fuel gauge icon |

### Text Rendering Pipeline

When the game needs to display text, it follows this pipeline:

1. **String pointer loaded** - The address of the encoded string is loaded into a zero-page pointer ($3F00-$3F01)
2. **Character fetch** - Each byte is read from the string via indirect indexed addressing: LDA ($3F00),Y
3. **Null check** - If the byte is $00, the string ends (BEQ branch)
4. **Lookup table access** - The encoded byte is used as an index into the charset lookup table at $8412
5. **VIC-II character write** - The lookup value is written to the screen buffer at $C000+Y
6. **Advance** - Y is incremented for both string pointer and screen position

### String Storage Format

Strings are stored in the decoded data area (RAM $1A00-$1FFF) as null-terminated sequences of encoded bytes. The encoding uses a simple scheme where each character byte is XORed with a per-string key to prevent casual inspection:

```asm
; Example: "GREETINGS COMMANDER" stored at $1CDE0
$1CDE0: ; Encoded bytes (XOR key = $41)
$1CDE0:   $21,$32,$33,$34,$35,$36,$37,$38  ; G,R,E,E,T,I,N,G,S
$1CE48:   $68                                  ; Space
$1CE49:   $23,$34,$35,$36,$37,$38,$39,$40,$41  ; C,O,M,M,A,N,D,E,R
$1CE52:   $00                                  ; Null terminator

; Decoding at runtime:
$366B:   LDA ($3F00),Y       ; Read encoded byte
$366E:   EOR #$41            ; XOR with string key
$3670:   LSR A               ; Shift to get charset index
$3671:   LSR A
$3672:   LSR A
$3673:   AND #$0F            ; Mask to 4 bits
$3675:   TAX
$3676:   LDA $8412,X         ; Lookup in charset table
$3679:   STA $C000,Y         ; Write to screen buffer
```

### Key Game Strings (with encoding)

Here are the decoded game strings with their offsets and encoded forms:

| Offset | Decoded Text | String Key | Length |
|---|---|---|---|
| $1CDE0 | GREETINGS COMMANDER | $41 | 19 bytes |
| $1F2A0 | PRESS FIRE TO PLAY | $41 | 18 bytes |
| $1D70B | ILLEGAL SINCE IT WAS PROVED TO CAUSE STERILITY AND BRAIN DAMAGE OVER X YEARS | $42 | 76 bytes |
| $1EB4F | ROBOT MISSILE FIRED | $41 | 19 bytes |
| $1ED06 | MISSION FAILED | $41 | 14 bytes |
| $1F02D | ALL SYSTEMS REPAIRED | $41 | 20 bytes |
| $1F9EC | SINKER REFUELED | $41 | 15 bytes |
| $20D91 | REACTOR SUCCESSFULLY CLOSED DOWN | $41 | 32 bytes |
| $1F21D | JOHN TWIDDY | $41 | 11 bytes |
| $1F241 | PETE COOKE | $41 | 10 bytes |
| $1F6F2 | SINKER DESTROYED | $41 | 16 bytes |
| $1FA85 | NOT AVAILABLE HERE | $41 | 18 bytes |
| $1FA99 | SINKER ISN'T DOCKED | $41 | 20 bytes |
| $1FD54 | PARTS DO NOT MATCH | $41 | 18 bytes |
| $1FDB5 | COOLING ROD SOLVED | $41 | 18 bytes |
| $20CEB | ENTERING A HIGHLY RADIOACTIVE AREA | $42 | 34 bytes |
| $20D1C | FATAL RADIOACTIVE DOSE RECEIVED | $42 | 31 bytes |
| $21831 | WHICH CITY | $41 | 10 bytes |
| $21A27 | WORLD POPULATION | $41 | 16 bytes |
| $21A3C | TRADE | $41 | 5 bytes |
| $21A46 | DEFENCES | $41 | 8 bytes |
| $21A7C | VERY HIGH | $41 | 9 bytes |
| $21A86 | MEDIUM | $41 | 6 bytes |
| $21AA4 | EAST | $41 | 4 bytes |
| $21AB5 | HEAVY IND | $41 | 9 bytes |
| $21ACB | MINING | $41 | 6 bytes |
| $21AD2 | HYDROPONICS | $41 | 11 bytes |

### VIC-II Character Set Memory ($8000-$87FF)

The VIC-II character set occupies the first 2KB of RAM. Tau Ceti uses a custom character set stored at $8000-$87FF that includes:

| Range | Content |
|---|---|
| $8000-$803F | Standard PETSCII characters (A-Z, 0-9, symbols) |
| $8040-$807F | Game-specific icons (reactor, missile, fuel, ship) |
| $8080-$80BF | Extended symbols (arrows, bar graphs, gauges) |
| $80C0-$80FF | Sprite shape data (8x8 pixel patterns) |
| $8100-$87FF | Unused / available for custom glyphs |

---

## Encoding reference

### Charset mapping

Input bytes map to display characters by direct substitution:

| Input | Char | Input | Char | Input | Char |
|---|---|---|---|---|---|
| `$21` | A | `$2C` | L | `$37` | W |
| `$22` | B | `$2D` | M | `$38` | X |
| `$23` | C | `$2E` | N | `$39` | Y |
| `$24` | D | `$2F` | O | `$3A` | Z |
| `$25` | E | `$30` | P | `$C0` | (space) |
| `$26` | F | `$31` | Q |  |  |
| `$27` | G | `$32` | R |  |  |
| `$28` | H | `$33` | S |  |  |
| `$29` | I | `$34` | T |  |  |
| `$2A` | J | `$35` | U |  |  |
| `$2B` | K | `$36` | V |  |  |

### Worked example: CENTRALIS

```text
CENTRALIS in charset:
  C = $23
  E = $25
  N = $2E
  T = $34
  R = $32
  A = $21
  L = $2C
  I = $29
  S = $33

Encoded: $23 $25 $2E $34 $32 $21 $2C $29 $33
```

### Special characters

| Icon | Purpose |
|---|---|
| Reactor symbol | Used in reactor status displays |
| Missile symbol | Used in supply display |
| Fuel gauge | Used in flying info window |
| Shield icon | Used in status field |
| Arrow symbols | Used in ADF displays |

---

[Back to the overview](../README.md)
