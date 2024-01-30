#include "monster.hexpat"

u24 magic @ 0x00;
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;

u32 playtime @ 0x2C; // TODO: confirm extent and format
u8 player_name[0x06] @ 0x32; // TODO: confirm extent
u32 gold @ 0x184; // TODO: confirm size
u32 atm @ 0x188;

u32 num_times_synthesized @ 0x3D8;

monster first_monster @ 0x65C;
monster second_monster @ 0x7F0;
monster third_monster @ 0x984;

// Probably the versions displayed on the save file window when starting the game
u8 first_party_monster_name[9] @ 0x3E;
u8 second_party_monster_name[9] @ 0x4A;
u8 third_party_monster_name[9] @ 0x56;