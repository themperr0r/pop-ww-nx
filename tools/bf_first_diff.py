import os
import glob

TARGET = "00 75 06 00"
ROOT = "bf_extracted"

files = []

for path in sorted(glob.glob(os.path.join(ROOT, "*"))):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        if f.read(4).hex(" ").upper() == TARGET:
            files.append(path)

with open(files[0], "rb") as f:
    reference = f.read()

print("Reference:", os.path.basename(files[0]))

for path in files[1:]:
    with open(path, "rb") as f:
        data = f.read()

    limit = min(len(reference), len(data))
    diff = next((i for i in range(limit) if reference[i] != data[i]), None)

    if diff is not None:
        print("\nFirst differing file:", os.path.basename(path))
        print(f"First difference: {diff:#x}")
        start = max(0, diff - 16)
        end = diff + 32

        print(f"Reference [{start:#x}]:", reference[start:end].hex(" "))
        print(f"Other     [{start:#x}]:", data[start:end].hex(" "))
        break
