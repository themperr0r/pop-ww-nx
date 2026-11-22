import json
import re

with open("entry_instructions.json", "r") as f:
    instructions = json.load(f)

SUPPORTED = {
    "mov", "add", "sub", "and", "or", "xor",
    "cmp", "push", "pop", "call",
    "jae", "jne", "lea", "ret",
    "cdq", "idiv"
}

ir = []

for ins in instructions:
    mnemonic = ins["mnemonic"]
    operands = ins["operands"].split(", ", 1)

    item = {
        "address": hex(ins["address"]),
        "op": "UNKNOWN",
        "dst": None,
        "src": None
    }

    if mnemonic == "mov":
        dst, src = operands
        item["op"] = "MOV"
        item["dst"] = dst.upper()
        item["src"] = src

    elif mnemonic in ("add", "sub", "and", "or", "xor"):
        dst, src = operands
        item["op"] = mnemonic.upper()
        item["dst"] = dst.upper()
        item["src"] = src

    elif mnemonic == "cmp":
        dst, src = operands
        item["op"] = "CMP"
        item["dst"] = dst.upper()
        item["src"] = src

    elif mnemonic == "ret":
        item["op"] = "RET"

    ir.append(item)

with open("entry_ir.json", "w") as f:
    json.dump(ir, f, indent=4)

print(f"{len(ir)} instructions translated.")
print("Output: entry_ir.json")
