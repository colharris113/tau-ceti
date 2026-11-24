# Tau Ceti — A Guide to the C64 Code

An address-level study of *Tau Ceti* (Pete Cooke, C64 conversion by John Twiddy;
CRL, 1986): what each part of the program does, how the record table is laid
out, how docking really works, how fuel is burned, and how the game's data
drives its robots.

The published site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
and is in the style of the [Elite](https://elite.bbcelite.com/) and
[The Sentinel](https://thesentinel.bbcelite.com/) code guides: prose tied to
real addresses, with diagrams generated from the game's own constants and
data.

## Status

Work in progress. The scaffold, the source-listing pipeline and three deep
dives are in place; the remaining routines and screens will be added as the
analysis is verified.

## Building the site

```sh
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt      # Windows
# .venv/bin/pip install -r requirements.txt        # Unix

.venv/Scripts/python tools/build_all.py
.venv/Scripts/mkdocs serve                         # http://127.0.0.1:8000
```

A strict build (warnings are errors) is the publishing gate:

```sh
.venv/Scripts/mkdocs build --strict
```

## Regenerating the derived content

Everything under `docs/source/routines/`, `docs/reference/type-tables.md`,
`docs/assets/diagrams/` and `sources/data/` is generated. Do not edit those by
hand; edit `tools/symbols.json` or the builders and re-run:

```sh
.venv/Scripts/python tools/build_all.py
```

If you have the game image extracted (the PRG that loads at `$8900`), the type
tables and the lathe profiles can be re-derived from your own copy:

```sh
.venv/Scripts/python -I tools/extract_tables.py path/to/04_8900-CC00.prg
```

The extractor lives in `tools/` and only slices bytes at known addresses; the
image is treated as data, never executed.

## Layout

```
sources/            disassembly listings and generated data
  data/             type_tables.json (generated)
tools/              builders: source listings, diagrams, tables
docs/               the site
  deep-dives/       long-form articles
  source/routines/  generated routine pages
  reference/        generated data pages
  assets/diagrams/  generated SVGs
```

## Provenance and copyright

The analysis is derived from the retail `TAUCETI.D64` image and the published
interface, and cross-checked against the DOS and Spectrum versions where they
differ. *Tau Ceti* is © CRL Group PLC (1986). This repository ships no game
image and is not affiliated with CRL or the authors. It is an independent,
non-commercial work of study; the disassembly listings are kept private until
that question is settled.
