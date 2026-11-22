import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

analysis = json.loads((ROOT / "analysis_results.json").read_text())
api_map = json.loads((ROOT / "kernel_call_map.json").read_text())

function_by_instruction = defaultdict(list)

for function, instructions in analysis["function_instructions"].items():
    for ins in instructions:
        function_by_instruction[ins["address"]].append(function)

resolved = []

for call in api_map["resolved_calls"]:
    address = int(call["call_address"], 16)
    functions = function_by_instruction.get(address, [])

    resolved.append({
        "call_address": call["call_address"],
        "api": call["api"],
        "ordinal": call["ordinal"],
        "functions": functions,
    })

report = {
    "mapped_calls": sum(bool(item["functions"]) for item in resolved),
    "unmapped_calls": sum(not item["functions"] for item in resolved),
    "calls": resolved,
}

output = ROOT / "calls_by_function.json"
output.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("===== API CALL -> FUNCTION =====")

for item in resolved:
    if item["functions"]:
        functions = ", ".join(item["functions"])
        print(f'{item["call_address"]}  {item["api"]:<30} {functions}')
    else:
        print(f'{item["call_address"]}  {item["api"]:<30} FUNCTION NOT FOUND')

print(f"\nMapped calls:   {report['mapped_calls']}")
print(f"Unmapped calls: {report['unmapped_calls']}")
print(f"Saved: {output}")
