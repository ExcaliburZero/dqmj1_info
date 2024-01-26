// Format for `data/ItemTbl.bin`

struct item {
    u8 unkown_a[26];
    u8 attack_increase;
    u8 defense_increase;
    u8 agility_increase;
    u8 wisdom_increase;
    u8 max_hp_increase;
    u8 max_mp_increase;
    u8 unknown[76];
};

u64 magic @ 0x0;
item items[160] @ 0x8;