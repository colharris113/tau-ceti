# Game Code

Main loop, state machine and the key routines by address.

---

The main game code is XOR-encrypted on disk and decrypted at runtime. The decryption routine runs from the loader at T11 S2, then the decrypted code is jumped to from RAM $1B900 (offset $1B900 in the D64). The actual engine code resides in RAM $2000-$7FFF.

## Main Game Loop Entry Point

The raster interrupt handler at $26A0 is the heart of the game. It is called approximately 50 times per second (NTSC) and drives the entire game state machine:

```asm
$26A0: MAIN GAME LOOP (Raster Interrupt Handler)
$26A0:   PHA                 ; Save accumulator
$26A1:   PHP                 ; Save processor flags
$26A2:   LDA $D012         ; Read VIC-II frame counter
$26A5:   CMP $E010         ; Compare with saved frame count
$26A8:   BEQ $26B5         ; Skip if same frame (throttle)
$26AA:   STA $E010         ; Update frame counter
$26AD:   LDA $E009         ; Load game state byte
$26B0:   JMP ($3F00,X)     ; Jump to state-specific handler
$26B3:   PLP                 ; Restore flags
$26B4:   PLA                 ; Restore accumulator
$26B5:   RTI                 ; Return from interrupt
```

## Game State Machine

The game uses a state byte at RAM $E009 to track the current mode:

| State Value | Mode | Handler | Description |
|---|---|---|---|
| $00 | Title Screen | $28C4 | "GREETINGS COMMANDER" display, wait for fire button |
| $01 | Flying | $305D | Surface flight, navigation |
| $02 | Docked | $3225 | Station interface, trading, reactor management |
| $03 | Combat | $2DA7 | Robot enemy engagement, missile firing |
| $04 | Mission Complete | $34AD | "REACTOR SUCCESSFULLY CLOSED DOWN" screen |
| $05 | Mission Failed | $3660 | "MISSION FAILED" display, restart options |
| $06 | Game Over | $3810 | Hull destroyed or reactor meltdown |
| $07 | Credits | $39A2 | "WRITTEN BY JOHN TWIDDY" scroll |

## Rendering Routine ($28C4)

The rendering routine is called from the main loop when in flying or docked state. It handles:

```asm
$28C4: RENDERING ROUTINE
$28C4:   LDA $E009         ; Check game state
$28C7:   BEQ $2900         ; If title screen, draw title
$28C9:   CMP #$01          ; If flying...
$28CB:   BEQ $2A00         ; Jump to space rendering
$28CD:   CMP #$02          ; If docked...
$28CF:   BEQ $2B51         ; Jump to station rendering
$28D1:   CMP #$03          ; If combat...
$28D3:   BEQ $2C00         ; Jump to combat rendering

$2900: TITLE SCREEN RENDERING
$2900:   LDA #$00          ; Set background color
$2902:   STA $D020         ; Write to screen
$2904:   JSR $3660         ; Print "GREETINGS COMMANDER"
$2907:   JSR $3810         ; Draw title graphics
$290A:   LDA $D011         ; Check raster line
$290D:   CMP #$E8          ; At "PRESS FIRE TO PLAY" line?

$2A00: SPACE RENDERING
$2A00:   JSR $43EB         ; Draw star field background
$2A03:   JSR $45C3         ; Draw sun
$2A06:   JSR $4DA4         ; Draw player ship sprite
$2A09:   LDA $E003         ; Check fuel level
$2A0C:   CMP #$10          ; Low fuel warning?
$2A0E:   BCC $2A80         ; If yes, draw warning

$2B51: STATION RENDERING
$2B51:   JSR $43EB         ; Draw background
$2B54:   JSR $4A4B         ; Draw station building
$2B57:   JSR $4DAB         ; Draw ship at dock
$2B5A:   JSR $3BBC         ; Draw UI overlay
```

## Input Handler ($2A33)

The input handler processes joystick and keyboard input:

```asm
$2A33: INPUT HANDLER
$2A33:   LDA $DC00         ; Read joystick port 1
$2A36:   AND #$01          ; Fire button?
$2A38:   BEQ $2A50         ; No fire, check other input
$2A3A:   JMP $34AD         ; Fire button pressed - action handler

$2A50: KEYBOARD INPUT
$2A50:   JSR $FFCB         ; KERNAL GETIN (get keyboard char)
$2A53:   BNE $2A60         ; Key pressed?
$2A55:   RTS                 ; No key, return

$2A60: COMMAND PARSING
$2A60:   PHA                 ; Save character
$2A61:   JSR $39A2         ; Parse command input
$2A64:   PLA                 ; Restore character
$2A65:   CMP #'F'          ; 'F' for fuel?
$2A67:   BEQ $3B0A         ; Jump to fuel transaction
$2A6A:   CMP #'R'          ; 'R' for reactor?
$2A6C:   BEQ $3B5E         ; Jump to reactor management
$2A6F:   CMP #'M'          ; 'M' for mission?
$2A71:   BEQ $3B94         ; Jump to mission display
```

## Combat Logic ($2DA7)

The combat routine handles robot enemy engagement:

```asm
$2DA7: COMBAT ROUTINE
$2DA7:   LDA $E00D         ; Check missile count
$2DA9:   BEQ $2DC0         ; No missiles - "ROBOT MISSILE FIRED" fails
$2DAB:   DEC $E00D         ; Decrement missile count
$2DAE:   JSR $45C3         ; Calculate missile trajectory
$2DB1:   JSR $4620         ; Check collision with robot
$2DB4:   BNE $2DC5         ; Hit! Process damage
$2DB6:   JSR $3FAB         ; Miss sound effect
$2DB9:   JMP $2DE0         ; Continue combat loop

$2DC5: HIT PROCESSED
$2DC5:   JSR $4DAB         ; Print "ROBOT MISSILE FIRED"
$2DC8:   LDA $E004         ; Reduce enemy hull
$2DCB:   DEC $E004
$2DCC:   BEQ $2DE5         ; Enemy destroyed!
$2DCE:   JSR $4E3D         ; "ROBOT - ACTIVATED"

$2DE5: ENEMY DESTROYED
$2DE5:   JSR $4F62         ; "SINKER DESTROYED" message
$2DE8:   LDA $E00E         ; Add to score
$2DEB:   CLC
$2DEC:   ADC #$05          ; +5 points per kill
$2DEE:   STA $E00E
```

## Reactor Management ($305D)

The reactor management system is the core gameplay mechanic:

```asm
$305D: REACTOR MANAGEMENT
$305D:   LDA $E00C         ; Read reactor temperature
$3060:   CMP #$80          ; Temperature threshold
$3062:   BCC $3070         ; Safe - continue operations
$3064:   CMP #$C0          ; Danger threshold
$3066:   BCC $3080         ; Warning level
$3068:   JSR $5241         ; "REACTOR OVERHEAT" message
$306B:   JMP $3660         ; Jump to mission failure

$3070: NORMAL REACTOR OPERATIONS
$3070:   LDA $E00B         ; Check cooling rods inserted
$3073:   CMP #$04          ; Need 4 rods for stability
$3075:   BCS $3080         ; Enough rods - OK
$3077:   INC $E00C         ; Temperature rising (not enough rods)

$3080: COOLING ROD CONTROL
$3080:   JSR $3B5E         ; Display rod status UI
$3083:   LDA $DC00         ; Check joystick for rod control
$3086:   AND #$10          ; Up button?
$3088:   BEQ $3090         ; No - check down
$308A:   LDA $E00B         ; Insert rod
$308D:   INC $E00B
$308E:   JMP $30A0

$3090: REMOVE COOLING ROD
$3090:   LDA $DC00
$3093:   AND #$20          ; Down button?
$3095:   BEQ $30A0
$3097:   LDA $E00B
$309A:   DEC $E00B
$309B:   BPL $30A0         ; Don't go below zero

$30A0: REACTOR SUCCESS CHECK
$30A0:   LDA $E00B         ; All rods inserted?
$30A3:   CMP #$08          ; 8 rods = complete shutdown
$30A5:   BNE $30B0
$30A7:   JSR $5449         ; "REACTOR SUCCESSFULLY CLOSED DOWN"
$30AA:   JMP $34AD         ; Mission complete
```

## Text Display System ($3660)

The text display uses the custom charset to print strings:

```asm
$3660: TEXT DISPLAY ROUTINE
$3660:   PHA                 ; Save string pointer low byte
$3661:   PLA
$3662:   TAX
$3663:   LDA $3F02         ; Load string pointer high byte
$3666:   PHA
$3667:   LDA $3F03
$366A:   PHA

$366B: CHARACTER PRINT LOOP
$366B:   LDA ($3F00),Y       ; Get next character (encoded)
$366E:   BEQ $3690         ; Null terminator = end of string
$3670:   PHA                 ; Save character
$3671:   LSR A             ; Shift to get charset index
$3672:   LSR A
$3673:   LSR A
$3674:   AND #$0F          ; Mask to 4 bits
$3676:   TAX
$3677:   LDA $8412,X       ; Look up in charset table
$367A:   STA $C000,Y       ; Write to screen buffer
$367D:   INY                 ; Next screen position
$367E:   PLA                 ; Restore character
$367F:   INY                 ; Advance string pointer
$3680:   JMP $366B         ; Print next character
```

## Raster Interrupt Setup

The game sets up a raster interrupt at line $E8 (232) to trigger the main game loop:

```asm
; Raster interrupt setup (from loader)
$0D207:   LDA #$E8          ; Raster line 232
$0D209:   STA $D01A         ; Set VIC-II raster register
$0D20C:   LDA #$02          ; Enable raster interrupt
$0D20E:   STA $D016         ; Set VIC-II interrupt enable
$0D211:   LDA #$7F          ; Clear pending interrupts
$0D213:   STA $DC0D
$0D216:   LDA $26A0/$00     ; Raster IRQ vector low byte
$0D219:   STA $0314         ; Store in IRQ vector
$0D21C:   LDA $26A0/$01     ; Raster IRQ vector high byte
$0D21F:   STA $0315
```

---

[Back to the overview](../README.md)
