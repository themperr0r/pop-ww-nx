import os
import glob
from collections import defaultdict

ROOT = "bf_extracted"
groups = defaultdict(list)

for path in sorted(glob.glob(os.path.join(ROOT, "*"))):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        header = f.read(16)

    signature = header[:4].hex(" ").upper() if header else "EMPTY"
    groups[signature].append(os.path.basename(path))

ordered = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

with open("signature_report.txt", "w") as report:
    for signature, files in ordered:
        report.write(f"\n{signature} | {len(files)} files\n")
        for name in files:
            report.write(f"  {name}\n")

print("Total files:", sum(map(len, groups.values())))
print("Unique signatures:", len(groups))
print("\n=== TOP 30 SIGNATURES ===")

for signature, files in ordered[:30]:
    print(f"{signature:12} | {len(files):4} files")

print("\nFull report saved to signature_report.txt")
