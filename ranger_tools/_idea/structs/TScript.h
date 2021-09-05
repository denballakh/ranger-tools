/** @file */
struct TScript {
    __cls* cls;

    int class_;                 ///< "класс" скрипта, прописывается в мейне: myscript=class_,Script.myscript
    STR name;                   ///< название скрипта
    TList* _0C;
    TList* _10;
    TList* _14;
    TList* _18;
    TList* groups;              ///< список групп ({@link TScriptGroup})
    TList* ships;               ///< список скриптовых кораблей ({@link TScriptShip})
    TList* states;              ///< список стейтов ({@link TScriptState})
    TList* _28;                 // списки диалоговых объектов
    TList* _2C;                 // списки диалоговых объектов
    TList* _30;                 // списки диалоговых объектов
    TCodeEC* code_init;         ///< Init-code
    TCodeEC* code_next_turn;    ///< Turn-code
    TCodeEC* code_dialog_begin; ///< DialogBegin-code
    TEther* ether;              ///< Ether? ({@link TEther})
    TShip* cur_ship;
    _gap_32 _48;
    _gap_32 _4C;
    _gap_32 _50;
    _gap_32 _54;
    _gap_32 _58;
    TStringsEC* _5C;
};

struct TScriptShip {
    __cls* cls;

    TScript* script;            ///< скрипт корабля
    int group;                  ///< номер группы корабля
    TShip* ship;                ///< указатель на сам корабль
    dword data[4];              ///< данные, которые можно менять GetData/SetData
    TScriptState* state;        ///< текущий стейт корабля
    WSTR custom_faction;        ///< кастомная фракция
    byte end_order;
    byte hit;
    byte hit_player;
    _gap _0;
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
    TItem* item;                ///< указатель на сам итем
    _gap_32 _2C;
    uint32_t data[3];
    _gap_32 _3C;
    _gap_32 _40;
    _gap_32 _44;
    _gap_32 _48;
    _gap_32 _4C;
    _gap_32 _50;
};

struct TScriptState {
    __cls* cls;

    WSTR name;                  ///< имя стейта
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
    int state;                  ///< дефолтный стейт
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
