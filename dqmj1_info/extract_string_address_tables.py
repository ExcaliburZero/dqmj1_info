from dataclasses import dataclass
from typing import List

import argparse
import logging
import pathlib
import sys

import pandas as pd


@dataclass
class StringAddressTable:
    name: str
    start: int
    end: int


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_directory", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--mined_strings_csv", required=True)

    args = parser.parse_args(argv)

    data_directory = pathlib.Path(args.data_directory)
    output_csv = pathlib.Path(args.output_csv)
    mined_strings_csv = pathlib.Path(args.mined_strings_csv)

    mined_strings = pd.read_csv(mined_strings_csv)

    string_locations = {
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringAddressTable("monster_species_names", 0x0207785C, 0x0207805C),
                StringAddressTable("skill_set_names", 0x020763E0, 0x020767E4),
                StringAddressTable("skill_names", 0x02076BE8, 0x0207705C),
                StringAddressTable("mnamemes", 0x02075FE0, 0x020763E0),
                StringAddressTable("unknown_a", 0x02074CE0, 0x02074DE0),
                StringAddressTable("tactic_names", 0x02074A88, 0x02074AA8),
                StringAddressTable("skill_descriptions", 0x02074FE0, 0x020753E0),
                StringAddressTable(
                    "skill_set_names_and_descriptions", 0x020753E0, 0x020757E0
                ),
                StringAddressTable("item_names", 0x020767E4, 0x02076BE8),
                StringAddressTable("trait_names", 0x020757E0, 0x02075BE0),
                StringAddressTable("enemy_scout_names", 0x02075BE0, 0x02075FE0),
                StringAddressTable("unknown_b", 0x0207705C, 0x0207785C),
                StringAddressTable("unknown_c", 0x02074A04, 0x02074A14),
                StringAddressTable("color_names", 0x02074A54, 0x02074A6C),
                StringAddressTable("day_and_night", 0x020749EC, 0x020749F4),
                StringAddressTable("nsbmd_filenames", 0x02074DE0, 0x02074FE0),
                StringAddressTable("unknown_d", 0x02074C60, 0x02074DDC),
                StringAddressTable("unknown_e", 0x02074B2C, 0x02074B74),
                StringAddressTable("unknown_f", 0x02074A6C, 0x02074A88),
                StringAddressTable(
                    "battle_and_field_and_anywhere", 0x020749F4, 0x02074A04
                ),
                StringAddressTable("unknown_g", 0x02074A3C, 0x02074A54),
                StringAddressTable("battle_targets", 0x02074A14, 0x02074A28),
                StringAddressTable("skill_targeting_types", 0x02074A28, 0x02074A3C),
                StringAddressTable("unknown_h", 0x02074AE8, 0x02074B2C),
                StringAddressTable("unknown_i", 0x02074BE0, 0x02074C60),
                StringAddressTable("unknown_j", 0x02084018, 0x02084118),
                StringAddressTable("unknown_k", 0x02083EBC, 0x02083EFC),
                StringAddressTable("battle_messages", 0x02084318, 0x02084B18),
            ],
        ),
    }

    strings = []
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
                buffer = []
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
