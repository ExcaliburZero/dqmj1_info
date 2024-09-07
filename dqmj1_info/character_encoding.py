from typing import List, Tuple, Union

BYTE_TO_CHAR_MAP_NA_AND_EU = {
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

BYTE_TO_CHAR_MAP = [
    # Not checked
    ([0x00], "0"),
    ([0x01], "1"),
    ([0x02], "2"),
    ([0x03], "3"),
    ([0x04], "4"),
    ([0x05], "5"),
    ([0x06], "6"),
    ([0x07], "7"),
    ([0x08], "8"),
    ([0x09], "9"),
    ###
    # Checked
    ###
    ([0x10], "G"),
    ([0x19], "P"),

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ([0x24], "あ"),
    ([0x25], "ぁ"),
    ([0x26], "い"),
    ([0x28], "う"),
    ([0x2A], "え"),
    ([0x2B], "ぇ"),
    ([0x2C], "お"),
    # k-
    ([0x2E], "か"),
    ([0x92, 0x2E], "が"),
    ([0x2F], "き"),
    ([0x92, 0x2F], "ぎ"),

    ([0x30], "く"),
    ([0x92, 0x30], "ぐ"),
    ([0x31], "け"),
    ([0x92, 0x31], "げ"),
    ([0x32], "こ"),
    ([0x92, 0x32], "ご"),
    # s-
    ([0x33], "さ"),
    ([0x92, 0x33], "ざ"),
    ([0x34], "し"),
    ([0x92, 0x34], "じ"),
    ([0x35], "す"),
    ([0x92, 0x35], "ず"),
    ([0x36], "せ"),
    ([0x92, 0x36], "ぜ"),
    ([0x37], "そ"),
    ([0x92, 0x37], "ぞ"),
    # t-
    ([0x38], "た"),
    ([0x92, 0x38], "だ"),
    ([0x39], "ち"),
    ([0x92, 0x39], "ぢ"),
    ([0x3A], "つ"),
    ([0x92, 0x3A], "づ"),
    ([0x3B], "っ"),
    ([0x3C], "て"),
    ([0x92, 0x3C], "で"),
    ([0x3D], "と"),
    ([0x92, 0x3D], "ど"),
    # n-
    ([0x3E], "な"),
    ([0x3F], "に"),

    ([0x41], "ね"),
    ([0x42], "の"),
    # h-
    ([0x43], "は"),
    ([0x92, 0x43], "ば"),
    ([0x44], "ひ"),
    ([0x92, 0x44], "び"),
    ([0x45], "ふ"),
    ([0x47], "ほ"),
    ([0x48], "ま"),
    # m-
    ([0x49], "み"),
    ([0x4A], "む"),
    ([0x4B], "め"),
    ([0x4C], "も"),
    # y-
    ([0x4D], "や"),
    ([0x4E], "ゃ"),
    ([0x4F], "ゆ"),

    ([0x50], "ゅ"),
    ([0x51], "よ"),
    ([0x52], "ょ"),
    # r-
    ([0x53], "ら"),
    ([0x54], "り"),
    ([0x55], "る"),
    ([0x56], "れ"),
    ([0x57], "ろ"),
    # w-
    ([0x58], "わ"),
    ([0x59], "を"),
    # n
    ([0x5A], "ん"),
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ([0x5B], "ア"),
    ([0x5D], "イ"),
    ([0x5F], "ウ"),

    ([0x62], "ェ"),
    # K-
    ([0x65], "カ"),
    ([0x66], "キ"),
    ([0x92, 0x66], "ギ"),
    ([0x67], "ク"),
    ([0x92, 0x67], "ぐ"),
    # S-
    ([0x6A], "サ"),
    ([0x6B], "シ"),
    ([0x92, 0x6B], "ジ"),
    ([0x6C], "ス"),
    ([0x6D], "セ"),
    ([0x92, 0x6D], "ゼ"),
    # T-
    ([0x6F], "タ"),

    ([0x71], "ツ"),
    ([0x72], "ッ"),
    ([0x74], "ト"),
    # H-
    ([0x7A], "ハ"),
    ([0x92, 0x7A], "バ"),
    ([0x7C], "フ"),
    ([0x92, 0x7C], "ブ"),
    ([0x93, 0x7C], "プ"),
    ([0x7E], "ホ"),
    ([0x92, 0x7E], "ボ"),
    ([0x93, 0x7E], "ポ"),
    # M-
    ([0x7F], "マ"),

    ([0x80], "ミ"),
    ([0x83], "モ"),
    # R-
    ([0x8A], "ラ"),
    ([0x8B], "リ"),
    ([0x8C], "ル"),
    ([0x8D], "レ"),
    ([0x8E], "ロ"),

    # N
    ([0x91], "ン"),

    ([0x94], "。"),
    ([0x95], "「"),
    ([0x9B], "?"),
    ([0x9C], "!"),
    ([0xA1], "ー"),
    ([0xA9], "…"),
    ([0xBF], " "),

    ([0xE0, 0x09], "[0xe0][0x09]"),
    ([0xE0, 0x33], "[0xe0][0x33]"),
    ([0xE0, 0x36], "[0xe0][0x36]"),
    ([0xE0, 0x3D], "[0xe0][0x3d]"),
    ([0xE0, 0x51], "[0xe0][0x51]"),
    ([0xE0, 0x5C], "[0xe0][0x5c]"),
    ([0xE0, 0x5D], "私"),
    ([0xE0, 0x68], "出"),
    ([0xE0, 0x7E], "[0xe0][0x7e]"),
    ([0xE0, 0x8B], "[0xe0][0x8b]"),
    ([0xE0, 0x8E], "[0xe0][0x8e]"),
    ([0xE0, 0x90], "中"),
    ([0xE0, 0x92], "[0xe0][0x92]"),
    ([0xE0, 0x99], "[0xe0][0x99]"),
    ([0xE0, 0xA0], "日"),
    ([0xE0, 0xC0], "[0xe0][0xc0]"),
    ([0xE0, 0xC3], "[0xe0][0xc3]"),
    ([0xE0, 0xE0], "[0xe0][0xe0]"),
    ([0xE0, 0xE1], "[0xe0][0xe1]"),

    #([0xE0, 0x], "[0xe0][0x]"),

    ([0xFE], "\\n"),
]

#CHAR_TO_BYTE_MAP = {c: b for b, c in BYTE_TO_CHAR_MAP.items()}
CHAR_TO_BYTE_MAP = {c: b for b, c in BYTE_TO_CHAR_MAP}

def string_to_bytes(string: str) -> bytes:
    try:
        string_bytes = []
        hex_buffer = []
        escape_buffer = []
        for char in string:
            if char == "]":
                char = "".join(hex_buffer[3:])
                string_bytes.append(int(char, 16))
                hex_buffer = []
                continue
            elif char == "[" or len(hex_buffer) > 0:
                hex_buffer.append(char)
                continue
            elif char == "\\":
                escape_buffer += [char]
                continue
            elif len(escape_buffer) > 0:
                char = "".join(escape_buffer) + char
                escape_buffer = []

            matching_bytes = CHAR_TO_BYTE_MAP[char]
            string_bytes.extend(matching_bytes)
    except Exception as e:
        raise ValueError(f'Failed to convert string to bytes: "{string}"') from e

    string_bytes.append(0xFF)

    return bytes(string_bytes)

def bytes_to_string(bs: Union[List[int], bytes]) -> str:
    chars = []
    i = 0
    while i != len(bs):
        b = bs[i]
        if b == 0xFF:
            break

        #chars.append(byte_to_char(b))
        #return "[" + hex(byte) + "]"
        char, i = get_bytes_match(bs, i)
        chars.append(char)

        # i += 1

    return "".join(chars)

def get_bytes_match(bs: Union[List[int], bytes], i: int) -> Tuple[List[Tuple[List[int], str]], int]:
    matches = list(BYTE_TO_CHAR_MAP)
    offset = 0
    while len(matches) >= 1:
        remaining_matches = []
        for match_bytes, match_char in matches:
            if match_bytes[offset] == bs[i + offset]:
                if len(match_bytes) == offset + 1:
                    return match_char, i + offset + 1
                else:
                    remaining_matches.append((match_bytes, match_char))
        matches = remaining_matches

        offset += 1

    #if len(matches) == 1 and len(matches[0][0]) > 1:
    #    print(matches)
    #    print([hex(b) for b in matches[0][0]])
    #    print([hex(b) for b in bs[i:i+offset+1]])
    #    print(offset)
    #    breakpoint()

    if len(matches) == 0 or (len(matches) == 1 and len(matches[0][0]) <= offset):
        return "[" + hex(bs[i]) + "]", i + 1
    elif len(matches) == 1:
        #if len(matches[0][0]) > 1:
        #    breakpoint()
        assert matches[0][0] == bs[i:i + offset], f"{matches[0][0]} != {bs[i:i + offset]}"

        return matches[0][1], i + offset
    else:
        assert False