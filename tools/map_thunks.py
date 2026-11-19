import re

thunks = {
    0x54B2E0: 3,  0x54B2E4: 6,  0x54B2F0: 8,
    0x54B2F4: 27, 0x54B2F8: 12, 0x54B2FC: 4,
    0x54B300: 14, 0x54B304: 19, 0x54B308: 8,
    0x54B30C: 10, 0x54B310: 5,  0x54B314: 9,
    0x54B318: 3,  0x54B324: 83, 0x54B328: 66,
    0x54B32C: 3,  0x54B334: 3,  0x54B340: 3,
    0x54B358: 28, 0x54B35C: 28, 0x54B360: 3,
    0x54B364: 4,  0x54B36C: 3,  0x54B39C: 3,
    0x54B3BC: 3,  0x54B3C0: 3,  0x54B3C8: 9,
    0x54B3CC: 6,  0x54B3D0: 7,  0x54B3D4: 11,
    0x54B414: 4,  0x54B43C: 5,  0x54B510: 5,
    0x54B514: 5,  0x54B524: 4,
}

exports = {}

with open("xboxkrnl.exe.def", encoding="utf-8", errors="replace") as f:
    for line in f:
        match = re.match(r"\s*(\S+)\s+@\s*(\d+)", line)
        if match:
            name, ordinal = match.groups()
            exports[int(ordinal)] = name

print(f"{'THUNK':<12} {'ORDINAL':<9} {'CALLS':<7} FUNCTION")
print("-" * 65)

for address, calls in sorted(thunks.items()):
    with open("default.xbe", "rb") as f:
        offset = 0x547000 + address - 0x54B2E0
        f.seek(offset)
        raw = int.from_bytes(f.read(4), "little")

    ordinal = raw & 0x7FFFFFFF
    name = exports.get(ordinal, "NOT FOUND")
    print(f"0x{address:08X} {ordinal:<9} {calls:<7} {name}")
