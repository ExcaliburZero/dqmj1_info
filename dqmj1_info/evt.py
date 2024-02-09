from dataclasses import dataclass
from typing import Any, Dict, IO, List, Literal, Optional, Set, Union

import csv
import enum
import io
import itertools
import os
import pathlib
import re

from .extract_strings import byte_to_char, get_string_chars, char_to_byte

ENDIANESS: Literal["little"] = "little"

STRING_END = 0xFF
STRING_END_PADDING = 0xCC


class ArgumentType(enum.Enum):
    U32 = enum.auto()
    String = enum.auto()
    AsciiString = enum.auto()
    Bytes = enum.auto()
    ValueLocation = enum.auto()


class ValueLocation(enum.Enum):
    Zero = 0
    One = 1
    Constant = 2
    Three = 3

    def to_script(self) -> str:
        if self == ValueLocation.Zero:
            return "Pool_0"
        elif self == ValueLocation.One:
            return "Pool_1"
        elif self == ValueLocation.Constant:
            return "Const"
        elif self == ValueLocation.Three:
            return "Pool_3"


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
    label_argument: Optional[int]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CommandType":
        type_id = int(d["Id"][2:], 16)
        name = d["Name"]
        arguments = [
            ArgumentType[arg.strip()]
            for arg in d["Arguments"][1:-1].split(",")
            if arg.strip() != ""
        ]

        return CommandType(
            type_id=type_id,
            name=name,
            arguments=arguments,
            label_argument=(
                int(d["Label Argument"]) if d["Label Argument"] != "" else None
            ),
        )


# Load the command type info from csv file
CURRENT_DIRECTORY = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
with open(CURRENT_DIRECTORY / "data" / "event_commands.csv", "r") as input_stream:
    reader = csv.DictReader(input_stream)
    COMMAND_TYPES = [CommandType.from_dict(line) for line in reader]


@dataclass
class Command:
    command_type: CommandType
    arguments: List[Any]

    @property
    def type_id(self) -> int:
        return self.command_type.type_id

    @property
    def length(self) -> int:
        stream = io.BytesIO()
        self.write_evt(stream)

        return len(stream.getbuffer())

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

        return CommandType(command_id, "UNKNOWN", [at.Bytes], None)

    def write_evt(self, output_stream: IO[bytes]) -> None:
        command_id_bytes = self.type_id.to_bytes(4, ENDIANESS)

        data = []
        for argument, argument_type in zip(self.arguments, self.command_type.arguments):
            if argument_type == at.Bytes:
                for b in argument:
                    data.append(b)
            elif argument_type == at.AsciiString:
                for c in argument:
                    data.append(ord(c))
                data.append(0x00)
            elif argument_type == at.U32:
                for b in argument.to_bytes(4, ENDIANESS):
                    data.append(b)
            elif argument_type == at.ValueLocation:
                assert isinstance(argument, ValueLocation)
                for b in argument.value.to_bytes(4, ENDIANESS):
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
            else:
                raise NotImplementedError(f"{argument_type}")

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
                current += len(raw.data)
            elif argument_type == at.AsciiString:
                string_bytes = raw.data[current:]
                string_character_bytes = []
                for b in string_bytes:
                    if b == 0x00:
                        break

                    string_character_bytes.append(b)

                arguments.append("".join((chr(b) for b in string_character_bytes)))
                current += len(string_bytes)
            elif argument_type == at.String:
                string = bytes_to_string(raw.data[current:])

                arguments.append(string)
                current += len(raw.data)
            elif argument_type == at.U32:
                value = int.from_bytes(raw.data[current : current + 4], ENDIANESS)

                arguments.append(value)
                current += 4
            elif argument_type == at.ValueLocation:
                value = int.from_bytes(raw.data[current : current + 4], ENDIANESS)

                arguments.append(ValueLocation(value))
                current += 4
            else:
                assert False, f"Unhandled arg type: {argument_type}"

        return Command(command_type=command_type, arguments=arguments)

    @staticmethod
    def from_script(line: str) -> Optional["Command"]:
        # Split on spaces, but ignore spaces in quotes
        # https://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python
        PATTERN = re.compile(r"""((?:[^ "']|"[^"]*"|'[^']*')+)""")

        parts = PATTERN.split(line.strip())
        parts = [p for p in parts if len(p.strip()) > 0]

        command_id = eval(parts[0])
        command_type = Command.get_command_type(command_id)

        arguments = []
        for i, _ in enumerate(command_type.arguments):
            arguments.append(eval(parts[i + 2]))

        return Command(command_type=command_type, arguments=arguments)

    def to_script(self, labels_by_position: Optional[Dict[int, str]]) -> str:
        command_id_reversed_endian = int.from_bytes(
            self.command_type.type_id.to_bytes(4, ENDIANESS), "big"
        )
        start = f"(0x{command_id_reversed_endian:08X}) {self.command_type.name}"
        end = ""
        if len(self.arguments) > 0:
            end = " " + " ".join(
                (
                    Command.value_to_script_literal(
                        a, t, self.command_type.label_argument == i, labels_by_position
                    )
                    for i, (a, t) in enumerate(
                        zip(self.arguments, self.command_type.arguments)
                    )
                )
            )

        return start + end

    @staticmethod
    def value_to_script_literal(
        value: Any,
        value_type: ArgumentType,
        is_label_argument: bool,
        labels_by_position: Optional[Dict[int, str]],
    ) -> str:
        if is_label_argument and labels_by_position is not None:
            assert value_type == at.U32
            assert isinstance(value, int)

            return labels_by_position[value]

        if value_type == at.U32:
            return hex(value)
        elif value_type == at.Bytes:
            return bytes_repr(value)
        elif value_type == at.ValueLocation:
            assert isinstance(value, ValueLocation)
            return value.to_script()

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

    @property
    def labels(self) -> Dict[str, int]:
        jump_destinations: Set[int] = set()
        for command in self.commands:
            label_argument_index = command.command_type.label_argument
            if label_argument_index is None:
                continue

            destination = command.arguments[label_argument_index]
            jump_destinations.add(destination)

        label_names = Event.create_label_names(len(jump_destinations))

        return {
            label_names[i]: dest for i, dest in enumerate(sorted(jump_destinations))
        }

    @property
    def labels_by_position(self) -> Dict[int, str]:
        return {pos: label for label, pos in self.labels.items()}

    @staticmethod
    def create_label_names(num_labels: int) -> List[str]:
        # https://stackoverflow.com/questions/58172537/generator-for-a-b-aa-ab-ba-bb-aaa-aab
        return list(
            "".join(l)
            for l in itertools.chain.from_iterable(
                itertools.product(
                    "".join((chr(c + ord("a")) for c in range(0, 26))), repeat=i
                )
                for i in range(1, 4)
            )
        )

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Event":
        input_stream.read(4)
        data = input_stream.read(0x1004 - 4)

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

        labels_by_position = self.labels_by_position

        position = 0x0
        for command in self.commands:
            if position in labels_by_position:
                label = labels_by_position[position]
                print(f".{label}:", file=output_stream, flush=False)

            print(
                "    " + command.to_script(labels_by_position),
                file=output_stream,
                flush=False,
            )
            position += command.length

    def write_evt(self, output_stream: IO[bytes]) -> None:
        output_stream.write(b"\x53\x43\x52\x00")
        output_stream.write(self.data)
        for command in self.commands:
            command.write_evt(output_stream)

    def get_command_at_ptr(self, pointer: int) -> Optional[Command]:
        start = 0x1004
        offsetted_pointer = pointer + start

        current_location = start
        for command in self.commands:
            if current_location == offsetted_pointer:
                return command

            current_location += command.length

        return None
