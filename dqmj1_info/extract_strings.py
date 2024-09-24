from typing import List, Tuple

import argparse
import logging
import pathlib
import sys

import pandas as pd

from .character_encoding import CHARACTER_ENCODINGS
from .region_configs.region_configs import REGION_CONFIGS


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_directory", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--character_encoding", required=True)

    args = parser.parse_args(argv)

    data_directory = pathlib.Path(args.data_directory)
    output_csv = pathlib.Path(args.output_csv)

    string_locations = REGION_CONFIGS[args.region].string_tables
    character_encoding = CHARACTER_ENCODINGS[args.character_encoding]

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
                buffer: List[int] = []
                for i, byte in enumerate(file_bytes[start : start + length]):
                    # Note: The skipping of 0x0A at possible string start is due to an edge case I
                    # saw at 0x0207d792
                    if (byte == 0x00 or byte == 0x0A) and len(buffer) == 0:
                        continue
                    # Note: The check against 0xFE is due to an edge case at 0x02079c16.
                    elif byte == 0xFF or (
                        byte == 0xFE and file_bytes[start + i + 1] == 0x0
                    ):
                        string = character_encoding.bytes_to_string(buffer)
                        j = i - len(buffer)

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
                        buffer.append(byte)

                num_after = len(strings)
                logging.debug(f"Read {num_after - num_before} strings from table.")

    pd.DataFrame(
        strings,
        columns=["filepath", "table_name", "global_address", "local_offset", "string"],
    ).to_csv(output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
