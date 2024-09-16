struct stat_increase_pattern {
    // One byte for each level. Each value is an 8bit unsigned int representing
    // the stat increase obtained for reaching that level
    u8 increase[99];
};

struct ability_tbl {
    stat_increase_pattern patterns[32];
};

ability_tbl table @ 0x0;