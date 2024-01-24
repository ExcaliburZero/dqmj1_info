struct monster_data {
    u8 unknown_a[16];
    u8 traits[5];
    u8 unknown[0x7F];
};

u32 magic @ 0x0;

// TODO: either the struct size or offset from start of file are wrong
monster_data monster_data[337] @ 0x4; // TODO: figure out how many entries, this seems like too few I would expect at least 344