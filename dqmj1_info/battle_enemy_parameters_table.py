from typing import List

import argparse
import ast
import logging
import sys

import pandas as pd

ENDIANESS = "little"


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--btl_enmy_prm_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)

    args = parser.parse_args(argv)

    strings = pd.read_csv(args.strings_csv, keep_default_na=False)
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

    monster_names = strings[strings["table_name"] == "monster_species_names"]
    skill_set_names = strings[strings["table_name"] == "skill_set_names"]

    def get_monster_name(species_id: int) -> str:
        name = monster_names[monster_names["index_dec"] == species_id]["string"].iloc[0]
        assert isinstance(name, str)

        return name

    def get_skill_set_name(skill_set_id: int) -> str:
        name = skill_set_names[skill_set_names["index_dec"] == skill_set_id][
            "string"
        ].iloc[0]
        assert isinstance(name, str)

        return name

    data_raw = []
    for i, row in btl_enmy_prm.iterrows():
        data_raw.append(
            (
                i,
                row["species_id"],
                get_monster_name(row["species_id"]),
                row["level"],
                row["max_hp"],
                row["max_mp"],
                row["attack"],
                row["defense"],
                row["agility"],
                row["wisdom"],
                [
                    get_skill_set_name(t)
                    for t in row["skill_set_ids"]
                    if not pd.isnull(get_skill_set_name(t))
                    and get_skill_set_name(t) != ""
                ],
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
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
