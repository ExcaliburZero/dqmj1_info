#include "monster.hexpat"

u24 magic @ 0x00;
u32 extra_magic[0x02] @ 0x04;
u32 checksum @ 0x0C;

u32 playtime @ 0x2C; // TODO: confirm extent and format
u8 player_name[0x06] @ 0x32; // TODO: confirm extent
u32 gold @ 0x184; // TODO: confirm size
u32 atm @ 0x188;

monster first_monster @ 0x65C;
monster second_monster @ 0x7F0;
monster third_monster @ 0x984;