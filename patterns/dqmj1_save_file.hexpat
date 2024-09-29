#include "player_info.hexpat"
#include "monster.hexpat"

import std.io;

fn format_playtime(u32 raw) {
    u32 remaining = raw & 0b111111;
    u32 seconds = (raw >> 6) & 0b111111;
    u32 minutes = (raw >> 12) & 0b111111;
    u32 hours = raw >> 18;

    return std::format("{}:{:0>2}:{:0>2} ({})", hours, minutes, seconds, remaining);
};

u32 magic @ 0x00;
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;

u8 unknown_a[16] @ 0x10;
u8 unknown_b[12] @ 0x20;

// Probably the versions displayed on the save file window when starting the game
u32 playtime @ 0x2C [[format("format_playtime")]]; // 6bits for subseconds, 6bits for seconds, 6bits for minutes, rest for hours?
u8 num_party_monsters @ 0x30;
u8 unknown_c @ 0x31;
name player_name @ 0x32;
name party_monster_names[3] @ 0x3E;

u16 party_monster_species_ids[3] @ 0x62;
u8 party_monster_levels[3] @ 0x68;
u8 unknown_cdc @ 0x6B;
u8 unknown_cdcc @ 0x6C;
u8 unknown_cdccc @ 0x6D;
u16 unknown_cdcccc @ 0x6E;

u8 unknown_cd[264] @ 0x70;

player_info player_info @ 0x178;
monster monsters[100] @ 0x65C;
monster incarnus @ 0xA42C;
u8 unknown_d[64] @ 0xA5C0;
u8 unknown_e[64] @ 0xA600;
u32 unknown_btl_enmy_prm_id @ 0xA640;