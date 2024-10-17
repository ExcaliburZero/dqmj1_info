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
    parser.add_argument("--skill_tbl_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--region", required=True)

    args = parser.parse_args(argv)

    with open(args.strings_csv, "r", encoding="utf-8") as input_stream:
        strings = StringTable.from_csv(input_stream)
    skill_tbl = pd.read_csv(args.skill_tbl_csv)
    region = args.region

    if region == "Japan":
        logging.warning(
            "Skill set table creation does not currently support the Japan region. Skipping."
        )
        return

    skill_tbl["skill_point_requirements"] = skill_tbl["skill_point_requirements"].apply(
        lambda x: ast.literal_eval(x)
    )
    skill_tbl["skill_ids"] = skill_tbl["skill_ids"].apply(lambda x: ast.literal_eval(x))
    skill_tbl["trait_ids"] = skill_tbl["trait_ids"].apply(lambda x: ast.literal_eval(x))

    data_raw = []
    for _, row in skill_tbl.iterrows():
        data_raw.append(
            (
                row["skill_set_id"],
                strings.get_skill_set_name(row["skill_set_id"]),
                row["skill_point_requirements"],
                row["skill_ids"],
                [
                    strings.get_skill_name(skill_id) if skill_id != 0 else ""
                    for skill_id in row["skill_ids"]
                ],
                row["trait_ids"],
                [
                    [
                        strings.get_trait_name(trait_id) if trait_id != 0 else ""
                        for trait_id in trait_ids
                    ]
                    for trait_ids in row["trait_ids"]
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
            "trait_ids",
            "trait_names",
        ],
    )

    pd.DataFrame(data).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
