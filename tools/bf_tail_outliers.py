import os
import glob

ROOT = "bf_extracted"
START = 0x6019
END = 0x9000
REFERENCE = "0030_A_fd91c932.bin"

with open(os.path.join(ROOT, REFERENCE), "rb") as f:
    f.seek(START)
    reference = f.read(END - START)

for path in sorted(glob.glob(os.path.join(ROOT, "*"))):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        if f.read(4).hex(" ").upper() != "00 75 06 00":
            continue
        f.seek(START)
        data = f.read(END - START)

    if data != reference:
        limit = min(len(data), len(reference))
        diffs = [i for i in range(limit) if data[i] != reference[i]]

        first = diffs[0] if diffs else limit

        print(
            os.path.basename(path),
            "| size:", os.path.getsize(path),
            "| first diff:", hex(START + first),
            "| differing bytes:", len(diffs),
            "| tail length:", len(data)
        )
