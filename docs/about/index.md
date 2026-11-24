# This project

<p class="lede">This is a study of a single Commodore 64 program: the 1986 conversion of Tau Ceti. It exists because the game's design is unusually legible from its code, and because almost nothing is written down about how that code works.</p>

## What it is

The site has three jobs:

1. **Explain the mechanics.** How docking really decides, what the fuel burn is, how a jump pad picks a destination, how the AI's fire counters work.
2. **Document the code.** A routine-by-routine guide with addresses, instruction streams, shared variables and call sites.
3. **Make it readable.** Diagrams, plain-language summaries and consistent notation, so the explanations work for players and programmers alike.

It is not a walkthrough, a longplay or a replacement for the manual. Spoilers for the game's structure are unavoidable, but the guide rarely gives tactical advice.

## Who made it

The guide is written by Colin Harris, with the analysis, tooling and diagrams produced alongside a modern remake of the game. The remake is a separate project; this site is the static, readable record of what the C64 original actually does.

The method is the point: every claim is traced to an address, and every generated table or figure is reproducible from the scripts in the repository. See [Method](method.md).

## Provenance and copyright

The analysis starts from a disk image of the author's own copy of Tau Ceti, disassembled locally. The site reproduces no original graphics, sound or in-game text. The Source guide does show disassembled routines — annotated with their addresses, bytes and call sites — because explaining how the code works means showing it. The message-font figure is a re-rendering of the game's own eight-by-eight glyphs for the purpose of explaining how text is encoded; it is an analytical reproduction, not an asset re-release.

*Tau Ceti* was designed and written by Pete Cooke, converted to the Commodore 64 by John Twiddy, and published by CRL Group PLC in 1986. *Tau Ceti* and its constituent parts remain the property of their rights holders. This site is independent and non-commercial, and is not affiliated with or endorsed by CRL or the original authors.

## Corrections

The C64 original is the authority, and if this guide disagrees with it, the guide is wrong. Corrections are welcome: the most useful reports name the routine or the game state, not just the conclusion.

## Thanks

See [Acknowledgements](acknowledgements.md).
