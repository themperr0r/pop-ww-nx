from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

XBE = Path("../default.xbe")
ENTRY = 0x3D674C

# İlk aşamada XBE'nin daha önce kullandığımız
# bölüm eşlemesini kullanacağız.
# Dosya offset'ini doğruladıktan sonra genelleştireceğiz.
FILE_OFFSET = ENTRY - 0x10000 

data = XBE.read_bytes()
code = data[FILE_OFFSET:FILE_OFFSET + 128]

md = Cs(CS_ARCH_X86, CS_MODE_32)
md.detail = True

print(f"XBE entry: {ENTRY:#010x}")
print(f"File offset: {FILE_OFFSET:#010x}")
print("\n=== X86 INSTRUCTIONS ===")

for ins in md.disasm(code, ENTRY):
    print(f"{ins.address:08X}: {ins.bytes.hex(' '):<24} "
          f"{ins.mnemonic:<10} {ins.op_str}")
        
    if ins.mnemonic == "ret":
        break
