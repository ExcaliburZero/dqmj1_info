from typing import Dict, IO, List

import pandas as pd

MONSTER_SPECIES_NAME = "monster_species_names"


class StringTable:
    def __init__(self, tables: Dict[str, List[str]]) -> None:
        self.tables = tables

    def get_monster_species_name(self, species_id: int) -> str:
        return self.__get_from_table(
            MONSTER_SPECIES_NAME, "monster species id", species_id
        )

    def __get_from_table(
        self, table_name: str, table_description: str, index: int
    ) -> str:
        try:
            return self.tables[table_name][index]
        except IndexError as e:
            raise ValueError(
                f'Invalid {table_description} "{index}". Allowed ids are [0 to {len(self.tables[table_name]) - 1}].'
            ) from e

    @staticmethod
    def from_csv(input_stream: IO[str]) -> "StringTable":
        strings = pd.read_csv(input_stream, keep_default_na=False)

        tables = {
            MONSTER_SPECIES_NAME: list(
                strings[strings["table_name"] == "monster_species_names"]["string"]
            ),
        }

        return StringTable(tables)
