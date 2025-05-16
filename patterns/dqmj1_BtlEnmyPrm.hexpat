// Format for `data/BtlEnmyPrm.bin`

struct item_drop {
    u16 item_id;
    u16 chance_denominator_2_power;
};

struct Skill {
    u16 unknown;
    u16 skill_id;
};

struct BtlEnmyPrmEntry {
    u16 species_id;
    u8 unknown_a[6];
    Skill skills[6];
    item_drop item_drops[2];
    u16 gold;
    u16 unknown_ab;
    u16 exp;
    u8 unknown_abb[2];
    u16 level;
    u8 unknown_b[2];
    u16 max_hp;
    u16 max_mp;
    u16 attack;
    u16 defense;
    u16 agility;
    u16 wisdom;
    u8 unknown[20];
    u8 skill_set_ids[3];
    u8 unknown_d;
};

struct BtlEnmyPrm {
    u32 magic;
    u32 length;
    BtlEnmyPrmEntry entries[length];
};

BtlEnmyPrm data @ 0x0;