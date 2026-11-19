import os
import glob
import hashlib
from collections import defaultdict, Counter

ROOT = "bf_extracted"
groups = defaultdict(list)

for path in glob.glob(os.path.join(ROOT, "*")):
    if not os.path.isfile(path) or path.endswith("manifest.csv"):
        continue

    with open(path, "rb") as f:
        signature = f.read(4).hex(" ").upper()

    groups[signature].append(path)


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


ordered = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

for signature, paths in ordered[:10]:
    sizes = Counter(os.path.getsize(p) for p in paths)
    hashes = Counter(sha256(p) for p in paths)

    print(f"\n{signature}")
    print(f"Files          : {len(paths)}")
    print(f"Unique sizes   : {len(sizes)}")
    print(f"Unique contents: {len(hashes)}")
    print(f"Exact duplicates: {len(paths) - len(hashes)}")

    print("Common sizes:")
    for size, count in sizes.most_common(3):
        print(f"  {size:,} bytes: {count} files")
