import struct
from pathlib import Path

XBE = Path("../default.xbe")

SECTION_TABLE_FO = 0x370
SECTION_COUNT = 35
SECTION_ENTRY_SIZE = 56


def load_sections(data):
    sections = []

    for i in range(SECTION_COUNT):
        offset = SECTION_TABLE_FO + i * SECTION_ENTRY_SIZE

        fields = struct.unpack_from("<9I", data, offset)

        flags = fields[0]
        va = fields[1]
        virtual_size = fields[2]
        raw_offset = fields[3]
        raw_size = fields[4]
        name_va = fields[5]

        sections.append({
            "index": i,
            "flags": flags,
            "va": va,
            "virtual_size": virtual_size,
            "raw_offset": raw_offset,
            "raw_size": raw_size,
            "name_va": name_va,
        })

    return sections


def va_to_file_offset(va, sections):
    for section in sections:
        start = section["va"]
        end = start + section["virtual_size"]

        if start <= va < end:
            delta = va - start

            if delta >= section["raw_size"]:
                return {
                    "status": "memory_only",
                    "section": section["index"],
                    "file_offset": None,
                }

            return {
                "status": "file_backed",
                "section": section["index"],
                "file_offset": section["raw_offset"] + delta,
            }

    return {
        "status": "unmapped",
        "section": None,
        "file_offset": None,
    }


def main():
    data = XBE.read_bytes()
    sections = load_sections(data)

    test_addresses = [
        0x3D1A6A,
        0x3D7C1C,
        0x3D1793,
        0x54B2E0,
        0x58C800,
        0x95A8E0,
    ]

    print("=== XBE VA -> FILE OFFSET ===")

    for va in test_addresses:
        result = va_to_file_offset(va, sections)

        print(f"\nVA: 0x{va:08X}")
        print(f"Status: {result['status']}")

        if result["section"] is not None:
            print(f"Section: {result['section']}")

        if result["file_offset"] is not None:
            print(f"File offset: 0x{result['file_offset']:08X}")


if __name__ == "__main__":
    main()
