from typing import List

import argparse
import logging
import pathlib
import sys

from .d16 import D16Image


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--d16_filepaths", required=True, nargs="+")
    parser.add_argument("--output_directory", required=True)

    args = parser.parse_args(argv)

    d16_filepaths = [pathlib.Path(filepath) for filepath in args.d16_filepaths]
    output_directory = pathlib.Path(args.output_directory)

    output_directory.mkdir(exist_ok=True, parents=True)

    for d16_filepath in d16_filepaths:
        logging.debug(f"Processing d16 file: {d16_filepath}")
        with open(d16_filepath, "rb") as input_stream:
            d16_image = D16Image.from_d16(input_stream)

        if d16_image is not None:
            output_filepath = output_directory / (d16_filepath.name + ".png")
            with open(output_filepath, "wb") as output_stream:
                d16_image.write_png(output_stream)


def main_without_args() -> None:
    main(sys.argv[1:])
