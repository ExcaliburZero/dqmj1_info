from dataclasses import dataclass
from typing import Any, Dict, IO, List, Literal, Optional, Type, Union

import enum

from .extract_strings import byte_to_char

ENDIANESS: Literal["little"] = "little"

STRING_END = 0xFF
STRING_END_PADDING = 0xCC


class ArgumentType(enum.Enum):
    U32 = enum.auto()
    String = enum.auto()
    Bytes = enum.auto()


at = ArgumentType


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


@dataclass
class CommandType:
    type_id: int
    name: str
    arguments: List[ArgumentType]


COMMAND_TYPES = [
    CommandType(0x15, "Cmd_0x15", [at.U32, at.U32, at.U32, at.U32]),
    CommandType(0x25, "StartDialog", []),
    CommandType(0x29, "ShowDialog", [at.String]),
    CommandType(0x2A, "SpeakerName", [at.String]),
    CommandType(0xE9, "ShowCreditsText", [at.String]),
]


@dataclass
class Command:
    command_type: CommandType
    arguments: List[Any]

    @property
    def type_id(self) -> int:
        return self.command_type.type_id

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> Optional["Command"]:
        raw = RawCommand.from_evt(input_stream)
        if raw is None:
            return None

        commands_by_type = Command.commands_by_type_id()

        if raw.command_type in commands_by_type:
            return Command.from_raw(raw, commands_by_type[raw.command_type])

        return Command.from_raw(
            raw=raw, command_type=CommandType(raw.command_type, "UNKNOWN", [at.Bytes])
        )

    @staticmethod
    def from_raw(raw: RawCommand, command_type: CommandType) -> Optional["Command"]:
        arguments: List[Any] = []

        current = 0
        for argument_type in command_type.arguments:
            if argument_type == at.Bytes:
                arguments.append(raw.data[current:])
                current = len(raw.data)
            elif argument_type == at.String:
                string = bytes_to_string(raw.data[current:])

                arguments.append(string)
                current = len(raw.data)
            elif argument_type == at.U32:
                value = int.from_bytes(raw.data[current : current + 4], ENDIANESS)

                arguments.append(value)
                current += 4

        return Command(command_type=command_type, arguments=arguments)

    def to_script(self) -> str:
        start = f"{self.command_type.name} (0x{self.command_type.type_id:02x})"
        end = ""
        if len(self.arguments) > 0:
            end = " " + " ".join(
                (
                    Command.value_to_script_literal(a, t)
                    for a, t in zip(self.arguments, self.command_type.arguments)
                )
            )

        return start + end

    @staticmethod
    def value_to_script_literal(value: Any, value_type: ArgumentType) -> str:
        if value_type == at.U32:
            return hex(value)
        elif value_type == at.Bytes:
            return 'b"' + "".join([f"\\x{b:02x}" for b in value]) + '"'

        return repr(value)

    @staticmethod
    def commands_by_type_id() -> Dict[int, CommandType]:
        return {cmd_type.type_id: cmd_type for cmd_type in COMMAND_TYPES}


def bytes_to_string(bs: Union[List[int], bytes]) -> str:
    chars = []
    for b in bs:
        if b == 0xFF:
            break

        chars.append(byte_to_char(b))

    return "".join(chars)


@dataclass
class Event:
    commands: List[Command]
    data: bytes

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Event":
        input_stream.read(4)
        data = input_stream.read(0x1010 - 4)

        commands = []
        while True:
            command = Command.from_evt(input_stream)
            if command is None:
                break

            commands.append(command)

        return Event(commands=commands, data=data)

    def write_script(self, output_stream: IO[str]) -> None:
        output_stream.write("DATA ")
        output_stream.write(repr(self.data))
        output_stream.write("\n")
        for command in self.commands:
            print(command.to_script(), file=output_stream, flush=False)
