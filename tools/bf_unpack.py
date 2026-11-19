import os
import csv
import struct
import argparse

INDEX = 0x1CB190
STRIDE = 0x54
COUNT = 5374
DATA_BASE = 0x02771000


def read_index(f):
    records = []

    f.seek(INDEX)

    for i in range(COUNT):
        record = f.read(STRIDE)

        if len(record) != STRIDE:
            raise RuntimeError(f"Incomplete index record: {i}")

        size_field = struct.unpack_from("<I", record, 4)[0]
        size = size_field + 4

        name_bytes = record[0x17:].split(b"\0", 1)[0]
        name = name_bytes.decode("ascii", errors="replace")

        records.append((i, name, size))

    return records


def unpack(archive_path, output_dir):
    archive_size = os.path.getsize(archive_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(archive_path, "rb") as archive:
        records = read_index(archive)

        offset = DATA_BASE
        manifest_path = os.path.join(output_dir, "manifest.csv")

        with open(manifest_path, "w", newline="", encoding="utf-8") as manifest:
            writer = csv.writer(manifest)
            writer.writerow(["index", "filename", "offset", "size"])

            for i, name, size in records:
                end = offset + size

                if end > archive_size:
                    raise RuntimeError(
                        f"Record {i} exceeds archive boundary: "
                        f"0x{offset:X} - 0x{end:X}"
                    )

                archive.seek(offset)
                data = archive.read(size)

                if len(data) != size:
                    raise RuntimeError(f"Short read at record {i}")

                output_name = f"{i:04d}_{os.path.basename(name)}"
                output_path = os.path.join(output_dir, output_name)

                with open(output_path, "wb") as output:
                    output.write(data)

                writer.writerow([
                    i,
                    name,
                    f"0x{offset:X}",
                    size
                ])

                if (i + 1) % 100 == 0 or i == len(records) - 1:
                    print(f"[{i + 1}/{len(records)}] {output_name}")

                offset = end

    print("\nExtraction complete!")
    print(f"Files     : {len(records)}")
    print(f"Data end  : 0x{offset:X}")
    print(f"Remaining : 0x{archive_size - offset:X}")
    print(f"Output    : {output_dir}")
    print(f"Manifest  : {manifest_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prince of Persia WW BF unpacker")
    parser.add_argument("archive", nargs="?", default="prince.bf")
    parser.add_argument("-o", "--output", default="bf_extracted")
    args = parser.parse_args()

    unpack(args.archive, args.output)
