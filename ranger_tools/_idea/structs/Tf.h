struct TfScoreUnit {
    __cls* cls;

    byte _04;
    bool _05; // bad flag?
    byte diff[8];
    _gap _0E[2];
    int level;
    STR name;
    int _18;
    byte race;
    _gap _1D;
    _gap _1E;
    _gap _1F;
    int date;
    byte rank;
    byte _25;
    _gap _26;
    _gap _27;
    int _28;
    int _2C;
    int _30;
    int liberation_system;
    int _38;
    int _3C;
    int _40;
    int _44;
    int rewards;
    PTR _4C; // dyn array
    int _50;
    byte skills[6];
    _gap _5A;
    _gap _5B;
    int _5C;
    TBufEC* _60;
    PTR _64; // dyn array
    int _68;
    PTR _6C; // dyn array
    byte _70;
    byte _71;
    byte _72;
    byte _73;
    int score;
    int _78;
};
