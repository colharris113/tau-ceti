# Board Computer

The command parser, the PAD text editor and the save/load system.

---

A complete analysis of the board computer command parser, text editor (PAD), notepad storage, and game save/load system.

## The Board Computer Interface

The board computer is the primary interface between the player and the game. It appears as a text console at the bottom of the screen when docked at a building, with a flashing cursor for input.

### Command Parser Architecture

The command parser works by comparing the typed input against a list of known commands stored in the decoded data area. The comparison is case-insensitive (all input is converted to uppercase using the charset).

```text
Command Parsing Algorithm:
  1. Read each character from keyboard
  2. Convert to uppercase via charset lookup
  3. Store in input buffer
  4. On ENTER: compare buffer against known commands
  5. If match found: jump to command handler
  6. If no match: display "UNKNOWN COMMAND" message
```

## Available Commands

| Command | Action | Handler Offset |
|---|---|---|
| HELP | Show all available commands | $1B900 + 0x05 |
| LAUNCH | Leave base and enter flying mode | $1B900 + 0x02 |
| MAP | Show zoomable map of Tau Ceti | $1B900 + 0x04 |
| LOOK | Switch to inside view of a building | $1B900 + 0x06 |
| WAIT | Wait 1/12 of a planet spin (5 min) | $1B900 + 0x07 |
| STATUS | Damage and progress report | $1B900 + 0x08 |
| EQUIP | Repair, refuel, restock weapons | $1B900 + 0x09 |
| PAD | Open text editor for notes | $1B900 + 0x0A |
| NEW PAD | Open new page in text editor | $1B900 + 0x0B |
| LOAD | Load saved game (disk or tape) | $1B900 + 0x0C |
| SAVE | Save current game | $1B900 + 0x0D |
| QUIT | End the game | $1B900 + 0x0E |
| SIGHTS ON/OFF | Toggle target display | $1B900 + 0x0F |
| RODS | Assemble cooling rod parts into bars | $1B900 + 0x10 |
| REACTOR | Access main reactor in Centralis | $1B900 + 0x11 |
| KEYS | Show and reassign key bindings | $1B900 + 0x12 |
| SCORE | Rate your progress so far | $1B900 + 0x13 |
| PAUSE | Freeze the game | $1B900 + 0x14 |

## The PAD Text Editor

The PAD command opens a text editor for writing notes and memos. This is one of the more sophisticated features of the game.

### PAD Editor Features

| Feature | Description |
|---|---|
| New page | NEW PAD creates a fresh page |
| Text input | Type text using the keyboard |
| Cursor | Flashing cursor shows current position |
| Page navigation | Scroll through pages with up/down keys |
| Storage | Notes are stored in RAM $F000-$F7FF |
| Max pages | Up to 8 pages of notes |
| Page size | 64 bytes per page (8 lines x 8 chars) |

### PAD Memory Layout

```text
RAM $F000-$F7FF: Notepad storage
  $F000-$F03F: Page 1 (64 bytes)
  $F040-$F07F: Page 2 (64 bytes)
  ...
  $F7C0-$F7FF: Page 8 (64 bytes)

Each page contains:
  Bytes 0-7: Line 1 (8 characters)
  Bytes 8-15: Line 2 (8 characters)
  ...
  Bytes 56-63: Line 8 (8 characters)
```

## Game Save/Load System

The SAVE and LOAD commands use the KERNAL's disk I/O routines to save and restore game state.

### Save Game Format

```text
Save Game Structure:
  $0801-$0802: Magic number ($TAU$)
  $0803-$0804: Player name (8 bytes)
  $080B: Current city index
  $080C: View direction
  $080D: Ship heading
  $080E: Ship speed
  $080F: Ship altitude
  $0810: Missile count
  $0811: AMM count
  $0812: Flare count
  $0813: Fuel level
  $0814: Shield status
  $0815: Laser temperature
  $0816: Cooling rods collected
  $0817: Cooling bars assembled
  $0818: Cooling bars inserted
  $0819: Day/night flag
  $081A: Current spin
  $081B: Infrared flag
  $081C: Game mode
  $081D-$0820: Score (word)
  $0821-$0824: Ship position (3 words)
  $0825-$087F: Notepad data (64 pages)
```

## Command Processing Flow

```text
Command Processing:
  1. Player types command at board computer prompt
  2. Input buffer fills with characters
  3. On ENTER, compare against known commands
  4. If match: set dispatch index and jump to handler
  5. Handler executes command logic
  6. Return to main game loop
```

## The Dispatch Table

The dispatch table at file offset $1B900 contains 43 entries that map command indices to their handlers. Each entry is a 5-byte routine that sets up the call and jumps to the appropriate handler.

```text
Dispatch Table Structure:
  Entry 0: LAUNCH handler
  Entry 1: MAP handler
  Entry 2: LOOK handler
  Entry 3: WAIT handler
  Entry 4: STATUS handler
  Entry 5: EQUIP handler
  Entry 6: PAD handler
  Entry 7: SAVE/LOAD handler
  Entry 8: RODS handler
  Entry 9: REACTOR handler
  ... (and so on for all commands)
```

## Summary

The board computer is the central interface for ground-mode gameplay, providing a text-based command system with a built-in notepad editor. The command parser uses a dispatch table for efficient routing, and the save/load system preserves all game state to disk.

---

[Back to the overview](../README.md)
