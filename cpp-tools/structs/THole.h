/** @file */
struct THole {
    VMT cls;

    UNK index;
    TStar* star_1;
    _pair_float pos_1;
    TStar* star_2;
    _pair_float pos_2;

    int open_turn;
    int status;
    // 1 - default
    // 2 - КЧД?
    // 3 - кто-то прыгнул
    // 4 - КЧД новая?
    PTR graph;
    _gap _2C;
    _gap _2D;
    _gap _2E;
    _gap _2F;
    STR _30;
};
