/*

TSpaceSE - 6c
TProcessSE - 50
TObjectSE - 4c
    TStarSE - 78
    TMeteoriteSE - 64
    TAngelSE - bc
    TCometSE - 120
    TBGObjSE - 58
    TAnimSE - 68
    TLaserSE - 78
    TStarFieldSE - 58
    TShip2SE - 1ac
    TShip2AnimSE - 1c
    TPlanetSE - 138
    TContainerSE - 5c
    THoleSE - 68
    TSputnikSE - b4
    TAsteroidSE - 60
    TRuinsSE - d4
    TWeaponSE - d8
    TGAIEffectSE - 70
    TMissileSE - 5c
    TGateEffectSE - 5c
    TGateSE - 74

*/

struct TObjectSE {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    STR type;
    _gap_32 _1C;
    _gap_32 _20;
    _gap_32 _24;
    _gap_32 _28;
    STR _2C;
    STR _30;
    _gap_32 _34;
    PTR _38;  // TSoundBufferControl
    _gap_32 _3C;
    _gap_32 _40;
    _gap_32 _44;
    _gap_32 _48;
};
