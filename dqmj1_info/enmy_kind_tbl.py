from dataclasses import dataclass
from typing import IO, List

import argparse
import logging
import sys

import pandas as pd

ENDIANESS = "little"


@dataclass
class EnemyKind:
    species_id: int
    rank: int
    traits: List[int]
    max_hp_limit: int
    max_mp_limit: int
    attack_limit: int
    defense_limit: int
    agility_limit: int
    wisdom_limit: int
    skill_set: int

    @staticmethod
    def from_bin(i: int, input_stream: IO[bytes]) -> "EnemyKind":
        input_stream.read(4)

        rank_and_something_else = int.from_bytes(input_stream.read(4), ENDIANESS)
        rank = rank_and_something_else & 0x0F

        input_stream.read(8)
        traits = [b for b in input_stream.read(5)]
        input_stream.read(15)

        max_hp_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        max_mp_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        attack_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        defense_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        agility_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        wisdom_limit = int.from_bytes(input_stream.read(2), ENDIANESS)

        input_stream.read(24)
        skil_set = int.from_bytes(input_stream.read(1), ENDIANESS)
        input_stream.read(75)

        return EnemyKind(
            species_id=i,
            rank=rank,
            traits=traits,
            max_hp_limit=max_hp_limit,
            max_mp_limit=max_mp_limit,
            attack_limit=attack_limit,
            defense_limit=defense_limit,
            agility_limit=agility_limit,
            wisdom_limit=wisdom_limit,
            skill_set=skil_set,
        )

    @staticmethod
    def read_bin(input_stream: IO[bytes]) -> List["EnemyKind"]:
        entries = []

        input_stream.read(8)
        for i in range(0, 352):
            entries.append(EnemyKind.from_bin(i, input_stream))

        return entries


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--table_filepath", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    with open(args.table_filepath, "rb") as input_stream:
        table = EnemyKind.read_bin(input_stream)

    logging.debug(f"Read {len(table)} entries from: {args.table_filepath}")

    pd.DataFrame(table).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
