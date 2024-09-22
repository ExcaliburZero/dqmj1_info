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
                StringTable("strings_a", 0x02083674, 0x02084CA4),
                StringTable("strings_b", 0x02084CA8, 0x02086828),
                StringTable("strings_c", 0x02086830, 0x0208886B),
                StringTable("strings_d", 0x0208888C, 0x02089020),
                StringTable("strings_e", 0x02089034, 0x020890C0),
                StringTable("strings_f", 0x020890D4, 0x02089B54),
                StringTable("strings_g", 0x02089B84, 0x0208A550),
                StringTable("strings_h", 0x0208A56C, 0x0208AACC),
                StringTable("strings_i", 0x0208AAEC, 0x0208AF1C),
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
                StringAddressTable("unknown_a", 0x0208C0D8, 0x0208C4D8),
                StringAddressTable("unknown_b", 0x0208C4D8, 0x0208C8D8),
                StringAddressTable("unknown_c", 0x0208C8D8, 0x0208CCD8),
                StringAddressTable("unknown_d", 0x0208CCD8, 0x0208D0D8),
                StringAddressTable("unknown_e", 0x0208D0D8, 0x0208D4D8),
                StringAddressTable("skill_set_names", 0x0208D4D8, 0x0208D8DC),
                StringAddressTable("item_names", 0x0208D8DC, 0x0208DCE0),
                StringAddressTable("skill_names", 0x0208DCE0, 0x0208E0E8),
                StringAddressTable("unknown_h", 0x0208E0E8, 0x0208E8E8),
                StringAddressTable("monster_species_names", 0x0208E8E8, 0x0208F0E8),
            ],
        ),
    },
)
