#pragma array_limit 9999999

struct map_header_element {
    u8 unknown[0x28];
};

u32 magic @ 0x00;
u32 header_size @ 0x04;

map_header_element header[header_size] @ 0x08;


struct map_section {
    /*u32 section_type;
    u8 unknown_1[8];
    u16 length;
    u8 unknown[length - 14];
    u32 full_length;*/
    u32 file_type;
    u32 magic_stamp;
    u32 size;
    u8 data[size - (4 * 3)];
};

map_section sections[5] @ $;


u32 unknown1 @ 0x176D0;
u32 data_length @ $; // TODO: confirm this

struct map_command {
    u8 unknown[0x48];
};

// map_command commands[data_length] @ $;