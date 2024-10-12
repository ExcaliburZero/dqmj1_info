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
                StringTable("strings_0x020735F0", 0x020735F0, 0x020749E8),
                StringTable("strings_0x0207805C", 0x0207805C, 0x02083DE3),
                StringTable("strings_0x02084B18", 0x02084B18, 0x0208A7B8),
                StringTable("strings_0x0208AA60", 0x0208AA60, 0x0208C768),
                StringTable("strings_0x0208C7AD", 0x0208C7AD, 0x0208C824),
                StringTable("strings_0x0208C9E8", 0x0208C9E8, 0x0208D498),
                StringTable("strings_0x0208D6E8", 0x0208D6E8, 0x0208E718),
                StringTable("strings_0x0208EA58", 0x0208EA58, 0x0208F9DC),
                StringTable("strings_0x0208FB98", 0x0208FB98, 0x020903C0),
                StringTable("strings_0x0209072C", 0x0209072C, 0x02091754),
                StringTable("strings_0x02091958", 0x02091958, 0x020925A4),
                StringTable("strings_0x020929a8", 0x020929A8, 0x02093004),
                StringTable("strings_0x02093274", 0x02093274, 0x02093D08),
                StringTable("strings_0x02094270", 0x02094270, 0x02094E50),
                StringTable("strings_0x02094e94", 0x02094E94, 0x02094F20),
                StringTable("strings_0x020950a0", 0x020950A0, 0x020959A0),
                StringTable("strings_0x02095a50", 0x02095A50, 0x02095A78),
                StringTable("strings_0x02095a9c", 0x02095A9C, 0x02095B9C),
                StringTable("strings_0x02095c00", 0x02095C00, 0x02095D7C),
                StringTable("strings_0x02095da8", 0x02095DA8, 0x02096024),
                StringTable("strings_0x0209642c", 0x0209642C, 0x02096B7C),
                StringTable("strings_0x02096e84", 0x02096E84, 0x02097EEC),
                StringTable("strings_0x020994e0", 0x020994E0, 0x0209B22C),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0000.bin": (
            0x021A0A00,
            [
                StringTable("strings_0x021F5950", 0x021F5950, 0x021F66EC),
                StringTable("strings_0x021F678C", 0x021F678C, 0x021F6D6C),
                StringTable("strings_0x021F6ED8", 0x021F6ED8, 0x021F78B8),
                StringTable("strings_0x021F80C0", 0x021F80C0, 0x021FC140),
                StringTable("strings_0x021FC224", 0x021FC224, 0x021FC940),
                StringTable("strings_0x021FCB10", 0x021FCB10, 0x021FD2A0),
                StringTable("strings_0x021FD2F8", 0x021FD2F8, 0x021FD45C),
                StringTable("strings_0x021FD588", 0x021FD588, 0x021FD874),
                StringTable("strings_0x021F5F30", 0x021F5F30, 0x021F66EC),
                StringTable("strings_0x021F678C", 0x021F678C, 0x021F6D6C),
                StringTable("strings_0x021F6ED8", 0x021F6ED8, 0x021F78B8),
                StringTable("strings_0x021F80C0", 0x021F80C0, 0x021FC140),
                StringTable("strings_0x021FC224", 0x021FC224, 0x021FC940),
                StringTable("strings_0x021FCB10", 0x021FCB10, 0x021FD2A0),
                StringTable("strings_0x021FD2F8", 0x021FD2F8, 0x021FD45C),
                StringTable("strings_0x021FD588", 0x021FD588, 0x021FD874),
                StringTable("strings_0x021FD8C0", 0x021FD8C0, 0x021FDAB0),
                StringTable("strings_0x021FDB78", 0x021FDB78, 0x021FE024),
                StringTable("strings_0x021FE2D8", 0x021FE2D8, 0x02201E0C),
                StringTable("strings_0x02201EBC", 0x02201EBC, 0x02202370),
                StringTable("strings_0x022025FC", 0x022025FC, 0x02203514),
                StringTable("strings_0x022035B8", 0x022035B8, 0x0220361C),
                StringTable("strings_0x022037E0", 0x022037E0, 0x02204060),
                StringTable("strings_0x022040F8", 0x022040F8, 0x02204398),
                StringTable("strings_0x022043B8", 0x022043B8, 0x0220441C),
                StringTable("strings_0x02204458", 0x02204458, 0x02204600),
                StringTable("strings_0x0220468C", 0x0220468C, 0x02204990),
                StringTable("strings_0x02204A70", 0x02204A70, 0x022050AC),
                StringTable("strings_0x022050D4", 0x022050D4, 0x02205144),
                StringTable("strings_0x02205174", 0x02205174, 0x02205300),
                StringTable("strings_0x0220533C", 0x0220533C, 0x02205444),
                StringTable("strings_0x02205450", 0x02205450, 0x02205498),
                StringTable("strings_0x02205524", 0x02205524, 0x022057D8),
                StringTable("strings_0x02205814", 0x02205814, 0x022059F4),
                StringTable("strings_0x0220663C", 0x0220663C, 0x02207FB8),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0002.bin": (
            0x021A0A00,
            [
                StringTable("strings_0x02209f70", 0x02209F70, 0x0220BC2C),
                StringTable("strings_0x02209be8", 0x02209BE8, 0x02209CC4),
            ],
        ),
    },
    string_address_tables={
        pathlib.Path("arm9.bin"): (
            0x02000000,
            [
                StringAddressTable("day_and_night", 0x20749EC, 0x20749F4),
                StringAddressTable(
                    "battle_and_field_and_anywhere", 0x20749F4, 0x2074A04
                ),
                StringAddressTable("unknown_0x02074A04", 0x2074A04, 0x2074A14),
                StringAddressTable("battle_targets", 0x2074A14, 0x2074A28),
                StringAddressTable("skill_targeting_types", 0x2074A28, 0x2074A3C),
                StringAddressTable("unknown_0x02074A3C", 0x2074A3C, 0x2074A54),
                StringAddressTable("color_names", 0x2074A54, 0x2074A6C),
                StringAddressTable("unknown_0x02074A6C", 0x2074A6C, 0x2074A88),
                StringAddressTable("tactic_names", 0x2074A88, 0x2074AA8),
                StringAddressTable("debug_menu", 0x2074AE8, 0x2074B2C),
                StringAddressTable("unknown_0x02074B2C", 0x2074B2C, 0x2074B74),
                StringAddressTable("trading_npc_names", 0x2074BE0, 0x2074C60),
                StringAddressTable("unknown_0x02074C60", 0x2074C60, 0x2074DDC),
                StringAddressTable("debug_model_viewer_menu", 0x2074CE0, 0x2074DE0),
                StringAddressTable("nsbmd_filenames", 0x2074DE0, 0x2074FE0),
                StringAddressTable("skill_descriptions", 0x2074FE0, 0x20753E0),
                StringAddressTable(
                    "skill_set_names_and_descriptions", 0x20753E0, 0x20757E0
                ),
                StringAddressTable("trait_names", 0x20757E0, 0x2075BE0),
                StringAddressTable("enemy_scout_names", 0x2075BE0, 0x2075FE0),
                StringAddressTable("mnamemes", 0x2075FE0, 0x20763E0),
                StringAddressTable("skill_set_names", 0x20763E0, 0x20767E4),
                StringAddressTable("item_names", 0x20767E4, 0x2076BE8),
                StringAddressTable("skill_names", 0x2076BE8, 0x207705C),
                StringAddressTable("unused_skill_names", 0x207705C, 0x207785C),
                StringAddressTable("monster_species_names", 0x207785C, 0x207805C),
                StringAddressTable(
                    "unused_gun_minigame_battle_text", 0x2083E7C, 0x2083EBC
                ),
                StringAddressTable("battle_start_messages", 0x2083EBC, 0x2083EFC),
                StringAddressTable("battle_scouting_messages", 0x2083F48, 0x2083F98),
                StringAddressTable(
                    "unused_partially_localized_element_and_status_names",
                    0x2083F98,
                    0x2084018,
                ),
                StringAddressTable("unknown_0x02084018", 0x2084018, 0x2084118),
                StringAddressTable("battle_end_messages", 0x2084118, 0x2084318),
                StringAddressTable("battle_messages", 0x2084318, 0x2084B18),
                StringAddressTable(
                    "item_names_and_descriptions", 0x208A7E0, 0x0208AA60
                ),
                StringAddressTable("monster_storage_menu", 0x208C824, 0x208C9E8),
                StringAddressTable("synthesis_menu", 0x208D498, 0x208D6E8),
                StringAddressTable("misc_menus", 0x208E71C, 0x208EA58),
                StringAddressTable("misc_battle_text", 0x208F9E0, 0x208FB98),
                StringAddressTable(
                    "elemental_weaknesses_on_monster_status_menu", 0x20903C4, 0x209072C
                ),
                StringAddressTable("save_error_messages", 0x2091760, 0x2091778),
                StringAddressTable("unknown_0x02091778", 0x2091778, 0x2091798),
                StringAddressTable(
                    "party_interface_for_world_cup_menu", 0x2091798, 0x2091958
                ),
                StringAddressTable(
                    "real_life_and_ingame_locations", 0x20925A8, 0x20929A8
                ),
                StringAddressTable("plural_item_names", 0x2093008, 0x2093274),
                StringAddressTable(
                    "plural_monster_species_names", 0x2093D0C, 0x2094270
                ),
                StringAddressTable("s_team", 0x2094E58, 0x2094E5C),
                StringAddressTable("enemy", 0x2094E5C, 0x2094E60),
                StringAddressTable("singular_item_grammar", 0x2094E64, 0x2094E94),
                StringAddressTable("unknown_0x02094f24", 0x2094F24, 0x20950A0),
                StringAddressTable("unknown_0x020959a4", 0x20959A4, 0x2095A50),
                StringAddressTable("unknown_0x02095a7c", 0x2095A7C, 0x2095A80),
                StringAddressTable("keyboards", 0x2095A80, 0x2095A9C),
                StringAddressTable("top_screen_menu", 0x2095BA0, 0x2095C00),
                StringAddressTable("unknown_0x02095d80", 0x2095D80, 0x2095DA8),
                StringAddressTable("item_names_abbreviated", 0x2096028, 0x209642C),
                StringAddressTable("skill_set_names_abbreviated", 0x2096B80, 0x2096E84),
                StringAddressTable("default_monster_names", 0x2097EF0, 0x20994E0),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0000.bin": (
            0x021A0A00,
            [
                StringAddressTable(
                    "monster_species_descriptions", 0x021F78C0, 0x021F80C0
                ),  # special case, they appear as two tables in ROM, but are actually one
                StringAddressTable("swear_words", 0x022059F8, 0x0220663C),
                StringAddressTable("wifi_trading", 0x021F5E0C, 0x021F5F30),
                StringAddressTable("chance_encounter_mode", 0x021F66F0, 0x021F678C),
                StringAddressTable(
                    "area_names_on_bottom_screen", 0x021F6D70, 0x021F6ED8
                ),
                StringAddressTable(
                    "monster_library_descriptions", 0x021F78C0, 0x021F7CC0
                ),
                StringAddressTable(
                    "monster_library_descriptions_2", 0x021F7CC0, 0x021F80C0
                ),
                StringAddressTable("unknown_0x021FC148", 0x021FC148, 0x021FC198),
                StringAddressTable("scoutpost_desk_menu", 0x021FC198, 0x021FC224),
                StringAddressTable("unknown_0x021FC944", 0x021FC944, 0x021FCB10),
                StringAddressTable("scouts_den_npc_names", 0x021FD2A4, 0x021FD2F8),
                StringAddressTable(
                    "scouts_den_trading_interface", 0x021FD460, 0x021FD588
                ),
                StringAddressTable("gold_bank_atm", 0x021FD878, 0x021FD8C0),
                StringAddressTable("main_quest_goals", 0x021FDAB4, 0x021FDB78),
                StringAddressTable("scoutpost_desk_tutorials", 0x021FE030, 0x021FE054),
                StringAddressTable(
                    "scoutpost_newsletter_names", 0x021FE054, 0x021FE194
                ),
                StringAddressTable(
                    "scoutpost_newsletter_contents", 0x021FE194, 0x021FE2D8
                ),
                StringAddressTable(
                    "skill_scroll_shop_interface", 0x02201E10, 0x02201EBC
                ),
                StringAddressTable("wifi_battle_manu", 0x02202374, 0x022025FC),
                StringAddressTable("items_menu", 0x02203620, 0x022037E0),
                StringAddressTable("arena_battle_menu", 0x02204064, 0x022040F8),
                StringAddressTable("unknown_0x0220439C", 0x0220439C, 0x022043B8),
                StringAddressTable("tactic_selection_menu", 0x02204420, 0x02204458),
                StringAddressTable(
                    "skill_results_outside_battle", 0x02204608, 0x0220468C
                ),
                StringAddressTable("title_menu", 0x02204994, 0x02204A70),
                StringAddressTable("locations", 0x022050B4, 0x022050D4),
                StringAddressTable("quicksave", 0x02205148, 0x02205174),
                StringAddressTable(
                    "optimize_to_strongest_weapon", 0x02205304, 0x0220533C
                ),
                StringAddressTable("unknown_0x02205448", 0x02205448, 0x02205450),
                StringAddressTable(
                    "monster_and_skill_library_interface", 0x0220549C, 0x02205524
                ),
                StringAddressTable("saving", 0x022057DC, 0x02205814),
            ],
        ),
        pathlib.Path("overlay")
        / "overlay_0002.bin": (
            0x021A0A00,
            [
                StringAddressTable("unknown_0x02209ccc", 0x02209CCC, 0x02209CEC),
                StringAddressTable("unknown_0x02209cec", 0x02209CEC, 0x02209F70),
            ],
        ),
    },
)
