import json
import struct
from collections import Counter, deque
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86_const import X86_OP_IMM

ROOT = Path(__file__).resolve().parent.parent
XBE_PATH = ROOT / "default.xbe"

SECTION_SIZE = 56
EXECUTABLE_FLAG = 4
ENTRY_XOR = 0xA8FC57AB
MAX_FUNCTIONS = 100000
MAX_INSTRUCTIONS = 2000000


def u32(data, offset):
    return struct.unpack_from("<I", data, offset)[0]


def main():
    data = XBE_PATH.read_bytes()

    if data[:4] != b"XBEH":
        raise RuntimeError("Invalid XBE header")

    base = u32(data, 0x104)
    count = u32(data, 0x11C)
    table_va = u32(data, 0x120)
    entry = u32(data, 0x128) ^ ENTRY_XOR
    table_offset = table_va - base

    sections = []

    for i in range(count):
        pos = table_offset + i * SECTION_SIZE
        fields = struct.unpack_from("<9I20s", data, pos)

        flags, va, vsize, raw, rsize = fields[:5]

        if flags & EXECUTABLE_FLAG and rsize:
            sections.append({
                "va": va,
                "end": va + min(vsize, rsize),
                "raw": raw,
            })

    def get_code(va):
        for section in sections:
            if section["va"] <= va < section["end"]:
                offset = section["raw"] + va - section["va"]
                return data[offset:min(offset + 15, len(data))]
        return None

    def executable(va):
        return get_code(va) is not None

    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True

    function_queue = deque([entry])
    queued = {entry}
    functions = set()

    instruction_cache = {}
    function_instruction_map = {}

    calls = Counter()
    indirect_calls = 0
    indirect_call_sites = []
    branch_targets = set()

    while function_queue and len(functions) < MAX_FUNCTIONS:
        function = function_queue.popleft()

        if function in functions or not executable(function):
            continue

        functions.add(function)

        pending_blocks = [function]
        visited_blocks = set()
        function_instructions = {}

        while pending_blocks and len(instruction_cache) < MAX_INSTRUCTIONS:
            address = pending_blocks.pop()

            if address in visited_blocks or not executable(address):
                continue

            visited_blocks.add(address)

            while executable(address):
                if address in function_instructions:
                    break

                ins = instruction_cache.get(address)

                if ins is None:
                    code = get_code(address)
                    instructions = list(md.disasm(code, address, count=1))

                    if not instructions:
                        break

                    ins = instructions[0]

                    instruction_cache[address] = {
                        "address": ins.address,
                        "size": ins.size,
                        "mnemonic": ins.mnemonic,
                        "op_str": ins.op_str,
                        "bytes": ins.bytes.hex(),
                    }

                record = instruction_cache[address]
                function_instructions[address] = record

                next_address = address + record["size"]
                mnemonic = record["mnemonic"]

                operands = list(md.disasm(
                    bytes.fromhex(record["bytes"]),
                    address,
                    count=1
                ))

                if not operands:
                    break

                operands = operands[0].operands

                if mnemonic == "call":
                    if operands and operands[0].type == X86_OP_IMM:
                        target = operands[0].imm & 0xFFFFFFFF
                        calls[target] += 1

                        if target not in queued and executable(target):
                            function_queue.append(target)
                            queued.add(target)
                    else:
                        indirect_calls += 1

                        indirect_call_sites.append({
                            "address": f"0x{address:08X}",
                            "operand": record["op_str"],
                            "bytes": record["bytes"],
                        })

                    address = next_address
                    continue

                if mnemonic.startswith("ret") or mnemonic == "iret":
                    break

                if mnemonic.startswith("j"):
                    if operands and operands[0].type == X86_OP_IMM:
                        target = operands[0].imm & 0xFFFFFFFF

                        if executable(target):
                            branch_targets.add(target)
                            pending_blocks.append(target)

                    if mnemonic == "jmp":
                        break

                    address = next_address
                    continue

                if mnemonic.startswith("loop"):
                    if operands and operands[0].type == X86_OP_IMM:
                        target = operands[0].imm & 0xFFFFFFFF

                        if executable(target):
                            branch_targets.add(target)
                            pending_blocks.append(target)

                    address = next_address
                    continue

                address = next_address

        function_instruction_map[function] = sorted(
            function_instructions.values(),
            key=lambda item: item["address"]
        )

    internal_calls = Counter({
        target: hits
        for target, hits in calls.items()
        if executable(target)
    })

    print("===== RECURSIVE XBE ANALYSIS =====")
    print(f"Entry point:                 0x{entry:08X}")
    print(f"Executable sections:         {len(sections)}")
    print(f"Discovered function entries: {len(functions):,}")
    print(f"Unique decoded instructions: {len(instruction_cache):,}")
    print(f"Direct call targets:         {len(calls):,}")
    print(f"Internal call targets:       {len(internal_calls):,}")
    print(f"Indirect call instructions:  {indirect_calls:,}")
    print(f"Branch destinations:         {len(branch_targets):,}")

    print("\n===== MOST CALLED FUNCTIONS =====")

    for target, hits in internal_calls.most_common(30):
        print(f"0x{target:08X}  {hits:4} calls")

    print("\n===== FUNCTION DISASSEMBLY =====")
    print(f"Functions with saved instructions: {len(function_instruction_map):,}")
    print(
        "Total function-instruction associations: "
        f"{sum(len(items) for items in function_instruction_map.values()):,}"
    )

    print("\n===== ANALYSIS LIMITS =====")
    print(f"Function limit reached: {len(functions) >= MAX_FUNCTIONS}")
    print(f"Instruction limit reached: {len(instruction_cache) >= MAX_INSTRUCTIONS}")

    report = {
        "entry_point": f"0x{entry:08X}",
        "executable_sections": len(sections),
        "discovered_functions": sorted(
            f"0x{x:08X}" for x in functions
        ),
        "instruction_count": len(instruction_cache),
        "function_instructions": {
            f"0x{address:08X}": instructions
            for address, instructions in sorted(function_instruction_map.items())
        },
        "direct_call_targets": [
            {"address": f"0x{target:08X}", "count": hits}
            for target, hits in calls.most_common()
        ],
        "indirect_call_count": indirect_calls,
        "indirect_call_sites": indirect_call_sites,
        "branch_targets": sorted(
            f"0x{x:08X}" for x in branch_targets
        ),
    }

    output = ROOT / "analysis_results.json"
    output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print(f"\nSaved analysis report: {output}")
    print("\nAnalysis complete. Function entries remain discovered candidates.")


if __name__ == "__main__":
    main()
