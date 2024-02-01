from dataclasses import dataclass
from typing import IO, List, Literal

import sys

HEADER_SIZE = 0x70
DATA_SIZE = 10613

DATA_CHECKSUM_START = 0xC
DATA_CHECKSUM_END = 0xF

ENDIANESS: Literal["little"] = "little"


@dataclass
class SaveDataRaw:
    raw: bytearray

    @property
    def checksum(self) -> int:
        return int.from_bytes(
            self.raw[DATA_CHECKSUM_START : DATA_CHECKSUM_END + 1], ENDIANESS
        )

    @checksum.setter
    def checksum(self, checksum: int) -> None:
        checksum_bytes = checksum.to_bytes(4, ENDIANESS)
        for i, b in enumerate(checksum_bytes):
            self.raw[i + DATA_CHECKSUM_START] = b

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "SaveDataRaw":
        return SaveDataRaw(bytearray(input_stream.read(HEADER_SIZE + DATA_SIZE * 4)))

    @staticmethod
    def __checksum(data: bytearray) -> int:
        num = 0
        j = 0
        while j < DATA_SIZE:
            value = int.from_bytes(data[j * 4 : j * 4 + 4], ENDIANESS)

            num += value
            num = num & 0xFFFFFFFF

            j += 1

        return num

    def calculate_data_checksum(self) -> int:
        return SaveDataRaw.__checksum(self.raw[HEADER_SIZE:])

    def write_sav(self, output_stream: IO[bytes]) -> None:
        output_stream.write(self.raw)


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as input_stream:
        data = SaveDataRaw.from_sav(input_stream)

    print(data.checksum)
    print(data.calculate_data_checksum())
    data.checksum = data.calculate_data_checksum()

    with open(sys.argv[1][:-4] + "_fixed_checksum.sav", "wb") as output_stream:
        data.write_sav(output_stream)
