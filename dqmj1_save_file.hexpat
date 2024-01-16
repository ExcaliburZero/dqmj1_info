u24 magic @ 0x00;
// u32 checksum @ 0x64; // This does not appear to be the checksum
u32 gold @ 0x184; // TODO: confirm size
u32 playtime @ 0x2C; // TODO: confirm extent and format
u32 extra_magic[0x02] @ 0x04;
u32 this_could_be_it_non_binary_checksum_individuals @ 0x0C;