struct a {
    u8 id;
    u8 unknown[15];
};

u32 magic @ 0x0;
u8 unknown_a[15] @ 0x4;
a unknown_b[4] @ $;
u8 unknown_c @ 0x51;
u8 unknown_d @ 0x84;
u8 unknown_e @ 0x85;