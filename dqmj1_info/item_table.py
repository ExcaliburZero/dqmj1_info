from typing import List, Literal

import argparse
import logging
import sys

import pandas as pd

ENDIANESS: Literal["little"] = "little"


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--item_tbl_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)

    args = parser.parse_args(argv)

    strings = pd.read_csv(args.strings_csv)
    item_tbl = pd.read_csv(args.item_tbl_csv)
    region = args.region

    if region == "Japan":
        logging.warning(
            "Item table creation does not currently support the Japan region. Skipping."
        )
        return

    item_names = strings[strings["table_name"] == "item_names"]

    def get_item_name(item_id: int) -> str:
        name = item_names[item_names["index_dec"] == item_id]["string"].iloc[0]
        assert isinstance(name, str)

        return name

    def get_item_category(category: int) -> str:
        if category == 0:
            return "0"
        elif category == 1:
            return "1"
        elif category >= 2:
            return "Weapon"

        raise ValueError()

    def get_weapon_type(category: int, weapon_type: int) -> str:
        if category < 2:
            return f"N/A ({weapon_type})"

        WEAPON_TYPES = ["Sword", "Spear", "Axe", "Hammer", "Whip", "Claw", "Staff"]

        return WEAPON_TYPES[weapon_type]

    data_raw = []
    for _, row in item_tbl.iterrows():
        data_raw.append(
            (
                row["item_id"],
                get_item_name(row["item_id"]),
                get_item_category(row["category"]),
                get_weapon_type(row["category"], row["weapon_type"]),
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
            "category",
            "weapon_type",
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
