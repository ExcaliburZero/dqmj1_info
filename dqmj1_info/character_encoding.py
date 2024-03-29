BYTE_TO_CHAR_MAP = {
    0x00: "0",
    0x01: "1",
    0x02: "2",
    0x03: "3",
    0x04: "4",
    0x05: "5",
    0x06: "6",
    0x07: "7",
    0x08: "8",
    0x09: "9",
    0x0A: " ",
    0x0B: "A",
    0x0C: "B",
    0x0D: "C",
    0x0E: "D",
    0x0F: "E",
    0x10: "F",
    0x11: "G",
    0x12: "H",
    0x13: "I",
    0x14: "J",
    0x15: "K",
    0x16: "L",
    0x17: "M",
    0x18: "N",
    0x19: "O",
    0x1A: "P",
    0x1B: "Q",
    0x1C: "R",
    0x1D: "S",
    0x1E: "T",
    0x1F: "U",
    0x20: "V",
    0x21: "W",
    0x22: "X",
    0x23: "Y",
    0x24: "Z",
    0x25: "a",
    0x26: "b",
    0x27: "c",
    0x28: "d",
    0x29: "e",
    0x2A: "f",
    0x2B: "g",
    0x2C: "h",
    0x2D: "i",
    0x2E: "j",
    0x2F: "k",
    0x30: "l",
    0x31: "m",
    0x32: "n",
    0x33: "o",
    0x34: "p",
    0x35: "q",
    0x36: "r",
    0x37: "s",
    0x38: "t",
    0x39: "u",
    0x3A: "v",
    0x3B: "w",
    0x3C: "x",
    0x3D: "y",
    0x3E: "z",
    0x55: "Ü",
    0x57: "á",
    0x70: "!",
    0x71: "?",
    0x87: "+",
    0x8D: "Ⅱ",
    0x8E: "Ⅲ",
    0x9A: "‘",
    0x9B: "’",
    0xAC: ".",
    0xAD: "&",
    0xCC: "-",
    0xCD: ",",
    0xFE: "\\n",
}

CHAR_TO_BYTE_MAP = {c: b for b, c in BYTE_TO_CHAR_MAP.items()}
