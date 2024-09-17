from typing import List

import argparse
import enum
import glob
import logging
import pathlib
import sys

import gooey  # type: ignore

from . import ability_tbl
from . import d16_to_png
from . import decompile_evt
from . import enmy_kind_tbl
from . import extract_fpks
from . import extract_strings
from . import extract_string_address_tables
from . import extract_script_dialogue
from . import item_table
from . import item_tbl
from . import monster_species_table
from . import region_configs
from . import skill_set_table
from . import skill_tbl
from . import meta_info

SUCCESS = 0
FAILURE = 1


class UiMode(enum.Enum):
    CLI = enum.auto()
    GUI = enum.auto()


def cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_directory",
        required=True,
        help="Directory containing the unpacked game files (typically unpacked using a program link DsLazy).",
    )
    parser.add_argument(
        "--output_directory",
        required=True,
        help="Directory to write extracted files to. It is recommended to create a new empty directory.",
    )
    parser.add_argument(
        "--region",
        default="North America",
        help="Region of the ROM that the game files are from. This determines where to look for strings and other data in the game's executable binaries.",
        choices=region_configs.REGION_CONFIGS.keys(),
    )

    return parser


ABOUT_MENU = {
    "name": "Help",
    "items": [
        {
            "type": "AboutDialog",
            "menuTitle": "About",
            "version": meta_info.version,
            "copyright": meta_info.copyright_year,
            "website": meta_info.website,
            "license": meta_info.license,
        }
    ],
}


@gooey.Gooey(
    program_name="DQMJ1 Unofficial File Extractor",
    default_size=(800, 500),
    progress_regex=r"^INFO> \((?P<current>\d+)/(?P<total>\d+)\)",
    progress_expr="current / total * 100",
    menu=[ABOUT_MENU],
)
def gui_parser() -> gooey.GooeyParser:
    parser = gooey.GooeyParser(
        description="Program that extracts data files from Dragon Quest Monsters: Joker."
    )

    parser.add_argument(
        "--input_directory",
        required=True,
        metavar="Input directory",
        widget="DirChooser",
        help="Directory containing the unpacked game files (typically unpacked using a program link DsLazy).",
    )
    parser.add_argument(
        "--output_directory",
        required=True,
        metavar="Output directory",
        widget="DirChooser",
        help="Directory to write extracted files to. It is recommended to create a new empty directory.",
    )
    parser.add_argument(
        "--region",
        default="North America",
        metavar="Region",
        help="Region of the ROM that the game files are from. This determines where to look for strings and other data in the game's executable binaries.",
        choices=region_configs.REGION_CONFIGS.keys(),
    )

    return parser


def setup_logging(log_filepath: pathlib.Path) -> None:
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(levelname)s> %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename=log_filepath)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)


def main(argv: List[str], mode: UiMode):
    if mode == UiMode.GUI:
        parser = gui_parser()
    else:
        parser = cli_parser()

    args = parser.parse_args(argv)

    setup_logging(log_filepath=pathlib.Path(".") / "extract_dqmj1_files_log.txt")

    logging.debug(f"Arguments: {args}")

    input_directory = pathlib.Path(args.input_directory)
    output_directory = pathlib.Path(args.output_directory)

    if not input_directory.exists():
        logging.error(f"Input directory does not exist: {input_directory}")
        return FAILURE

    if args.region not in region_configs.REGION_CONFIGS:
        logging.error(
            f'Unrecognized region "{args.region}". Known regions are: {", ".join(sorted(region_configs.REGION_CONFIGS.keys()))}'
        )
        return FAILURE

    total_steps = 14
    steps_completed = 0

    ###
    # Setup output directory
    ###
    output_directory.mkdir(exist_ok=True, parents=True)
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Created output directory: {output_directory}"
    )

    ###
    # Extract FPK file parchives / packages
    ###
    fpk_extracted_files_dir = output_directory / "fpk_extracted_files"
    extract_fpks.main(
        [
            "--fpk_bin_filepaths",
            *sorted(
                list(glob.glob(str(input_directory / "data" / "*.bin")))
                + list(glob.glob(str(input_directory / "data" / "*.map")))
            ),
            "--output_directory",
            str(fpk_extracted_files_dir),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracted files from FPKs to: {fpk_extracted_files_dir}"
    )

    ###
    # Extract strings
    ###
    strings_without_context_csv = output_directory / "strings_without_context.csv"
    extract_strings.main(
        [
            "--data_directory",
            str(input_directory),
            "--output_csv",
            str(strings_without_context_csv),
            "--region",
            args.region,
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished writing extracted strings to: {strings_without_context_csv}"
    )

    ###
    # Lookup strings by table
    ###
    strings_by_table_csv = output_directory / "strings_by_table.csv"
    extract_string_address_tables.main(
        [
            "--data_directory",
            str(input_directory),
            "--mined_strings",
            str(strings_without_context_csv),
            "--output_csv",
            str(strings_by_table_csv),
            "--region",
            args.region,
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished writing extracted string tables to: {strings_by_table_csv}"
    )

    ###
    # Extract EnmyKindTbl
    ###
    ability_tbl_csv = output_directory / "AbilityTbl.csv"
    ability_tbl.main(
        [
            "--table_filepath",
            str(input_directory / "data" / "AbilityTbl.bin"),
            "--output_csv",
            str(ability_tbl_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracting AbilityTbl.bin to: {ability_tbl_csv}"
    )

    ###
    # Extract EnmyKindTbl
    ###
    enmy_kind_tbl_csv = output_directory / "EnmyKindTbl.csv"
    enmy_kind_tbl.main(
        [
            "--table_filepath",
            str(input_directory / "data" / "EnmyKindTbl.bin"),
            "--output_csv",
            str(enmy_kind_tbl_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracting EnmyKindTbl.bin to: {enmy_kind_tbl_csv}"
    )

    ###
    # Extract SkillTbl
    ###
    skill_tbl_csv = output_directory / "SkillTbl.csv"
    skill_tbl.main(
        [
            "--table_filepath",
            str(input_directory / "data" / "SkillTbl.bin"),
            "--output_csv",
            str(skill_tbl_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracting SkillTbl.bin to: {skill_tbl_csv}"
    )

    ###
    # Extract ItemTbl
    ###
    item_tbl_csv = output_directory / "ItemTbl.csv"
    item_tbl.main(
        [
            "--table_filepath",
            str(input_directory / "data" / "ItemTbl.bin"),
            "--output_csv",
            str(item_tbl_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracting ItemTbl.bin to: {skill_tbl_csv}"
    )

    ###
    # Extract D16 images
    ###
    d16_images_dir = output_directory / "d16_images"
    d16_to_png.main(
        [
            "--d16_filepaths",
            *sorted(glob.glob(str(input_directory / "data" / "*.d16"))),
            "--output_directory",
            str(d16_images_dir),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracting d16 images to: {d16_images_dir}"
    )

    ###
    # Decompile scripts
    ###
    scripts_dir = output_directory / "scripts"
    decompile_evt.main(
        [
            "--evt_filepaths",
            *sorted(glob.glob(str(input_directory / "data" / "*.evt"))),
            *sorted(glob.glob(str(fpk_extracted_files_dir / "*.ev*"))),
            "--output_directory",
            str(scripts_dir),
            # "--ignore_unknown_commands",
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished decompiling scripts to: {scripts_dir}"
    )

    ###
    # Extract dialogue
    ###
    event_dialogue_csv = output_directory / "scripts" / "dialogue.csv"
    extract_script_dialogue.main(
        [
            "--script_filepaths",
            *sorted(glob.glob(str(scripts_dir / "*.dqmj1_script"))),
            "--output_csv",
            str(event_dialogue_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished extracting scripts dialogue to: {event_dialogue_csv}"
    )

    ###
    # Create monster species table
    ###
    monster_species_table_csv = output_directory / "monster_species.csv"
    monster_species_table.main(
        [
            "--strings_csv",
            str(strings_by_table_csv),
            "--enmy_kind_tbl_csv",
            str(enmy_kind_tbl_csv),
            "--output_csv",
            str(monster_species_table_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished creating monster species table: {monster_species_table_csv}"
    )

    ###
    # Create skill set table
    ###
    skill_set_table_csv = output_directory / "skill_sets.csv"
    skill_set_table.main(
        [
            "--strings_csv",
            str(strings_by_table_csv),
            "--skill_tbl_csv",
            str(skill_tbl_csv),
            "--output_csv",
            str(skill_set_table_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished creating skill set table: {skill_set_table_csv}"
    )

    ###
    # Create item set table
    ###
    item_table_csv = output_directory / "items.csv"
    item_table.main(
        [
            "--strings_csv",
            str(strings_by_table_csv),
            "--item_tbl_csv",
            str(item_tbl_csv),
            "--output_csv",
            str(item_table_csv),
        ]
    )
    steps_completed += 1
    logging.info(
        f"({steps_completed}/{total_steps}) Finished creating item set table: {item_table_csv}"
    )

    return SUCCESS


def main_cli() -> None:
    return main(sys.argv[1:], mode=UiMode.CLI)


def main_gui() -> None:
    return main(sys.argv[1:], mode=UiMode.GUI)
