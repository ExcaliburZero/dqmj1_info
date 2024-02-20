from typing import List

import argparse
import sys

import numpy as np


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument("--num_iterations", default=10000000, type=int)

    args = parser.parse_args(argv)

    np.random.seed(args.seed)

    num_plus = 0
    num_minus = 0
    num_pm = 0
    for _ in range(0, args.num_iterations):
        result = simulate()

        if result == 0:
            num_plus += 1
        elif result == 1:
            num_minus += 1
        elif result == 2:
            num_pm += 1

    def fraction(count: int) -> str:
        return f"{(count / args.num_iterations) * 100.0:.03f}%"

    print(f"+   = {fraction(num_plus)} ({num_plus})")
    print(f"-   = {fraction(num_minus)} ({num_minus})")
    print(f"+/- = {fraction(num_pm)} ({num_pm})")


def simulate() -> int:
    rng_value = np.random.randint(0, np.iinfo(np.uint32).max, dtype=np.uint32)

    constant = np.uint32(0xF0F0F0F1)
    assert hex(constant) == "0xF0F0F0F1".lower(), hex(constant)

    value = (np.uint32((int((np.uint64(constant) * np.uint64(rng_value))) >> 36))) * 17

    if rng_value == value:
        return 2

    rng_value = np.random.randint(0, np.iinfo(np.uint32).max, dtype=np.uint32)
    return int(rng_value & 0x1)


if __name__ == "__main__":
    main(sys.argv[1:])
