// Format for `data/SkillTbl.bin`

u8 magic[0x5] @ 0x0;

struct skill_points_requirement {
    u16 points_delta;
    u16 points_total;
};

struct skill_entry {
    u16 skill_id;
    u16 unknown_2;
    u16 unknown_3;
    u16 unknown_4;
    u8 unknown_5[4];
};

struct skill_set {
    u8 unknown_1;
    u8 unknown_2[3];
    skill_points_requirement skill_points_requirements[10];
    skill_entry skills[10];
    u8 unknown_3[0x4C];
};

skill_set skill_sets[0xC2] @ 0x8;