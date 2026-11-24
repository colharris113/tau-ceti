#!/usr/bin/env python3
"""Run every generator for the guide.

    .venv/Scripts/python tools/build_all.py

Order matters only in that the diagrams and tables are independent of the
source pages; all of them read from ``sources/`` and write under ``docs/``.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

STEPS = [
    "build_diagrams.py",
    "build_type_tables.py",
    "build_source.py",
]


def main() -> int:
    for step in STEPS:
        print(f"--- {step}")
        result = subprocess.run(
            [sys.executable, "-I", str(TOOLS / step)], cwd=ROOT
        )
        if result.returncode != 0:
            print(f"{step} failed with {result.returncode}")
            return result.returncode
    print("all generators finished")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
