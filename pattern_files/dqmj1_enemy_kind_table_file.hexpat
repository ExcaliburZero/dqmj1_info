// data/EnmyKindTbl.bin

struct monster_data {
    u32 unknown_a;
    u8 rank_and_family; // Lower 4 bits are the rank (0x0F), higher 4 bits are the family (0xF0)
    u8 unkown_b[]3;
    u8 unknown_c[4];
    u32 weapon_compatibility_and_something_else;
    u8 traits[5];
    u8 unknown_d[51];
    u8 skill_set;
    u8 unknown[75];
};

u32 magic @ 0x0;
monster_data monster_data[352] @ 0x8;