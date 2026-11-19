import os
import glob
from collections import defaultdict

ROOT = "bf_extracted"
groups = defaultdict(list)

for path in glob.glob(os.path.join(ROOT, "*")):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        sig = f.read(4).hex(" ").upper()

    groups[sig].append(path)


def common_prefix(files):
    data = []

    for path in files:
        with open(path, "rb") as f:
            data.append(f.read(128))

    limit = min(map(len, data))
    for i in range(limit):
        if len({item[i] for item in data}) != 1:
            return i

    return limit


ordered = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

for sig, files in ordered[:10]:
    prefix = common_prefix(files)

    with open(files[0], "rb") as f:
        sample = f.read(64)

    print(f"\n{sig} | {len(files)} files")
    print(f"Common prefix: {prefix} bytes")
    print("Sample:", sample.hex(" "))
