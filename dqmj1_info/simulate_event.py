from dataclasses import dataclass
from typing import List

import argparse
import pathlib
import sys

from .evt import Event


@dataclass
class EventFrame:
    command_ptr: int
    counter: int
    is_running: bool
    command_return_value: int


class EventSimulator:
    def __init__(self, event: Event) -> None:
        self.event = event
        self.frames = [
            EventFrame(0x0, 0, True, 0),
            EventFrame(0x0, 0, False, 0),
            EventFrame(0x0, 0, False, 0),
            EventFrame(0x0, 0, False, 0),
        ]

    def step(self) -> None:
        for i in range(0, 4):
            print(f"[frame={i}]")
            cur_frame = self.frames[i]
            if not cur_frame.is_running:
                continue

            while True:
                self.run_command(cur_frame)

                if cur_frame.command_return_value != 0:
                    break

    def run_command(self, frame: EventFrame) -> None:
        current_command = self.event.get_command_at_ptr(frame.command_ptr)
        if current_command is None:
            raise Exception(
                f"Could not find a command at pointer: 0x{frame.command_ptr:04x}"
            )

        print(f"  (0x{frame.command_ptr:04x}) 0x{current_command.type_id:02x}")

        if current_command.type_id == 0x00:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x0A:
            self.activate_next_frame(current_command.arguments[0])
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x0B:
            # TODO: not accurate
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x0C:
            print(f"    Jump to 0x{current_command.arguments[0]:x}")
            frame.command_ptr = current_command.arguments[0]
            frame.command_return_value = 0
        elif current_command.type_id == 0x15:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x2B:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x2E:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x2F:
            frame.command_ptr += current_command.length
            frame.command_return_value = 1
        elif current_command.type_id == 0x48:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x49:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x86:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x87:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x89:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x92:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x91:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x98:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x99:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x9B:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0x9A:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0xD4:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        elif current_command.type_id == 0xD5:
            frame.command_ptr += current_command.length
            frame.command_return_value = 0
        else:
            raise NotImplementedError(f"command: 0x{current_command.type_id:02x}")
            frame.command_ptr += current_command.length
            frame.command_return_value = 0

    def activate_next_frame(self, command_pointer: int) -> None:
        next_frame = None
        for i, frame in enumerate(self.frames):
            if not frame.is_running:
                next_frame = frame
                break

        assert next_frame is not None

        print(f"    Activated frame {i}")

        next_frame.command_ptr = command_pointer
        next_frame.is_running = True


def main(argv: List[str]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--evt_filepath", required=True, type=pathlib.Path)

    args = parser.parse_args(argv)

    with open(args.evt_filepath, "rb") as input_stream:
        event = Event.from_evt(input_stream)

    simulator = EventSimulator(event)
    for _ in range(0, 100):
        simulator.step()


def main_without_args() -> None:
    main(sys.argv[1:])
