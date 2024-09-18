from typing import List, Tuple

import argparse
import logging
import pathlib
import sys

import pandas as pd

from .character_encoding import CHARACTER_ENCODINGS
from .region_configs.region_configs import REGION_CONFIGS


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_directory", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--character_encoding", required=True)

    args = parser.parse_args(argv)

    data_directory = pathlib.Path(args.data_directory)
    output_csv = pathlib.Path(args.output_csv)

    string_locations = REGION_CONFIGS[args.region].string_tables
    if args.character_encoding == "Japan":
        logging.warning(
            f'extract strings does not support "Japan" character encoding yet. Using "North America / Europe" instead.'
        )
        character_encoding = CHARACTER_ENCODINGS["North America / Europe"]
    else:
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
                        char = character_encoding.bytes_to_string([byte])
                        buffer.append(char)

                num_after = len(strings)
                logging.debug(f"Read {num_after - num_before} strings from table.")

    pd.DataFrame(
        strings,
        columns=["filepath", "table_name", "global_address", "local_offset", "string"],
    ).to_csv(output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
