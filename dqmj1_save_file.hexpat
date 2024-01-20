u24 magic @ 0x00;
u32 gold @ 0x184; // TODO: confirm size
u32 playtime @ 0x2C; // TODO: confirm extent and format
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;
u32 atm @ 0x188;
struct monster {
    // Maybe there are separate stats for the 2 base monsters?
    u8 monster_name[0x09];
    u8 unknown[0x7];
    u8 sex; // 0=+, 1=-, 2=+-
    u8 unknown_b[0x61];
    
    u8 level; // Confirmed
    u8 unknown_2;
    u16 base_max_hp;
    u16 base_max_mp;
    u16 base_attack; // TODO: confirm
    u16 base_defense; // Maybe each stat has 2 entries, one for the "base" and one for the "adjusted" (ex. due to equipment?)
    u16 base_agility;
    u16 base_wisdom;
    u16 current_hp; // This appears to be healed right after loading the game (at least at a centre)
    u16 adjusted_max_h;
    u16 current_mp; // This appears to be healed right after loading the game (at least at a centre)
    u16 adjusted_max_mp;
    u16 adjusted_attack;
    u16 adjusted_defense;
    u16 adjusted_agility;
    u16 adjusted_wisdom;
    u32 exp; // TODO: confirm the size
    // Note: Exp to next level is not stored, it is re-calculated based on the monster's level
    u8 unknown_17[0xB];
    u8 equipment;
    u8 unknown_last[0x64];
};
//monster first_monster @ 0x6CE;
monster first_monster @ 0x65C;
monster second_monster @ 0x7F0;