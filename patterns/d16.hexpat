struct pixel {
    // 16bit color, 0b1BBBBBGGGGGRRRRR
    u16 color;
};

struct d16 {
    u32 magic;
    u16 width;
    u16 height;
    pixel pixels[width * height];
};

d16 d16 @ 0x0;