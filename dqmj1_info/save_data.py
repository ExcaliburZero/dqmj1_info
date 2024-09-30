from dataclasses import dataclass
from typing import IO, List, Literal, Tuple

import io
import sys

from .character_encoding import CharacterEncoding

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


@dataclass
class MonsterPreview:
    name: str
    level: int

    @staticmethod
    def multiple_from_raw(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> List["MonsterPreview"]:
        names = []
        for _ in range(0, 3):
            input_stream.read(3)
            names.append(character_encoding.bytes_to_string(input_stream.read(9)))

        input_stream.read(9)

        levels = [int.from_bytes(input_stream.read(1)) for _ in range(0, 3)]

        return [
            MonsterPreview(name=name, level=level) for name, level in zip(names, levels)
        ]


@dataclass
class Playtime:
    hours: int
    minutes: int
    seconds: int
    remaining: int

    @staticmethod
    def from_int(raw: int) -> "Playtime":
        remaining = raw & 0b111111
        seconds = (raw >> 6) & 0b111111
        minutes = (raw >> 12) & 0b111111
        hours = raw >> 18

        return Playtime(
            hours=hours, minutes=minutes, seconds=seconds, remaining=remaining
        )


@dataclass
class Header:
    magic_1: int
    magic_2: int
    magic_3: int
    checksum: int

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "Header":
        magic_1 = int.from_bytes(input_stream.read(4), ENDIANESS)
        magic_2 = int.from_bytes(input_stream.read(4), ENDIANESS)
        magic_3 = int.from_bytes(input_stream.read(4), ENDIANESS)
        checksum = int.from_bytes(input_stream.read(4), ENDIANESS)

        return Header(
            magic_1=magic_1, magic_2=magic_2, magic_3=magic_3, checksum=checksum
        )


@dataclass
class Summary:
    playtime: Playtime
    player_name: str
    party_previews: List[MonsterPreview]
    num_darkonium_times_5: int

    @staticmethod
    def from_sav(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> "Summary":
        input_stream.read(28)
        playtime = Playtime.from_int(int.from_bytes(input_stream.read(4), ENDIANESS))

        num_party_monsters = int.from_bytes(input_stream.read(1))

        input_stream.read(1)
        player_name = character_encoding.bytes_to_string(input_stream.read(9))

        party_previews = MonsterPreview.multiple_from_raw(
            input_stream, character_encoding
        )[0:num_party_monsters]
        num_darkonium_times_5 = int.from_bytes(input_stream.read(1))

        return Summary(
            playtime=playtime,
            player_name=player_name,
            party_previews=party_previews,
            num_darkonium_times_5=num_darkonium_times_5,
        )


@dataclass
class PlayerInfo:
    player_name: str
    gold: int
    atm_gold: int
    items_in_hand: List[int]  # List of 16 ids
    item_in_bag_counts: List[int]  # List of counts (256 entries)
    num_darkonuium_times_5: int
    playtime: Playtime
    num_party_monsters: int
    num_monsters: int
    num_monsters_scouted: int
    num_battles_won: int
    num_times_synthesized: int

    @staticmethod
    def from_sav(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> "PlayerInfo":
        player_name = character_encoding.bytes_to_string(input_stream.read(12))
        gold = int.from_bytes(input_stream.read(4), ENDIANESS)
        atm_gold = int.from_bytes(input_stream.read(4), ENDIANESS)
        items_in_hand = [b for b in input_stream.read(16)]
        item_in_bag_counts = [b for b in input_stream.read(256)]
        num_darkonuium_times_5 = int.from_bytes(input_stream.read(1))
        input_stream.read(3)
        playtime = Playtime.from_int(int.from_bytes(input_stream.read(4), ENDIANESS))
        num_party_monsters = int.from_bytes(input_stream.read(1))
        num_monsters = int.from_bytes(input_stream.read(1))
        input_stream.read(290)
        num_monsters_scouted = int.from_bytes(input_stream.read(4), ENDIANESS)
        input_stream.read(4)
        input_stream.read(4)
        num_battles_won = int.from_bytes(input_stream.read(4), ENDIANESS)
        num_times_synthesized = int.from_bytes(input_stream.read(4), ENDIANESS)
        input_stream.read(640)

        return PlayerInfo(
            player_name=player_name,
            gold=gold,
            atm_gold=atm_gold,
            items_in_hand=items_in_hand,
            item_in_bag_counts=item_in_bag_counts,
            num_darkonuium_times_5=num_darkonuium_times_5,
            playtime=playtime,
            num_party_monsters=num_party_monsters,
            num_monsters=num_monsters,
            num_monsters_scouted=num_monsters_scouted,
            num_battles_won=num_battles_won,
            num_times_synthesized=num_times_synthesized,
        )


@dataclass
class SaveData:
    header: Header
    summary: Summary
    player_info: PlayerInfo

    @staticmethod
    def from_sav(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> Tuple["SaveData", SaveDataRaw]:
        raw = SaveDataRaw.from_sav(input_stream)

        return SaveData.from_raw(raw, character_encoding), raw

    @staticmethod
    def from_raw(raw: SaveDataRaw, character_encoding: CharacterEncoding) -> "SaveData":
        input_stream = io.BytesIO(raw.raw)

        header = Header.from_sav(input_stream)
        summary = Summary.from_sav(input_stream, character_encoding)

        input_stream.read(268)
        player_info = PlayerInfo.from_sav(input_stream, character_encoding)

        return SaveData(
            header=header,
            summary=summary,
            player_info=player_info,
        )


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as input_stream:
        data = SaveDataRaw.from_sav(input_stream)

    print(data.checksum)
    print(data.calculate_data_checksum())
    data.checksum = data.calculate_data_checksum()

    with open(sys.argv[1][:-4] + "_fixed_checksum.sav", "wb") as output_stream:
        data.write_sav(output_stream)
