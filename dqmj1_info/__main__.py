from typing import List

import argparse
import logging
import pathlib
import sys

from . import enmy_kind_tbl
from . import extract_strings
from . import extract_string_address_tables
from . import monster_species_table


def main(argv: List[str]):
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s> %(message)s")

    parser = argparse.ArgumentParser()

    parser.add_argument("--input_directory", required=True)
    parser.add_argument("--output_directory", required=True)

    args = parser.parse_args(argv)

    input_directory = pathlib.Path(args.input_directory)
    output_directory = pathlib.Path(args.output_directory)

    if not input_directory.exists():
        logging.error(f"Input directory does not exist: {input_directory}")

    ###
    # Setup output directory
    ###
    output_directory.mkdir(exist_ok=True, parents=True)
    logging.info(f"Created output directory: {output_directory}")

    ###
    # Extract strings
    ###
    strings_without_context_csv = output_directory / "strings_without_context.csv"
    extract_strings.main(
        [
            "--data_directory",
            str(input_directory),
            "--output_csv",
            str(strings_without_context_csv),
        ]
    )
    logging.info(
        f"Finished writing extracted strings to: {strings_without_context_csv}"
    )

    ###
    # Lookup strings by table
    ###
    strings_by_table_csv = output_directory / "strings_by_table.csv"
    extract_string_address_tables.main(
        [
            "--data_directory",
            str(input_directory),
            "--mined_strings",
            str(strings_without_context_csv),
            "--output_csv",
            str(strings_by_table_csv),
        ]
    )
    logging.info(f"Finished writing extracted string tables to: {strings_by_table_csv}")

    ###
    # Extract EnmyKindTbl
    ###
    enmy_kind_tbl_csv = output_directory / "EnmyKindTbl.csv"
    enmy_kind_tbl.main(
        [
            "--table_filepath",
            str(input_directory / "data" / "EnmyKindTbl.bin"),
            "--output_csv",
            str(enmy_kind_tbl_csv),
        ]
    )
    logging.info(f"Finished extracting EnmyKindTbl.bin to: {enmy_kind_tbl_csv}")

    ###
    # Create monster species table
    ###
    monster_species_table_csv = output_directory / "monster_species.csv"
    monster_species_table.main(
        [
            "--strings_csv",
            str(strings_by_table_csv),
            "--enmy_kind_tbl_csv",
            str(enmy_kind_tbl_csv),
            "--output_csv",
            str(monster_species_table_csv),
        ]
    )
    logging.info(
        f"Finished creating monster species table: {monster_species_table_csv}"
    )


if __name__ == "__main__":
    main(sys.argv[1:])
