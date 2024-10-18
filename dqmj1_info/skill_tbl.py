from dataclasses import dataclass
from typing import IO, List, Literal

import argparse
import logging
import sys

import pandas as pd

ENDIANESS: Literal["little"] = "little"


@dataclass
class SkillSet:
    skill_set_id: int
    skill_point_requirements: List[int]
    skill_ids: List[List[int]]
    trait_ids: List[List[int]]

    @staticmethod
    def from_bin(i: int, input_stream: IO[bytes]) -> "SkillSet":
        input_stream.read(1)
        input_stream.read(3)

        skill_point_requirements = []
        for _ in range(0, 10):
            input_stream.read(2)
            skill_point_requirements.append(
                int.from_bytes(input_stream.read(2), ENDIANESS)
            )

        skill_ids = []
        for _ in range(0, 10):
            skill_ids_list = [
                int.from_bytes(input_stream.read(2), ENDIANESS) for _ in range(0, 4)
            ]
            skill_ids_list = [i for i in skill_ids_list if i != 0]

            input_stream.read(4)

            skill_ids.append(skill_ids_list)

        trait_ids = []
        for _ in range(0, 10):
            trait_id_list = [int.from_bytes(input_stream.read(1)) for _ in range(0, 4)]
            trait_id_list = [i for i in trait_id_list if i != 0]

            trait_ids.append(trait_id_list)

        input_stream.read(36)

        return SkillSet(
            skill_set_id=i,
            skill_point_requirements=skill_point_requirements,
            skill_ids=skill_ids,
            trait_ids=trait_ids,
        )

    @staticmethod
    def read_bin(input_stream: IO[bytes]) -> List["SkillSet"]:
        entries = []

        input_stream.read(8)
        for i in range(0, 0xC2):
            entries.append(SkillSet.from_bin(i, input_stream))

        return entries


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--table_filepath", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    with open(args.table_filepath, "rb") as input_stream:
        table = SkillSet.read_bin(input_stream)

    logging.debug(f"Read {len(table)} entries from: {args.table_filepath}")

    pd.DataFrame(table).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
