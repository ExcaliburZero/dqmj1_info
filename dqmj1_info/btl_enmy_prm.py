from dataclasses import dataclass
from typing import IO, List, Literal

import argparse
import logging
import sys

import pandas as pd

ENDIANESS: Literal["little"] = "little"


@dataclass
class ItemDrop:
    item_id: int
    chance_denominator_2_power: int

    @staticmethod
    def from_bin(input_stream: IO[bytes]) -> "ItemDrop":
        item_id = int.from_bytes(input_stream.read(2), ENDIANESS)
        chance_denominator_2_power = int.from_bytes(input_stream.read(2), ENDIANESS)

        return ItemDrop(
            item_id=item_id, chance_denominator_2_power=chance_denominator_2_power
        )


@dataclass
class BtlEnmyPrmEntry:
    species_id: int
    item_drops: List[ItemDrop]
    level: int
    max_hp: int
    max_mp: int
    attack: int
    defense: int
    agility: int
    wisdom: int
    skill_set_ids: List[int]

    @staticmethod
    def from_bin(input_stream: IO[bytes]) -> "BtlEnmyPrmEntry":
        species_id = int.from_bytes(input_stream.read(2), ENDIANESS)

        input_stream.read(30)
        item_drops = [
            ItemDrop.from_bin(input_stream),
            ItemDrop.from_bin(input_stream),
        ]
        input_stream.read(8)
        level = int.from_bytes(input_stream.read(2), ENDIANESS)

        input_stream.read(2)
        max_hp = int.from_bytes(input_stream.read(2), ENDIANESS)
        max_mp = int.from_bytes(input_stream.read(2), ENDIANESS)
        attack = int.from_bytes(input_stream.read(2), ENDIANESS)
        defense = int.from_bytes(input_stream.read(2), ENDIANESS)
        agility = int.from_bytes(input_stream.read(2), ENDIANESS)
        wisdom = int.from_bytes(input_stream.read(2), ENDIANESS)

        input_stream.read(20)
        skill_set_ids = [int.from_bytes(input_stream.read(1)) for _ in range(0, 3)]

        input_stream.read(1)

        return BtlEnmyPrmEntry(
            species_id=species_id,
            item_drops=item_drops,
            level=level,
            max_hp=max_hp,
            max_mp=max_mp,
            attack=attack,
            defense=defense,
            agility=agility,
            wisdom=wisdom,
            skill_set_ids=skill_set_ids,
        )


@dataclass
class BtlEnmyPrm:
    entries: List[BtlEnmyPrmEntry]

    @staticmethod
    def from_bin(input_stream: IO[bytes]) -> "BtlEnmyPrm":
        int.from_bytes(input_stream.read(4), ENDIANESS)
        length = int.from_bytes(input_stream.read(4), ENDIANESS)

        entries = []

        for i in range(0, length):
            entries.append(BtlEnmyPrmEntry.from_bin(input_stream))

        return BtlEnmyPrm(entries)


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--table_filepath", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    with open(args.table_filepath, "rb") as input_stream:
        table = BtlEnmyPrm.from_bin(input_stream)

    logging.debug(f"Read {len(table.entries)} entries from: {args.table_filepath}")

    pd.DataFrame(table.entries).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
