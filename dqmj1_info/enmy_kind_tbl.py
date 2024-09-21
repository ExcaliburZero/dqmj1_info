from dataclasses import dataclass
from typing import IO, List, Literal, Tuple

import argparse
import logging
import sys

import pandas as pd

ENDIANESS: Literal["little"] = "little"


@dataclass
class EnemyKind:
    species_id: int
    rank: int
    race: int
    sword_compat: bool
    spear_compat: bool
    axe_compat: bool
    hammer_compat: bool
    whip_compat: bool
    claw_compat: bool
    staff_compat: bool
    traits: List[int]
    max_hp_limit: int
    max_mp_limit: int
    attack_limit: int
    defense_limit: int
    agility_limit: int
    wisdom_limit: int
    max_hp_increase_pattern: Tuple[int, int, int, int]
    max_mp_increase_pattern: Tuple[int, int, int, int]
    attack_increase_pattern: Tuple[int, int, int, int]
    defense_increase_pattern: Tuple[int, int, int, int]
    agility_increase_pattern: Tuple[int, int, int, int]
    wisdom_increase_pattern: Tuple[int, int, int, int]
    skill_set: int

    @staticmethod
    def from_bin(i: int, input_stream: IO[bytes]) -> "EnemyKind":
        input_stream.read(4)

        rank_and_something_else = int.from_bytes(input_stream.read(4), ENDIANESS)
        rank = rank_and_something_else & 0x0F
        race = (rank_and_something_else & 0xFF) >> 4
        input_stream.read(4)

        weapon_compat_and_something_else = int.from_bytes(
            input_stream.read(4), ENDIANESS
        )

        sword_compat = weapon_compat_and_something_else & 0b1 != 0
        spear_compat = weapon_compat_and_something_else >> 1 & 0b1 != 0
        axe_compat = weapon_compat_and_something_else >> 2 & 0b1 != 0
        hammer_compat = weapon_compat_and_something_else >> 3 & 0b1 != 0
        whip_compat = weapon_compat_and_something_else >> 4 & 0b1 != 0
        claw_compat = weapon_compat_and_something_else >> 5 & 0b1 != 0
        staff_compat = weapon_compat_and_something_else >> 6 & 0b1 != 0

        traits = [b for b in input_stream.read(5)]
        input_stream.read(15)

        max_hp_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        max_mp_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        attack_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        defense_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        agility_limit = int.from_bytes(input_stream.read(2), ENDIANESS)
        wisdom_limit = int.from_bytes(input_stream.read(2), ENDIANESS)

        max_hp_increase_pattern = (
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
        )
        max_mp_increase_pattern = (
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
        )
        attack_increase_pattern = (
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
        )
        defense_increase_pattern = (
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
        )
        agility_increase_pattern = (
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
        )
        wisdom_increase_pattern = (
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
            int.from_bytes(input_stream.read(1), ENDIANESS),
        )

        skil_set = int.from_bytes(input_stream.read(1), ENDIANESS)
        input_stream.read(75)

        return EnemyKind(
            species_id=i,
            rank=rank,
            race=race,
            sword_compat=sword_compat,
            spear_compat=spear_compat,
            axe_compat=axe_compat,
            hammer_compat=hammer_compat,
            whip_compat=whip_compat,
            claw_compat=claw_compat,
            staff_compat=staff_compat,
            traits=traits,
            max_hp_limit=max_hp_limit,
            max_mp_limit=max_mp_limit,
            attack_limit=attack_limit,
            defense_limit=defense_limit,
            agility_limit=agility_limit,
            wisdom_limit=wisdom_limit,
            max_hp_increase_pattern=max_hp_increase_pattern,
            max_mp_increase_pattern=max_mp_increase_pattern,
            attack_increase_pattern=attack_increase_pattern,
            defense_increase_pattern=defense_increase_pattern,
            agility_increase_pattern=agility_increase_pattern,
            wisdom_increase_pattern=wisdom_increase_pattern,
            skill_set=skil_set,
        )

    @staticmethod
    def read_bin(input_stream: IO[bytes]) -> List["EnemyKind"]:
        entries = []

        input_stream.read(8)
        for i in range(0, 352):
            entries.append(EnemyKind.from_bin(i, input_stream))

        return entries


def main(argv: List[str]) -> None:
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
