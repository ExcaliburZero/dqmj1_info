#include "player_info.hexpat"
#include "monster.hexpat"

struct header {
    u32 magic_1;
    u32 magic_2;
    u32 magic_3;
    u32 checksum;
};

struct preview_name {
    u8 unknown[3];
    u8 name[9];
};

struct monster_previews {
    preview_name names[3];
    u8 unknown_a[3];
    u16 species_ids[3];
    u8 levels[3];
};

struct summary {
    u8 unknown_a[16];
    u8 unknown_b[12];
    u32 playtime [[format("format_playtime")]];
    u8 num_party_monsters;
    u8 current_island;
    u8 player_name[9];
    monster_previews party_monster_previews;
    u8 num_darkonium_times_5;
    u8 unknown_d[268];
};

struct other {
    u8 unknown_a[64];
    u8 unknown_b[64];
    u32 unknown_btl_enmy_prm_value;
};

struct save_file {
    header header;
    summary summary;
    player_info player_info;
    monster player_monsters[100];
    monster incarnus;
    other other;
};

save_file save_file @ 0x0;