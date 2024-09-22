from .region_configs import (
    RegionConfig,
    REGION_CONFIGS,
    StringTable,
    StringAddressTable,
)

import pathlib

REGION_CONFIGS["Japan"] = RegionConfig(
    string_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringTable("strings_a", 0x02083674, 0x020890BF),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0000.bin": (
            0x021A0A00,
            [],
        ),
    },
    string_address_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [],
        ),
    },
)
