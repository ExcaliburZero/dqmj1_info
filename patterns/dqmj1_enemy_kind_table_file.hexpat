// data/EnmyKindTbl.bin

struct monster_data {
    u32 unknown_a;
    
    u8 rank_and_family; // Lower 4 bits are the rank (0x0F), higher 4 bits are the family (0xF0)

    u8 unkown_b[3];
    u8 unknown_c[4];
    
    u32 weapon_compatibility_and_something_else;
    u8 traits[5];
    
    u8 unknown_d[3];
    u8 unknown_dde[4];
    
    u8 default_max_hp;
    u8 default_max_mp;
    u8 default_attack;
    u8 default_defense;
    u8 default_agility;
    u8 default_wisdom;
    
    u8 unknown_de[2];
    
    u16 max_hp_limit;
    u16 max_mp_limit;
    u16 attack_limit;
    u16 defense_limit;
    u16 agility_limit;
    u16 wisdom_limit;
    
    u8 max_hp_increase_indicies[4];
    u8 max_mp_increase_indicies[4];
    u8 attack_increase_indicies[4];
    u8 defense_increase_indicies[4];
    u8 agility_increase_indicies[4];
    u8 wisdom_increase_indicies[4];
    
    u8 skill_set;

    u8 unknown[75];
};

u32 magic @ 0x0;
monster_data monster_data[352] @ 0x8;