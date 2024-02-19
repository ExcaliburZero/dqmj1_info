u32 magic @ 0x0;
u32 num_files @ 0x4;

struct file {
    u8 unknown[0x20];
    u32 offset;
    u32 size;
};

file files[num_files] @ $;