/** @file */
struct TStarDist {
    int dist;
    TStar* star;
};


struct TPlanetTempl {
    VMT cls;
    int type;
    STR mask_0;
    STR light_0;
    STR mask_1;
    STR light_1;
    int _14;
};


struct TShipGoodsItem {
    int cnt;
    int cost;
    int _8;
    int _C;
};


struct TGoodsShopItem {
    int count;
    float e_price;
    int sell_price;
    int buy_price;
};


struct TGoneItem {
    _pair_byte pos;
    byte terrain_type;
    _gap _3;
    int terrain_needed;
    _gap_32 _8;
    TItem* item;
};


struct TDomResearchProgress {
    float progress;
    int material;
};


struct TGalaxyEvent {
    VMT cls;

    int type;
    int turn;
    TList* data_list;
    TList* text_list;
};


struct TSetItem {
    int a;
    int b;
    word c;
};


struct TMessagePlayer {
    VMT cls;

    _gap_32 _004;
    _gap_32 _008;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
    _gap_32 _018;
    _gap_32 _01C;
    _gap_32 _020;
    _gap_32 _024;
    _gap_32 _028;
    _gap_32 _02C;
    _gap_32 _030;
    _gap_32 _034;
    _gap_32 _038;
    _gap_32 _03C;
};


// struct TDemo {
//     VMT cls;
//     TBufEC* buf_p;
// };


struct TStorageUnit {
    PTR place;
    _gap_32 _004;
    TItem* item;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
    _gap_32 _018;
    _gap_32 _01C;
};


struct TQuestGameContent {};
struct TTextField {};
struct TQuestParameter {};
struct TArrayRectGR {};
struct TShopSlot {};
struct TStoredItem {};
struct TPlayerHoldUnit {};
struct TJournalRecord {}; // 0x0c


struct TPlanetNews {
    int _00;
    int date;
    byte type;
    _gap _09;
    _gap _0A;
    _gap _0B;
    STR text;
};

struct TEther {
    VMT cls;

    _gap_32 _004;
    _gap_32 _008;
    _gap_32 _00C;
    _gap_32 _010;
    _gap_32 _014;
};

struct TCustomShipInfo {
    STR InfoType;
    STR InfoDescription;

    STR InfoData1;
    STR InfoData2;
    STR InfoData3;

    STR InfoTextData1;
    STR InfoTextData2;
    STR InfoTextData3;

    PTR OnActCode;
    bool IsInit;
    bool Delete;
    _gap _[2];
};

struct TPoint {
    int x;
    int y;
};

struct TPos {
    float x;
    float y;
};

struct TRect {
    int x_1;
    int y_1;
    int x_2;
    int y_2;
};

struct TPos_pair {
    TPos p1;
    TPos p2;
};

struct RacesConfig {
    int _0;
    int _1;
    float _2;
    float _3;
    int _4;
    int _5;
    float _6;
    int _7;
};

struct TTextQuest {};

/*

TEther - 18
TEtherUnit - 14

TSputnik - 10




TObjectGI - 11c
    TPSWeaponGI - 130
        TPSWeapon01GI - 14c
        TPSWeapon06GI - 144
        TPSWeapon08GI - 150
        TPSWeapon09GI - 160
        TPSWeapon09BranchGI - 148
        TPSWeapon13GI - 150
        TPSRocketGI - 158
        TPSLBoltGI - 168
        TPSPDWeaponGI - 144
        TPSAcidWeaponGI - 170
        TPSRadEffectGI - 16c
        TPSRayGI - 164
        TPSRailRayGI - 2bc
            TPSBlueWhirlGI - 2c0
            TPSGreenWhirlGI - 2c0
        TPSLaserCannonRayGI - 178
        TPSEyesGI - 15c
        TPSWindGI - 16c
        TPSPhaserGI - 168

*/
