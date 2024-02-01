from dataclasses import dataclass
from typing import IO, List, Literal

import argparse
import logging
import sys

import pandas as pd

ENDIANESS: Literal["little"] = "little"


@dataclass
class Item:
    item_id: int
    category: int
    weapon_type: int
    attack_increase: int
    defense_increase: int
    agility_increase: int
    wisdom_increase: int
    max_hp_increase: int
    max_mp_increase: int

    @staticmethod
    def from_bin(i: int, input_stream: IO[bytes]) -> "Item":
        category = int.from_bytes(input_stream.read(1), ENDIANESS)

        input_stream.read(7)
        input_stream.read(1)

        weapon_type = int.from_bytes(input_stream.read(1), ENDIANESS)

        input_stream.read(16)

        attack_increase = int.from_bytes(input_stream.read(1), ENDIANESS)
        defense_increase = int.from_bytes(input_stream.read(1), ENDIANESS)
        agility_increase = int.from_bytes(input_stream.read(1), ENDIANESS)
        wisdom_increase = int.from_bytes(input_stream.read(1), ENDIANESS)
        max_hp_increase = int.from_bytes(input_stream.read(1), ENDIANESS)
        max_mp_increase = int.from_bytes(input_stream.read(1), ENDIANESS)

        input_stream.read(76)

        return Item(
            item_id=i,
            category=category,
            weapon_type=weapon_type,
            attack_increase=attack_increase,
            defense_increase=defense_increase,
            agility_increase=agility_increase,
            wisdom_increase=wisdom_increase,
            max_hp_increase=max_hp_increase,
            max_mp_increase=max_mp_increase,
        )

    @staticmethod
    def read_bin(input_stream: IO[bytes]) -> List["Item"]:
        entries = []

        input_stream.read(8)
        for i in range(0, 160):
            entries.append(Item.from_bin(i, input_stream))

        return entries


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--table_filepath", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    with open(args.table_filepath, "rb") as input_stream:
        table = Item.read_bin(input_stream)

    logging.debug(f"Read {len(table)} entries from: {args.table_filepath}")

    pd.DataFrame(table).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
