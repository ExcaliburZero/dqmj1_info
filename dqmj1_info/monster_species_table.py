from dataclasses import dataclass
from typing import IO, List

import argparse
import logging
import sys

import pandas as pd

ENDIANESS = "little"


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--enmy_kind_tbl_csv", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    strings = pd.read_csv(args.strings_csv)
    enmy_kind_tbl = pd.read_csv(args.enmy_kind_tbl_csv)

    monster_names = strings[strings["table_name"] == "monster_species_names"]

    def get_monster_name(species_id: int) -> str:
        return monster_names[monster_names["index_dec"] == species_id]["string"].iloc[0]

    data_raw = []
    for _, row in enmy_kind_tbl.iterrows():
        data_raw.append(
            (
                row["species_id"],
                get_monster_name(row["species_id"]),
                row["traits"],
                row["skill_set"],
            )
        )

    data = pd.DataFrame(
        data_raw, columns=["index", "name", "trait_ids", "skill_set_id"]
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
