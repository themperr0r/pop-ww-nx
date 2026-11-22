from pathlib import Path
import json
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

XBE = Path("../default.xbe")
ENTRY = 0x3D674C
FILE_OFFSET = ENTRY - 0x10000

data = XBE.read_bytes()
code = data[FILE_OFFSET:FILE_OFFSET + 128]

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

instructions = []

for ins in md.disasm(code, ENTRY):
    instructions.append({
        "address": ins.address,
        "size": ins.size,
        "bytes": ins.bytes.hex(),
        "mnemonic": ins.mnemonic,
        "operands": ins.op_str,
        "groups": list(ins.groups),
        "operands_detail": [
    {
        "type": op.type,
        "size": op.size,
        "register": ins.reg_name(op.reg) if op.type == 1 else None,
        "immediate": op.imm if op.type == 2 else None,
        "memory": {
            "base": ins.reg_name(op.mem.base) if op.mem.base else None,
            "index": ins.reg_name(op.mem.index) if op.mem.index else None,
            "scale": op.mem.scale,
            "displacement": op.mem.disp
        } if op.type == 3 else None
    }
    for op in ins.operands
]
    })

    if ins.mnemonic == "ret":
        break

output = Path("entry_instructions.json")
output.write_text(
    json.dumps(instructions, indent=4),
    encoding="utf-8"
)

print(f"{len(instructions)} instructions decoded.")
print(f"Saved to: {output}")
