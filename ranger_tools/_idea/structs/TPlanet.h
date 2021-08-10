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

struct TPlanet {
    __cls* cls;

    _gap _004;
    _gap _005;
    _gap _006;
    _gap _007;
    _gap _008;
    _gap _009;
    _gap _00A;
    _gap _00B;
    _gap _00C;
    _gap _00D;
    _gap _00E;
    _gap _00F;
    int graph_no;
    _gap _014;
    _gap _015;
    _gap _016;
    _gap _017;
    TStar* star;
    _gap _01C;
    _gap _01D;
    _gap _01E;
    _gap _01F;
    _pair_double polar_pos;
    _gap _030;
    _gap _031;
    _gap _032;
    _gap _033;
    _gap _034;
    _gap _035;
    _gap _036;
    _gap _037;
    int radius;
    _gap _03C;
    _gap _03D;
    _gap _03E;
    _gap _03F;
    double angle_speed;
    byte invention_levels[1]; // точное кол-во уровней не знаю, оставлю пока 1
    _gap _049;
    _gap _04A;
    _gap _04B;
    _gap _04C;
    _gap _04D;
    _gap _04E;
    _gap _04F;
    _gap _050;
    _gap _051;
    _gap _052;
    _gap _053;
    _gap _054;
    _gap _055;
    _gap _056;
    _gap _057;
    _gap _058;
    _gap _059;
    _gap _05A;
    _gap _05B;
    byte cur_invention;
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
    int population;
    byte eco;
    _gap _06D;
    _gap _06E;
    _gap _06F;
    _gap _070;
    _gap _071;
    _gap _072;
    _gap _073;
    byte owner;
    _gap _075;
    byte race;
    byte gov;
    _gap _078;
    _gap _079;
    _gap _07A;
    _gap _07B;
    _gap _07C;
    _gap _07D;
    _gap _07E;
    _gap _07F;
    _gap _080;
    _gap _081;
    _gap _082;
    _gap _083;
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
    _gap _098;
    _gap _099;
    _gap _09A;
    _gap _09B;
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
    _gap _0B0;
    _gap _0B1;
    _gap _0B2;
    _gap _0B3;
    _gap _0B4;
    _gap _0B5;
    _gap _0B6;
    _gap _0B7;
    _gap _0B8;
    _gap _0B9;
    _gap _0BA;
    _gap _0BB;
    _gap _0BC;
    _gap _0BD;
    _gap _0BE;
    _gap _0BF;
    _gap _0C0;
    _gap _0C1;
    _gap _0C2;
    _gap _0C3;
    _gap _0C4;
    _gap _0C5;
    _gap _0C6;
    _gap _0C7;
    _gap _0C8;
    _gap _0C9;
    _gap _0CA;
    _gap _0CB;
    _gap _0CC;
    _gap _0CD;
    _gap _0CE;
    _gap _0CF;
    _gap _0D0;
    _gap _0D1;
    _gap _0D2;
    _gap _0D3;
    _gap _0D4;
    _gap _0D5;
    _gap _0D6;
    _gap _0D7;
    _gap _0D8;
    _gap _0D9;
    _gap _0DA;
    _gap _0DB;
    _gap _0DC;
    _gap _0DD;
    _gap _0DE;
    _gap _0DF;
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
    _gap _0F0;
    _gap _0F1;
    _gap _0F2;
    _gap _0F3;
    _gap _0F4;
    _gap _0F5;
    _gap _0F6;
    _gap _0F7;
    _gap _0F8;
    _gap _0F9;
    _gap _0FA;
    _gap _0FB;
    _gap _0FC;
    _gap _0FD;
    _gap _0FE;
    _gap _0FF;
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
    TList* relation_to_rangers;
    TList* equipment_shop;
    _gap_32 _114;
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
    _gap_32 _128;
    int water_total;
    int water_complate;
    int land_total;
    int land_complate;
    int hill_total;
    int hill_complate;
    _gap_32 _144;
    TList* gone_items;
    int graph_radius;
    PTR graph_planet;
    WSTR graph_name;

    _gap _158;
    _gap _159;
    _gap _15A;
    _gap _15B;
    _gap_32 _15C;
    _gap_32 _160;// UNK size;
    _gap_32 _164;// PTR graph;
    byte no_landing;
    byte no_shopupdate;
    _gap _16A;
    _gap _16B;
}; // 16C
