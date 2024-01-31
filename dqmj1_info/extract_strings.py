from dataclasses import dataclass
from typing import List

import argparse
import logging
import pathlib
import sys

import pandas as pd


@dataclass
class StringTable:
    name: str
    start: int
    end: int


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_directory", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    data_directory = pathlib.Path(args.data_directory)
    output_csv = pathlib.Path(args.output_csv)

    string_locations = {
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringTable("strings_a", 0x020735F0, 0x020749E8),
                StringTable("strings_b", 0x0207805C, 0x02083DE3),
                StringTable("strings_c", 0x02084B18, 0x0208A7B8),
                StringTable("strings_d", 0x0209072C, 0x02091753),
            ],
        ),
        pathlib.Path("overlay") / "overlay_0000.bin": (
            0x021a0a00,
            [
                StringTable("strings_h", 0x021f5950, 0x021f66ec),
                StringTable("strings_i", 0x021f678c, 0x021f6d6c),
                StringTable("strings_j", 0x021f6ed8, 0x021f78b8),
                StringTable("strings_k", 0x021f80c0, 0x021fc140),
                StringTable("strings_l", 0x021fc224, 0x021fc940),
                StringTable("strings_m", 0x021fcb10, 0x021fd2a0),
                StringTable("strings_n", 0x021fd2f8, 0x021fd45c),
                StringTable("strings_o", 0x021fd588, 0x021fd874),
            ],
        ),
    }

    strings = []
    for file_subpath, (offset, tables) in sorted(string_locations.items()):
        filepath = data_directory / file_subpath
        logging.debug(f"Extracting strings from: {filepath}")

        with open(filepath, "rb") as input_stream:
            file_bytes = input_stream.read()
            logging.debug(f"Read {len(file_bytes)} bytes from {filepath}")

            for table in tables:
                logging.debug(f"Reading table: {table}")

                start = table.start - offset
                length = table.end - table.start

                num_before = len(strings)
                buffer = []
                for i, byte in enumerate(file_bytes[start : start + length]):
                    # Note: The skipping of 0x0A at possible string start is due to an edge case I
                    # saw at 0x0207d792
                    if (byte == 0x00 or byte == 0x0A) and len(buffer) == 0:
                        continue
                    # Note: The check against 0xFE is due ot an edge case at 0x02079c16.
                    elif byte == 0xFF or byte == 0xFE:
                        string = "".join(buffer)
                        j = i - len(buffer)

                        # if string != "":
                        #    print(string, hex(i + start))
                        buffer = []

                        strings.append(
                            (
                                file_subpath,
                                table.name,
                                hex(start + j + offset),
                                hex(start + j),
                                string,
                            )
                        )
                    else:
                        char = byte_to_char(byte)
                        buffer.append(char)

                num_after = len(strings)
                logging.debug(f"Read {num_after - num_before} strings from table.")

    pd.DataFrame(
        strings,
        columns=["filepath", "table_name", "global_address", "local_offset", "string"],
    ).to_csv(output_csv, index=False)


def byte_to_char(byte: int) -> str:
    a = 0x25
    A = 0x0B
    char_lower = chr((byte - a) + ord("a"))
    char_upper = chr((byte - A) + ord("A"))

    mapping = {
        0x0: "0",
        0x1: "1",
        0x2: "2",
        0x3: "3",
        0x4: "4",
        0x5: "5",
        0x6: "6",
        0x7: "7",
        0x8: "8",
        0x9: "9",
        0xA: " ",
        0x55: "Ü",
        0x57: "á",
        0x70: "!",
        0x71: "?",
        0x87: "+",
        0x8D: "II",
        0x8E: "III",
        0x9A: "‘",
        0x9B: "’",
        0xAC: ".",
        0xAD: "&",
        0xCC: "-",
        0xCD: ",",
        0xFE: "\\n",
    }

    if char_lower.islower() and char_lower.isascii():
        return char_lower
    elif char_upper.isupper() and char_upper.isascii():
        return char_upper
    elif byte in mapping:
        return mapping[byte]
    else:
        # return "?"
        # return "[" + char + "]"
        return "[" + hex(byte) + "]"


if __name__ == "__main__":
    main(sys.argv[1:])
