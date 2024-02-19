from dataclasses import dataclass
from typing import Dict, List, Tuple

import pathlib


@dataclass(frozen=True)
class StringTable:
    name: str
    start: int
    end: int


@dataclass(frozen=True)
class StringAddressTable:
    name: str
    start: int
    end: int


@dataclass(frozen=True)
class LanguageConfig:
    string_tables: Dict[pathlib.Path, Tuple[int, List[StringTable]]]
    string_address_tables: Dict[pathlib.Path, Tuple[int, List[StringAddressTable]]]


LANGUAGE_CONFIGS: Dict[str, LanguageConfig] = {}
