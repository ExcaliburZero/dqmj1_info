import collections.abc
from dataclasses import dataclass
from typing import Iterator, List, Tuple

import argparse
import collections
import sys

SUCCESS = 0
FAILURE = 1

BITS_32 = 0xFFFFFFFF


@dataclass
class Rng(collections.abc.Iterable[int]):
    value: int
    counter: int

    def __iter__(self) -> Iterator[int]:
        while True:
            yield next(self)

    def __next__(self) -> int:
        assert self.value & BITS_32 == self.value

        self.value = (
            ((((self.value + self.counter) & BITS_32) + (self.value >> 1)) & BITS_32)
            + 0x795B3D1F
        ) & BITS_32

        self.counter = (self.counter + 1) & BITS_32

        return self.value


def monobit_test(
    rng: Rng, iterations: int, check_interval: int
) -> Tuple[float, List[Tuple[int, float]]]:
    num_zeroes = 0
    num_ones = 0

    intermediate_results = []

    for i in range(0, iterations):
        value = next(rng)

        for b in range(0, 32):
            if (value & 2**b) == 0:
                num_zeroes += 1
            else:
                num_ones += 1

        if (i + 1) % check_interval == 0:
            intermediate_results.append((i + 1, num_ones / (num_zeroes + num_ones)))

    return num_ones / (num_zeroes + num_ones), intermediate_results


def perbit_test(rng: Rng, iterations: int) -> List[float]:
    num_zeroes = [0 for _ in range(0, 32)]
    num_ones = [0 for _ in range(0, 32)]

    for _ in range(0, iterations):
        value = next(rng)

        for b in range(0, 32):
            if (value & 2**b) == 0:
                num_zeroes[b] += 1
            else:
                num_ones[b] += 1

    return [num_ones[b] / (num_zeroes[b] + num_ones[b]) for b in range(0, 32)]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("--start_value", type=int, required=True)
    parser.add_argument("--start_counter", type=int, required=True)

    args = parser.parse_args(argv)

    num_iterations = 10000000

    rng = Rng(value=args.start_value, counter=args.start_counter)
    monobit_results = monobit_test(rng, num_iterations, int(num_iterations / 10))
    print("monobit:", monobit_results[0])
    for i, r in monobit_results[1]:
        print(f"\t{i}\t{r}")
    print(rng)

    rng = Rng(value=args.start_value, counter=args.start_counter)
    perbit_results = perbit_test(rng, num_iterations)
    print("perbit:")
    for b in range(0, 32):
        print(f"{b}\t{perbit_results[b]}")
    print(rng)

    rng = Rng(value=args.start_value, counter=args.start_counter)
    print("sample:")
    for _ in range(0, 10):
        print(f"\t{next(rng):032b}")

    return SUCCESS


if __name__ == "__main__":
    main(sys.argv[1:])
