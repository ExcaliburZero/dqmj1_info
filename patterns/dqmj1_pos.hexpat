struct entry {
    u32 size;
};

struct pos {
    u32 magic;
    entry entries[1];
};

pos pos @ 0x0;