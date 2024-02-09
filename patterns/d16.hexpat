u32 magic @ 0x00;
u16 width @ 0x04;
u16 height @ 0x06;

// 16bit colors, 0b1BBBBBGGGGGRRRRR
u16 pixels[width * height] @ 0x08;