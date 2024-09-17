from .region_configs import (
    RegionConfig,
    REGION_CONFIGS,
    StringTable,
    StringAddressTable,
)

import pathlib

REGION_CONFIGS["Europe"] = RegionConfig(
    string_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringTable("strings_a", 0x020763C0, 0x02076B30),
                StringTable("strings_b", 0x02075FF0, 0x02076138),
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
            [
                StringAddressTable("unknown_a", 0x0207616C, 0x020763C0),
            ],
        ),
    },
)
