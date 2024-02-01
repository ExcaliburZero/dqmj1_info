from typing import List

import argparse
import collections
import pathlib
import sys

from .evt import Event, UnknownCommand


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--evt_filepaths", required=True, nargs="+")
    parser.add_argument("--output_directory", required=True)
    parser.add_argument("--ignore_unknown_commands", default=False, action="store_true")

    args = parser.parse_args(argv)

    evt_filepaths = [pathlib.Path(filepath) for filepath in args.evt_filepaths]
    output_directory = pathlib.Path(args.output_directory)

    output_directory.mkdir(exist_ok=True, parents=True)

    commands_by_type = collections.defaultdict(lambda: [])
    for evt_filepath in evt_filepaths:
        with open(evt_filepath, "rb") as input_stream:
            event = Event.from_evt(input_stream)

        output_filepath = output_directory / (evt_filepath.name + ".dqmj1_script")
        with open(output_filepath, "w") as output_stream:
            for command in event.commands:
                commands_by_type[command.type_id].append(command)

                if not args.ignore_unknown_commands or not isinstance(
                    command, UnknownCommand
                ):
                    print(command, file=output_stream)

    command_examples_dir = output_directory / "command_examples"
    command_examples_dir.mkdir(exist_ok=True)

    for command_type, commands in commands_by_type.items():
        filepath = command_examples_dir / f"{command_type:02x}.txt"
        with open(filepath, "w") as output_stream:
            examples = set()
            for command in commands:
                examples.add(str(command))

            for command_str in sorted(examples):
                print(command_str, file=output_stream)


if __name__ == "__main__":
    main(sys.argv[1:])
