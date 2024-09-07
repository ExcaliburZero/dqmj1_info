from typing import List, Tuple

import argparse
import logging
import pathlib
import sys

import pandas as pd

from .character_encoding import BYTE_TO_CHAR_MAP, CHAR_TO_BYTE_MAP
from .region_configs.region_configs import REGION_CONFIGS


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_directory", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)

    args = parser.parse_args(argv)

    data_directory = pathlib.Path(args.data_directory)
    output_csv = pathlib.Path(args.output_csv)

    string_locations = REGION_CONFIGS[args.region].string_tables

    strings: List[Tuple[pathlib.Path, str, str, str, str]] = []
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
                buffer: List[str] = []
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
    mapping = BYTE_TO_CHAR_MAP

    if byte in mapping:
        return mapping[byte]
    else:
        # return "?"
        # return "[" + char + "]"
        return "[" + hex(byte) + "]"


def char_to_byte(c: str) -> int:
    mapping = CHAR_TO_BYTE_MAP

    if c in mapping:
        return mapping[c]
    elif c.startswith("[0x"):
        assert c.endswith("]"), c
        return int(c[1:-1], base=16)
    else:
        print(repr(c))
        assert False
        # return "?"
        # return "[" + char + "]"
        # return "[" + hex(byte) + "]"


def get_string_chars(string: str) -> List[str]:
    chars = []

    current = 0
    while current < len(string):
        c = string[current]
        if c == "[":
            # ex. [0xff]
            c = string[current : current + 6]
        elif c == "\\":
            c = string[current : current + 2]

        chars.append(c)
        current += len(c)

    return chars


if __name__ == "__main__":
    main(sys.argv[1:])
