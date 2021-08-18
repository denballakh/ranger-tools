struct TScript {
    __cls* cls;

    _gap_32 _04;
    STR script_name;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    TList* groups;
    TList* ships;
    _gap_32 _30;
    _gap_32 _34;
    _gap_32 _38;
    _gap_32 _3C;
    _gap_32 _40;
    _gap_32 _44;
    _gap_32 _48;
    _gap_32 _4C;
    _gap_32 _50;
    _gap_32 _54;
    _gap_32 _58;
    _gap_32 _5C;
};


struct TScriptShip {
    __cls* cls;

    TScript* script;
    int group;
    TShip* ship;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
    WSTR custom_faction;
    _gap_32 _28;
};

struct TScriptPlace {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
    _gap_32 _24;
    _gap_32 _28;
};


struct TScriptItem {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
    _gap_32 _24;
    TItem* item;
    _gap_32 _2C;
    _gap_32 _30;
    _gap_32 _34;
    _gap_32 _38;
    _gap_32 _3C;
    _gap_32 _40;
    _gap_32 _44;
    _gap_32 _48;
    _gap_32 _4C;
    _gap_32 _50;
};

struct TScriptState {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
    _gap_32 _24;
    _gap_32 _28;
    _gap_32 _2C;
    _gap_32 _30;
    _gap_32 _34;
    _gap_32 _38;
    _gap_32 _3C;
};

struct TScriptGroup {
    __cls* cls;

    STR name;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
    _gap_32 _24;
    _gap_32 _28;
    _gap_32 _2C;
    _gap_32 _30;
    _gap_32 _34;
    _gap_32 _38;
    _gap_32 _3C;
    _gap_32 _40;
    _gap_32 _44;
    _gap_32 _48;
    _gap_32 _4C;
    _gap_32 _50;
    _gap_32 _54;
    _gap_32 _58;
    _gap_32 _5C;
    _gap_32 _60;
    _gap_32 _64;
    _gap_32 _68;
    _gap_32 _6C;
};

struct TScriptStar {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
};

struct TScriptConstellation {
    __cls* cls;

    _gap_32 _04;
};

struct TScriptDialog {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
};

struct TScriptDialogMsg {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
};

struct TScriptDialogAnswer {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
};
