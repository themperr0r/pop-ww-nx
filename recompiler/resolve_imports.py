import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
XBE_PATH = ROOT.parent / "default.xbe"
HEADER_PATH = ROOT / "xboxkrnl.h"
OUTPUT_PATH = ROOT / "kernel_imports.json"

RETAIL_XOR = 0x5B6D40B6
KERNEL_THUNK_FIELD = 0x158

data = XBE_PATH.read_bytes()
header = HEADER_PATH.read_text(encoding="utf-8", errors="replace")

u32 = lambda offset: struct.unpack_from("<I", data, offset)[0]

# Xbox kernel export tablosunu oku.
ordinal_names = {}

for line in header.splitlines():
    match = re.search(r'"([^"]+)"\s*,\s*//\s*@(\d+)', line)
    if match:
        name, ordinal = match.groups()
        ordinal_names[int(ordinal)] = name

# XBE section tablosunu oku.
base = u32(0x104)
section_count = u32(0x11C)
section_table = u32(0x120) - base

sections = []

for i in range(section_count):
    pos = section_table + i * 56
    flags, va, vsize, raw, rsize = struct.unpack_from("<5I", data, pos)
    sections.append((va, vsize, raw, rsize))

def va_to_offset(va):
    for start, vsize, raw, rsize in sections:
        if start <= va < start + vsize:
            delta = va - start
            if delta < rsize:
                return raw + delta
    return None

# Kernel thunk tablosunun adresini çöz.
encoded = u32(KERNEL_THUNK_FIELD)
thunk_va = encoded ^ RETAIL_XOR
thunk_offset = va_to_offset(thunk_va)

if thunk_offset is None:
    raise RuntimeError(f"Kernel thunk VA not mapped: 0x{thunk_va:08X}")

imports = []

for index in range(1000):
    value = u32(thunk_offset + index * 4)

    if value == 0:
        break

    if not value & 0x80000000:
        raise RuntimeError(
            f"Unexpected thunk value at index {index}: 0x{value:08X}"
        )

    ordinal = value & 0x7FFFFFFF
    imports.append({
        "index": index,
        "thunk_va": f"0x{thunk_va + index * 4:08X}",
        "ordinal": ordinal,
        "name": ordinal_names.get(ordinal, "UNKNOWN"),
    })
else:
    raise RuntimeError("Thunk terminator not found")

OUTPUT_PATH.write_text(
    json.dumps(imports, indent=2),
    encoding="utf-8"
)

known = [item for item in imports if item["name"] != "UNKNOWN"]
unknown = [item for item in imports if item["name"] == "UNKNOWN"]

print("===== KERNEL IMPORT RESOLUTION =====")
print(f"Thunk table:       0x{thunk_va:08X}")
print(f"Total imports:     {len(imports)}")
print(f"Resolved names:    {len(known)}")
print(f"Unknown ordinals:  {len(unknown)}")

print("\n===== FIRST 25 IMPORTS =====")

for item in imports[:25]:
    print(
        f'{item["thunk_va"]}  '
        f'ordinal {item["ordinal"]:3}  '
        f'{item["name"]}'
    )

if unknown:
    print("\n===== UNKNOWN ORDINALS =====")
    for item in unknown:
        print(item["ordinal"])

print(f"\nSaved: {OUTPUT_PATH}")
