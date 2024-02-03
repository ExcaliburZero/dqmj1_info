from dataclasses import dataclass
from typing import Any, Dict, IO, List, Literal, Optional, Type, Union

import enum
import re

from .extract_strings import byte_to_char, get_string_chars, char_to_byte

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

        return Command.from_raw(
            raw=raw, command_type=Command.get_command_type(raw.command_type)
        )

    @staticmethod
    def get_command_type(command_id: int) -> CommandType:
        commands_by_type = Command.commands_by_type_id()
        if command_id in commands_by_type:
            return commands_by_type[command_id]

        return CommandType(command_id, "UNKNOWN", [at.Bytes])

    def write_evt(self, output_stream: IO[bytes]) -> None:
        command_id_bytes = self.type_id.to_bytes(4, ENDIANESS)

        data = []
        for argument, argument_type in zip(self.arguments, self.command_type.arguments):
            if argument_type == at.Bytes:
                for b in argument:
                    data.append(b)
            elif argument_type == at.U32:
                for b in argument.to_bytes(4, ENDIANESS):
                    data.append(b)
            elif argument_type == at.String:
                string_bytes = string_to_bytes(argument)
                for b in string_bytes:
                    data.append(b)

                num_padding_bytes = (
                    0 if len(string_bytes) % 4 == 0 else 4 - len(string_bytes) % 4
                )
                for _ in range(0, num_padding_bytes):
                    data.append(0xCC)

        length = len(data) + 8
        length_bytes = length.to_bytes(4, ENDIANESS)

        data_bytes = bytearray(data)

        output_stream.write(command_id_bytes)
        output_stream.write(length_bytes)
        output_stream.write(data_bytes)

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

    @staticmethod
    def from_script(line: str) -> Optional["Command"]:
        # Split on spaces, but ignore spaces in quotes
        # https://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python
        PATTERN = re.compile(r"""((?:[^ "']|"[^"]*"|'[^']*')+)""")

        parts = PATTERN.split(line.strip())
        parts = [p for p in parts if len(p.strip()) > 0]

        command_id = eval(parts[1])
        command_type = Command.get_command_type(command_id)

        arguments = []
        for i, _ in enumerate(command_type.arguments):
            arguments.append(eval(parts[i + 2]))

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
            return bytes_repr(value)

        return repr(value)

    @staticmethod
    def commands_by_type_id() -> Dict[int, CommandType]:
        return {cmd_type.type_id: cmd_type for cmd_type in COMMAND_TYPES}


def bytes_repr(bs: bytes) -> str:
    return 'b"' + "".join([f"\\x{b:02x}" for b in bs]) + '"'


def string_to_bytes(string: str) -> bytes:
    individual_bytes = []
    for c in get_string_chars(string):
        individual_bytes.append(char_to_byte(c))

    individual_bytes.append(0xFF)

    return bytes(individual_bytes)


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

    @staticmethod
    def from_script(input_stream: IO[str]) -> "Event":
        data: Optional[Any] = None
        commands: List[Command] = []
        for line in input_stream:
            if data is None:
                assert line.startswith('DATA b"')

                data = eval(line[len("DATA ") :])
                continue

            command = Command.from_script(line)
            assert command is not None

            commands.append(command)

        assert data is not None
        assert isinstance(data, bytes)

        return Event(data=data, commands=commands)

    def write_script(self, output_stream: IO[str]) -> None:
        output_stream.write("DATA ")
        output_stream.write(bytes_repr(self.data))
        output_stream.write("\n")
        for command in self.commands:
            print(command.to_script(), file=output_stream, flush=False)

    def write_evt(self, output_stream: IO[bytes]) -> None:
        output_stream.write(b"\x53\x43\x52\x00")
        output_stream.write(self.data)
        for command in self.commands:
            command.write_evt(output_stream)
