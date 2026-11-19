import os
import glob
from collections import defaultdict

ROOT = "bf_extracted"
TARGETS = {
    "00 75 06 00",
    "06 00 00 75",
    "6F 24 A8 55",
    "96 4D 00 A4",
}

groups = defaultdict(list)

for path in glob.glob(os.path.join(ROOT, "*")):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        sig = f.read(4).hex(" ").upper()

    if sig in TARGETS:
        groups[sig].append(path)


def common_prefix(files):
    with open(files[0], "rb") as f:
        reference = f.read()

    prefix = len(reference)

    for path in files[1:]:
        with open(path, "rb") as f:
            data = f.read()

        limit = min(prefix, len(data))
        i = 0

        while i < limit and reference[i] == data[i]:
            i += 1

        prefix = min(prefix, i)

        if prefix == 0:
            break

    return prefix, reference


for sig in sorted(groups):
    files = groups[sig]
    prefix, sample = common_prefix(files)

    print(f"\n{sig} | {len(files)} files")
    print(f"Full common prefix: {prefix} bytes")
    print("Bytes around divergence:")
    start = max(0, prefix - 16)
    end = min(len(sample), prefix + 16)
    print(f"  Offset {start:#x}: {sample[start:end].hex(' ')}")
