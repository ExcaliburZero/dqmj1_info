#include "monster.hexpat"

// Note: Need to set base address to 0x02000000 before loading this pattern file

monster party_monsters[7] @ 0x020B3D8C; // TODO: is this all player's monsters?

u32 rng_counter @ 0x020BEC98;
u32 rng_value @ 0x020BEC9C;

u8 save_file_validation_result @ 0x0219CA9C;

u32 skill_table_pointer @ 0x0218B628;
u8 skill_table[0x0000B5E8] @ skill_table_pointer;

u32 item_table_pointer @ 0x020B01CC;
u8 item_table[0x4388] @ item_table_pointer;

u32 monster_species_table_pointer @ 0x0218B53C;
u8 monster_species_table[0xCB88] @ monster_species_table_pointer;

u32 fld_enmy_prm_pointer @ 0x02249C18;
u8 fld_enmy_prm[0x6E08] @ fld_enmy_prm_pointer;

u8 trait_stat_increment_values_adaw[11] @ 0x0208c778;
u8 trait_stat_increment_values_hp_mp[11] @ 0x0208c76c;

u8 strings_a[5112] @ 0x020735F0;
u8 strings_b[48519] @ 0x0207805C;
u8 strings_c[23712] @ 0x02084B18;
u8 strings_d[4135] @ 0x0209072C;