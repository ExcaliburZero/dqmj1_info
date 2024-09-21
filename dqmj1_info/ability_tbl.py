from dataclasses import dataclass
from typing import IO, List, Literal

import argparse
import logging
import sys

import pandas as pd

ENDIANESS: Literal["little"] = "little"


@dataclass
class StatIncreases:
    stat_increases: List[int]

    @staticmethod
    def from_bin(input_stream: IO[bytes]) -> "StatIncreases":
        return StatIncreases(stat_increases=[byte for byte in input_stream.read(99)])

    @staticmethod
    def read_bin(input_stream: IO[bytes]) -> List["StatIncreases"]:
        entries = []

        for i in range(0, 32):
            entries.append(StatIncreases.from_bin(input_stream))

        return entries


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--table_filepath", required=True)
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    with open(args.table_filepath, "rb") as input_stream:
        table = StatIncreases.read_bin(input_stream)

    logging.debug(f"Read {len(table)} entries from: {args.table_filepath}")

    pd.DataFrame(
        [(i, *[v for v in value.stat_increases]) for i, value in enumerate(table)],
        columns=["pattern_id", *[str(level) for level in range(1, 100)]],
    ).to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
