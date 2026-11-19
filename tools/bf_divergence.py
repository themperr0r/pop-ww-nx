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

for path in files[:8]:
    with open(path, "rb") as f:
        f.seek(0xD0)
        data = f.read(64)

    print(f"\n{os.path.basename(path)}")
    print(f"0xD0: {data.hex(' ')}")
    print("ASCII:", "".join(chr(b) if 32 <= b < 127 else "." for b in data))
