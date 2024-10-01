#include "monster.hexpat"
#include "player_info.hexpat"

// Note: Need to set base address to 0x02000000 before loading this pattern file

u32 rng_counter @ 0x020BEC98;
u32 rng_value @ 0x020BEC9C;

u8 save_file_validation_result @ 0x0219CA9C;

u32 skill_table_pointer @ 0x0218B628;
//u8 skill_table[0x0000B5E8] @ skill_table_pointer;

u32 item_table_pointer @ 0x020B01CC;
u8 item_table[0x4388] @ item_table_pointer;

u32 monster_species_table_pointer @ 0x0218B53C;
u8 monster_species_table[0xCB88] @ monster_species_table_pointer;

u32 fld_mstr_prm_pointer @ 0x02249C10;
//u8 fld_mstr_prm[0x408] @ fld_mstr_prm_pointer;

u32 fld_enmy_prm_start_pointer @ 0x02249C14;
//u8 fld_enmy_prm_data_start @ fld_enmy_prm_start_pointer;

u32 fld_enmy_prm_pointer @ 0x02249C18;
//u8 fld_enmy_prm[0x6E08] @ fld_enmy_prm_pointer;

u8 trait_stat_increment_values_adaw[11] @ 0x0208c778;
u8 trait_stat_increment_values_hp_mp[11] @ 0x0208c76c;

u8 strings_a[5112] @ 0x020735F0;
u8 strings_b[48519] @ 0x0207805C;
u8 strings_c[23712] @ 0x02084B18;
u8 strings_d[4135] @ 0x0209072C;

u8 unknown_big_struct @ 0x0224B610;

u8 save_data_in_ram @ 0x225114C;

// This appears to be only partial...
// monster another_first_party_monster @ 0x02238FD8;
struct partial_monster {
    u8 monster_name[0x09];
    u8 unkown_a[0x3];
    u16 species; // Confirmed, but does not appear to auto update rank + traits + resistances, does update family
    u8 rank; // 1=F, 2=E, 3=D, 4=C, 5=B, 6=A, 7=S, 8=X, 9=???
    u8 family;
    u8 sex; // 0=+, 1=-, 2=+-

    u8 unknown_d[3];
    u8 synthesis_plus_number;
    u8 unknown_de[112];
    
    u8 level; // Confirmed
    u8 level_limit;
    
    u8 unknown;
    
    // TODO: these locations aren't quite right
    u16 base_max_hp;
    u16 base_max_mp;
    u16 base_attack;
    u16 base_defense;
    u16 base_agility;
    u16 base_wisdom;
    u16 unknown_f;
    u16 current_hp; // This appears to be healed right after loading the game (at least at a centre)
    u16 adjusted_max_h;
    u16 current_mp; // This appears to be healed right after loading the game (at least at a centre)
    u16 adjusted_max_mp;
    u16 adjusted_attack;
    u16 adjusted_defense;
    u16 adjusted_agility;
    u16 adjusted_wisdom;
    
    u32 exp; // TODO: confirm the size
};

partial_monster monster_in_battle @ 0x02238FD8;

u32 first_evt_file_ptr @ 0x223DF9C;
u32 first_evt_file_data_start @ 0x223DFA0;

struct unknown_struct_b {
    u8 unknown_a[3];
    u8 unknown_index;
    u32 unknown_ab;
    u32 script_start_ptr;
    u32 script_data_start_ptr;
    u32 unknown_b_to_h[7];
    u8 unknown[936];
    u32 unknown_j;
    u32 unknown_2[152];
    u32 unknown_3[268]; // size unclear
};


unknown_struct_b start_unknown_struct_b @ 0x223DF94;

u32 pos_file_pointer @ 0x224B61C;

player_info player_info @ 0x020BE340;
monster player_monsters[100] @ 0x20B3D8C;
monster incarnus @ 0x020B2DBC;