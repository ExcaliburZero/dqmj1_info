from typing import List

import argparse
import pathlib
import sys

import pandas as pd

from .evt import Instruction


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--script_filepaths", required=True, nargs="+")
    parser.add_argument("--output_csv", required=True)

    args = parser.parse_args(argv)

    script_filepaths = [pathlib.Path(filepath) for filepath in args.script_filepaths]
    output_csv = pathlib.Path(args.output_csv)

    text = []
    for script_filepath in script_filepaths:
        with open(script_filepath, "r") as input_stream:
            for i, line in enumerate(input_stream):
                if "SpeakerName" in line:
                    instruction = Instruction.from_script(line)
                    assert instruction is not None
                    text.append(
                        (script_filepath, i, "SpeakerName", instruction.arguments[0])
                    )
                elif "SetDialog" in line:
                    instruction = Instruction.from_script(line)
                    assert instruction is not None
                    text.append(
                        (script_filepath, i, "SetDialog", instruction.arguments[0])
                    )

    data = pd.DataFrame(
        text, columns=["Filepath", "Line Number", "Instruction Type", "Text"]
    )
    data.to_csv(output_csv, index=False)


def main_without_args() -> None:
    main(sys.argv[1:])
