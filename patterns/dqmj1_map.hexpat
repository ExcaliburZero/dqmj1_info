struct map_element {
    u8 unknown[0x28];
};

u32 magic @ 0x00;
u32 header_size @ 0x04;

map_element elements[header_size] @ 0x08;