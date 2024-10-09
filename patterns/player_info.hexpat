import std.io;

fn format_playtime(u32 raw) {
    u32 remaining = raw & 0b111111;
    u32 seconds = (raw >> 6) & 0b111111;
    u32 minutes = (raw >> 12) & 0b111111;
    u32 hours = raw >> 18;

    return std::format("{}:{:0>2}:{:0>2} ({})", hours, minutes, seconds, remaining);
};

struct name {
    u8 name[9];
    u8 unknown_a[3];
};

struct player_info {
    name name;
    u32 gold;
    u32 atm_gold;
    u8 items_in_hand[16];
    u8 item_in_bag_counts[256];
    u8 num_darkonium_times_5;
    u8 unknown_b[3];
    u32 playtime [[format("format_playtime")]];
    u8 num_party_monsters;
    u8 num_monsters;
    u8 party_monster_indicies[3];
    u8 species_encountered[45];
    u8 species_defeated[45];
    u8 species_obtained[45];
    u8 skill_library[121];
    u8 unknown_c[10];
    u8 player_skills;
    u8 unknown_cd[20];
    u32 num_monsters_scouted;
    u8 unknown_d[8];
    u32 num_battles_won;
    u32 num_times_synthesized;
    u8 unknown[640];
};