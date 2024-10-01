from dataclasses import dataclass
from typing import IO, List, Literal, Tuple

import io
import sys

from .character_encoding import CharacterEncoding

HEADER_SIZE = 0x70
DATA_SIZE = 10613

DATA_CHECKSUM_START = 0xC
DATA_CHECKSUM_END = 0xF

MAX_NUM_MONSTERS = 100

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
    species_id: int
    level: int

    @staticmethod
    def multiple_from_raw(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> List["MonsterPreview"]:
        names = []
        for _ in range(0, 3):
            input_stream.read(3)
            names.append(character_encoding.bytes_to_string(input_stream.read(9)))

        input_stream.read(3)

        species_ids = [
            int.from_bytes(input_stream.read(2), ENDIANESS) for _ in range(0, 3)
        ]
        levels = [int.from_bytes(input_stream.read(1)) for _ in range(0, 3)]

        return [
            MonsterPreview(name=name, species_id=species_id, level=level)
            for name, species_id, level in zip(names, species_ids, levels)
        ]


@dataclass
class Playtime:
    hours: int
    minutes: int
    seconds: int
    frames: int

    @staticmethod
    def from_int(raw: int) -> "Playtime":
        frames = raw & 0b111111
        seconds = (raw >> 6) & 0b111111
        minutes = (raw >> 12) & 0b111111
        hours = raw >> 18

        return Playtime(hours=hours, minutes=minutes, seconds=seconds, frames=frames)


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
    party_monsters: List[MonsterPreview]
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

        party_monsters = MonsterPreview.multiple_from_raw(
            input_stream, character_encoding
        )[0:num_party_monsters]
        num_darkonium_times_5 = int.from_bytes(input_stream.read(1))

        input_stream.read(268)

        return Summary(
            playtime=playtime,
            player_name=player_name,
            party_monsters=party_monsters,
            num_darkonium_times_5=num_darkonium_times_5,
        )


@dataclass
class PlayerInfo:
    player_name: str
    gold: int
    atm_gold: int
    items_in_hand: List[int]  # List of 16 ids
    item_in_bag_counts: List[int]  # List of counts (256 entries)
    num_darkonium_times_5: int
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
        num_darkonium_times_5 = int.from_bytes(input_stream.read(1))
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
            num_darkonium_times_5=num_darkonium_times_5,
            playtime=playtime,
            num_party_monsters=num_party_monsters,
            num_monsters=num_monsters,
            num_monsters_scouted=num_monsters_scouted,
            num_battles_won=num_battles_won,
            num_times_synthesized=num_times_synthesized,
        )


@dataclass
class Stats:
    max_hp: int
    max_mp: int
    attack: int
    defense: int
    agility: int
    wisdom: int


@dataclass
class SkillSet:
    id: int
    points: int
    num_unlocked_skills: int

    @staticmethod
    def multiple_from_sav(input_stream: IO[bytes]) -> List["SkillSet"]:
        ids = [int.from_bytes(input_stream.read(1)) for _ in range(0, 3)]
        nums_points = [int.from_bytes(input_stream.read(1)) for _ in range(0, 3)]
        nums_unlocked_skills = [
            int.from_bytes(input_stream.read(1)) for _ in range(0, 3)
        ]

        return [
            SkillSet(
                id=ids[i],
                points=nums_points[i],
                num_unlocked_skills=nums_unlocked_skills[i],
            )
            for i in range(0, 3)
        ]


@dataclass
class ParentMonster:
    species_id: int
    name: str
    scout_name: str

    @staticmethod
    def from_sav(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> "ParentMonster":
        species_id = int.from_bytes(input_stream.read(2), ENDIANESS)
        name = character_encoding.bytes_to_string(input_stream.read(9))
        input_stream.read(2)
        scout_name = character_encoding.bytes_to_string(input_stream.read(11))

        return ParentMonster(species_id=species_id, name=name, scout_name=scout_name)


@dataclass
class Monster:
    name: str
    species_id: int
    rank: int
    family: int
    sex: int
    synthesis_plus_number: int
    level: int
    level_limit: int
    base_stats: Stats
    current_hp: int
    current_mp: int
    adjusted_stats: Stats
    exp: int
    tactic: int
    equipment: int
    skill_sets: List[SkillSet]
    unallocated_skill_points: int
    skills: List[int]
    traits: List[int]
    level_when_hashed: int
    hash: int
    scout_name: str
    parents: List[ParentMonster]
    grandparents: List[ParentMonster]

    @staticmethod
    def from_sav(
        input_stream: IO[bytes], character_encoding: CharacterEncoding
    ) -> "Monster":
        name = character_encoding.bytes_to_string(input_stream.read(12))
        species_id = int.from_bytes(input_stream.read(2), ENDIANESS)
        rank = int.from_bytes(input_stream.read(1))
        family = int.from_bytes(input_stream.read(1))
        sex = int.from_bytes(input_stream.read(1))
        input_stream.read(3)
        synthesis_plus_number = int.from_bytes(input_stream.read(1))
        input_stream.read(4)
        input_stream.read(24)
        input_stream.read(29)
        input_stream.read(2)
        input_stream.read(29)
        input_stream.read(5)
        level = int.from_bytes(input_stream.read(1))
        level_limit = int.from_bytes(input_stream.read(1))

        base_stats = Stats(
            max_hp=int.from_bytes(input_stream.read(2), ENDIANESS),
            max_mp=int.from_bytes(input_stream.read(2), ENDIANESS),
            attack=int.from_bytes(input_stream.read(2), ENDIANESS),
            defense=int.from_bytes(input_stream.read(2), ENDIANESS),
            agility=int.from_bytes(input_stream.read(2), ENDIANESS),
            wisdom=int.from_bytes(input_stream.read(2), ENDIANESS),
        )

        current_hp = int.from_bytes(input_stream.read(2), ENDIANESS)
        adjusted_max_hp = int.from_bytes(input_stream.read(2), ENDIANESS)
        current_mp = int.from_bytes(input_stream.read(2), ENDIANESS)
        adjusted_max_mp = int.from_bytes(input_stream.read(2), ENDIANESS)
        adjusted_stats = Stats(
            max_hp=adjusted_max_hp,
            max_mp=adjusted_max_mp,
            attack=int.from_bytes(input_stream.read(2), ENDIANESS),
            defense=int.from_bytes(input_stream.read(2), ENDIANESS),
            agility=int.from_bytes(input_stream.read(2), ENDIANESS),
            wisdom=int.from_bytes(input_stream.read(2), ENDIANESS),
        )

        exp = int.from_bytes(input_stream.read(4), ENDIANESS)
        tactic = int.from_bytes(input_stream.read(1))
        input_stream.read(6)
        input_stream.read(4)
        equipment = int.from_bytes(input_stream.read(1))

        skill_sets = SkillSet.multiple_from_sav(input_stream)

        input_stream.read(1)
        unallocated_skill_points = int.from_bytes(input_stream.read(2), ENDIANESS)
        skills = list(input_stream.read(30))
        traits = list(input_stream.read(31))
        input_stream.read(10)
        level_when_hashed = int.from_bytes(input_stream.read(1))
        monster_hash = int.from_bytes(input_stream.read(2), ENDIANESS)
        input_stream.read(2)
        scout_name = character_encoding.bytes_to_string(input_stream.read(12))

        parents = [
            ParentMonster.from_sav(input_stream, character_encoding),
            ParentMonster.from_sav(input_stream, character_encoding),
        ]
        grandparents = [
            ParentMonster.from_sav(input_stream, character_encoding),
            ParentMonster.from_sav(input_stream, character_encoding),
            ParentMonster.from_sav(input_stream, character_encoding),
            ParentMonster.from_sav(input_stream, character_encoding),
        ]

        return Monster(
            name=name,
            species_id=species_id,
            rank=rank,
            family=family,
            sex=sex,
            synthesis_plus_number=synthesis_plus_number,
            level=level,
            level_limit=level_limit,
            base_stats=base_stats,
            current_hp=current_hp,
            current_mp=current_mp,
            adjusted_stats=adjusted_stats,
            exp=exp,
            tactic=tactic,
            equipment=equipment,
            skill_sets=skill_sets,
            unallocated_skill_points=unallocated_skill_points,
            skills=skills,
            traits=traits,
            level_when_hashed=level_when_hashed,
            hash=monster_hash,
            scout_name=scout_name,
            parents=parents,
            grandparents=grandparents,
        )


@dataclass
class Other:
    battle_enemy_parameters_id: int

    @staticmethod
    def from_sav(input_stream: IO[bytes]) -> "Other":
        input_stream.read(64)
        input_stream.read(64)
        battle_enemy_parameters_id = int.from_bytes(input_stream.read(4), ENDIANESS)

        return Other(battle_enemy_parameters_id=battle_enemy_parameters_id)


@dataclass
class SaveData:
    header: Header
    summary: Summary
    player_info: PlayerInfo
    monsters: List[Monster]
    incarnus: Monster
    other: Other

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
        player_info = PlayerInfo.from_sav(input_stream, character_encoding)
        monsters = [
            Monster.from_sav(input_stream, character_encoding)
            for _ in range(0, MAX_NUM_MONSTERS)
        ]
        incarnus = Monster.from_sav(input_stream, character_encoding)
        other = Other.from_sav(input_stream)

        return SaveData(
            header=header,
            summary=summary,
            player_info=player_info,
            monsters=monsters,
            incarnus=incarnus,
            other=other,
        )


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as input_stream:
        data = SaveDataRaw.from_sav(input_stream)

    print(data.checksum)
    print(data.calculate_data_checksum())
    data.checksum = data.calculate_data_checksum()

    with open(sys.argv[1][:-4] + "_fixed_checksum.sav", "wb") as output_stream:
        data.write_sav(output_stream)
