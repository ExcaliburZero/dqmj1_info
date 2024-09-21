from typing import List

import argparse
import ast
import sys

import pandas as pd

ENDIANESS = "little"


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--skill_tbl_csv", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    strings = pd.read_csv(args.strings_csv)
    skill_tbl = pd.read_csv(args.skill_tbl_csv)

    skill_tbl["skill_point_requirements"] = skill_tbl["skill_point_requirements"].apply(
        lambda x: ast.literal_eval(x)
    )
    skill_tbl["skill_ids"] = skill_tbl["skill_ids"].apply(lambda x: ast.literal_eval(x))

    skill_set_names = strings[strings["table_name"] == "skill_set_names"]
    skill_names = strings[strings["table_name"] == "skill_names"]

    def get_skill_set_name(skill_set_id: int) -> str:
        name = skill_set_names[skill_set_names["index_dec"] == skill_set_id][
            "string"
        ].iloc[0]
        assert isinstance(name, str)

        return name

    def get_skill_name(skill_id: int) -> str:
        name = skill_names[skill_names["index_dec"] == skill_id]["string"].iloc[0]
        assert isinstance(name, str)

        return name

    data_raw = []
    for _, row in skill_tbl.iterrows():
        data_raw.append(
            (
                row["skill_set_id"],
                get_skill_set_name(row["skill_set_id"]),
                row["skill_point_requirements"],
                row["skill_ids"],
                [
                    get_skill_name(skill_id) if skill_id != 0 else ""
                    for skill_id in row["skill_ids"]
                ],
            )
        )

    data = pd.DataFrame(
        data_raw,
        columns=[
            "id",
            "name",
            "skill_point_requirements",
            "skill_ids",
            "skill_names",
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
