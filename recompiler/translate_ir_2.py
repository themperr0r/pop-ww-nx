
import json

with open("entry_instructions.json", "r") as f:
    instructions = json.load(f)


def translate_operand(op):
    if op["type"] == 1:
        return {
            "kind": "register",
            "name": op["register"]
        }

    if op["type"] == 2:
        return {
            "kind": "immediate",
            "value": op["immediate"]
        }

    if op["type"] == 3:
        return {
            "kind": "memory",
            "base": op["memory"]["base"],
            "index": op["memory"]["index"],
            "scale": op["memory"]["scale"],
            "displacement": op["memory"]["displacement"]
        }

    return {"kind": "unknown"}


ir = []

for ins in instructions:
    operands = [
        translate_operand(op)
        for op in ins["operands_detail"]
    ]

    ir.append({
        "address": hex(ins["address"]),
        "op": ins["mnemonic"].upper(),
        "operands": operands
    })


with open("entry_ir.json", "w") as f:
    json.dump(ir, f, indent=4)

print(f"{len(ir)} instructions translated.")
print("Output: entry_ir.json")

