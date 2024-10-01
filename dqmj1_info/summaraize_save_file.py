from dataclasses import asdict
from typing import List, Tuple

import argparse
import csv
import glob
import json
import logging
import pathlib
import sys

from .character_encoding import CHARACTER_ENCODINGS
from .save_data import SaveData, SaveDataRaw
from .string_tables import StringTable


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--save_data_filepaths", required=True, nargs="+", type=pathlib.Path
    )
    parser.add_argument("--strings_csv", required=True)
    parser.add_argument("--output_csv_filepath", required=True, type=pathlib.Path)
    parser.add_argument("--output_json_directory", required=True, type=pathlib.Path)
    parser.add_argument("--character_encoding", required=True)

    args = parser.parse_args(argv)

    save_data_filepaths: List[pathlib.Path] = [
        pathlib.Path(filepath)
        for filepath_pattern in args.save_data_filepaths
        for filepath in sorted(glob.glob(str(filepath_pattern)))
    ]
    with open(args.strings_csv, "r", encoding="utf-8") as input_stream:
        strings = StringTable.from_csv(input_stream)
    output_json_directory: pathlib.Path = args.output_json_directory
    output_csv_filepath: pathlib.Path = args.output_csv_filepath

    character_encoding = CHARACTER_ENCODINGS[args.character_encoding]

    output_json_directory.mkdir(exist_ok=True, parents=True)

    save_data_list: List[Tuple[pathlib.Path, SaveData, SaveDataRaw]] = []
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
    with open(output_csv_filepath, "w", encoding="utf-8") as output_stream:
        writer = csv.DictWriter(output_stream, fieldnames=columns)
        writer.writeheader()

        for filepath, save_data, raw in save_data_list:
            cli_output = summarize_save_file_to_cli_output(save_data, raw, strings)
            print_cli_output(filepath, cli_output)

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

            with open(
                output_json_directory / filepath.with_suffix(".json").name,
                "w",
                encoding="utf-8",
            ) as output_stream:
                json.dump(asdict(save_data), output_stream, indent=4)


def summarize_save_file_to_cli_output(
    save_data: SaveData, raw: SaveDataRaw, strings: StringTable
) -> List[Tuple[str, List[Tuple[str, str | List[str]]]]]:
    header = save_data.header
    summary = save_data.summary
    player_info = save_data.player_info
    monsters = save_data.monsters
    incarnus = save_data.incarnus
    other = save_data.other

    calculated_checksum = raw.checksum
    checksum_check_string = (
        "(✓)"
        if calculated_checksum == header.checksum
        else f"(Incorrect, {hex(calculated_checksum)})"
    )

    data: List[Tuple[str, List[Tuple[str, str | List[str]]]]] = [
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
                        f"{party_monster.name} lv.{party_monster.level} ({strings.get_monster_species_name(party_monster.species_id)})"
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
                (
                    "Items in hand",
                    f"{len([item_id for item_id in player_info.items_in_hand if item_id != 0])}",
                ),
                (
                    "Items in bag",
                    f"{sum(player_info.item_in_bag_counts)} (total)",
                ),
                (
                    "Num darkonium",
                    f"{int(player_info.num_darkonium_times_5 / 5)} ({player_info.num_darkonium_times_5})",
                ),
                (
                    "Playtime",
                    f"{player_info.playtime.hours}:{player_info.playtime.minutes:0>2}:{player_info.playtime.seconds:0>2}",
                ),
                ("Num party monsters", str(player_info.num_party_monsters)),
                ("Num monsters", str(player_info.num_monsters)),
                ("Num monsters scouted", str(player_info.num_monsters_scouted)),
                ("Num battles won", str(player_info.num_battles_won)),
                ("Num times synthesized", str(player_info.num_times_synthesized)),
            ],
        ),
        (
            "Monsters",
            [
                (
                    str(i),
                    f"{monsters[i].name} lv. {monsters[i].level} ({strings.get_monster_species_name(monsters[i].species_id)})",
                )
                for i in range(0, player_info.num_monsters)
            ],
        ),
        (
            "Incarnus",
            [
                (
                    str(0),
                    f"{incarnus.name} lv. {incarnus.level} ({strings.get_monster_species_name(incarnus.species_id)})",
                )
            ],
        ),
        (
            "Other",
            [
                (
                    "Battle enemy parameters id",
                    str(other.battle_enemy_parameters_id),
                )
            ],
        ),
    ]

    return data


def print_cli_output(
    filepath: pathlib.Path, data: List[Tuple[str, List[Tuple[str, str | List[str]]]]]
) -> None:
    print("=================")
    print(f"[{filepath}]")

    for section, section_data in data:
        print(f"{section}:")
        for field, value in section_data:
            if isinstance(value, list):
                print(f"  {field}:")
                for v in value:
                    print(f"    {v}")
            else:
                print(f"  {field}: {value}")


def main_without_args() -> None:
    main(sys.argv[1:])
