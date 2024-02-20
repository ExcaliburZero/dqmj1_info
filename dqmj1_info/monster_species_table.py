from typing import Any, List

import argparse
import ast
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

    # TODO: lookup from relevant string table
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

    # TODO: lookup from relevant string table
    races = {
        0: "",
        1: "Slime",
        2: "Dragon",
        3: "Nature",
        4: "Beast",
        5: "Material",
        6: "Demon",
        7: "Undead",
        8: "Incarni",
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

    def get_weapons(row: Any) -> List[str]:
        weapons = []
        if row["sword_compat"]:
            weapons.append("Sword")
        if row["spear_compat"]:
            weapons.append("Spear")
        if row["axe_compat"]:
            weapons.append("Axe")
        if row["hammer_compat"]:
            weapons.append("Hammer")
        if row["whip_compat"]:
            weapons.append("Whip")
        if row["claw_compat"]:
            weapons.append("Claw")
        if row["staff_compat"]:
            weapons.append("Staff")

        return weapons

    data_raw = []
    for _, row in enmy_kind_tbl.iterrows():
        data_raw.append(
            (
                row["species_id"],
                get_monster_name(row["species_id"]),
                ranks[row["rank"]],
                races[row["race"]],
                row["traits"],
                [
                    get_trait_name(t)
                    for t in row["traits"]
                    if not pd.isnull(get_trait_name(t))
                ],
                row["skill_set"],
                get_skill_set_name(row["skill_set"]),
                row["max_hp_limit"],
                row["max_mp_limit"],
                row["attack_limit"],
                row["defense_limit"],
                row["agility_limit"],
                row["wisdom_limit"],
                get_weapons(row),
            )
        )

    data = pd.DataFrame(
        data_raw,
        columns=[
            "index",
            "name",
            "rank",
            "race",
            "trait_ids",
            "traits",
            "skill_set_id",
            "skill_set",
            "max_hp_limit",
            "max_mp_limit",
            "attack_limit",
            "defense_limit",
            "agility_limit",
            "wisdom_limit",
            "weapons",
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
