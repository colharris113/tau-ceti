"""Helpers for reading the (linear) disassembly listings.

The listings in ``sources/`` were swept straight through the code, so they
decode data as instructions and their line starts do not always coincide with
real routine entries.  They do, however, carry the *bytes* of every address,
which is all we need: build one 64K byte map, then re-disassemble from any
address that is genuinely an instruction boundary.

py65 is used for the opcode tables so the mnemonics are right.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LINE_RE = re.compile(r"^([0-9A-F]{4}): ((?:[0-9A-F]{2}(?: [0-9A-F]{2})*)??)(?: +)(.*)$")
HEX_RE = re.compile(r"^[0-9A-F]{2}$")

# A concise mnemonic table for branches, so cross-references can be followed.
BRANCHES = {
    0x10: "BPL", 0x30: "BMI", 0x50: "BVC", 0x70: "BVS",
    0x90: "BCC", 0xB0: "BCS", 0xD0: "BNE", 0xF0: "BEQ",
}


def load_byte_map(paths: list[Path]) -> dict[int, int]:
    """Read every ``ADDR: XX XX`` line and return address -> byte."""
    memory: dict[int, int] = {}
    for path in paths:
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^([0-9A-Fa-f]{4}): ((?:[0-9A-Fa-f]{2} ?)+)", raw)
            if not m:
                continue
            addr = int(m.group(1), 16)
            for i, byte in enumerate(m.group(2).split()):
                memory[(addr + i) & 0xFFFF] = int(byte, 16)
    return memory


class Disassembler:
    """Thin wrapper over py65 that decodes from our byte map."""

    def __init__(self, memory: dict[int, int]):
        from py65.devices.mpu6502 import MPU
        from py65.disassembler import Disassembler as Py65Disassembler

        self.bytes = bytearray(0x10000)
        for addr, byte in memory.items():
            self.bytes[addr] = byte
        self.mpu = MPU(memory=self.bytes)
        self.tool = Py65Disassembler(self.mpu)

    def instruction(self, addr: int) -> tuple[int, str, str]:
        """Return (length, mnemonic, operand-text) at addr."""
        length, text = self.tool.instruction_at(addr)
        parts = text.split(None, 1)
        mnemonic = parts[0] if parts else "???"
        operand = parts[1].split(";")[0].strip() if len(parts) > 1 else ""
        return length, mnemonic, operand

    def target(self, addr: int, mnemonic: str, operand: str) -> int | None:
        """Target of a control-flow instruction, if it has a fixed one.

        py65 has already resolved relative branches to absolute addresses in
        the operand text, so every fixed target looks the same.
        """
        if mnemonic not in BRANCHES.values() and mnemonic not in ("JSR", "JMP"):
            return None
        m = re.match(r"^\$([0-9A-Fa-f]{4})$", operand)
        return int(m.group(1), 16) if m else None


def dump(memory: dict[int, int], start: int, end: int) -> str:
    """Format the bytes in [start, end) as a linear listing."""
    dis = Disassembler(memory)
    out = []
    addr = start
    while addr < end:
        length, mnemonic, operand = dis.instruction(addr)
        raw = " ".join(f"{memory.get(addr + i, 0):02X}" for i in range(length))
        out.append(f"{addr:04X}: {raw:<8} {mnemonic:<3} {operand}".rstrip())
        addr += length
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: listing.py START END   (hex, e.g. 2B60 2C60)", file=sys.stderr)
        return 2
    here = Path(__file__).resolve().parent.parent
    paths = sorted((here / "sources").glob("dis_*.txt"))
    memory = load_byte_map(paths)
    print(dump(memory, int(argv[1], 16), int(argv[2], 16)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
