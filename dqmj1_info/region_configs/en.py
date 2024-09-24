from .region_configs import (
    RegionConfig,
    REGION_CONFIGS,
    StringTable,
    StringAddressTable,
)

import pathlib

REGION_CONFIGS["North America"] = RegionConfig(
    string_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringTable("strings_a", 0x020735F0, 0x020749E8),
                StringTable("strings_b", 0x0207805C, 0x02083DE3),
                StringTable("strings_c", 0x02084B18, 0x0208A7B8),
                StringTable("strings_d", 0x0209072C, 0x02091753),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0000.bin": (
            0x021A0A00,
            [
                StringTable("strings_h", 0x021F5950, 0x021F66EC),
                StringTable("strings_i", 0x021F678C, 0x021F6D6C),
                StringTable("strings_j", 0x021F6ED8, 0x021F78B8),
                StringTable("strings_k", 0x021F80C0, 0x021FC140),
                StringTable("strings_l", 0x021FC224, 0x021FC940),
                StringTable("strings_m", 0x021FCB10, 0x021FD2A0),
                StringTable("strings_n", 0x021FD2F8, 0x021FD45C),
                StringTable("strings_o", 0x021FD588, 0x021FD874),
            ],
        ),
    },
    string_address_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringAddressTable("monster_species_names", 0x0207785C, 0x0207805C),
                StringAddressTable("skill_set_names", 0x020763E0, 0x020767E4),
                StringAddressTable("skill_names", 0x02076BE8, 0x0207705C),
                StringAddressTable("mnamemes", 0x02075FE0, 0x020763E0),
                StringAddressTable("unknown_a", 0x02074CE0, 0x02074DE0),
                StringAddressTable("tactic_names", 0x02074A88, 0x02074AA8),
                StringAddressTable("skill_descriptions", 0x02074FE0, 0x020753E0),
                StringAddressTable(
                    "skill_set_names_and_descriptions", 0x020753E0, 0x020757E0
                ),
                StringAddressTable("item_names", 0x020767E4, 0x02076BE8),
                StringAddressTable("trait_names", 0x020757E0, 0x02075BE0),
                StringAddressTable("enemy_scout_names", 0x02075BE0, 0x02075FE0),
                StringAddressTable("unknown_b", 0x0207705C, 0x0207785C),
                StringAddressTable("unknown_c", 0x02074A04, 0x02074A14),
                StringAddressTable("color_names", 0x02074A54, 0x02074A6C),
                StringAddressTable("day_and_night", 0x020749EC, 0x020749F4),
                StringAddressTable("nsbmd_filenames", 0x02074DE0, 0x02074FE0),
                StringAddressTable("unknown_d", 0x02074C60, 0x02074DDC),
                StringAddressTable("unknown_e", 0x02074B2C, 0x02074B74),
                StringAddressTable("unknown_f", 0x02074A6C, 0x02074A88),
                StringAddressTable(
                    "battle_and_field_and_anywhere", 0x020749F4, 0x02074A04
                ),
                StringAddressTable("unknown_g", 0x02074A3C, 0x02074A54),
                StringAddressTable("battle_targets", 0x02074A14, 0x02074A28),
                StringAddressTable("skill_targeting_types", 0x02074A28, 0x02074A3C),
                StringAddressTable("unknown_h", 0x02074AE8, 0x02074B2C),
                StringAddressTable("unknown_i", 0x02074BE0, 0x02074C60),
                StringAddressTable("unknown_6", 0x02083F48, 0x02083F98),
                StringAddressTable("unknown_7", 0x02083F98, 0x02084018),
                StringAddressTable("unknown_j", 0x02084018, 0x02084118),
                StringAddressTable("unknown_9", 0x02084118, 0x02084318),
                StringAddressTable("battle_messages", 0x02084318, 0x02084B18),
                StringAddressTable("unknown_k", 0x02083EBC, 0x02083EFC),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0000.bin": (
            0x021A0A00,
            [
                StringAddressTable(
                    "monster_species_descriptions", 0x021F78C0, 0x021F80C0
                ),  # special case, they appear as two tables in ROM, but are actually one
            ],
        ),
    },
)
