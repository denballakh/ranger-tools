struct TItem {
    __cls* cls;

    byte _field_004;
    byte _field_005;
    byte _field_006;
    byte _field_007;
    byte _field_008;
    byte _field_009;
    byte _field_00A;
    byte _field_00B;
    byte item_type;
    byte _field_00D;
    byte _field_00E;
    byte _field_00F;
    byte _field_010;
    byte _field_011;
    byte _field_012;
    byte _field_013;
    byte _field_014;
    byte _field_015;
    byte _field_016;
    byte _field_017;
    byte _field_018;
    byte _field_019;
    byte _field_01A;
    byte _field_01B;
    byte _field_01C;
    byte _field_01D;
    byte _field_01E;
    byte _field_01F;
    byte _field_020;
    byte _field_021;
    byte _field_022;
    byte _field_023;
    byte _field_024;
    byte _field_025;
    byte _field_026;
    byte _field_027;
    byte _field_028;
    byte _field_029;
    byte _field_02A;
    byte _field_02B;
    byte _field_02C;
    byte _field_02D;
    byte _field_02E;
    byte _field_02F;
    byte _field_030;
    byte _field_031;
    byte _field_032;
    byte _field_033;
    byte no_drop;
    byte _field_035;
    byte _field_036;
    byte _field_037;
}; // 38
struct TGoods {
    TItem _;

    byte _field_038;
    byte _field_039;
    byte _field_03A;
    byte _field_03B;
    byte natural;
    byte _field_03D;
    byte _field_03E;
    byte _field_03F;
}; // 40
struct TEquipment {
    TItem _;

    byte _field_038;
    byte _field_039;
    byte _field_03A;
    byte _field_03B;
    UNK custom_faction;
    bool explotable;
    byte _field_041;
    byte _field_042;
    byte _field_043;
    byte _field_044;
    byte _field_045;
    byte _field_046;
    byte _field_047;
    double duration;
    bool broken;
    byte _field_051;
    byte _field_052;
    byte _field_053;
    byte _field_054;
    byte _field_055;
    byte _field_056;
    byte _field_057;
    int bonus;
    int special;
    byte _field_060;
    byte _field_061;
    byte _field_062;
    byte _field_063;
    byte _field_064;
    byte _field_065;
    byte _field_066;
    byte _field_067;
    byte _field_068;
    byte _field_069;
    byte _field_06A;
    byte _field_06B;
}; // 6C
struct THull {
    TEquipment _;

    int hitpoints;
    byte _field_070;
    byte _field_071;
    byte hulltype;
    byte _field_073;
    byte series;
    byte _field_075;
    byte _field_076;
    byte _field_077;
    TShip* ship;
    byte _field_07C;
    byte _field_07D;
    byte _field_07E;
    byte _field_07F;
    byte _field_080;
    byte _field_081;
    byte _field_082;
    byte _field_083;
    byte _field_084;
    byte _field_085;
    byte _field_086;
    byte _field_087;
    byte _field_088;
    byte _field_089;
    byte _field_08A;
    byte _field_08B;
    byte _field_08C;
    byte _field_08D;
    byte _field_08E;
    byte _field_08F;
    byte _field_090;
    byte _field_091;
    byte _field_092;
    byte _field_093;
}; // 94
struct TFuelTanks {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    int fuel;
    int capacity;
    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
}; // 7C
struct TEngine {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
}; // 7C
struct TRadar {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
}; // 78
struct TScaner {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
}; // 74
struct TRepairRobot {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
}; // 74
struct TCargoHook {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
    byte _field_07C;
    byte _field_07D;
    byte _field_07E;
    byte _field_07F;
    byte _field_080;
    byte _field_081;
    byte _field_082;
    byte _field_083;
}; // 84
struct TDefGenerator {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
}; // 78
struct TWeapon {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte level;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
    byte _field_07C;
    byte _field_07D;
    byte _field_07E;
    byte _field_07F;
    byte _field_080;
    byte _field_081;
    byte _field_082;
    byte _field_083;
    byte _field_084;
    byte _field_085;
    byte _field_086;
    byte _field_087;
    byte _field_088;
    byte _field_089;
    byte _field_08A;
    byte _field_08B;
    byte _field_08C;
    byte _field_08D;
    byte _field_08E;
    byte _field_08F;
}; // 90
struct TCountableItem {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte _field_070;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
}; // 78
struct TEquipmentWithActCode {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte _field_070;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
}; // 78
struct TCistern {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    int fuel;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
}; // 78
struct TSatellite {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte _field_070;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
    byte _field_07C;
    byte _field_07D;
    byte _field_07E;
    byte _field_07F;
    byte _field_080;
    byte _field_081;
    byte _field_082;
    byte _field_083;
}; // 84
struct TTreasureMap {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
    byte _field_070;
    byte _field_071;
    byte _field_072;
    byte _field_073;
    byte _field_074;
    byte _field_075;
    byte _field_076;
    byte _field_077;
    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
    byte _field_07C;
    byte _field_07D;
    byte _field_07E;
    byte _field_07F;
}; // 80
struct TMicromodule {
    TEquipment _;

    byte _field_06C;
    byte _field_06D;
    byte _field_06E;
    byte _field_06F;
}; // 70
struct TArtefact {
    TEquipmentWithActCode _;
}; // 78
struct TUselessItem {
    TEquipmentWithActCode _;

    UNK custom_text;
    int data[3];
}; // 88
struct TProtoplasm {
    TCountableItem _;
}; // 78
struct TArtefactTransmitter {
    TArtefact _;

    int power;
}; // 7C
struct TArtefactTranctucator {
    TArtefact _;

    byte _field_078;
    byte _field_079;
    byte _field_07A;
    byte _field_07B;
}; // 7C
struct TArtefactCustom {
    TArtefact _;

    byte _field_07C;
    byte _field_07D;
    byte _field_07E;
    byte _field_07F;
    byte _field_080;
    byte _field_081;
    byte _field_082;
    byte _field_083;
    byte _field_084;
    byte _field_085;
    byte _field_086;
    byte _field_087;
    byte _field_088;
    byte _field_089;
    byte _field_08A;
    byte _field_08B;
    byte _field_08C;
    byte _field_08D;
    byte _field_08E;
    byte _field_08F;
    byte _field_090;
    byte _field_091;
    byte _field_092;
    byte _field_093;
}; // 94
struct TCustomWeapon {
    TWeapon _;

    byte _field_090;
    byte _field_091;
    byte _field_092;
    byte _field_093;
}; // 94

