// data/EnmyKindTbl.bin

struct monster_data {
    u32 unknown_a;
    u32 rank_and_something_else; // Lowest 4 bits are the rank, remaining 28 bits are shifted and truncated to form monster.unknown_c
    u8 unknown_b[8];
    u8 traits[5];
    u8 unknown[0x7F];
};

u32 magic @ 0x0;
monster_data monster_data[352] @ 0x8;