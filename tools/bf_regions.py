import os

ROOT = "bf_extracted"
A = open(os.path.join(ROOT, "0030_A_fd91c932.bin"), "rb").read()
B = open(os.path.join(ROOT, "0740_A_fd97ca0c.bin"), "rb").read()

same = [x == y for x, y in zip(A, B)]

start = 0
for i in range(1, len(same) + 1):
    if i == len(same) or same[i] != same[start]:
        length = i - start

        if length >= 32:
            status = "SAME" if same[start] else "DIFFERENT"
            print(f"{status:9} 0x{start:04X} - 0x{i-1:04X}  ({length:,} bytes)")

        start = i
