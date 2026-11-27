# Object distance and the docking test

**Address** `$2B60-$2CBF` · **Group** Docking

Works out the distance to the record in `$61`/`$62`, scales it through the tables at `$C800`/`$C900` and stores the product in bytes 12/13. Only a product under 128 is close enough to dock; anything up to 4,095 is added to the target list, and anything larger is dropped. For a close record, type 16 docks as a jump pad before anything else. A dockable building must pass |altitude - 28| + 55 < aperture, then a bearing test of 2 * (|bearing offset| + 28) against the same aperture - at the full 72-point opening that is an offset of at most 7 steps of the 512-step circle, about 5 degrees. Passing both sets `$0396` = `$80` and copies the building's type and cell to `$03A4`/`$0398`/`$0399`.

## Listing

*Decoded from the byte map within the curated code ranges for this routine.*

```text
2B60: A6 5A    LDX $5A
2B62: A5 5B    LDA $5B
2B64: C9 01    CMP #$01
2B66: F0 1A    BEQ $2B82
2B68: C9 0A    CMP #$0A
2B6A: B0 1C    BCS $2B88
2B6C: 38       SEC
2B6D: E9 02    SBC #$02
2B6F: 86 55    STX $55
2B71: 4A       LSR A
2B72: 66 55    ROR $55
2B74: 4A       LSR A
2B75: 66 55    ROR $55
2B77: 4A       LSR A
2B78: 66 55    ROR $55
2B7A: A6 55    LDX $55
2B7C: BD 00 C9 LDA $C900,X
2B7F: 4C 8A 2B JMP $2B8A
2B82: BD 00 C8 LDA $C800,X
2B85: 4C 8A 2B JMP $2B8A
2B88: A9 00    LDA #$00
2B8A: 85 26    STA $26
2B8C: A6 58    LDX $58
2B8E: A4 59    LDY $59
2B90: A9 00    LDA #$00
2B92: 85 57    STA $57
2B94: 85 55    STA $55
2B96: 46 26    LSR $26
2B98: 90 0F    BCC $2BA9
2B9A: A5 57    LDA $57
2B9C: 18       CLC
2B9D: 65 58    ADC $58
2B9F: 85 57    STA $57
2BA1: 8A       TXA
2BA2: 65 59    ADC $59
2BA4: AA       TAX
2BA5: 98       TYA
2BA6: 65 55    ADC $55
2BA8: A8       TAY
2BA9: 06 58    ASL $58
2BAB: 26 59    ROL $59
2BAD: 26 55    ROL $55
2BAF: A5 26    LDA $26
2BB1: D0 E3    BNE $2B96
2BB3: C0 10    CPY #$10
2BB5: 90 03    BCC $2BBA
2BB7: 4C 5B 2A JMP $2A5B
2BBA: 98       TYA
2BBB: 08       PHP
2BBC: A0 0D    LDY #$0D
2BBE: 91 61    STA ($61),Y
2BC0: 88       DEY
2BC1: 8A       TXA
2BC2: 91 61    STA ($61),Y
2BC4: A0 03    LDY #$03
2BC6: B1 61    LDA ($61),Y
2BC8: 09 40    ORA #$40
2BCA: 91 61    STA ($61),Y
2BCC: 28       PLP
2BCD: D0 04    BNE $2BD3
2BCF: E0 80    CPX #$80
2BD1: 90 03    BCC $2BD6
2BD3: 4C C0 2C JMP $2CC0
2BD6: A0 00    LDY #$00
2BD8: B1 61    LDA ($61),Y
2BDA: 29 C0    AND #$C0
2BDC: D0 3B    BNE $2C19
2BDE: B1 61    LDA ($61),Y
2BE0: C9 10    CMP #$10
2BE2: D0 15    BNE $2BF9
2BE4: AD 6C 03 LDA $036C
2BE7: D0 08    BNE $2BF1
2BE9: AE 0F 01 LDX $010F
2BEC: 20 18 3D JSR $3D18   ; Flag-bit test
2BEF: D0 28    BNE $2C19
2BF1: A9 FF    LDA #$FF
2BF3: 8D 9B 03 STA $039B   ; Jump pad docked
2BF6: 4C BD 2C JMP $2CBD
2BF9: A8       TAY
2BFA: B9 9A C3 LDA $C39A,Y
2BFD: 10 61    BPL $2C60
2BFF: AD 44 03 LDA $0344   ; Altitude
2C02: 38       SEC
2C03: E9 1C    SBC #$1C
2C05: B0 04    BCS $2C0B
2C07: 49 FF    EOR #$FF
2C09: 69 01    ADC #$01
2C0B: 18       CLC
2C0C: 69 37    ADC #$37
2C0E: A0 08    LDY #$08
2C10: D1 61    CMP ($61),Y
2C12: 90 08    BCC $2C1C
2C14: A9 FF    LDA #$FF
2C16: 8D 81 03 STA $0381   ; Dock refused
2C19: 4C BD 2C JMP $2CBD
2C1C: 20 C6 2C JSR $2CC6
2C1F: 38       SEC
2C20: ED 38 03 SBC $0338   ; Launch heading (low)
2C23: 08       PHP
2C24: 38       SEC
2C25: E9 20    SBC #$20
2C27: A8       TAY
2C28: 8A       TXA
2C29: E9 00    SBC #$00
2C2B: 28       PLP
2C2C: ED 39 03 SBC $0339   ; Launch heading (high)
2C2F: 4A       LSR A
2C30: 98       TYA
2C31: 90 04    BCC $2C37
2C33: 49 FF    EOR #$FF
2C35: 69 00    ADC #$00
2C37: 18       CLC
2C38: 69 1C    ADC #$1C
2C3A: B0 D8    BCS $2C14
2C3C: 0A       ASL A
2C3D: B0 D5    BCS $2C14
2C3F: A0 08    LDY #$08
2C41: D1 61    CMP ($61),Y
2C43: B0 CF    BCS $2C14
2C45: A9 80    LDA #$80
2C47: 8D 96 03 STA $0396   ; Dock state
2C4A: A0 00    LDY #$00
2C4C: B1 61    LDA ($61),Y
2C4E: 8D A4 03 STA $03A4   ; Docked type
2C51: C8       INY
2C52: B1 61    LDA ($61),Y
2C54: 8D 98 03 STA $0398   ; Docked cell (low)
2C57: C8       INY
2C58: B1 61    LDA ($61),Y
2C5A: 8D 99 03 STA $0399   ; Docked cell (high)
2C5D: 4C BD 2C JMP $2CBD
2C60: 29 0C    AND #$0C
2C62: D0 59    BNE $2CBD
2C64: A0 06    LDY #$06
2C66: B1 61    LDA ($61),Y
2C68: CD 44 03 CMP $0344   ; Altitude
2C6B: 90 3C    BCC $2CA9
2C6D: E9 80    SBC #$80
2C6F: 90 05    BCC $2C76
2C71: CD 44 03 CMP $0344   ; Altitude
2C74: B0 47    BCS $2CBD
2C76: A0 00    LDY #$00
2C78: B1 61    LDA ($61),Y
2C7A: 09 40    ORA #$40
2C7C: 91 61    STA ($61),Y
2C7E: A0 08    LDY #$08
2C80: A9 00    LDA #$00
2C82: 91 61    STA ($61),Y
2C84: A0 07    LDY #$07
2C86: B1 61    LDA ($61),Y
2C88: 18       CLC
2C89: 69 40    ADC #$40
2C8B: 90 02    BCC $2C8F
2C8D: A9 FF    LDA #$FF
2C8F: 20 65 3E JSR $3E65
2C92: A9 FF    LDA #$FF
2C94: 8D 92 03 STA $0392
2C97: A9 01    LDA #$01
2C99: 8D 93 03 STA $0393
2C9C: A9 04    LDA #$04
2C9E: 8D C5 03 STA $03C5
2CA1: A9 00    LDA #$00
2CA3: 8D C4 03 STA $03C4
2CA6: 4C BD 2C JMP $2CBD
2CA9: 48       PHA
2CAA: A0 00    LDY #$00
2CAC: B1 61    LDA ($61),Y
2CAE: 29 3F    AND #$3F
2CB0: A8       TAY
2CB1: 68       PLA
2CB2: 18       CLC
2CB3: 79 E4 C3 ADC $C3E4,Y
2CB6: B0 BE    BCS $2C76
2CB8: CD 44 03 CMP $0344   ; Altitude
2CBB: B0 B9    BCS $2C76
2CBD: 4C 5B 2A JMP $2A5B
```

### Additional code at `$2CC0`

```text
2CC0: 20 C6 2C JSR $2CC6
2CC3: 4C 5F 2D JMP $2D5F
```

### Additional code at `$2CC6`

```text
2CC6: A5 5B    LDA $5B
2CC8: C9 40    CMP #$40
2CCA: 90 04    BCC $2CD0
2CCC: A9 7F    LDA #$7F
2CCE: D0 21    BNE $2CF1
2CD0: 06 5A    ASL $5A
2CD2: 2A       ROL A
2CD3: 06 5A    ASL $5A
2CD5: 2A       ROL A
2CD6: C9 10    CMP #$10
2CD8: B0 13    BCS $2CED
2CDA: 06 5A    ASL $5A
2CDC: 2A       ROL A
2CDD: 06 5A    ASL $5A
2CDF: 2A       ROL A
2CE0: 06 5A    ASL $5A
2CE2: 2A       ROL A
2CE3: 06 5A    ASL $5A
2CE5: 2A       ROL A
2CE6: A8       TAY
2CE7: B9 00 8B LDA $8B00,Y
2CEA: 4C F1 2C JMP $2CF1
2CED: A8       TAY
2CEE: B9 00 8A LDA $8A00,Y
2CF1: 85 26    STA $26
2CF3: A5 E7    LDA $E7
2CF5: D0 28    BNE $2D1F
2CF7: A5 E8    LDA $E8
2CF9: D0 12    BNE $2D0D
2CFB: A5 E9    LDA $E9
2CFD: D0 07    BNE $2D06
2CFF: A2 00    LDX #$00
2D01: A0 00    LDY #$00
2D03: 4C 47 2D JMP $2D47
2D06: A2 7F    LDX #$7F
2D08: A0 00    LDY #$00
2D0A: 4C 52 2D JMP $2D52
2D0D: A5 E9    LDA $E9
2D0F: D0 07    BNE $2D18
2D11: A2 FF    LDX #$FF
2D13: A0 00    LDY #$00
2D15: 4C 52 2D JMP $2D52
2D18: A2 80    LDX #$80
2D1A: A0 00    LDY #$00
2D1C: 4C 47 2D JMP $2D47
2D1F: A5 E8    LDA $E8
2D21: D0 12    BNE $2D35
2D23: A5 E9    LDA $E9
2D25: D0 07    BNE $2D2E
2D27: A2 FF    LDX #$FF
2D29: A0 01    LDY #$01
2D2B: 4C 52 2D JMP $2D52
2D2E: A2 80    LDX #$80
2D30: A0 01    LDY #$01
2D32: 4C 47 2D JMP $2D47
2D35: A5 E9    LDA $E9
2D37: D0 07    BNE $2D40
2D39: A2 00    LDX #$00
2D3B: A0 01    LDY #$01
2D3D: 4C 47 2D JMP $2D47
2D40: A2 7F    LDX #$7F
2D42: A0 01    LDY #$01
2D44: 4C 52 2D JMP $2D52
2D47: 8A       TXA
2D48: 18       CLC
2D49: 65 26    ADC $26
2D4B: 48       PHA
2D4C: 98       TYA
2D4D: 69 00    ADC #$00
2D4F: 4C 5A 2D JMP $2D5A
2D52: 8A       TXA
2D53: 38       SEC
2D54: E5 26    SBC $26
2D56: 48       PHA
2D57: 98       TYA
2D58: E9 00    SBC #$00
2D5A: 29 01    AND #$01
2D5C: AA       TAX
2D5D: 68       PLA
2D5E: 60       RTS
```

## Calls

- [`Flag-bit test`](bit-test.md) from `$2BEC`

## Called by

- `JMP` at `$2ADB`

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
