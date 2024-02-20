from typing import List

import argparse
import logging
import pathlib
import sys

from .fpk import Fpk


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fpk_bin_filepaths", required=True, nargs="+", type=pathlib.Path
    )
    parser.add_argument("--output_directory", required=True, type=pathlib.Path)

    args = parser.parse_args(argv)

    fpk_bin_filepaths: List[pathlib.Path] = args.fpk_bin_filepaths
    output_directory: pathlib.Path = args.output_directory

    output_directory.mkdir(exist_ok=True, parents=True)

    for fpk_bin_filepath in fpk_bin_filepaths:
        logging.info(f"Looking at bin file: {fpk_bin_filepath}")
        with open(fpk_bin_filepath, "rb") as input_stream:
            fpk_bin = Fpk.from_bin(input_stream)

        if fpk_bin is not None:
            logging.info(f"{fpk_bin_filepath} is an FPK file.")
            for file_description, contents in fpk_bin.files.items():
                output_filepath = output_directory / file_description.name
                with open(output_filepath, "wb") as output_stream:
                    output_stream.write(contents)

                logging.debug(f"Wrote extracted file: {output_filepath}")
        else:
            logging.info(f"{fpk_bin_filepath} is not an FPK file.")


def main_without_args() -> None:
    main(sys.argv[1:])
