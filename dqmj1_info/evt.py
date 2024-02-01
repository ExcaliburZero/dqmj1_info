from dataclasses import dataclass
from typing import IO, List, Optional

import abc

import extract_strings

ENDIANESS = "little"

STRING_END = 0xFF
STRING_END_PADDING = 0xCC


class Command(abc.ABC):
    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> Optional["Command"]:
        type_bytes = input_stream.read(4)
        if len(type_bytes) != 4:
            return None

        command_type = int.from_bytes(type_bytes, ENDIANESS)

        if command_type == 0x2A:
            return SpeakerName.from_evt(input_stream)
        if command_type == 0x29:
            return ShowDialog.from_evt(input_stream)

        return UnknownCommand(command_type)


def bytes_to_string(bs: List[int]) -> str:
    chars = []
    for b in bs:
        if b == 0xFF:
            break

        chars.append(extract_strings.byte_to_char(b))

    return "".join(chars)


@dataclass
class Event:
    commands: List[Command]

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Event":
        # Magic
        input_stream.read(4)

        commands = []
        while True:
            command = Command.from_evt(input_stream)
            if command is None:
                break

            commands.append(command)

        return Event(commands=commands)


@dataclass
class SpeakerName(Command):
    name: str

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Command":
        name_bytes = []
        input_stream.read(4)

        # Grab the string
        while True:
            b = input_stream.read(1)
            if len(b) == 0:
                return SpeakerName("")

            b = int.from_bytes(b)

            name_bytes.append(b)

            if b == STRING_END:
                break

        # Move the read pointer past the padding
        while True:
            b = input_stream.peek(1)
            if len(b) == 0:
                return SpeakerName("")

            b = b[0]

            if b == STRING_END_PADDING:
                input_stream.read(1)
            else:
                break

        return SpeakerName(bytes_to_string(name_bytes))


@dataclass
class ShowDialog(Command):
    text: str

    @staticmethod
    def from_evt(input_stream: IO[bytes]) -> "Command":
        name_bytes = []
        input_stream.read(4)

        # Grab the string
        while True:
            b = input_stream.read(1)
            if len(b) == 0:
                return ShowDialog("")

            b = int.from_bytes(b)

            name_bytes.append(b)

            if b == STRING_END:
                break

        # Move the read pointer past the padding
        while True:
            b = input_stream.peek(1)
            if len(b) == 0:
                return ShowDialog("")

            b = b[0]

            if b == STRING_END_PADDING:
                input_stream.read(1)
            else:
                break

        return ShowDialog(bytes_to_string(name_bytes))


@dataclass
class UnknownCommand(Command):
    command_type: int
