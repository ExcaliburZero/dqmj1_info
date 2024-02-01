from dataclasses import dataclass
from typing import Dict, IO, List, Literal, Optional, Type

import abc

from .extract_strings import byte_to_char

ENDIANESS: Literal["little"] = "little"

STRING_END = 0xFF
STRING_END_PADDING = 0xCC


@dataclass
class RawCommand:
    command_type: int
    data: bytes

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> Optional["RawCommand"]:
        type_bytes = input_stream.read(4)
        if len(type_bytes) != 4:
            return None

        command_type = int.from_bytes(type_bytes, ENDIANESS)
        length = int.from_bytes(input_stream.read(4), ENDIANESS)

        data = input_stream.read(length - 8)

        return RawCommand(command_type=command_type, data=data)


class Command(abc.ABC):
    @property
    def type_id(self) -> int:
        if type(self) in Command.types_by_command():
            return Command.types_by_command()[type(self)]

        assert isinstance(self, UnknownCommand)
        return self.raw.command_type

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> Optional["Command"]:
        raw = RawCommand.from_evt(input_stream)
        if raw is None:
            return None

        commands_by_type = Command.commands_by_type()

        if raw.command_type in commands_by_type:
            return commands_by_type[raw.command_type].from_raw(raw)

        return UnknownCommand(type_hex=hex(raw.command_type), raw=raw)

    @staticmethod
    def from_raw(raw: RawCommand) -> Optional["Command"]:
        raise NotImplemented

    @staticmethod
    def types_by_command() -> Dict[Type["Command"], int]:
        return {
            command_class: type_id
            for type_id, command_class in Command.commands_by_type().items()
        }

    @staticmethod
    def commands_by_type() -> Dict[int, Type["Command"]]:
        return {
            0x15: Command_0x15,
            0x25: StartDialog,
            0x29: ShowDialog,
            0x2A: SpeakerName,
        }


def bytes_to_string(bs: List[int]) -> str:
    chars = []
    for b in bs:
        if b == 0xFF:
            break

        chars.append(byte_to_char(b))

    return "".join(chars)


@dataclass
class Event:
    commands: List[Command]

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Event":
        # Magic
        input_stream.read(8)

        # TODO: figure out how to calculate correct offset
        input_stream.read(0x1010 - 8)
        """while len(input_stream.peek()) > 0:
            next_3_nums = input_stream.peek()[0:4 * 3]

            if next_3_nums == b'\x0C\x00\x00\x00\x0C\x00\x00\x00\x0C\x00\x00\x00':
                input_stream.read(4 * 3)
                break

            input_stream.read(4)

        print(hex(input_stream.tell()))"""

        commands = []
        while True:
            command = Command.from_evt(input_stream)
            if command is None:
                break

            commands.append(command)

        return Event(commands=commands)


@dataclass
class Command_0x15(Command):
    a: int
    b: str
    c: int
    d: str

    @staticmethod
    def from_raw(raw: RawCommand) -> "Command":
        a = int.from_bytes(raw.data[0:4], ENDIANESS)
        b = hex(int.from_bytes(raw.data[4:8], ENDIANESS))
        c = int.from_bytes(raw.data[8:12], ENDIANESS)
        d = hex(int.from_bytes(raw.data[12:16], ENDIANESS))

        return Command_0x15(a, b, c, d)


@dataclass
class SpeakerName(Command):
    name: str

    @staticmethod
    def from_raw(raw: RawCommand) -> "Command":
        name_bytes = []

        # Grab the string
        for b in raw.data:
            name_bytes.append(b)

            if b == STRING_END:
                break

        return SpeakerName(bytes_to_string(name_bytes))


@dataclass
class ShowDialog(Command):
    text: str

    @staticmethod
    def from_raw(raw: RawCommand) -> "Command":
        name_bytes = []

        # Grab the string
        for b in raw.data:
            name_bytes.append(b)

            if b == STRING_END:
                break

        return ShowDialog(bytes_to_string(name_bytes))


@dataclass
class StartDialog(Command):
    @staticmethod
    def from_raw(raw: RawCommand) -> "Command":
        return StartDialog()


@dataclass
class UnknownCommand(Command):
    type_hex: str
    raw: RawCommand
