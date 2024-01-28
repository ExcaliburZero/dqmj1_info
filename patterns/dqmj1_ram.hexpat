#include "monster.hexpat"

// Need to set base address to 0x02000000
monster party_monsters @ 0x020B3D8C;

u32 rng_counter @ 0x020BEC98;
u32 rng_value @ 0x020BEC9C;

u8 save_file_validation_result @ 0x0219CA9C;

u32 skill_table_pointer @ 0x0218B628;
u8 skill_table @ skill_table_pointer;