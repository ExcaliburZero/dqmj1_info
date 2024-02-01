from typing import List

import argparse
import sys

import evt


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--evt_filepath")

    args = parser.parse_args(argv)

    with open(args.evt_filepath, "rb") as input_stream:
        event = evt.Event.from_evt(input_stream)

    for command in event.commands:
        if not isinstance(command, evt.UnknownCommand):
            print(command)


if __name__ == "__main__":
    main(sys.argv[1:])
