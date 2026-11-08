import sys

ROWS = [
 ("BRK imp","ORA izx",None,None,None,"ORA zp","ASL zp",None,"PHP imp","ORA imm","ASL acc",None,None,"ORA abs","ASL abs",None),
 ("BPL rel","ORA izy",None,None,None,"ORA zpx","ASL zpx",None,"CLC imp","ORA aby",None,None,None,"ORA abx","ASL abx",None),
 ("JSR abs","AND izx",None,None,"BIT zp","AND zp","ROL zp",None,"PLP imp","AND imm","ROL acc",None,"BIT abs","AND abs","ROL abs",None),
 ("BMI rel","AND izy",None,None,None,"AND zpx","ROL zpx",None,"SEC imp","AND aby",None,None,None,"AND abx","ROL abx",None),
 ("RTI imp","EOR izx",None,None,None,"EOR zp","LSR zp",None,"PHA imp","EOR imm","LSR acc",None,"JMP abs","EOR abs","LSR abs",None),
 ("BVC rel","EOR izy",None,None,None,"EOR zpx","LSR zpx",None,"CLI imp","EOR aby",None,None,None,"EOR abx","LSR abx",None),
 ("RTS imp","ADC izx",None,None,None,"ADC zp","ROR zp",None,"PLA imp","ADC imm","ROR acc",None,"JMP ind","ADC abs","ROR abs",None),
 ("BVS rel","ADC izy",None,None,None,"ADC zpx","ROR zpx",None,"SEI imp","ADC aby",None,None,None,"ADC abx","ROR abx",None),
 (None,"STA izx",None,None,"STY zp","STA zp","STX zp",None,"DEY imp",None,"TXA imp",None,"STY abs","STA abs","STX abs",None),
 ("BCC rel","STA izy",None,None,"STY zpx","STA zpx","STX zpy",None,"TYA imp","STA aby","TXS imp",None,None,"STA abx",None,None),
 ("LDY imm","LDA izx","LDX imm",None,"LDY zp","LDA zp","LDX zp",None,"TAY imp","LDA imm","TAX imp",None,"LDY abs","LDA abs","LDX abs",None),
 ("BCS rel","LDA izy",None,None,"LDY zpx","LDA zpx","LDX zpy",None,"CLV imp","LDA aby","TSX imp",None,"LDY abx","LDA abx","LDX aby",None),
 ("CPY imm","CMP izx",None,None,"CPY zp","CMP zp","DEC zp",None,"INY imp","CMP imm","DEX imp",None,"CPY abs","CMP abs","DEC abs",None),
 ("BNE rel","CMP izy",None,None,None,"CMP zpx","DEC zpx",None,"CLD imp","CMP aby",None,None,None,"CMP abx","DEC abx",None),
 ("CPX imm","SBC izx",None,None,"CPX zp","SBC zp","INC zp",None,"INX imp","SBC imm","NOP imp",None,"CPX abs","SBC abs","INC abs",None),
 ("BEQ rel","SBC izy",None,None,None,"SBC zpx","INC zpx",None,"SED imp","SBC aby",None,None,None,"SBC abx","INC abx",None),
]
OPS = {}
for r, row in enumerate(ROWS):
    for c, e in enumerate(row):
        if e is None:
            continue
        m, mode = e.split()
        OPS[r * 16 + c] = (m, mode)
LEN = {"imp":1,"acc":1,"imm":2,"zp":2,"zpx":2,"zpy":2,"izx":2,"izy":2,"rel":2,"abs":3,"abx":3,"aby":3,"ind":3}

def dis(mem, base, start, end, one_per_line=True):
    a = start
    out = []
    while a < end:
        op = mem[a - base]
        if op not in OPS:
            out.append("%04X  .byte $%02X" % (a, op)); a += 1; continue
        m, mode = OPS[op]
        n = LEN[mode]
        bs = mem[a - base:a - base + n]
        if len(bs) < n: break
        arg = ""
        if mode == "imm": arg = "#$%02X" % bs[1]
        elif mode == "zp": arg = "$%02X" % bs[1]
        elif mode == "zpx": arg = "$%02X,X" % bs[1]
        elif mode == "zpy": arg = "$%02X,Y" % bs[1]
        elif mode == "izx": arg = "($%02X,X)" % bs[1]
        elif mode == "izy": arg = "($%02X),Y" % bs[1]
        elif mode == "rel":
            d = bs[1] - 256 if bs[1] > 127 else bs[1]
            arg = "$%04X" % ((a + 2 + d) & 0xFFFF)
        elif mode == "abs": arg = "$%04X" % (bs[1] | bs[2] << 8)
        elif mode == "abx": arg = "$%04X,X" % (bs[1] | bs[2] << 8)
        elif mode == "aby": arg = "$%04X,Y" % (bs[1] | bs[2] << 8)
        elif mode == "ind": arg = "($%04X)" % (bs[1] | bs[2] << 8)
        out.append("%04X  %-9s %s %s" % (a, " ".join("%02X" % b for b in bs), m, arg))
        a += n
    return "\n".join(out)

if __name__ == "__main__":
    f, base, s, e = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16), int(sys.argv[4], 16)
    mem = open(f, "rb").read()
    print(dis(mem, base, s, e))
