#include "monster.hexpat"

import std.io;

fn format_playtime(u32 raw) {
    u32 remaining = raw & 0b111111;
    u32 seconds = (raw >> 6) & 0b111111;
    u32 minutes = (raw >> 12) & 0b111111;
    u32 hours = raw >> 18;

    return std::format("{}:{:0>2}:{:0>2} ({})", hours, minutes, seconds, remaining);
};

struct party_monster_name {
    u8 name[9];
    u8 unknown[3];
};

u24 magic @ 0x00;
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;

u32 playtime @ 0x2C [[format("format_playtime")]]; // 6bits for subseconds, 6bits for seconds, 6bits for minutes, rest for hours?
u8 player_name[0x09] @ 0x32;
u32 gold @ 0x184; // TODO: confirm size
u32 atm @ 0x188;

u32 num_times_synthesized @ 0x3D8;

monster first_monster @ 0x65C;
monster second_monster @ 0x7F0;
monster third_monster @ 0x984;

// Probably the versions displayed on the save file window when starting the game
party_monster_name party_monster_names[3] @ 0x3E;

u16 party_monster_species_ids[3] @ 0x62;
u8 party_monster_levels[3] @ 0x68;

u8 num_party_monsters @ 0x30;

u8 unknown_a[16] @ 0x10;
u8 unknown_b[12] @ 0x20;
u8 unknown_c @ 0x31;