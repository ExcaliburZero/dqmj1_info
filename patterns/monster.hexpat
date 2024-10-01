struct parent_monster {
    u16 species;
    u8 name[0x09];
    u16 unknown;
    u8 scout_name[11];
};

struct monster {
    u8 monster_name[12];
    u16 species; // Confirmed, but does not appear to auto update rank + traits + resistances, does update family
    u8 rank; // 1=F, 2=E, 3=D, 4=C, 5=B, 6=A, 7=S, 8=X, 9=???
    u8 family;
    u8 sex; // 0=+, 1=-, 2=+-
    u8 unknown_d[3];
    u8 synthesis_plus_number;
    u8 unknown_de[4];
    u8 unknown_e[24];
    u8 unknown_f[29];
    u8 unknown_f2[2];
    u8 unknown_g[29];
    u8 unknown_g2[5];
    
    u8 level; // Confirmed
    u8 level_limit;
    
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
    u16 adjusted_max_hp;
    u16 current_mp; // This appears to be healed right after loading the game (at least at a centre)
    u16 adjusted_max_mp;
    u16 adjusted_attack;
    u16 adjusted_defense;
    u16 adjusted_agility;
    u16 adjusted_wisdom;
    
    u32 exp; // TODO: confirm the size
    // Note: Exp to next level is not stored, it is re-calculated based on the monster's level
    u8 tactic;
    u8 unknown_17[0x6];
    u8 unknown_18[0x4];
    u8 equipment;

    // Skill sets // TODO: change to arrays of 3 elements
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
    u16 unallocated_skill_points;
    u8 skills[0x1E]; // TODO: confirm size
    u8 traits[0x1F]; // TODO: confirm size
    u8 unknown_21[10];
    u8 level_when_hashed;
    u16 hash;
    u16 unknown_22;
    u8 scout_name[12];
    parent_monster parents[2];
    parent_monster grandparents[4]; // These have no name or scout name info
};