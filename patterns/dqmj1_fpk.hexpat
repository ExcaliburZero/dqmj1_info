struct file {
    u8 name_info[0x20];
    u32 offset;
    u32 size;
    u8 data[size] @ offset;
};

struct fpk {
    u32 magic;
    u32 num_files;
    file files[num_files];  
};

fpk fpk @ 0x0;