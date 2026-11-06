# Easter Eggs

The swear filter, the insult response, hidden messages and the victory message.

---

A complete analysis of hidden features, the bad language filter, insult responses, and secret codes.

## BAD LANGUAGE FILTER (The Lockout)

Entering X-rated or inappropriate terms into the game terminal triggers a response that locks you out of the game. This is not just a humorous message - it actually prevents further gameplay.

> [!WARNING]
> Entering bad language will LOCK YOU OUT of the game. This is not a simple Easter egg - it's a permanent lockout that requires restarting the game.

### BAD LANGUAGE Detection

The game checks input against a list of forbidden words stored in the decoded data area. If any match is found, the game displays a response and locks the terminal.

```text
Bad Language Detection:
  1. Player types input at board computer prompt
  2. Compare input against forbidden word list
  3. If match found:
     a. Display "ILLEGAL SINCE IT WAS PROVED TO CAUSE STERILITY AND BRAIN DAMAGE OVER [X] YEARS"
     b. Lock terminal (no further input accepted)
     c. Game is effectively ended
```

### Forbidden Word List

The forbidden words are stored in the decoded data area at offset $1D70B. The list includes various X-rated terms that trigger the lockout response.

| Category | Examples | Trigger |
|---|---|---|
| X-rated terms | Variety of profanity | Any match locks game |
| Insults | Offensive terms | May trigger humorous response |

## INSULT ME Response

The game also has a response for "INSULT ME" input, which triggers a humorous message rather than a lockout.

```text
INSULT ME Response:
  Location: Offset $1F195 in decoded data area
  Response: A humorous insult directed at the player
  Effect: No lockout, just a joke message
```

## Hidden Messages

The game contains several hidden messages in the decoded data area:

| Offset | Message | Context |
|---|---|---|
| $1CDE0 | "GREETINGS COMMANDER" | Title screen greeting |
| $1F2A0 | "PRESS FIRE TO PLAY" | Start prompt |
| $1EB4F | "ROBOT MISSILE FIRED" | Combat message |
| $1ED06 | "MISSION FAILED" | Mission end state |
| $1F02D | "ALL SYSTEMS REPAIRED" | Repair confirmation |
| $1F9EC | "SINKER REFUELED" | Fuel transaction |
| $20D91 | "REACTOR SUCCESSFULLY CLOSED DOWN" | Mission complete |
| $1F21D | "JOHN TWIDDY" | Credits: programmer |
| $1F241 | "PETE COOKE" | Credits: original idea |

## Victory Condition

The game is won by inserting all 20 cooling bars into the main reactor in Centralis. When this happens, the "REACTOR SUCCESSFULLY CLOSED DOWN" message appears and the mission is complete.

> [!NOTE]
> **Win condition:** All 20 cooling bars must be inserted into the main reactor in Centralis. This is the only way to complete the mission.

## FLASHING LIGHTS ON BUILDINGS

Several buildings display flashing or flickering lights. This is implemented using VIC-II sprite manipulation and color RAM writes, controlled by timer-based animation routines.

### The Mechanism

The flashing lights use two zero-page timer variables and the VIC-II sprite enable register ($D011):

| Variable | Address | Purpose |
|---|---|---|
| Light Timer | $0064 | Controls building light flash rate (set to $0E, $0D, $C5, or $FF) |
| Airlock Timer | $0063 | Controls DFP airlock flicker pattern (set to $00 or $C0) |

### Animation Code Flow

```asm
Flash Check Routine (at file offset $1CDAB):
  LDA $0064       ; Load light timer
  AND #$C0        ; Mask bits 7 and 6
  BNE +$0D        ; If non-zero, call flash routine
  RTS             ; Otherwise skip animation

$0063 (airlock timer) follows same pattern:
  LDA $0063       ; Load airlock timer
  AND #$C0        ; Mask bits 7 and 6
  BNE +$0D        ; If non-zero, call airlock flicker
  RTS
```

### Sprite Enable Toggling

The flash routine writes different values to $D011 (VIC-II Sprite Enable Register) to create the flashing effect. Each value enables a different combination of sprites:

| Value | Binary | Sprites Enabled | Visual Effect |
|---|---|---|---|
| $3B | %00111011 | 0, 1, 3, 4, 5 | Normal state (no sprite 2) |
| $2B | %00101011 | 0, 1, 4, 5 | Dimmed (no sprites 2, 3) |
| $34 | %00110100 | 2, 3, 4, 5 | Alternate pattern (no sprites 0, 1) |
| $37 | %00110111 | 0, 1, 2, 3, 4, 5 | All sprites (full brightness) |

Sprite 5 is the primary light indicator on buildings. By rapidly toggling between these sprite configurations each frame, the game creates a visible flashing effect.

### DFP Airlock Flicker

The DFP airlocks (mentioned in the manual as having a "flickering pattern") use the same mechanism. The airlock timer ($0063) is set to $00 or $C0 and toggles the sprite enable register to create the characteristic flicker effect seen on airlock doors.

### Color RAM Animation

In addition to sprite manipulation, the game also writes to color RAM at $DC00 and $DC0D with values $7F or $FF. These writes occur during building rendering and contribute to the flashing effect by rapidly changing the color attributes of building pixels on screen.

```asm
Color RAM Writes (during building render):
  $1E2D5: LDA #$7F -> STA $DC0D
  $1EA23: LDA #$7F -> STA $DC00
  $1FC81: LDA #$7F -> STA $DC00
  $1FC8E: LDA #$7F -> STA $DC0D

These values ($7F = bright, $FF = maximum brightness) are written
at different points in the rendering loop to create varying flash intensities.
```

> [!NOTE]
> **Key insight:** The flashing lights are not a separate animation - they are an emergent effect created by toggling sprite enable bits and color RAM values at high speed. This is a clever use of the C64's hardware capabilities to create visual effects without consuming CPU cycles for complex rendering.

## Score System

The SCORE command rates your progress. Points are awarded for various achievements including collecting cooling rods, assembling bars, inserting bars, destroying enemies, and visiting cities.

## Summary

Tau Ceti contains several hidden features including a bad language lockout (which is actually a game-ending penalty), insult responses, hidden messages, and a score system. The most notable Easter egg is the bad language filter, which punishes inappropriate input by locking you out of the game.

---

[Back to the overview](../README.md)
