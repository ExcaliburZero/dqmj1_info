// Format for `data/ItemTbl.bin`

struct item {
    u8 category; // 0=?, 1=?, 2+ = equipment?
    u8 unknown_ab[7];
    u8 unknown_b;
    u8 weapon_type; // 0 through 6
    u8 unknown_c[16];
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