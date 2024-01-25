from dataclasses import dataclass
from typing import IO, List

import argparse
import ast
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

    enmy_kind_tbl["traits"] = enmy_kind_tbl["traits"].apply(
        lambda x: ast.literal_eval(x)
    )

    monster_names = strings[strings["table_name"] == "monster_species_names"]
    trait_names = strings[strings["table_name"] == "trait_names"]
    skill_set_names = strings[strings["table_name"] == "skill_set_names"]

    ranks = {
        0: "",
        1: "F",
        2: "E",
        3: "D",
        4: "C",
        5: "B",
        6: "A",
        7: "S",
        8: "X",
        9: "???",
    }

    def get_monster_name(species_id: int) -> str:
        return monster_names[monster_names["index_dec"] == species_id]["string"].iloc[0]

    def get_trait_name(trait_id: int) -> str:
        try:
            return trait_names[trait_names["index_dec"] == trait_id]["string"].iloc[0]
        except IndexError:
            raise ValueError(f"Failed to find trait for id: {trait_id}")

    def get_skill_set_name(skill_set_id: int) -> str:
        return skill_set_names[skill_set_names["index_dec"] == skill_set_id][
            "string"
        ].iloc[0]

    data_raw = []
    for _, row in enmy_kind_tbl.iterrows():
        data_raw.append(
            (
                row["species_id"],
                get_monster_name(row["species_id"]),
                ranks[row["rank"]],
                row["traits"],
                [
                    get_trait_name(t)
                    for t in row["traits"]
                    if not pd.isnull(get_trait_name(t))
                ],
                row["skill_set"],
                get_skill_set_name(row["skill_set"]),
            )
        )

    data = pd.DataFrame(
        data_raw,
        columns=[
            "index",
            "name",
            "rank",
            "trait_ids",
            "traits",
            "skill_set_id",
            "skill_set",
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
