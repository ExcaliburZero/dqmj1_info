from dataclasses import dataclass
from typing import IO, List

import argparse
import sys

import pandas as pd

ENDIANESS = "little"

@dataclass
class EnemyKind:
    species_id: int
    traits: List[int]
    skill_set: int

    @staticmethod
    def from_bin(i: int, input_stream: IO[bytes]) -> "EnemyKind":
        input_stream.read(4)
        input_stream.read(4)
        input_stream.read(8)
        traits = [b for b in input_stream.read(5)]
        input_stream.read(51)
        skil_set = int.from_bytes(input_stream.read(1), ENDIANESS)
        input_stream.read(75)
        
        return EnemyKind(species_id=i, traits=traits, skill_set=skil_set)

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

    pd.DataFrame(table).to_csv(args.output_csv, index=False)

if __name__ == "__main__":
    main(sys.argv[1:])