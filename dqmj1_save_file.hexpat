u24 magic @ 0x00;
u32 gold @ 0x184; // TODO: confirm size
u32 playtime @ 0x2C; // TODO: confirm extent and format
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;
u32 atm @ 0x188;
struct monster {
    // Maybe there are separate stats for the 2 base monsters?
    u8 first_monster_name[0x09];
    u8 unknown[0x69];
    
    u8 level; // Confirmed
    u8 unknown_2;
    u16 max_hp;
    u16 unknown_4; // Changed this, but did not see a noticable effect
    u16 unknown_5; // Changed but no noticeable effect
    u16 maybe_defense;
    u16 maybe_agility;
    u16 unknown_8;
    u16 unknown_9;
    u16 unknown_10;
    u16 unknown_11;
    u16 unknown_12;
    u16 unknown_13;
    u16 unknown_14;
    u16 unknown_15;
    u16 unknown_16;
    u32 exp; // TODO: confirm the size
    // Note: Exp to next level is not stored, it is re-calculated based on the monster's level
    u8 unknown_last[0x70];
};
//monster first_monster @ 0x6CE;
monster first_monster @ 0x65C;
monster second_monster @ 0x7F0;