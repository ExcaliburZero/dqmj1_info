from typing import IO, List

import sys

HEADER_SIZE = 0x70
DATA_SIZE = 10613

#ENDIANESS = "big"
ENDIANESS = "little" #confirmed for DQJ2 save files

class SaveDataRaw:

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "SaveDataRaw":
        header = input_stream.read(HEADER_SIZE)
        print(header)
        print(header[12:16])

        data = input_stream.read(DATA_SIZE * 4) # Seems to be the correct ending index

        print(len(data), HEADER_SIZE + DATA_SIZE * 4)
        print("---------------")
        checksum = int(SaveDataRaw.dqj1_checksum(data)).to_bytes(4, ENDIANESS)

        print("Checksum:", checksum)
        print(f"{len(header)=}")
        print(f"{len(data)=}")

    @staticmethod
    def dqj1_checksum(data: List[bytes]) -> int:
        num = 0
        j = 0
        while j < DATA_SIZE:
            value = int.from_bytes(data[j * 4:j * 4 + 4], ENDIANESS)

            print(data[j * 4:j * 4 + 4])

            num += value
            num = num & 0xFFFFFFFF

            j += 1

        return num

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as input_stream:
        data = SaveDataRaw.from_sav(input_stream)
        print(data)