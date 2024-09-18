from typing import List

import argparse
import pathlib
import sys

from .character_encoding import CHARACTER_ENCODINGS
from .evt import Event


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--script_filepaths", required=True, nargs="+")
    parser.add_argument("--output_directory", required=True)
    parser.add_argument("--character_encoding", required=True)

    args = parser.parse_args(argv)

    script_filepaths = [pathlib.Path(filepath) for filepath in args.script_filepaths]
    output_directory = pathlib.Path(args.output_directory)
    character_encoding = CHARACTER_ENCODINGS[args.character_encoding]

    output_directory.mkdir(exist_ok=True, parents=True)

    for script_filepath in script_filepaths:
        with open(script_filepath, "r") as input_stream:
            try:
                event = Event.from_script(input_stream, character_encoding)
            except Exception as e:
                raise Exception(f"Failed to load script: {script_filepath}") from e

        output_filepath = output_directory / (
            script_filepath.name.replace(".dqmj1_script", "")
        )
        if not output_filepath.name.endswith(".evt"):
            output_filepath = output_filepath.with_suffix(".evt")

        with open(output_filepath, "wb") as output_stream:
            try:
                event.write_evt(output_stream, character_encoding)
            except Exception as e:
                raise Exception(f"Failed to write evt file: {output_filepath}") from e


def main_without_args() -> None:
    main(sys.argv[1:])
