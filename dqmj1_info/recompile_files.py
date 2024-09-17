from typing import List

import argparse
import enum
import glob
import logging
import pathlib
import sys

import gooey  # type: ignore

from . import compile_evt
from . import region_configs

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
        help="Directory containing the extracted game files.",
    )
    parser.add_argument(
        "--output_directory",
        required=True,
        help="Directory to write extracted files to. Typically the directory containing the unpacked game files (unpacked using a program link DsLazy).",
    )
    parser.add_argument(
        "--region",
        default="North America",
        choices=region_configs.REGION_CONFIGS.keys(),
    )

    return parser


@gooey.Gooey(program_name="DQMJ1 Unofficial File Recompiler")
def gui_parser() -> gooey.GooeyParser:
    parser = gooey.GooeyParser(
        description="Program that recompiles extracted data files from Dragon Quest Monsters: Joker."
    )

    parser.add_argument(
        "--input_directory",
        required=True,
        widget="DirChooser",
        help="Directory containing the extracted game files.",
    )
    parser.add_argument(
        "--output_directory",
        required=True,
        widget="DirChooser",
        help="Directory to write extracted files to. Typically the directory containing the unpacked game files (unpacked using a program link DsLazy).",
    )
    parser.add_argument(
        "--region",
        default="North America",
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

    setup_logging(log_filepath=pathlib.Path(".") / "recompile_dqmj1_files_log.txt")

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

    ###
    # Setup output directory
    ###
    output_directory.mkdir(exist_ok=True, parents=True)
    logging.info(f"Created output directory: {output_directory}")

    data_dir = input_directory / "data"

    ###
    # Recompile event scripts
    ###
    scripts_dir = input_directory / "scripts"
    compile_evt.main(
        [
            "--script_filepaths",
            *sorted(glob.glob(str(scripts_dir / "*.dqmj1_script"))),
            "--output_directory",
            str(data_dir),
        ]
    )
    logging.info(f"Finished recompiling event scripts to: {data_dir}")

    return SUCCESS


def main_cli() -> None:
    return main(sys.argv[1:], mode=UiMode.CLI)


def main_gui() -> None:
    return main(sys.argv[1:], mode=UiMode.GUI)
