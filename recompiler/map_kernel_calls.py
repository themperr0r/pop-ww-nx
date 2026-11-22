import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

imports = json.loads((ROOT / "kernel_imports.json").read_text())
analysis = json.loads((ROOT / "analysis_results.json").read_text())

by_va = {
    int(item["thunk_va"], 16): item
    for item in imports
}

def as_int(value):
    return int(value, 16) if isinstance(value, str) else value

results = []
unresolved = []

for call in analysis["indirect_call_sites"]:
    address = as_int(call["address"])
    operand = call["operand"]

    match = re.search(r"\[0x([0-9a-fA-F]+)\]", operand)

    if not match:
        unresolved.append({
            "address": f"0x{address:08X}",
            "operand": operand,
            "kind": "dynamic_indirect_call",
        })
        continue

    target = int(match.group(1), 16)
    item = by_va.get(target)

    if item:
        results.append({
            "call_address": f"0x{address:08X}",
            "thunk_address": item["thunk_va"],
            "ordinal": item["ordinal"],
            "api": item["name"],
        })
    else:
        unresolved.append({
            "address": f"0x{address:08X}",
            "operand": operand,
            "kind": "non_kernel_or_dynamic_pointer",
        })

counts = Counter(item["api"] for item in results)

report = {
    "resolved_call_count": len(results),
    "unresolved_call_count": len(unresolved),
    "api_call_counts": dict(counts.most_common()),
    "resolved_calls": results,
    "unresolved_calls": unresolved,
}

output = ROOT / "kernel_call_map.json"
output.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("===== API CALL FREQUENCY =====")
for api, count in counts.most_common():
    print(f"{count:3}  {api}")

print(f"\nResolved:   {len(results)}")
print(f"Unresolved: {len(unresolved)}")
print(f"Saved: {output}")
