from typing import Any, List, Tuple

import argparse
import logging
import pathlib
import sys

import pandas as pd

from .region_configs.region_configs import REGION_CONFIGS


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_directory", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--mined_strings_csv", required=True)
    parser.add_argument("--region", required=True)

    args = parser.parse_args(argv)

    data_directory = pathlib.Path(args.data_directory)
    output_csv = pathlib.Path(args.output_csv)
    mined_strings_csv = pathlib.Path(args.mined_strings_csv)

    mined_strings = pd.read_csv(mined_strings_csv)

    string_locations = REGION_CONFIGS[args.region].string_address_tables

    strings: List[Tuple[pathlib.Path, str, int, str, str, str, str, Any]] = []
    for file_subpath, (offset, tables) in sorted(string_locations.items()):
        filepath = data_directory / file_subpath
        logging.debug(f"Reading string tables from: {filepath}")

        with open(filepath, "rb") as input_stream:
            file_bytes = input_stream.read()
            logging.debug(f"Read {len(file_bytes)} bytes from {filepath}")

            for table in tables:
                logging.debug(f"Reading table: {table}")

                start = table.start - offset
                length = table.end - table.start

                num_before = len(strings)
                buffer: List[int] = []
                num_found = 0
                for i, byte in enumerate(file_bytes[start : start + length + 1]):
                    if len(buffer) == 4:
                        j = i - len(buffer)

                        string_address = hex(
                            buffer[0]
                            + buffer[1] * 0x100
                            + buffer[2] * 0x10000
                            + buffer[3] * 0x1000000
                        )
                        matches = mined_strings[
                            mined_strings["global_address"] == string_address
                        ]["string"]
                        string = (
                            matches.iloc[0]
                            if len(matches) > 0
                            else "ADDRESS_NOT_FOUND_DURING_DATA_MINING"
                        )
                        strings.append(
                            (
                                file_subpath,
                                table.name,
                                num_found,
                                hex(num_found),
                                hex(start + j + offset),
                                hex(start + j),
                                string_address,
                                string,
                            )
                        )

                        buffer = []
                        num_found += 1

                    buffer.append(byte)

                if len(buffer) == 4:
                    j = i - len(buffer)

                    string_address = hex(
                        buffer[0]
                        + buffer[1] * 0x100
                        + buffer[2] * 0x10000
                        + buffer[3] * 0x1000000
                    )
                    matches = mined_strings[
                        mined_strings["global_address"] == string_address
                    ]["string"]
                    string = (
                        matches.iloc[0]
                        if len(matches) > 0
                        else "ADDRESS_NOT_FOUND_DURING_DATA_MINING"
                    )
                    strings.append(
                        (
                            file_subpath,
                            table.name,
                            num_found,
                            hex(num_found),
                            hex(start + j + offset),
                            hex(start + j),
                            string_address,
                            string,
                        )
                    )

                    buffer = []
                    num_found += 1

                num_after = len(strings)
                logging.debug(f"Read {num_after - num_before} strings")

    pd.DataFrame(
        strings,
        columns=[
            "filepath",
            "table_name",
            "index_dec",
            "index_hex",
            "global_address",
            "local_offset",
            "string_address",
            "string",
        ],
    ).to_csv(output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
