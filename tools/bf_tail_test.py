import os
import glob
import hashlib

ROOT = "bf_extracted"
TARGET = "00 75 06 00"
START = 0x6019
END = 0x9000

reference_path = os.path.join(ROOT, "0030_A_fd91c932.bin")

with open(reference_path, "rb") as f:
    f.seek(START)
    reference = f.read(END - START)

target_hash = hashlib.sha256(reference).hexdigest()

files = []

for path in sorted(glob.glob(os.path.join(ROOT, "*"))):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        if f.read(4).hex(" ").upper() == TARGET:
            files.append(path)

matches = []

for path in files:
    with open(path, "rb") as f:
        f.seek(START)
        chunk = f.read(END - START)

    if len(chunk) == len(reference):
        if hashlib.sha256(chunk).hexdigest() == target_hash:
            matches.append(path)

print("Total files:", len(files))
print("Matching tail:", len(matches))
print("Reference:", os.path.basename(reference_path))
print("\nFirst 20 matches:")

for path in matches[:20]:
    print(os.path.basename(path))
