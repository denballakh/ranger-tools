struct TMessagePlayer {
    __cls* cls;

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

struct TDemo {
    __cls* cls;
    TBufEC* buf_p;
};

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

/*

TSputnik - 10

TabObject - b0
    TabHit - d0
        TabShip - 2e0
            TabShipAI - 388
    TabWall - e0

    TabItem - c4
    TabW01 - ec
    TabW02 - c4
    TabW03 - bc
    TabW04 - c8
    TabW05 - e4
    TabW06 - c4
    TabW07 - cc
    TabW08 - c4
    TabW09 - c0
    TabW10 - e4
    TabW11 - e4
    TabW12 - cc
    TabW13 - c4
    TabW14 - c0
    TabW15 - c8
    TabW16 - c4
    TabW17 - c4
    TabW18 - cc
TabSpace - 6c


TScript - 60
TEther - 18
TEtherUnit - 14

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
    TGAIEffectSESE - 70
    TMissileSE - 5c
    TGateEffectSE - 5c
    TGateSE - 74


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