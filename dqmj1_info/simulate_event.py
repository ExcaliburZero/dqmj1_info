from dataclasses import dataclass
from typing import List

import argparse
import pathlib
import sys

from .character_encoding import CharacterEncoding, CHARACTER_ENCODINGS
from .evt import Event


@dataclass
class EventFrame:
    instruction_ptr: int
    counter: int
    is_running: bool
    instruction_return_value: int


class EventSimulator:
    def __init__(self, event: Event, character_encoding: CharacterEncoding) -> None:
        self.event = event
        self.frames = [
            EventFrame(0x0, 0, True, 0),
            EventFrame(0x0, 0, False, 0),
            EventFrame(0x0, 0, False, 0),
            EventFrame(0x0, 0, False, 0),
        ]
        self.character_encoding = character_encoding

    def step(self) -> None:
        for i in range(0, 4):
            print(f"[frame={i}]")
            cur_frame = self.frames[i]
            if not cur_frame.is_running:
                continue

            while True:
                self.run_instruction(cur_frame)

                if cur_frame.instruction_return_value != 0:
                    break

    def run_instruction(self, frame: EventFrame) -> None:
        current_instruction = self.event.get_instruction_at_ptr(
            frame.instruction_ptr, self.character_encoding
        )
        if current_instruction is None:
            raise Exception(
                f"Could not find a instruction at pointer: 0x{frame.instruction_ptr:04x}"
            )

        print(f"  (0x{frame.instruction_ptr:04x}) 0x{current_instruction.type_id:02x}")

        if current_instruction.type_id == 0x00:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x0A:
            self.activate_next_frame(current_instruction.arguments[0])
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x0B:
            # TODO: not accurate
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x0C:
            print(f"    Jump to 0x{current_instruction.arguments[0]:x}")
            frame.instruction_ptr = current_instruction.arguments[0]
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x15:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x2B:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x2E:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x2F:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 1
        elif current_instruction.type_id == 0x48:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x49:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x86:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x87:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x89:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x92:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x91:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x98:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x99:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x9B:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0x9A:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0xD4:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        elif current_instruction.type_id == 0xD5:
            frame.instruction_ptr += current_instruction.length(self.character_encoding)
            frame.instruction_return_value = 0
        else:
            raise NotImplementedError(
                f"instruction: 0x{current_instruction.type_id:02x}"
            )
            frame.instruction_ptr += current_instruction.length
            frame.instruction_return_value = 0

    def activate_next_frame(self, instruction_pointer: int) -> None:
        next_frame = None
        for i, frame in enumerate(self.frames):
            if not frame.is_running:
                next_frame = frame
                break

        assert next_frame is not None

        print(f"    Activated frame {i}")

        next_frame.instruction_ptr = instruction_pointer
        next_frame.is_running = True


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--evt_filepath", required=True, type=pathlib.Path)
    parser.add_argument("--character_encoding", required=True)

    args = parser.parse_args(argv)

    character_encoding = CHARACTER_ENCODINGS[args.character_encoding]

    with open(args.evt_filepath, "rb") as input_stream:
        event = Event.from_evt(input_stream, character_encoding)

    simulator = EventSimulator(event, character_encoding)
    for _ in range(0, 100):
        simulator.step()


def main_without_args() -> None:
    main(sys.argv[1:])
