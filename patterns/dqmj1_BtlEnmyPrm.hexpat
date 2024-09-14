// Format for `data/BtlEnmyPrm.bin`


struct entry {
    u16 species_id; // double check
    u8 unknown[86];
};

struct BtlEnmyPrm {
    u32 magic;
    u32 length;
    entry entries[length];
};

BtlEnmyPrm data @ 0x0;