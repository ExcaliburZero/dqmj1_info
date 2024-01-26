from dataclasses import dataclass
from typing import IO, List

import argparse
import sys

import pandas as pd

ENDIANESS = "little"


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--item_tbl_csv", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    strings = pd.read_csv(args.strings_csv)
    item_tbl = pd.read_csv(args.item_tbl_csv)

    item_names = strings[strings["table_name"] == "item_names"]

    def get_item_name(item_id: int) -> str:
        return item_names[item_names["index_dec"] == item_id]["string"].iloc[0]

    data_raw = []
    for _, row in item_tbl.iterrows():
        data_raw.append(
            (
                row["item_id"],
                get_item_name(row["item_id"]),
                row["attack_increase"],
                row["defense_increase"],
                row["agility_increase"],
                row["wisdom_increase"],
                row["max_hp_increase"],
                row["max_mp_increase"],
            )
        )

    data = pd.DataFrame(
        data_raw,
        columns=[
            "id",
            "name",
            "attack_increase",
            "defense_increase",
            "agility_increase",
            "wisdom_increase",
            "max_hp_increase",
            "max_mp_increase",
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
