import os

ROOT = "bf_extracted"
A = open(os.path.join(ROOT, "0030_A_fd91c932.bin"), "rb").read()
B = open(os.path.join(ROOT, "0740_A_fd97ca0c.bin"), "rb").read()

BLOCK = 256

print("Offset      Different  Same")
print("-" * 35)

for start in range(0, min(len(A), len(B)), BLOCK):
    end = min(start + BLOCK, len(A))
    diff = sum(x != y for x, y in zip(A[start:end], B[start:end]))
    same = end - start - diff

    if diff:
        print(f"{start:#08x}    {diff:3}/{end-start:<3}    {same:3}")

