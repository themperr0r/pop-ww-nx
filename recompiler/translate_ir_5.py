
import json

INPUT_FILE = "entry_instructions.json"
OUTPUT_FILE = "entry_ir.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    instructions = json.load(f)


def translate_operand(text):
    text = text.strip()

    if text.startswith("dword ptr"):
        text = text.replace("dword ptr", "").strip()

    if text.startswith("[") and text.endswith("]"):
        return {
            "kind": "memory",
            "expression": text[1:-1]
        }

    registers = {
        "eax", "ebx", "ecx", "edx",
        "esi", "edi", "ebp", "esp",
        "ax", "bx", "cx", "dx",
        "al", "ah", "bl", "bh",
        "cl", "ch", "dl", "dh"
    }

    if text.lower() in registers:
        return {
            "kind": "register",
            "name": text.lower()
        }

    try:
        return {
            "kind": "immediate",
            "value": int(text, 0)
        }
    except ValueError:
        return {
            "kind": "expression",
            "value": text
        }


ir = []

for ins in instructions:
    mnemonic = ins["mnemonic"].lower()
    operands = ins["operands"].split(", ", 1)

    item = {
        "address": hex(ins["address"]),
        "op": "UNKNOWN",
        "operands": []
    }

    if mnemonic in ("mov", "add", "sub", "and", "or", "xor", "cmp"):
        item["op"] = mnemonic.upper()
        item["operands"] = [
            translate_operand(op) for op in operands
        ]

    elif mnemonic in ("push", "pop"):
        item["op"] = mnemonic.upper()
        item["operands"] = [
            translate_operand(operands[0])
        ]

    elif mnemonic == "call":
        item["op"] = "CALL"
        target = translate_operand(operands[0])
        item["operands"] = [target]

        if target["kind"] == "immediate":
            item["call_type"] = (
                "internal"
                if 0x10000 <= target["value"] < 0x500000
                else "external_or_import"
            )
        else:
            item["call_type"] = "indirect"

    elif mnemonic in ("jae", "jne"):
        item["op"] = mnemonic.upper()
        item["operands"] = [
            translate_operand(operands[0])
        ]

    elif mnemonic == "lea":
        item["op"] = "LEA"
        item["operands"] = [
            translate_operand(op) for op in operands
        ]

    elif mnemonic == "ret":
        item["op"] = "RET"

    elif mnemonic in ("cdq", "idiv"):
        item["op"] = mnemonic.upper()
        item["operands"] = [
            translate_operand(op) for op in operands
        ] if ins["operands"] else []

    ir.append(item)


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(ir, f, indent=4)

unknown = [x for x in ir if x["op"] == "UNKNOWN"]

print(f"{len(ir)} instructions processed.")
print(f"{len(unknown)} unsupported instructions.")

for ins in ir:
    if ins["op"] == "CALL":
        print(
            f"CALL at {ins['address']} -> "
            f"{ins['operands'][0]} "
            f"({ins['call_type']})"
        )

print(f"Output: {OUTPUT_FILE}")

