from typing import List

import argparse
import sys


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", required=True)
    parser.add_argument("--start_hex", required=True)
    parser.add_argument("--length", required=True, type=int)

    args = parser.parse_args(argv)

    start = int(args.start_hex, 0)
    length: int = args.length

    with open(args.file, "rb") as input_stream:
        file_bytes = input_stream.read()

    buffer: List[str] = []
    for i, byte in enumerate(file_bytes[start : start + length]):
        if byte == 0x00:
            continue
        elif byte == 0xFF:
            string = "".join(buffer)
            if string != "":
                print(string, hex(i + start))
            buffer = []
        else:
            char = byte_to_char(byte)
            buffer.append(char)


def byte_to_char(byte: int) -> str:
    a = 0x25
    A = 0x0B
    char_lower = chr((byte - a) + ord("a"))
    char_upper = chr((byte - A) + ord("A"))

    mapping = {
        0x1: "1",
        0x2: "2",
        0x3: "3",
        0x4: "4",
        0x5: "5",
        0x6: "6",
        0x7: "7",
        0x8: "8",
        0x9: "9",
        0xA: " ",
        0x55: "Ü",
        0x71: "?",
        0x87: "+",
        0x8D: "II",
        0x8E: "III",
        0x9B: "'",
        0xAC: ".",
        0xAD: "&",
        0xFE: "\\n",
    }

    if char_lower.islower() and char_lower.isascii():
        return char_lower
    elif char_upper.isupper() and char_upper.isascii():
        return char_upper
    elif byte in mapping:
        return mapping[byte]
    else:
        # return "?"
        # return "[" + char + "]"
        return "[" + hex(byte) + "]"


if __name__ == "__main__":
    main(sys.argv[1:])
