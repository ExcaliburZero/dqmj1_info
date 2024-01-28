#include "monster.hexpat"

// Note all these byte positions are 0x02000000 off from their locations when running the game
monster party_monsters @ 0x000B3D8C;

u32 rng_counter @ 0xBEC98;
u32 rng_value @ 0xBEC9C;

u8 save_file_validation_result @ 0x19CA9C;