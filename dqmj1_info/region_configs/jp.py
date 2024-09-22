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
                StringTable("strings_a", 0x02083674, 0x02084CA3),
                StringTable("strings_b", 0x02084CA9, 0x02086827),
                StringTable("strings_c", 0x02086830, 0x0208886B),
                StringTable("strings_d", 0x0208888C, 0x020890BF),
                StringTable("strings_e", 0x020890D4, 0x02089B53),
                StringTable("strings_f", 0x02089B84, 0x0208A54F),
                StringTable("strings_g", 0x0208A56C, 0x0208AACB),
                StringTable("strings_h", 0x0208AAEC, 0x0208AF1B),
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
                StringAddressTable("unknown_a", 0x0208C0D8, 0x0208C4D4),
                StringAddressTable("unknown_b", 0x0208C4D8, 0x0208C8D4),
                StringAddressTable("unknown_c", 0x0208C8D8, 0x0208CCD4),
                StringAddressTable("unknown_d", 0x0208CCD8, 0x0208D0D4),
                StringAddressTable("unknown_e", 0x0208D0D8, 0x0208D4D4),
                StringAddressTable("unknown_f", 0x0208D4D8, 0x0208D8D8),
                StringAddressTable("unknown_g", 0x0208D8DC, 0x0208DCDC),
                StringAddressTable("unknown_h", 0x0208DCE0, 0x0208E0E4),
                StringAddressTable("skill_names", 0x0208E0E8, 0x0208E8E4),
                StringAddressTable("monster_species_names", 0x0208E8E8, 0x0208F0E4),
            ],
        ),
    },
)
