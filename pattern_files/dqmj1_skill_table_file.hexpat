// Format for `data/SkillTbl.bin`

u8 magic[0x5] @ 0x0;

struct skill_set_entry {
    u16 skill_id;
    u16 num_points_needed;
};

struct skill_set {
    u8 unknown_1;
    u8 unknown_2[3];
    skill_set_entry learnable_skills[10];
    u8 unknown_3[0xC4];
};

skill_set skill_sets[0xC2] @ 0x8;