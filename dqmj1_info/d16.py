from dataclasses import dataclass
from typing import IO, List, Literal, Optional, Tuple

import PIL.Image
import PIL.ImageColor

ENDIANESS: Literal["little"] = "little"


@dataclass
class Color16Bit:
    red: int
    green: int
    blue: int

    @staticmethod
    def from_bgr(value: int) -> "Color16Bit":
        if value > 0xFFFF:
            raise ValueError(f"16bit color value is too large: {value}")

        # blue = (value & 0b1111100000000000) >> 11
        # green = (value & 0b0000011111100000) >> 5
        # red = value & 0b0000000000011111

        # Top bit is always set to 1, colors are B5G5R5
        blue = (value & 0b0111110000000000) >> 10
        green = (value & 0b0000001111100000) >> 5
        red = value & 0b0000000000011111

        # print(hex(value), f"{value:b}", blue, green, red, Color16Bit(red=red, green=green, blue=blue).to_32bit_rgb_tuple())

        return Color16Bit(red=red, green=green, blue=blue)

    def to_32bit_rgb_tuple(self) -> Tuple[int, int, int]:
        # https://stackoverflow.com/a/8579650/4764550
        red_8bit = (self.red << 3) | (self.red >> 2)
        green_8bit = (self.green << 3) | (self.green >> 2)
        blue_8bit = (self.blue << 3) | (self.blue >> 2)

        return (red_8bit, green_8bit, blue_8bit)


@dataclass
class D16Image:
    pixels: List[List[Color16Bit]]

    @property
    def width(self) -> int:
        if len(self.pixels) > 0:
            return len(self.pixels[0])
        else:
            return 0

    @property
    def height(self) -> int:
        return len(self.pixels)

    @staticmethod
    def from_d16(input_stream: IO[bytes]) -> Optional["D16Image"]:
        # Magic "D16 " (0x44313600)
        magic = int.from_bytes(input_stream.read(4), "big")
        if magic != 0x44313600:
            return None

        width = int.from_bytes(input_stream.read(2), ENDIANESS)
        height = int.from_bytes(input_stream.read(2), ENDIANESS)

        pixels: List[List[Color16Bit]] = []
        for _ in range(0, height):
            pixels.append([])
            for _ in range(0, width):
                color_value = int.from_bytes(input_stream.read(2), ENDIANESS)

                color = Color16Bit.from_bgr(color_value)
                pixels[-1].append(color)

        return D16Image(pixels=pixels)

    def write_png(self, output_stream: IO[bytes]) -> None:
        image = PIL.Image.new("RGB", (self.width, self.height))
        pixels = image.load()
        assert pixels is not None

        for r, row in enumerate(self.pixels):
            for c, color_16bit in enumerate(row):
                color = color_16bit.to_32bit_rgb_tuple()
                pixels[c, r] = color

        image.save(output_stream)
