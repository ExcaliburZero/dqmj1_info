// data/EnmyKindTbl.bin

struct monster_data {
    u32 unknown_a;
    u32 rank_and_something_else; // Lowest 4 bits are the rank, remaining 28 bits are shifted and truncated to form monster.unknown_c
    u8 unknown_c[4];
    u32 weapon_compatibility_and_something_else;
    u8 traits[5];
    u8 unknown_d[51];
    u8 skill_set;
    u8 unknown[75];
};

u32 magic @ 0x0;
monster_data monster_data[352] @ 0x8;