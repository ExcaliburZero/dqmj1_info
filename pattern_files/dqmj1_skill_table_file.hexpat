// Format for `data/SkillTbl.bin`

u8 magic[0x5] @ 0x0;

struct skill_set {
    u8 unknown_1;
    u8 unknown_2[0xEF];
};

skill_set skill_sets[0xC2] @ 0x8;