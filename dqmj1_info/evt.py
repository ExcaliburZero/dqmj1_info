from dataclasses import dataclass
from typing import Any, Dict, IO, List, Literal, Optional, Set, Tuple, Union

import abc
import collections
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

LabelDict = Dict[str, int]


class ArgumentType(enum.Enum):
    U32 = enum.auto()
    String = enum.auto()
    AsciiString = enum.auto()
    Bytes = enum.auto()
    ValueLocation = enum.auto()
    InstructionLocation = enum.auto()


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
class RawInstruction:
    instruction_type: int
    data: bytes

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> Optional["RawInstruction"]:
        type_bytes = input_stream.read(4)
        if len(type_bytes) != 4:
            return None

        instruction_type = int.from_bytes(type_bytes, ENDIANESS)
        length = int.from_bytes(input_stream.read(4), ENDIANESS)

        data = input_stream.read(length - 8)

        return RawInstruction(instruction_type=instruction_type, data=data)


@dataclass
class InstructionType:
    type_id: int
    name: str
    arguments: List[ArgumentType]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "InstructionType":
        type_id = int(d["Id"][2:], 16)
        name = d["Name"]
        arguments = [
            ArgumentType[arg.strip()]
            for arg in d["Arguments"][1:-1].split(",")
            if arg.strip() != ""
        ]

        return InstructionType(
            type_id=type_id,
            name=name,
            arguments=arguments,
        )


# Load the instruction type info from csv file
CURRENT_DIRECTORY = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
with open(CURRENT_DIRECTORY / "data" / "event_instructions.csv", "r") as input_stream:
    reader = csv.DictReader(input_stream)
    COMMAND_TYPES = [InstructionType.from_dict(line) for line in reader]


@dataclass
class Instruction:
    instruction_type: InstructionType
    arguments: List[Any]

    @property
    def type_id(self) -> int:
        return self.instruction_type.type_id

    @property
    def length(self) -> int:
        stream = io.BytesIO()
        self.write_evt(stream, collections.defaultdict(lambda: 0))

        return len(stream.getbuffer())

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> Optional[Tuple["Instruction", LabelDict]]:
        raw = RawInstruction.from_evt(input_stream)
        if raw is None:
            return None

        return Instruction.from_raw(
            raw=raw,
            instruction_type=Instruction.get_instruction_type(raw.instruction_type),
        )

    @staticmethod
    def get_instruction_type(instruction_id: int) -> InstructionType:
        instructions_by_type = Instruction.instructions_by_type_id()
        if instruction_id in instructions_by_type:
            return instructions_by_type[instruction_id]

        return InstructionType(instruction_id, "UNKNOWN", [at.Bytes])

    def write_evt(self, output_stream: IO[bytes], labels: LabelDict) -> None:
        instruction_id_bytes = self.type_id.to_bytes(4, ENDIANESS)

        data = []
        for argument, argument_type in zip(
            self.arguments, self.instruction_type.arguments
        ):
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
            elif argument_type == at.InstructionLocation:
                assert isinstance(argument, str)
                position = labels[argument]

                for b in position.to_bytes(4, ENDIANESS):
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

        output_stream.write(instruction_id_bytes)
        output_stream.write(length_bytes)
        output_stream.write(data_bytes)

    @staticmethod
    def from_raw(
        raw: RawInstruction, instruction_type: InstructionType
    ) -> Optional[Tuple["Instruction", LabelDict]]:
        arguments: List[Any] = []

        labels = {}

        current = 0
        for argument_type in instruction_type.arguments:
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
            elif argument_type == at.InstructionLocation:
                value = int.from_bytes(raw.data[current : current + 4], ENDIANESS)

                label = f"0x{value:x}"
                labels[label] = value

                arguments.append(label)
                current += 4
            else:
                assert False, f"Unhandled arg type: {argument_type}"

        return (
            Instruction(instruction_type=instruction_type, arguments=arguments),
            labels,
        )

    @staticmethod
    def from_script(line: str) -> Optional["Instruction"]:
        # Split on spaces, but ignore spaces in quotes
        # https://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python
        PATTERN = re.compile(r"""((?:[^ "']|"[^"]*"|'[^']*')+)""")

        parts = PATTERN.split(line.strip())
        parts = [p for p in parts if len(p.strip()) > 0]

        instruction_id = eval(parts[0])
        instruction_type = Instruction.get_instruction_type(instruction_id)

        arguments = []
        for i, _ in enumerate(instruction_type.arguments):
            arguments.append(eval(parts[i + 2]))

        return Instruction(instruction_type=instruction_type, arguments=arguments)

    def to_script(self) -> str:
        instruction_id_reversed_endian = int.from_bytes(
            self.instruction_type.type_id.to_bytes(4, ENDIANESS), "big"
        )
        start = f"(0x{instruction_id_reversed_endian:08X}) {self.instruction_type.name}"
        end = ""
        if len(self.arguments) > 0:
            end = " " + " ".join(
                (
                    Instruction.value_to_script_literal(a, t)
                    for i, (a, t) in enumerate(
                        zip(self.arguments, self.instruction_type.arguments)
                    )
                )
            )

        return start + end

    @staticmethod
    def value_to_script_literal(
        value: Any,
        value_type: ArgumentType,
    ) -> str:
        if value_type == at.U32:
            return hex(value)
        elif value_type == at.Bytes:
            return bytes_repr(value)
        elif value_type == at.ValueLocation:
            assert isinstance(value, ValueLocation)
            return value.to_script()
        elif value_type == at.InstructionLocation:
            return str(value)

        return repr(value)

    @staticmethod
    def instructions_by_type_id() -> Dict[int, InstructionType]:
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
    instructions: List[Instruction]
    data: bytes
    labels: LabelDict

    @property
    def labels_by_position(self) -> Dict[int, str]:
        return {pos: label for label, pos in self.labels.items()}

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Event":
        input_stream.read(4)
        data = input_stream.read(0x1004 - 4)

        instructions = []
        labels = {}
        while True:
            result = Instruction.from_evt(input_stream)
            if result is None:
                break

            instruction, new_labels = result
            instructions.append(instruction)
            labels.update(new_labels)

        return Event(instructions=instructions, data=data, labels=labels)

    @staticmethod
    def from_script(input_stream: IO[str]) -> "Event":
        data: Optional[Any] = None
        instructions: List[Instruction] = []
        for line in input_stream:
            if data is None:
                assert line.startswith('DATA b"')

                data = eval(line[len("DATA ") :])
                continue

            instruction = Instruction.from_script(line)
            assert instruction is not None

            instructions.append(instruction)

        assert data is not None
        assert isinstance(data, bytes)

        raise NotImplementedError()
        return Event(data=data, instructions=instructions, labels={})

    def write_script(self, output_stream: IO[str]) -> None:
        output_stream.write("DATA ")
        output_stream.write(bytes_repr(self.data))
        output_stream.write("\n")

        labels_by_position = self.labels_by_position

        position = 0x0
        for instruction in self.instructions:
            if position in labels_by_position:
                label = labels_by_position[position]
                print(f".{label}:", file=output_stream, flush=False)

            print(
                "    " + instruction.to_script(),
                file=output_stream,
                flush=False,
            )
            position += instruction.length

    def write_evt(self, output_stream: IO[bytes]) -> None:
        output_stream.write(b"\x53\x43\x52\x00")
        output_stream.write(self.data)
        for instruction in self.instructions:
            instruction.write_evt(output_stream, self.labels)

    def get_instruction_at_ptr(self, pointer: int) -> Optional[Instruction]:
        start = 0x1004
        offsetted_pointer = pointer + start

        current_location = start
        for instruction in self.instructions:
            if current_location == offsetted_pointer:
                return instruction

            current_location += instruction.length

        return None
