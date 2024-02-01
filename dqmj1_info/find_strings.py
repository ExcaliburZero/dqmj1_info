from dataclasses import dataclass
from typing import Deque, List, Optional

import argparse
import collections
import sys

# TODO: endianess


@dataclass(frozen=True)
class StringPattern:
    string: str
    pattern: List[int]

    def match(self, ints: List[int]) -> Optional[List[int]]:
        if len(ints) < len(self.string):
            return None

        match = []
        changes = [b - a for a, b in zip(ints[:-1], ints[1:])]
        for a, b in zip(self.pattern, changes):
            if a != b:
                return None

        match = ints[: len(self.string)]

        return match

    @staticmethod
    def from_str(string: str) -> "StringPattern":
        character_ints = [ord(c) for c in string]
        pattern = [b - a for a, b in zip(character_ints[:-1], character_ints[1:])]

        return StringPattern(string=string, pattern=pattern)


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--string_files", nargs="+", required=True)

    args = parser.parse_args(argv)

    string_patterns = []
    max_length = 1
    for filepath in args.string_files:
        with open(filepath, "r") as input_stream:
            for string in input_stream:
                string = string.strip()
                if not string.isalpha():
                    continue

                # string = string[1:] # Remove first character since it is probably uppercase
                max_length = max(max_length, len(string))

                string_patterns.append(StringPattern.from_str(string))

    # for pattern in string_patterns:
    #    print(pattern)

    for filepath in args.files:
        # print("====", filepath, "====")
        with open(filepath, "rb") as input_stream:
            file_bytes = input_stream.read()

        byte_buffer: Deque[int] = collections.deque(maxlen=max_length)
        for i, byte in enumerate(file_bytes):
            # print(byte, byte_buffer)
            byte_buffer.append(byte)

            for pattern in string_patterns:
                for j in range(0, len(byte_buffer)):
                    match = pattern.match(list(byte_buffer)[j:])
                    if match:
                        match_hexes = [hex(b) for b in match]
                        print(
                            f"{filepath}:{hex(i + 1 - ((len(byte_buffer) - j)))}:",
                            match_hexes,
                            "matched_to:",
                            pattern.string,
                        )


if __name__ == "__main__":
    main(sys.argv[1:])
