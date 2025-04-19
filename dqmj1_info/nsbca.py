from dataclasses import dataclass, asdict
from typing import IO, List, Literal

import argparse
import io
import json
import sys

ENDIANESS: Literal["little"] = "little"


def read_int(input_stream: IO[bytes], size: int) -> int:
    return int.from_bytes(input_stream.read(size), ENDIANESS)


def read_ints(input_stream: IO[bytes], size: int, count: int) -> List[int]:
    return [int.from_bytes(input_stream.read(size), ENDIANESS) for _ in range(0, count)]


def read_ascii(input_stream: IO[bytes], size: int) -> str:
    return input_stream.read(size).decode("ascii")


def read_asciis(input_stream: IO[bytes], size: int, count: int) -> List[str]:
    return [input_stream.read(size).decode("ascii") for _ in range(0, count)]


def trim_ascii(string: str) -> str:
    return string.replace(b"\x00".decode("ascii"), "")


@dataclass
class NitroHeader:
    header_id: str
    magic: int
    file_size: int
    header_size: int
    num_sections: int
    section_offsets: List[int]

    @staticmethod
    def from_bytes(input_stream: IO[bytes]) -> "NitroHeader":
        header_id = read_ascii(input_stream, 4)
        magic = read_int(input_stream, 4)
        file_size = read_int(input_stream, 4)
        header_size = read_int(input_stream, 2)
        num_sections = read_int(input_stream, 2)
        section_offsets = [read_int(input_stream, 4) for _ in range(0, num_sections)]
        return NitroHeader(
            header_id=header_id,
            magic=magic,
            file_size=file_size,
            header_size=header_size,
            num_sections=num_sections,
            section_offsets=section_offsets,
        )


@dataclass
class UnknownBlock:
    header_size: int
    section_size: int
    constant: int
    unknown_1: List[int]
    unknown_2: List[int]

    @staticmethod
    def from_bytes(input_stream: IO[bytes], num_objects: int) -> "UnknownBlock":
        header_size = read_int(input_stream, 2)
        section_size = read_int(input_stream, 2)
        constant = read_int(input_stream, 4)

        unknown_1 = []
        unknown_2 = []
        for _ in range(0, num_objects):
            unknown_1.append(read_int(input_stream, 2))
            unknown_2.append(read_int(input_stream, 2))

        return UnknownBlock(
            header_size=header_size,
            section_size=section_size,
            constant=constant,
            unknown_1=unknown_1,
            unknown_2=unknown_2,
        )


@dataclass
class InfoBlock:
    header_size: int
    data_size: int
    offsets: List[int]

    @staticmethod
    def from_bytes(input_stream: IO[bytes], num_objects: int) -> "InfoBlock":
        header_size = read_int(input_stream, 2)
        data_size = read_int(input_stream, 2)

        offsets = read_ints(input_stream, 4, num_objects)

        return InfoBlock(header_size=header_size, data_size=data_size, offsets=offsets)


@dataclass
class ObjectInfo:
    flag: int
    unknown_1: int
    id: int


@dataclass
class Jac:
    num_frames: int
    num_objects: int
    unknown_1: int
    offset_1: int
    offset_2: int
    object_info_offsets: List[int]
    objects_info: List[ObjectInfo]

    @staticmethod
    def from_bytes(input_stream: io.BytesIO) -> "Jac":
        jac_id = read_ascii(input_stream, 4)
        assert jac_id == "J" + b"\x00".decode("ascii") + "AC"

        num_frames = read_int(input_stream, 2)
        num_objects = read_int(input_stream, 2)
        unknown_1 = read_int(input_stream, 4)
        offset_1 = read_int(input_stream, 4)
        offset_2 = read_int(input_stream, 4)

        # TODO: Joint data

        object_info_offsets = read_ints(input_stream, 2, num_objects)

        # TODO: Loop over object numbers
        objects_info = []
        for _ in range(0, 1):
            flag = read_int(input_stream, 2)
            object_unknown_1 = read_int(input_stream, 1)
            object_id = read_int(input_stream, 1)

            if ((flag >> 1) & 1) == 0:
                for k in range(0, 3):
                    # TODO: finish implementing
                    t_flag = None

            objects_info.append(
                ObjectInfo(flag=flag, unknown_1=object_unknown_1, id=object_id)
            )

        return Jac(
            num_frames=num_frames,
            num_objects=num_objects,
            unknown_1=unknown_1,
            offset_1=offset_1,
            offset_2=offset_2,
            object_info_offsets=object_info_offsets,
            objects_info=objects_info,
        )


@dataclass
class Jnt0:
    size: int
    dummy: int
    num_objects: int
    section_size: int
    unkown_block: UnknownBlock
    info_block: InfoBlock
    object_names: List[str]
    jacs: List[Jac]

    @staticmethod
    def from_bytes(input_stream: io.BytesIO) -> "Jnt0":
        size = read_int(input_stream, 4)
        dummy = read_int(input_stream, 1)
        num_objects = read_int(input_stream, 1)
        section_size = read_int(input_stream, 2)

        unknown_block = UnknownBlock.from_bytes(input_stream, num_objects)
        info_block = InfoBlock.from_bytes(input_stream, num_objects)

        object_names = [
            trim_ascii(s) for s in read_asciis(input_stream, 16, num_objects)
        ]

        # TODO: Loop over each object number
        jacs = [Jac.from_bytes(input_stream)]

        return Jnt0(
            size=size,
            dummy=dummy,
            num_objects=num_objects,
            section_size=section_size,
            unkown_block=unknown_block,
            info_block=info_block,
            object_names=object_names,
            jacs=jacs,
        )


@dataclass
class Nsbca:
    nitro_header: NitroHeader
    jnt0: Jnt0

    @staticmethod
    def from_nsbca(input_stream: IO[bytes]) -> "Nsbca":
        input_stream = io.BytesIO(input_stream.read())

        nitro_header = NitroHeader.from_bytes(input_stream)
        assert nitro_header.header_id == "BCA0"

        jnt0_id = read_ascii(input_stream, 4)
        assert jnt0_id == "JNT0"

        jnt0 = Jnt0.from_bytes(input_stream)

        return Nsbca(nitro_header=nitro_header, jnt0=jnt0)


def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_nsbca", required=True)

    args = parser.parse_args(argv)

    with open(args.input_nsbca, "rb") as input_stream:
        nsbca = Nsbca.from_nsbca(input_stream)

    print(json.dumps(asdict(nsbca), indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
