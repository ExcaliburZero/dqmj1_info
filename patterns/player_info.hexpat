
struct name {
    u8 name[9];
    u8 unknown_a[3];
};

struct player_info {
    name name;
    u32 gold;
    u32 atm;
    u8 items_in_hand[16];
    u8 item_in_bag_counts[256];
    u8 num_darkonium_times_5;
    u8 unknown_b[3];
    u32 playtime;
    u8 num_party_monsters;
    u8 num_monsters;
    u8 unknown_c[306];
    u32 num_times_synthesized;
    u8 unknown[640];
};