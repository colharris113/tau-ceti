# Static defence AI

**Address** `$81F3-$8359` · **Group** Combat

Static defence AI. Type flags bit 5 (mobile units) always run; everyone else runs only while the provocation latch `$03BF` is set. Out of class range it does nothing. In range it sets byte 3 bit 3, answers a player lock with an AMM after 24 frames (clearing its own lock first), and otherwise counts byte 9 against the fire interval at `$C45E`. A random roll masked by `$C44E` reloads the counter; behaviour bit 7 units also roll against `$C46E` and, on success, take a free record from `$1000` and spawn a missile into it. Type 26 has an early path of its own at `$8202`. Movement ends at `$8347`.

## Listing

*Decoded from the byte map within the curated code ranges for this routine.*

```text
81F3: A0 00    LDY #$00
81F5: B1 61    LDA ($61),Y
81F7: 29 3F    AND #$3F
81F9: A8       TAY
81FA: B9 09 C4 LDA $C409,Y
81FD: 85 67    STA $67
81FF: 29 0F    AND #$0F
8201: AA       TAX
8202: C0 1A    CPY #$1A
8204: D0 39    BNE $823F
8206: A0 0D    LDY #$0D
8208: B1 61    LDA ($61),Y
820A: C9 06    CMP #$06
820C: B0 0C    BCS $821A
820E: C9 04    CMP #$04
8210: 90 09    BCC $821B
8212: AD B0 03 LDA $03B0
8215: 09 10    ORA #$10
8217: 8D B0 03 STA $03B0
821A: 60       RTS
821B: A9 E8    LDA #$E8
821D: A2 65    LDX #$65
821F: 20 27 41 JSR $4127   ; Message queue
8222: A9 32    LDA #$32
8224: 8D 79 03 STA $0379
8227: A0 00    LDY #$00
8229: B1 61    LDA ($61),Y
822B: 09 40    ORA #$40
822D: 91 61    STA ($61),Y
822F: A9 30    LDA #$30
8231: 20 65 3E JSR $3E65
8234: A9 00    LDA #$00
8236: 8D C4 03 STA $03C4
8239: A9 04    LDA #$04
823B: 8D C5 03 STA $03C5
823E: 60       RTS
823F: B9 9A C3 LDA $C39A,Y
8242: 29 20    AND #$20
8244: 0D BF 03 ORA $03BF   ; Provocation latch
8247: D0 01    BNE $824A
8249: 60       RTS
824A: A0 03    LDY #$03
824C: B1 61    LDA ($61),Y
824E: 29 F3    AND #$F3
8250: 91 61    STA ($61),Y
8252: A0 0D    LDY #$0D
8254: B1 61    LDA ($61),Y
8256: DD 2E C4 CMP $C42E,X
8259: 90 01    BCC $825C
825B: 60       RTS
825C: A0 03    LDY #$03
825E: B1 61    LDA ($61),Y
8260: 09 08    ORA #$08
8262: 91 61    STA ($61),Y
8264: AD B0 03 LDA $03B0
8267: 09 08    ORA #$08
8269: 8D B0 03 STA $03B0
826C: A5 67    LDA $67
826E: 29 40    AND #$40
8270: F0 2C    BEQ $829E
8272: A0 03    LDY #$03
8274: B1 61    LDA ($61),Y
8276: 29 10    AND #$10
8278: F0 24    BEQ $829E
827A: A0 09    LDY #$09
827C: B1 61    LDA ($61),Y
827E: 18       CLC
827F: 69 01    ADC #$01
8281: 91 61    STA ($61),Y
8283: C9 18    CMP #$18
8285: 90 16    BCC $829D
8287: A9 00    LDA #$00
8289: 91 61    STA ($61),Y
828B: A0 03    LDY #$03
828D: B1 61    LDA ($61),Y
828F: 29 EF    AND #$EF
8291: 91 61    STA ($61),Y
8293: A9 D3    LDA #$D3
8295: A2 65    LDX #$65
8297: 20 27 41 JSR $4127   ; Message queue
829A: 20 38 48 JSR $4838   ; Clear all missiles (AMM)
829D: 60       RTS
829E: A0 00    LDY #$00
82A0: B1 61    LDA ($61),Y
82A2: C9 15    CMP #$15
82A4: F0 0B    BEQ $82B1
82A6: A0 06    LDY #$06
82A8: B1 61    LDA ($61),Y
82AA: F0 05    BEQ $82B1
82AC: C9 40    CMP #$40
82AE: F0 01    BEQ $82B1
82B0: 60       RTS
82B1: A5 67    LDA $67
82B3: 29 20    AND #$20
82B5: F0 09    BEQ $82C0
82B7: A0 03    LDY #$03
82B9: B1 61    LDA ($61),Y
82BB: 29 30    AND #$30
82BD: D0 01    BNE $82C0
82BF: 60       RTS
82C0: A0 09    LDY #$09
82C2: B1 61    LDA ($61),Y
82C4: 18       CLC
82C5: 69 01    ADC #$01
82C7: 91 61    STA ($61),Y
82C9: 29 3F    AND #$3F
82CB: AC 74 03 LDY $0374
82CE: F0 01    BEQ $82D1
82D0: 0A       ASL A
82D1: DD 5E C4 CMP $C45E,X
82D4: B0 01    BCS $82D7
82D6: 60       RTS
82D7: 20 0E 33 JSR $330E
82DA: A0 09    LDY #$09
82DC: 3D 4E C4 AND $C44E,X
82DF: 91 61    STA ($61),Y
82E1: A5 67    LDA $67
82E3: 10 62    BPL $8347
82E5: 20 0E 33 JSR $330E
82E8: DD 6E C4 CMP $C46E,X
82EB: 90 5A    BCC $8347
82ED: A9 00    LDA #$00
82EF: 85 63    STA $63
82F1: A9 10    LDA #$10
82F3: 85 64    STA $64
82F5: A0 00    LDY #$00
82F7: B1 63    LDA ($63),Y
82F9: 30 0A    BMI $8305
82FB: 98       TYA
82FC: 18       CLC
82FD: 69 10    ADC #$10
82FF: A8       TAY
8300: D0 F5    BNE $82F7
8302: 4C 47 83 JMP $8347
8305: 84 63    STY $63
8307: A9 BE    LDA #$BE
8309: A2 65    LDX #$65
830B: 20 27 41 JSR $4127   ; Message queue
830E: A9 06    LDA #$06
8310: 8D C5 03 STA $03C5
8313: A0 00    LDY #$00
8315: A9 0B    LDA #$0B
8317: 91 63    STA ($63),Y
8319: C8       INY
831A: B1 61    LDA ($61),Y
831C: 91 63    STA ($63),Y
831E: C8       INY
831F: B1 61    LDA ($61),Y
8321: 91 63    STA ($63),Y
8323: C8       INY
8324: A9 48    LDA #$48
8326: 91 63    STA ($63),Y
8328: C8       INY
8329: A9 00    LDA #$00
832B: 91 63    STA ($63),Y
832D: C8       INY
832E: 91 63    STA ($63),Y
8330: C8       INY
8331: B1 61    LDA ($61),Y
8333: 18       CLC
8334: 69 80    ADC #$80
8336: 90 02    BCC $833A
8338: A9 FF    LDA #$FF
833A: 91 63    STA ($63),Y
833C: C8       INY
833D: A9 00    LDA #$00
833F: 91 63    STA ($63),Y
8341: C8       INY
8342: C0 10    CPY #$10
8344: D0 F4    BNE $833A
8346: 60       RTS
8347: A9 03    LDA #$03
8349: 20 65 3E JSR $3E65
834C: A0 03    LDY #$03
834E: B1 61    LDA ($61),Y
8350: 09 04    ORA #$04
8352: 91 61    STA ($61),Y
8354: A9 00    LDA #$00
8356: 8D C4 03 STA $03C4
8359: 60       RTS
```

## Calls

- [`Message queue`](message-queue.md) from `$821F`
- [`Clear all missiles (AMM)`](clear-missiles.md) from `$829A`

## Called by

- `JSR` at `$4640` in [`Robot dispatch`](ai-dispatch.md)

---

*Generated by `tools/build_source.py` from `tools/symbols.json`. Correct the symbol file, not this page.*

[Back to the source guide](../index.md)
