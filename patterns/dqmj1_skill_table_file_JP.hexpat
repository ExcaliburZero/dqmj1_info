// Format for `data/SkillTbl.bin` (JP)

u8 magic[0x5] @ 0x0;

struct skill_points_requirement {
    u16 points_delta;
    u16 points_total;
};

struct skill_entry {
    u16 skill_ids[4];
    u8 unknown_5[4];
};

struct trait_entry {
    u8 traits[4];
};

struct skill_set {
    u8 can_upgrade;
    u8 category;
    u8 max_skill_points;
    u8 unknown_3;
    skill_points_requirement skill_points_requirements[10];
    skill_entry skills[10];
    trait_entry traits[10];
    u16 skill_set_id;
    u8 unknown_a[2];
    u16 species_ids[6];
};

skill_set skill_sets[0xC2] @ 0x8;