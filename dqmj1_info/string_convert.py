from typing import List

import argparse
import sys

def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("text")

    args = parser.parse_args(argv)

    converted_text = convert_string_to_hex(args.text)
    print(converted_text)

def convert_string_to_hex(text: str) -> List[str]:
    return [
        hex(char_to_hex(c))
        for c in text
    ]

def char_to_hex(c: str) -> int:
    if c == c.upper():
        return ord(c) - ord("A") + 11
    elif c == c.lower():
        return ord(c) - ord("a") + 37

    raise NotImplementedError()


if __name__ == "__main__":
    main(sys.argv[1:])