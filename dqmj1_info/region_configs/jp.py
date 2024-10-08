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
            0x0219DEC0,
            [
                StringTable("strings_1", 0x021F52B8, 0x021F566B),
                StringTable("strings_2", 0x021F5704, 0x021F5B60),
                StringTable("strings_3", 0x021F5CC8, 0x021F8090),
                StringTable("strings_4", 0x021F8890, 0x021F8E38),
                StringTable("strings_5", 0x021F8EC4, 0x021F96B0),
            ],
        ),
    },
    string_address_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringAddressTable("skill_descriptions", 0x0208C0D8, 0x0208C4D8),
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
        pathlib.Path("overlay")
        / "overlay_0000.bin": (
            0x0219DEC0,
            [
                StringAddressTable("unknown_1", 0x021F566C, 0x021F5704),
                StringAddressTable("unknown_2", 0x021F5B60, 0x021F5CC4),
                StringAddressTable(
                    "monster_species_descriptions", 0x021F8090, 0x021F8890
                ),
                StringAddressTable("unknown_4", 0x021F8E38, 0x021F8EC4),
            ],
        ),
    },
)
