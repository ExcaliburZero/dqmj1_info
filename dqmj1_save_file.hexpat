u24 magic @ 0x00;
u32 gold @ 0x184; // TODO: confirm size
u32 playtime @ 0x2C; // TODO: confirm extent and format
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;
u32 atm @ 0x188;
struct monster {
    u8 monster_name[0x09];
    u8 unknown[0x7];
    u8 sex; // 0=+, 1=-, 2=+-
    u8 unknown_b[0x61];
    
    u8 level; // Confirmed
    u8 unknown_2;
    
    // Stats
    //
    // Stats are represented by two sets of values "base" stat values and
    // "adjusted" stat values.
    //
    // "base" stat values are the stat values without accounting for the
    // monster's current equipment. "adjusted" stat values are the stat
    // values after accounting for the effects of equipment.
    //
    // A monster will use its "adjusted" stat values. Once the monster's
    // equipment is removed, its "adjusted" stats values will be set back
    // to the corresponding "base" stat values.
    //
    // If you want to edit the stat values of a monster, be sure to change
    // both the "base" stat value and the corresponding "adjusted" stat
    // value.
    u16 base_max_hp;
    u16 base_max_mp;
    u16 base_attack;
    u16 base_defense;
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
    u8 tactic;
    u8 unknown_17[0xA];
    u8 equipment;

    // Skill sets
    u8 first_skill_set_id;
    u8 second_skill_set_id;
    u8 third_skill_set_id;
    u8 first_skill_set_points;
    u8 second_skill_set_points;
    u8 third_skill_set_points;
    u8 first_set_num_unlocked_skills;
    u8 second_set_num_unlocked_skills;
    u8 third_set_num_unlocked_skills;

    u8 unknown_20;
    u16 unallocated_skill_points; // TODO: confirm size
    u8 first_skill_set_skills[0x1E]; // TODO: confirm size
    u8 unkown_21;
    u8 second_skill_set_skills[0x1E]; // TODO: confirm size
    // TODO: find exact location and size of third skill set skills
    u8 unknown_last[0x1C];
};
//monster first_monster @ 0x6CE;
monster first_monster @ 0x65C;
monster second_monster @ 0x7F0;
monster third_monster @ 0x984;