/** @file */
/*
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

*/

struct TabShipWeapon {
    byte type;
    byte item_type;
    _gap _02;
    _gap _03;
    _gap_32 _04;
    int energy_cur;
    int energy_max;
    int energy_inc;
    int energy_dec;
    int takt_last;
    int takt_reload;
    int damage;
    _gap_32 _24;
    int dist_shot;
    float _2C;
};

struct TabObject {
    VMT cls;

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
    _gap_32 _40;
    float _44;
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
    _gap_32 _70;
    _gap_32 _74;
    _gap_32 _78;
    _gap_32 _7C;
    _gap_32 _80;
    _gap_32 _84;
    _gap_32 _88;
    _gap_32 _8C;
    _gap_32 _90;
    _gap_32 _94;
    _gap_32 _98;
    _gap_32 _9C;
    _gap_32 _A0;
    _gap_32 _A4;
    _gap_32 _A8;
    _gap_32 _AC;
};

struct TabHit: TabObject {
    _gap_32 _B0; // HP
    _gap_32 _B4; // max HP
    _gap_32 _B8;
    _gap_32 _BC;
    _gap_32 _C0;
    _gap_32 _C4;
    _gap_32 _C8;
    _gap_32 _CC;
};


struct TabShip: TabHit {
    _gap_32 _0D0;
    _gap_32 _0D4;
    _gap_32 _0D8;
    _gap_32 _0DC;
    TList* _0E0;  // TabShip*
    TList* _0E4;  // TabShip*
    _gap_32 _0E8;
    _gap_32 _0EC;
    double _0F0;
    _gap_32 _0F8;
    _gap_32 _0FC;
    _gap_32 _100;
    _gap_32 _104;

    TabShipWeapon weapons[5];

    _gap_32 _1F8;

    _gap_32 _1FC;
    _gap_32 _200;
    _gap_32 _204;
    _gap_32 _208;
    _gap_32 _20C;
    _gap_32 _210;
    _gap_32 _214;
    _gap_32 _218;
    _gap_32 _21C;
    _gap_32 _220;
    _gap_32 _224;
    _gap_32 _228;
    _gap_32 _22C;
    _gap_32 _230;
    _gap_32 _234;
    _gap_32 _238;
    _gap_32 _23C;
    _gap_32 _240;
    _gap_32 _244;
    _gap_32 _248;
    _gap_32 _24C;
    _gap_32 _250;
    _gap_32 _254;
    _gap_32 _258;
    _gap_32 _25C;
    _gap_32 _260;
    _gap_32 _264;
    _gap_32 _268;
    _gap_32 _26C;
    _gap_32 _270;
    _gap_32 _274;
    _gap_32 _278;
    _gap_32 _27C;
    _gap_32 _280;
    _gap_32 _284;
    _gap_32 _288;
    _gap_32 _28C;
    _gap_32 _290;
    _gap_32 _294;
    _gap_32 _298;
    _gap_32 _29C;
    _gap_32 _2A0;
    _gap_32 _2A4;
    _gap_32 _2A8;
    _gap_32 _2AC;
    _gap_32 _2B0;
    _gap_32 _2B4;
    _gap_32 _2B8;
    _gap_32 _2BC;
    _gap_32 _2C0;
    _gap_32 _2C4;
    _gap_32 _2C8;
    _gap_32 _2CC;
    _gap_32 _2D0;
    _gap_32 _2D4;
    _gap_32 _2D8;
    _gap_32 _2DC;
};

struct TabShipAI: TabShip {
    _gap_32 _2E0;
    _gap_32 _2E4;
    _gap_32 _2E8;
    _gap_32 _2EC;
    _gap_32 _2F0;
    _gap_32 _2F4;
    _gap_32 _2F8;
    _gap_32 _2FC;
    _gap_32 _300;
    _gap_32 _304;
    _gap_32 _308;
    _gap_32 _30C;
    _gap_32 _310;
    _gap_32 _314;
    _gap_32 _318;
    _gap_32 _31C;
    _gap_32 _320;
    _gap_32 _324;
    _gap_32 _328;
    _gap_32 _32C;
    _gap_32 _330;
    _gap_32 _334;
    _gap_32 _338;
    _gap_32 _33C;
    _gap_32 _340;
    _gap_32 _344;
    _gap_32 _348;
    _gap_32 _34C;
    _gap_32 _350;
    _gap_32 _354;
    _gap_32 _358;
    _gap_32 _35C;
    _gap_32 _360;
    _gap_32 _364;
    _gap_32 _368;
    _gap_32 _36C;
    _gap_32 _370;
    _gap_32 _374;
    _gap_32 _378;
    _gap_32 _37C;
    _gap_32 _380;
    _gap_32 _384;
};



struct TabSpace {
    VMT cls;

    _gap_32 _04;
    TabSpace* _08;
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
    float _4C;
    _gap_32 _50;
    _gap_32 _54;
    _gap_32 _58;
    _gap_32 _5C;
    _gap_32 _60;
    _gap_32 _64;
    _gap_32 _68;
};

