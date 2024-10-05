from typing import Dict, IO, List

import pandas as pd

MONSTER_SPECIES_NAME = "monster_species_names"
LOCATION = "locations"


class StringTable:
    def __init__(self, tables: Dict[str, List[str]]) -> None:
        self.tables = tables

    def get_monster_species_name(self, species_id: int) -> str:
        return self.__get_from_table(
            MONSTER_SPECIES_NAME, "monster species", species_id
        )

    def get_location(self, location: int) -> str:
        return self.__get_from_table(LOCATION, "location", location)

    def __get_from_table(
        self, table_name: str, table_description: str, index: int
    ) -> str:
        if len(self.tables[table_name]) == 0:
            raise ValueError(f'String table "{table_name}" has no entries.')

        try:
            return self.tables[table_name][index]
        except IndexError as e:
            raise ValueError(
                f'Invalid {table_description} id "{index}". Allowed ids are [0 to {len(self.tables[table_name]) - 1}].'
            ) from e

    @staticmethod
    def from_csv(input_stream: IO[str]) -> "StringTable":
        strings = pd.read_csv(input_stream, keep_default_na=False)

        def extract_table(name: str) -> List[str]:
            return list(strings[strings["table_name"] == name]["string"])

        tables = {
            MONSTER_SPECIES_NAME: extract_table(MONSTER_SPECIES_NAME),
            LOCATION: extract_table(LOCATION),
        }

        return StringTable(tables)
