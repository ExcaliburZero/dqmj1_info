from typing import List

import argparse
import collections
import pathlib
import sys

from .evt import Event


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--evt_filepaths", required=True, nargs="+")
    parser.add_argument("--output_directory", required=True)
    parser.add_argument(
        "--ignore_unknown_instructions", default=False, action="store_true"
    )

    args = parser.parse_args(argv)

    evt_filepaths = [pathlib.Path(filepath) for filepath in args.evt_filepaths]
    output_directory = pathlib.Path(args.output_directory)

    output_directory.mkdir(exist_ok=True, parents=True)

    instructions_by_type = collections.defaultdict(lambda: [])
    for evt_filepath in evt_filepaths:
        with open(evt_filepath, "rb") as input_stream:
            try:
                event = Event.from_evt(input_stream)
            except Exception as e:
                raise Exception(f"Failed to parse evt file: {evt_filepath}") from e

        for instruction in event.instructions:
            instructions_by_type[instruction.type_id].append(instruction)

        output_filepath = output_directory / (evt_filepath.name + ".dqmj1_script")
        with open(output_filepath, "w") as output_stream:
            if args.ignore_unknown_instructions:
                for instruction in event.instructions:
                    if not instruction.instruction_type.name == "UNKNOWN":
                        print(instruction.to_script(), file=output_stream)
            else:
                event.write_script(output_stream)

    instruction_examples_dir = output_directory / "instruction_examples"
    instruction_examples_dir.mkdir(exist_ok=True)

    for instruction_type, instructions in sorted(instructions_by_type.items()):
        filepath = instruction_examples_dir / f"{instruction_type:02x}.txt"
        with open(filepath, "w") as output_stream:
            examples = set()
            for instruction in instructions:
                examples.add(instruction.to_script())

            for instruction_str in sorted(examples):
                print(instruction_str, file=output_stream)


def main_without_args() -> None:
    main(sys.argv[1:])
