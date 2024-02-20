from dataclasses import dataclass
from typing import IO, Literal, Optional, OrderedDict

import collections

ENDIANESS: Literal["little"] = "little"
FPK_MAGIC = b"\x46\x50\x4B\x00"


@dataclass(frozen=True)
class FileDescription:
    name: str
    extension: str


@dataclass(frozen=True)
class Fpk:
    files: OrderedDict[FileDescription, bytes]

    @staticmethod
    def from_bin(input_stream: IO[bytes]) -> Optional["Fpk"]:
        magic = input_stream.read(4)
        if magic != FPK_MAGIC:
            return None

        num_files = int.from_bytes(input_stream.read(4), ENDIANESS)
        file_info = []
        for _ in range(0, num_files):
            name_info = input_stream.read(0x20)
            offset = int.from_bytes(input_stream.read(4), ENDIANESS)
            size = int.from_bytes(input_stream.read(4), ENDIANESS)

            file_info.append((name_info, offset, size))

        # Note: Parsing in two parts to avoid moving the file handle pointer back and forth

        files = collections.OrderedDict()
        for name_info, offset, size in file_info:
            name_info_parts = name_info.split(b"\x00")
            file_name = name_info_parts[0]
            file_extension = name_info_parts[1]

            file_description = FileDescription(
                name=file_name.decode("utf8"), extension=file_extension.decode("utf8")
            )

            input_stream.seek(offset)
            contents = input_stream.read(size)

            files[file_description] = contents

        return Fpk(files=files)
