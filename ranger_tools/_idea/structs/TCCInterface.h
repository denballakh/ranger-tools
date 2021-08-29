struct TCCInterface {
    __cls* cls;

    TBufEC* buf;
    TCCInterface_El* data;
    PTR critical_section;
};

struct TCBufControlEC {
    __cls* cls;

    _gap_32 _004;
    _gap_32 _008;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
}; // 0x18

struct TCCInterface_El {
    __cls* cls;

    TCCInterface_El* next;
    bool bad_file_crack;
    bool money_crack;
    _gap _gap_0A; // мусор?
    _gap _0B;
    _gap_32 _0C; // RandInt(0, 2000000000)
    _gap_32 _gap_10; // мусор?
    _gap_32 _14;
    _gap_32 _18; // val + 1000000 * {0,1,2}
    _gap_32 _1C; // мусор? = 0xFFFFFFFF
    _gap_32 _20; // мусор? = 0xFFFFFFFF
    _gap_32 _24; // мусор? = 0xFFFFFFFF
    _gap_32 _28; // мусор? = 0xFFFFFFFF
    bool dump_crack;
    _gap _2D;
    _gap _2E;
    _gap _2F;
};
