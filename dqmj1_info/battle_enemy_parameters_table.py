from typing import List

import argparse
import ast
import logging
import sys

import pandas as pd

from .string_tables import StringTable

ENDIANESS = "little"


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--btl_enmy_prm_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)

    args = parser.parse_args(argv)

    with open(args.strings_csv, "r", encoding="utf-8") as input_stream:
        strings = StringTable.from_csv(input_stream)

    btl_enmy_prm = pd.read_csv(args.btl_enmy_prm_csv)
    region = args.region

    if region == "Japan":
        logging.warning(
            "Battle enemy parameters table creation does not currently support the Japan region. Skipping."
        )
        return

    btl_enmy_prm["skill_set_ids"] = btl_enmy_prm["skill_set_ids"].apply(
        lambda x: ast.literal_eval(x)
    )
    btl_enmy_prm["item_drops"] = btl_enmy_prm["item_drops"].apply(
        lambda x: ast.literal_eval(x)
    )

    data_raw = []
    for i, row in btl_enmy_prm.iterrows():
        data_raw.append(
            (
                i,
                row["species_id"],
                strings.get_monster_species_name(row["species_id"]),
                row["level"],
                row["max_hp"],
                row["max_mp"],
                row["attack"],
                row["defense"],
                row["agility"],
                row["wisdom"],
                [
                    strings.get_skill_set_name(t)
                    for t in row["skill_set_ids"]
                    if not pd.isnull(strings.get_skill_set_name(t))
                    and strings.get_skill_set_name(t) != ""
                ],
                ", ".join(
                    [
                        " ".join(
                            [
                                strings.get_item_name(d["item_id"]),
                                f"{(1.0 / 2 ** d['chance_denominator_2_power']) * 100.0}%",
                            ]
                        )
                        for d in row["item_drops"]
                        if not pd.isnull(strings.get_item_name(d["item_id"]))
                        and strings.get_item_name(d["item_id"]) != ""
                    ]
                ),
            )
        )

    data = pd.DataFrame(
        data_raw,
        columns=[
            "index",
            "species_id",
            "species_name",
            "level",
            "max_hp",
            "max_mp",
            "attack",
            "defense",
            "agility",
            "wisdom",
            "skill_sets",
            "item_drops",
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
