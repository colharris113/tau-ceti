# Tau Ceti — A Guide to the C64 Code

An address-level study of *Tau Ceti* (Pete Cooke, C64 conversion by John Twiddy;
CRL, 1986): what each part of the program does, how the record table is laid
out, how docking really works, how fuel is burned, and how the game's data
drives its robots.

## Read the guide

Open the [guide index](docs/index.md) on GitHub or in a Markdown viewer. The
articles, routine listings and figures are ready to read without setup.

- [Deep Dives](docs/deep-dives/index.md) covers the flight loop, cities, mission, rendering, combat and sound.
- [Source Guide](docs/source/index.md) shows the annotated 6502 routines and shared variables.
- [Type Tables](docs/reference/type-tables.md) documents the object flags, combat data and AI classes.

The presentation takes inspiration from the [Elite](https://elite.bbcelite.com/)
and [The Sentinel](https://thesentinel.bbcelite.com/) code guides.

## Layout

```
sources/            disassembly listings and generated data
  data/             cities.json and type_tables.json (generated)
tools/              optional maintenance tools for the generated material
docs/               the Markdown guide
  deep-dives/       long-form articles
  source/routines/  generated routine pages
  reference/        generated data pages
  assets/diagrams/  generated SVGs
```

[Method](docs/about/method.md) explains the evidence behind the guides and how
contributors can regenerate the derived material after a source change.

## Provenance and copyright

The analysis is derived from the retail `TAUCETI.D64` image and the published
interface, and cross-checked against the DOS and Spectrum versions where they
differ. *Tau Ceti* is © CRL Group PLC (1986). This repository ships no game
image and is not affiliated with CRL or the authors. It is an independent,
non-commercial work of study; the disassembly listings are kept private until
that question is settled.
