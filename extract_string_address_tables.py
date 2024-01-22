from dataclasses import dataclass
from typing import List

import argparse
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
        pathlib.Path("arm9.bin"): (0x02000000, [
            StringAddressTable("monster_species_names", 0x0207785c, 0x02078058),
            StringAddressTable("skill_set_names", 0x020763e0, 0x020767e0),
            StringAddressTable("skill_names", 0x02076be8, 0x02077058),
            StringAddressTable("mnamemes", 0x02075fe0, 0x020763dc),
            StringAddressTable("unknown_a", 0x02074ce0, 0x02074ddc),
            StringAddressTable("tactic_names", 0x02074a88, 0x02074aa4),
            StringAddressTable("skill_descriptions", 0x02074fe0, 0x020753dc),
        ]),
    }

    strings = []
    for file_subpath, (offset, tables) in sorted(string_locations.items()):
        filepath = data_directory / file_subpath
        print(filepath)

        with open(filepath, "rb") as input_stream:
            file_bytes = input_stream.read()
            print(len(file_bytes))

            for table in tables:
                print(table)

                start = table.start - offset
                length = table.end - table.start

                num_before = len(strings)
                buffer = []
                num_found = 0
                for i, byte in enumerate(file_bytes[start:start + length + 1]):
                    if len(buffer) == 4:
                        j = i - len(buffer)

                        string_address = hex(
                            buffer[0] + buffer[1] * 0x100 + buffer[2] * 0x10000 + buffer[3] * 0x1000000
                        )
                        matches = mined_strings[mined_strings["global_address"] == string_address]["string"]
                        string = matches.iloc[0] if len(matches) > 0 else "ADDRESS_NOT_FOUND_DURING_DATA_MINING"
                        strings.append((file_subpath, table.name, num_found, hex(num_found), hex(start + j + offset), hex(start + j), string_address, string))

                        buffer = []
                        num_found += 1

                    buffer.append(byte)

                if len(buffer) == 4:
                    j = i - len(buffer)

                    string_address = hex(
                        buffer[0] + buffer[1] * 0x100 + buffer[2] * 0x10000 + buffer[3] * 0x1000000
                    )
                    matches = mined_strings[mined_strings["global_address"] == string_address]["string"]
                    string = matches.iloc[0] if len(matches) > 0 else "ADDRESS_NOT_FOUND_DURING_DATA_MINING"
                    strings.append((file_subpath, table.name, num_found, hex(num_found), hex(start + j + offset), hex(start + j), string_address, string))

                    buffer = []
                    num_found += 1

                num_after = len(strings)
                print("\t", num_after - num_before)

    pd.DataFrame(strings, columns=["filepath", "table_name", "index_dec", "index_hex", "global_address", "local_offset", "string_address", "string"]).to_csv(output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])