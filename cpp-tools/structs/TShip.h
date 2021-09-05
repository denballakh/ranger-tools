/** @file */
struct TShip {
    VMT cls;

    int id;
    STR name;
    WSTR custom_type_name;
    byte type;  // 1 - TRanger, 3 - TPirate
    byte owner;
    _gap _012;
    _gap _013;
    _pair_float pos;
    TPlanet* cur_planet;
    TRuins* cur_ship;
    TStar* cur_star;
    TStar* _028;  // home_star ?
    TPlanet* home_planet;

    TShipGoodsItem goods[8];

    int capital;
    _gap _054;
    _gap _055;
    _gap _056;
    _gap _057;
    _gap _058;
    _gap _059;
    _gap _05A;
    _gap _05B;
    _gap _05C;
    _gap _05D;
    _gap _05E;
    _gap _05F;
    _gap _060;
    _gap _061;
    _gap _062;
    _gap _063;
    _gap _064;
    _gap _065;
    _gap _066;
    _gap _067;
    _gap _068;
    _gap _069;
    _gap _06A;
    _gap _06B;
    _gap _06C;
    _gap _06D;
    _gap _06E;
    _gap _06F;
    _gap _070;
    _gap _071;
    _gap _072;
    _gap _073;
    byte _074;
    _gap _075;
    _gap _076;
    _gap _077;
    _gap _078;
    _gap _079;
    _gap _07A;
    _gap _07B;
    int free_space;
    int rnd_seed;
    _gap _084;
    _gap _085;
    _gap _086;
    _gap _087;
    _gap _088;
    _gap _089;
    _gap _08A;
    _gap _08B;
    _gap _08C;
    _gap _08D;
    _gap _08E;
    _gap _08F;
    _gap _090;
    _gap _091;
    _gap _092;
    _gap _093;
    _gap _094;
    _gap _095;
    _gap _096;
    _gap _097;
    THull* hull;
    _gap _09C;
    _gap _09D;
    _gap _09E;
    _gap _09F;
    _gap _0A0;
    _gap _0A1;
    _gap _0A2;
    _gap _0A3;
    _gap _0A4;
    _gap _0A5;
    _gap _0A6;
    _gap _0A7;
    _gap _0A8;
    _gap _0A9;
    _gap _0AA;
    _gap _0AB;
    _gap _0AC;
    _gap _0AD;
    _gap _0AE;
    _gap _0AF;
    _gap_32 _B0;
    TWeapon* weapons[6];
    byte weapon_cnt;
    _gap _0CD;

    byte skills[6];

    _gap _0D4;
    _gap _0D5;
    _gap _0D6;
    _gap _0D7;
    _gap _0D8;
    _gap _0D9;
    _gap _0DA;
    _gap _0DB;
    int _0DC;
    _gap _0E0;
    _gap _0E1;
    _gap _0E2;
    _gap _0E3;
    _gap _0E4;
    _gap _0E5;
    _gap _0E6;
    _gap _0E7;
    _gap _0E8;
    _gap _0E9;
    _gap _0EA;
    _gap _0EB;
    _gap _0EC;
    _gap _0ED;
    _gap _0EE;
    _gap _0EF;
    int money;
    int group_no;  ///< номер группы, но не скриптовой? Используется в военных операциях
    _gap_32 _0F8;
    _gap_32 _0FC;
    _gap _100;
    _gap _101;
    _gap _102;
    _gap _103;
    _gap _104;
    _gap _105;
    _gap _106;
    _gap _107;
    _gap _108;
    _gap _109;
    _gap _10A;
    _gap _10B;
    _gap _10C;
    _gap _10D;
    _gap _10E;
    _gap _10F;
    _gap _110;
    _gap _111;
    _gap _112;
    _gap _113;
    _gap _114;
    _gap _115;
    _gap _116;
    _gap _117;
    _gap _118;
    _gap _119;
    _gap _11A;
    _gap _11B;
    _gap _11C;
    _gap _11D;
    _gap _11E;
    _gap _11F;
    _gap _120;
    _gap _121;
    _gap _122;
    _gap _123;
    _gap _124;
    _gap _125;
    _gap _126;
    _gap _127;
    _gap _128;
    _gap _129;
    _gap _12A;
    _gap _12B;
    _gap _12C;
    _gap _12D;
    _gap _12E[6];
    _gap _134;
    _gap _135;
    _gap _136;
    _gap _137;
    _gap _138;
    _gap _139;
    _gap _13A;
    _gap _13B;
    _gap _13C;
    _gap _13D;
    _gap _13E;
    _gap _13F;
    _gap _140;
    _gap _141;
    _gap _142;
    _gap _143;
    _gap _144;
    _gap _145;
    _gap _146;
    _gap _147;
    _gap _148;
    _gap _149;
    _gap _14A;
    _gap _14B;
    _gap _14C;
    _gap _14D;
    _gap _14E;
    _gap _14F;
    _gap _150;
    _gap _151;
    _gap _152;
    _gap _153;
    _gap _154;
    _gap _155;
    UNK fly_to_star;
    _gap _15A;
    _gap _15B;
    _gap _15C;
    _gap _15D;
    _gap _15E;
    _gap _15F;
    _gap _160;
    _gap _161;
    _gap _162;
    _gap _163;
    _gap _164;
    _gap _165;
    _gap _166;
    _gap _167;
    _gap _168;
    _gap _169;
    _gap _16A;
    _gap _16B;
    _gap _16C;
    _gap _16D;
    _gap _16E;
    _gap _16F;
    _gap _170;
    _gap _171;
    _gap _172;
    _gap _173;
    _gap _174;
    _gap _175;
    _gap _176;
    _gap _177;
    _gap _178;
    _gap _179;
    _gap _17A;
    _gap _17B;
    _gap _17C;
    _gap _17D;
    _gap _17E;
    _gap _17F;
    _gap _180;
    _gap _181;
    _gap _182;
    _gap _183;
    _gap _184;
    _gap _185;
    _gap _186;
    _gap _187;
    _gap _188;
    _gap _189;
    _gap _18A;
    _gap _18B;
    _gap _18C;
    _gap _18D;
    _gap _18E;
    _gap _18F;
    _gap _190;
    _gap _191;
    _gap _192;
    _gap _193;
    _gap _194;
    _gap _195;
    _gap _196;
    _gap _197;
    _gap _198;
    _gap _199;
    _gap _19A;
    _gap _19B;
    _gap _19C;
    _gap _19D;
    _gap _19E;
    _gap _19F;
    _gap _1A0;
    _gap _1A1;
    _gap _1A2;
    _gap _1A3;
    _gap _1A4;
    _gap _1A5;
    _gap _1A6;
    _gap _1A7;
    _gap _1A8;
    _gap _1A9;
    _gap _1AA;
    _gap _1AB;
    _gap _1AC;
    _gap _1AD;
    _gap _1AE;
    _gap _1AF;
    _gap _1B0;
    _gap _1B1;
    _gap _1B2;
    _gap _1B3;
    _gap _1B4;
    _gap _1B5;
    _gap _1B6;
    _gap _1B7;
    _gap _1B8;
    _gap _1B9;
    _gap _1BA;
    _gap _1BB;
    _gap _1BC;
    _gap _1BD;
    _gap _1BE;
    _gap _1BF;
    _gap _1C0;
    _gap _1C1;
    _gap _1C2;
    _gap _1C3;
    _gap _1C4;
    _gap _1C5;
    _gap _1C6;
    _gap _1C7;
    _gap _1C8;
    _gap _1C9;
    _gap _1CA;
    _gap _1CB;
    _gap _1CC;
    _gap _1CD;
    _gap _1CE;
    _gap _1CF;
    _gap _1D0;
    _gap _1D1;
    _gap _1D2;
    _gap _1D3;
    _gap _1D4;
    _gap _1D5;
    _gap _1D6;
    _gap _1D7;
    _gap _1D8;
    _gap _1D9;
    _gap _1DA;
    _gap _1DB;
    _gap _1DC;
    _gap _1DD;
    _gap _1DE;
    _gap _1DF;
    _gap _1E0;
    _gap _1E1;
    _gap _1E2;
    _gap _1E3;
    _gap _1E4;
    _gap _1E5;
    _gap _1E6;
    _gap _1E7;
    _gap _1E8;
    _gap _1E9;
    _gap _1EA;
    _gap _1EB;
    _gap _1EC;
    _gap _1ED;
    _gap _1EE;
    _gap _1EF;
    _gap _1F0;
    _gap _1F1;
    _gap _1F2;
    _gap _1F3;
    _gap _1F4;
    _gap _1F5;
    _gap _1F6;
    _gap _1F7;
    _gap _1F8;
    _gap _1F9;
    _gap _1FA;
    _gap _1FB;
    _gap _1FC;
    _gap _1FD;
    _gap _1FE;
    _gap _1FF;
    _gap _200;
    _gap _201;
    _gap _202;
    _gap _203;
    _gap _204;
    _gap _205;
    _gap _206;
    _gap _207;
    _gap _208;
    _gap _209;
    _gap _20A;
    _gap _20B;
    _gap _20C;
    _gap _20D;
    _gap _20E;
    _gap _20F;
    _gap _210;
    _gap _211;
    _gap _212;
    _gap _213;
    _gap _214;
    _gap _215;
    _gap _216;
    _gap _217;
    _gap _218;
    _gap _219;
    _gap _21A;
    _gap _21B;
    _gap _21C;
    _gap _21D;
    _gap _21E;
    _gap _21F;
    _gap _220;
    _gap _221;
    _gap _222;
    _gap _223;
    _gap _224;
    _gap _225;
    _gap _226;
    _gap _227;
    _gap _228;
    _gap _229;
    _gap _22A;
    _gap _22B;
    _gap _22C;
    _gap _22D;
    _gap _22E;
    _gap _22F;
    _gap _230;
    _gap _231;
    _gap _232;
    _gap _233;
    _gap _234;
    _gap _235;
    _gap _236;
    _gap _237;
    _gap _238;
    _gap _239;
    _gap _23A;
    _gap _23B;
    _gap _23C;
    _gap _23D;
    _gap _23E;
    _gap _23F;
    _gap _240;
    _gap _241;
    _gap _242;
    _gap _243;
    _gap _244;
    _gap _245;
    _gap _246;
    _gap _247;
    _gap _248;
    _gap _249;
    _gap _24A;
    _gap _24B;
    _gap _24C;
    _gap _24D;
    _gap _24E;
    _gap _24F;
    _gap _250;
    _gap _251;
    _gap _252;
    _gap _253;
    _gap _254;
    _gap _255;
    _gap _256;
    _gap _257;
    _gap _258;
    _gap _259;
    _gap _25A;
    _gap _25B;
    _gap _25C;
    _gap _25D;
    _gap _25E;
    _gap _25F;
    _gap _260;
    _gap _261;
    _gap _262;
    _gap _263;
    _gap _264;
    _gap _265;
    _gap _266;
    _gap _267;
    _gap _268;
    _gap _269;
    _gap _26A;
    _gap _26B;
    _gap _26C;
    _gap _26D;
    _gap _26E;
    _gap _26F;
    _gap _270;
    _gap _271;
    _gap _272;
    _gap _273;
    _gap _274;
    _gap _275;
    _gap _276;
    _gap _277;
    _gap _278;
    _gap _279;
    _gap _27A;
    _gap _27B;
    _gap _27C;
    _gap _27D;
    _gap _27E;
    _gap _27F;
    _gap _280;
    _gap _281;
    _gap _282;
    _gap _283;
    _gap _284;
    _gap _285;
    _gap _286;
    _gap _287;
    _gap _288;
    _gap _289;
    _gap _28A;
    _gap _28B;
    _gap _28C;
    _gap _28D;
    _gap _28E;
    _gap _28F;
    _gap _290;
    _gap _291;
    _gap _292;
    _gap _293;
    _gap _294;
    _gap _295;
    _gap _296;
    _gap _297;
    _gap _298;
    _gap _299;
    _gap _29A;
    _gap _29B;
    _gap _29C;
    _gap _29D;
    _gap _29E;
    _gap _29F;
    _gap _2A0;
    _gap _2A1;
    _gap _2A2;
    _gap _2A3;
    _gap _2A4;
    _gap _2A5;
    _gap _2A6;
    _gap _2A7;
    _gap _2A8;
    _gap _2A9;
    _gap _2AA;
    _gap _2AB;
    _gap _2AC;
    _gap _2AD;
    _gap _2AE;
    _gap _2AF;
    _gap _2B0;
    _gap _2B1;
    _gap _2B2;
    _gap _2B3;
    _gap _2B4;
    _gap _2B5;
    _gap _2B6;
    _gap _2B7;
    _gap _2B8;
    _gap _2B9;
    _gap _2BA;
    _gap _2BB;
    _gap _2BC;
    _gap _2BD;
    _gap _2BE;
    _gap _2BF;
    _gap _2C0;
    _gap _2C1;
    _gap _2C2;
    _gap _2C3;
    _gap _2C4;
    _gap _2C5;
    _gap _2C6;
    _gap _2C7;
    _gap _2C8;
    _gap _2C9;
    _gap _2CA;
    _gap _2CB;
    _gap _2CC;
    _gap _2CD;
    _gap _2CE;
    _gap _2CF;
    _gap _2D0;
    _gap _2D1;
    _gap _2D2;
    _gap _2D3;
    _gap _2D4;
    _gap _2D5;
    _gap _2D6;
    _gap _2D7;
    _gap _2D8;
    _gap _2D9;
    _gap _2DA;
    _gap _2DB;
    _gap _2DC;
    _gap _2DD;
    _gap _2DE;
    _gap _2DF;
    _gap _2E0;
    _gap _2E1;
    _gap _2E2;
    _gap _2E3;
    _gap _2E4;
    _gap _2E5;
    _gap _2E6;
    _gap _2E7;
    _gap _2E8;
    _gap _2E9;
    _gap _2EA;
    _gap _2EB;
    _gap _2EC;
    _gap _2ED;
    _gap _2EE;
    _gap _2EF;
    _gap _2F0;
    _gap _2F1;
    _gap _2F2;
    _gap _2F3;
    _gap _2F4;
    _gap _2F5;
    _gap _2F6;
    _gap _2F7;
    _gap _2F8;
    _gap _2F9;
    _gap _2FA;
    _gap _2FB;
    _gap _2FC;
    _gap _2FD;
    _gap _2FE;
    _gap _2FF;
    _gap _300;
    _gap _301;
    _gap _302;
    _gap _303;
    _gap _304;
    _gap _305;
    _gap _306;
    _gap _307;
    _gap _308;
    _gap _309;
    _gap _30A;
    _gap _30B;
    _gap _30C;
    _gap _30D;
    _gap _30E;
    _gap _30F;
    _gap _310;
    _gap _311;
    _gap _312;
    _gap _313;
    _gap _314;
    _gap _315;
    _gap _316;
    _gap _317;
    _gap_32 _318;
    _gap_32 _31C;
    _gap _320;
    _gap _321;
    _gap _322;
    _gap _323;
    _gap_32 _324;
    _gap _328;
    _gap _329;
    _gap _32A;
    _gap _32B;
    _gap _32C;
    _gap _32D;
    _gap _32E;
    _gap _32F;
    TList* custom_ship_infos;
    _gap _334;
    _gap _335;
    _gap _336;
    _gap _337;
    _gap _338;
    _gap _339;
    _gap _33A;
    _gap _33B;
    _gap _33C;
    _gap _33D;
    _gap _33E;
    _gap _33F;
    byte ship_tech_level_knowledge;
    _gap _3A1;
    _gap _3A2;
    _gap _3A3;
    STR face_;
    int points;
    int free_points;
    _gap _3B0;
    _gap _3B1;
    _gap _3B2;
    _gap _3B3;
    _gap _3B4;
    _gap _3B5;
    _gap _3B6;
    _gap _3B7;
    TList* equipments;
    TList* artefacts;
    TList* drop_items;
    TList* _3C4;
    TScriptShip* script_ship;
    _gap_32 _3CC;
    _gap _3D0;
    _gap _3D1;
    _gap _3D2;
    _gap _3D3;
    _gap _3D4;
    _gap _3D5;
    _gap _3D6;
    _gap _3D7;
    TList* _3D8;
    TList* recently_dropped_items;
    _gap _3E0;
    _gap _3E1;
    _gap _3E2;
    _gap _3E3;
    TList* _3E4;
    TList* rewards;
    int _3EC;
    TList* relation_to_rangers;
    TShip* ship_bad;
    TShip* _3F8;
    TShip* partner;
    int contract_days;
    STR face;
    byte pilot_race;
    _gap _409;
    _gap _40A;
    _gap _40B;
    _gap _40C;
    _gap _40D;
    _gap _40E;
    _gap _40F;
    _gap _410;
    _gap _411;
    _gap _412;
    _gap _413;
    _gap _414;
    _gap _415;
    _gap _416;
    _gap _417;
    _gap _418;
    _gap _419;
    _gap _41A;
    _gap _41B;
    _gap _41C;
    _gap _41D;
    _gap _41E;
    _gap _41F;
    _gap _420;
    _gap _421;
    _gap _422;
    _gap _423;
    _gap _424;
    _gap _425;
    _gap _426;
    _gap _427;
    byte order;
    _gap _429;
    _gap _42A;
    _gap _42B;
    _gap_32 _42C;  // связано с приказом
    TStar* dest_obj;
    _pair_float dest_pos;
    _gap _43C;  // связано с приказом
    _gap _43D;
    _gap _43E;
    _gap _43F;
    _gap _440;
    _gap _441;
    _gap _442;
    _gap _443;
    _gap _444;
    _gap _445;
    _gap _446;
    _gap _447;
    _gap _448;
    _gap _449;
    _gap _44A;
    _gap _44B;
    byte script_order_absolute;
    _gap _44D;
    _gap _44E;
    _gap _44F;
    PTR graph_ship;
    STR skin;  // или строка шкурки, или объект SE
    _gap _458;
    byte in_hyper_space;
    _gap _45A;
    _gap _45B;
    _gap _45C;
    _gap _45D;
    _gap _45E;
    _gap _45F;
    _gap _460;  // destroy=true
    _gap _461;
    _gap _462;
    _gap _463;
    _gap _464;
    _gap _465;
    _gap _466;
    _gap _467;
    _gap _468;
    _gap _469;
    _gap _46A;
    _gap _46B;
    _gap _46C;
    _gap _46D;
    _gap _46E;
    _gap _46F;
    _gap _470;
    _gap _471;
    _gap _472;
    _gap _473;
    _gap _474;
    _gap _475;
    _gap _476;
    _gap _477;
    _gap _478;
    _gap _479;
    _gap _47A;
    _gap _47B;
    _gap _47C;
    _gap _47D;
    _gap _47E;
    _gap _47F;
    _gap _480;
    _gap _481;
    _gap _482;
    _gap _483;
    _gap _484;
    _gap _485;
    _gap _486;
    _gap _487;
    _gap _488;
    _gap _489;
    _gap _48A;
    _gap _48B;
    _gap _48C;
    _gap _48D;
    _gap _48E;
    _gap _48F;
    int money_xored;  // money ^ 0xA4A576AD
    _gap _494;
    _gap _495;
    _gap _496;
    _gap _497;
    bool no_drop;
    bool no_target;
    bool no_talk;
    bool no_scan;
    _gap _49C;
    _gap _49D;
    _gap _49E;
    _gap _49F;
    _gap _4A0;
    _gap _4A1;
    _gap _4A2;
    _gap _4A3;
    TShip* _4A4;
    _gap _4A8;
    _gap _4A9;
    _gap _4AA;
    _gap _4AB;
    _gap _4AC;
    _gap _4AD;
    _gap _4AE;
    _gap _4AF;

    byte cur_standing;
    _gap _4B1;
    _gap _4B2;
    _gap _4B3;

    float _4B4[7];
};

struct TRuins: public TShip {
    TList* equipment_shop;
    _gap _4D4;
    _gap _4D5;
    _gap _4D6;
    _gap _4D7;
    _gap _4D8;
    _gap _4D9;
    _gap _4DA;
    _gap _4DB;
    _gap _4DC;
    _gap _4DD;
    _gap _4DE;
    _gap _4DF;
    _gap _4E0;
    _gap _4E1;
    _gap _4E2;
    _gap _4E3;
    _gap _4E4;
    _gap _4E5;
    _gap _4E6;
    _gap _4E7;
    _gap _4E8;
    _gap _4E9;
    _gap _4EA;
    _gap _4EB;
    _gap _4EC;
    _gap _4ED;
    _gap _4EE;
    _gap _4EF;
    _gap _4F0;
    _gap _4F1;
    _gap _4F2;
    _gap _4F3;
    _gap _4F4;
    _gap _4F5;
    _gap _4F6;
    _gap _4F7;
    _gap _4F8;
    _gap _4F9;
    _gap _4FA;
    _gap _4FB;
    _gap _4FC;
    _gap _4FD;
    _gap _4FE;
    _gap _4FF;
    _gap _500;
    _gap _501;
    _gap _502;
    _gap _503;
    _gap _504;
    _gap _505;
    _gap _506;
    _gap _507;
    _gap _508;
    _gap _509;
    _gap _50A;
    _gap _50B;
    _gap _50C;
    _gap _50D;
    _gap _50E;
    _gap _50F;
    _gap _510;
    _gap _511;
    _gap _512;
    _gap _513;
    _gap _514;
    _gap _515;
    _gap _516;
    _gap _517;
    _gap _518;
    _gap _519;
    _gap _51A;
    _gap _51B;
    _gap _51C;
    _gap _51D;
    _gap _51E;
    _gap _51F;
    _gap _520;
    _gap _521;
    _gap _522;
    _gap _523;
    _gap _524;
    _gap _525;
    _gap _526;
    _gap _527;
    _gap _528;
    _gap _529;
    _gap _52A;
    _gap _52B;
    _gap _52C;
    _gap _52D;
    _gap _52E;
    _gap _52F;
    _gap _530;
    _gap _531;
    _gap _532;
    _gap _533;
    _gap _534;
    _gap _535;
    _gap _536;
    _gap _537;
    _gap _538;
    _gap _539;
    _gap _53A;
    _gap _53B;
    _gap _53C;
    _gap _53D;
    _gap _53E;
    _gap _53F;
    _gap _540;
    _gap _541;
    _gap _542;
    _gap _543;
    _gap _544;
    _gap _545;
    _gap _546;
    _gap _547;
    _gap _548;
    _gap _549;
    _gap _54A;
    _gap _54B;
    _gap _54C;
    _gap _54D;
    _gap _54E;
    _gap _54F;
    _gap _550;
    _gap _551;
    _gap _552;
    _gap _553;
    float _554;
    TStar* dest_star;
    _gap _55C;
    _gap _55D;
    _gap _55E;
    _gap _55F;
    TSatellite* _560;
    byte _564;
    byte _565;
    byte _566;
    byte _567;
};

struct TTranclucator: public TShip {
    float _4D0;
    STR _4D4;
    TShip* proprietor;
    _gap _4DC;
    _gap _4DD;
    _gap _4DE;
    _gap _4DF;
    _gap _4E0;
    _gap _4E1;
    _gap _4E2;
    _gap _4E3;
    _gap _4E4;
    _gap _4E5;
    _gap _4E6;
    _gap _4E7;
    _gap _4E8;
    _gap _4E9;
    _gap _4EA;
    _gap _4EB;
};

struct TKling: public TShip {
    byte sub_type;
    byte _4D1;
    _gap _4D2;
    _gap _4D3;
    int _4D4;
    byte _4D8;
    byte _4D9;
    _gap _4DA;
    _gap _4DB;
};

struct TNormalShip: public TShip {
    TPlanet* _4D0;
    _gap_32 _4D4;
    _gap_32 _4D8;
    _gap_32 _4DC;
    _gap_32 _4E0;
    _gap_32 _4E4;
    _gap_32 _4E8;
    _gap_32 _4EC;
    word _4F0;
    word _4F2;
    word _4F4;
    word _4F6;
    TPlanet* _4F8;
    float _4FC;
    _gap _500;  // rank?
    _gap _501;
    _gap _502;
    _gap _503;
    _gap_32 _504;
    _gap_32 _508;
    _gap_32 _50C;
};

struct TPirate: public TNormalShip {
    byte in_prison;
    _gap _511;
    _gap _512;
    _gap _513;
    byte sub_type;
    _gap _515;
    _gap _516;
    _gap _517;
    _gap_32 _518;
};

struct TWarrior: public TNormalShip {
    byte sub_type;
    _gap _511;
    _gap _512;
    _gap _513;
};

struct TTransport: public TNormalShip {
    byte sub_type;
    _gap _511;
    _gap _512;
    _gap _513;
};

struct TRanger: public TNormalShip {
    _gap_16 _510;
    _gap _512;
    byte status[3];
    _gap _516;
    _gap _517;
    _gap _518;
    _gap _519;
    _gap _51A;
    _gap _51B;
    _gap _51C;
    _gap _51D;
    _gap _51E;
    _gap _51F;
    TList* _520;
    byte in_prison;
    _gap _525;
    _gap _526;
    _gap _527;
    TShip* _528;
    int base_nod_cur;
    int programs[12];
};

