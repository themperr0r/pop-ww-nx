import os

ROOT = "bf_extracted"
A = os.path.join(ROOT, "0030_A_fd91c932.bin")
B = os.path.join(ROOT, "0740_A_fd97ca0c.bin")

a = open(A, "rb").read()
b = open(B, "rb").read()

print("Sizes:", len(a), len(b))

diffs = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]

print("Different bytes:", len(diffs))
print("Same bytes:", len(a) - len(diffs))
print("Difference ratio: {:.2f}%".format(100 * len(diffs) / len(a)))

print("\nFirst 30 differing offsets:")
for off in diffs[:30]:
    print(f"{off:#08x}: {a[off]:02x} -> {b[off]:02x}")

ranges = []
for off in diffs:
    if not ranges or off > ranges[-1][1] + 1:
        ranges.append([off, off])
    else:
        ranges[-1][1] = off

print("\nDifference ranges:", len(ranges))
for start, end in ranges[:20]:
    print(f"{start:#08x} - {end:#08x} ({end-start+1} bytes)")
