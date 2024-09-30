from typing import List

import argparse
import csv
import glob
import logging
import pathlib
import sys

import pandas as pd

from .character_encoding import CHARACTER_ENCODINGS
from .save_data import SaveData


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--save_data_filepaths", required=True, nargs="+", type=pathlib.Path
    )
    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--output_filepath", required=True, type=pathlib.Path)
    parser.add_argument("--character_encoding", required=True)

    args = parser.parse_args(argv)

    save_data_filepaths: List[pathlib.Path] = [
        pathlib.Path(filepath)
        for filepath_pattern in args.save_data_filepaths
        for filepath in sorted(glob.glob(str(filepath_pattern)))
    ]
    strings = pd.read_csv(args.strings_csv, keep_default_na=False)
    output_filepath: pathlib.Path = args.output_filepath

    character_encoding = CHARACTER_ENCODINGS[args.character_encoding]

    monster_species_names = strings[strings["table_name"] == "monster_species_names"]

    def get_monster_species_name(species_id: int) -> str:
        name = monster_species_names[monster_species_names["index_dec"] == species_id][
            "string"
        ].iloc[0]
        assert isinstance(name, str)

        return name

    save_data_list = []
    for save_data_filepath in save_data_filepaths:
        logging.debug(f"Looking at save data file: {save_data_filepath}")
        with open(save_data_filepath, "rb") as input_stream:
            save_data, raw = SaveData.from_sav(input_stream, character_encoding)

        save_data_list.append((save_data_filepath, save_data, raw))

    columns = [
        "Filepath",
        "Player name",
        "Playtime",
        "Party",
        "Gold",
        "Atm",
        "Num darkonium times 5",
    ]
    with open(output_filepath, "w", encoding="utf-8") as output_stream:
        writer = csv.DictWriter(output_stream, fieldnames=columns)
        writer.writeheader()

        for filepath, save_data, raw in save_data_list:
            print("=================")
            print(f"[{filepath}]")

            header = save_data.header
            summary = save_data.summary
            player_info = save_data.player_info

            calculated_checksum = raw.checksum
            checksum_check_string = (
                "(✓)"
                if calculated_checksum == header.checksum
                else f"(Incorrect, {hex(calculated_checksum)})"
            )

            data = [
                (
                    "Header",
                    [
                        (
                            "Magic",
                            f"{hex(header.magic_1)} {hex(header.magic_2)} {hex(header.magic_3)}",
                        ),
                        (
                            "Checksum",
                            f"{hex(header.checksum)} {checksum_check_string}",
                        ),
                    ],
                ),
                (
                    "Summary",
                    [
                        (
                            "Playtime",
                            f"{summary.playtime.hours}:{summary.playtime.minutes:0>2}:{summary.playtime.seconds:0>2}",
                        ),
                        (
                            "Player name",
                            summary.player_name,
                        ),
                        (
                            "Party",
                            [
                                f"{party_monster.name} lv.{party_monster.level} ({get_monster_species_name(party_monster.species_id)})"
                                for party_monster in summary.party_monsters
                            ],
                        ),
                        (
                            "Num darkonium",
                            f"{int(summary.num_darkonium_times_5 / 5)} ({summary.num_darkonium_times_5})",
                        ),
                    ],
                ),
                (
                    "Player info",
                    [
                        ("Player name", player_info.player_name),
                        ("Gold", str(player_info.gold)),
                        ("ATM gold", str(player_info.atm_gold)),
                    ],
                ),
            ]

            for section, section_data in data:
                print(f"{section}:")
                for field, value in section_data:
                    if isinstance(value, list):
                        print(f"  {field}:")
                        for v in value:
                            print(f"    {v}")
                    else:
                        print(f"  {field}: {value}")

            writer.writerow(
                {
                    "Filepath": filepath,
                    "Player name": save_data.summary.player_name,
                    "Playtime": f"{save_data.summary.playtime.hours}:{save_data.summary.playtime.minutes:0>2}:{save_data.summary.playtime.seconds:0>2}",
                    "Party": ", ".join(
                        [
                            f"{preview.name} lv.{preview.level}"
                            for preview in save_data.summary.party_monsters
                        ]
                    ),
                    "Gold": save_data.player_info.gold,
                    "Atm": save_data.player_info.atm_gold,
                    "Num darkonium times 5": save_data.summary.num_darkonium_times_5,
                }
            )


def main_without_args() -> None:
    main(sys.argv[1:])
