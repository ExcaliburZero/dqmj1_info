// data/EnmyKindTbl.bin

struct monster_data {
    u8 unknown_a[16];
    u8 traits[5];
    u8 unknown[0x7F];
};

u32 magic @ 0x0;
monster_data monster_data[352] @ 0x8;