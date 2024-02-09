#include "std/mem.pat"

u32 magic @ 0x00;
u8 data[0x1000] @ 0x04;

struct command {
    u32 type;
    u32 length;
    u8 arguments[length - 8];
};

// Commands from end of data section to end of file
command commands[while(!std::mem::eof())] @ 0x1004;