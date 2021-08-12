struct TItem {
    __cls* cls;

    UNK _04; // появляется в космосе
    int index;
    byte item_type;
    _gap _0D;
    _gap _0E;
    _gap _0F;
    _pair_float pos;
    int size;
    byte race;
    _gap _1D;
    _gap _1E;
    _gap _1F;

    int cost;
    _gap_32 _24; // связь со скриптовыми предметами?
    _gap _28;
    _gap _29;
    _gap _2A;
    _gap _2B;
    PTR script_item;
    _gap _30;
    _gap _31;
    _gap _32;
    _gap _33;
    byte no_drop;
    _gap _35;
    _gap _36;
    _gap _37;
}; // 38

struct TGoods {
    TItem;

    _gap _38;
    _gap _39;
    _gap _3A;
    _gap _3B;
    byte natural;
    _gap _3D;
    _gap _3E;
    _gap _3F;
}; // 40

struct TEquipment {
    TItem;

    _gap _38;
    _gap _39;
    _gap _3A;
    _gap _3B;
    WSTR custom_faction;
    bool explotable;
    _gap _41;
    _gap _42;
    _gap _43;
    _gap _44;
    _gap _45;
    _gap _46;
    _gap _47;
    double duration;
    bool broken;
    _gap _51;
    _gap _52;
    _gap _53;
    _gap _54;
    _gap _55;
    _gap _56;
    _gap _57;
    int bonus;
    int special;
    int* weapon_info;
    _gap _64;
    _gap _65;
    _gap _66;
    _gap _67;
    _gap _68;
    _gap _69;
    _gap _6A;
    _gap _6B;
}; // 6C

struct THull {
    TEquipment;

    int hitpoints;
    byte tech_level;
    byte hit_protect;
    byte hull_type;
    _gap _73;
    int series;
    TShip* ship;
    _gap _7C;
    _gap _7D;
    _gap _7E;
    _gap _7F;
    _gap_32 _80;
    _gap_32 _84;
    _gap_32 _88;
    _gap _8C;
    _gap _8D;
    _gap _8E;
    _gap _8F;
    _gap _90;
    _gap _91;
    _gap _92;
    _gap _93;
}; // 94

struct TFuelTanks {
    TEquipment;

    byte tech_level;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    int fuel;
    byte capacity;
    _gap _75;
    _gap _76;
    _gap _77;
    _gap _78;
    _gap _79;
    _gap _7A;
    _gap _7B;
}; // 7C

struct TEngine {
    TEquipment;

    byte tech_level;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    int speed;
    byte parsec;
    _gap _75;
    _gap _76;
    _gap _77;
    _gap _78;
    _gap _79;
    _gap _7A;
    _gap _7B;
}; // 7C

struct TRadar {
    TEquipment;

    byte tech_level;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    int radius;
    _gap _74;
    _gap _75;
    _gap _76;
    _gap _77;
}; // 78

struct TScaner {
    TEquipment;

    byte tech_level;
    byte scan_protect;
    _gap _6E;
    _gap _6F;
    _gap _70;
    _gap _71;
    _gap _72;
    _gap _73;
}; // 74

struct TRepairRobot {
    TEquipment;

    byte tech_level;
    byte recover_hit_points;
    _gap _6E;
    _gap _6F;
    _gap _70;
    _gap _71;
    _gap _72;
    _gap _73;
}; // 74

struct TCargoHook {
    TEquipment;

    byte tech_level;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    int pick_up_size;
    int radius;
    _gap _78;
    _gap _79;
    _gap _7A;
    _gap _7B;
    float speed_min;
    float speed_max;
}; // 84

struct TDefGenerator {
    TEquipment;

    byte tech_level;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    float def_factor;
    _gap _74;
    _gap _75;
    _gap _76;
    _gap _77;
}; // 78

struct TWeapon {
    TEquipment;

    byte tech_level;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    int radius;
    int min_dmg;
    int max_dmg;
    _gap_32 _7C;
    _gap _80;
    _gap _81;
    _gap _82;
    _gap _83;
    _gap_32 _84;
    _gap_32 _88;
    _gap _8C;
    _gap _8D;
    _gap _8E;
    _gap _8F;
}; // 90

struct TCountableItem {
    TEquipment;

    _gap _6C;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    _gap _70;
    _gap _71;
    _gap _72;
    _gap _73;
    _gap _74;
    _gap _75;
    _gap _76;
    _gap _77;
}; // 78

struct TEquipmentWithActCode {
    TEquipment;

    _gap _6C;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    _gap _70;
    _gap _71;
    _gap _72;
    _gap _73;
    int data_1;
}; // 78

struct TCistern {
    TEquipment;

    int capacity;
    int fuel;
    _gap _74;
    _gap _75;
    _gap _76;
    _gap _77;
}; // 78

struct TSatellite {
    TEquipment;

    _gap _6C;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    TPlanet* planet;
    _gap _74;
    _gap _75;
    _gap _76;
    _gap _77;
    _gap _78;
    _gap _79;
    _gap _7A;
    _gap _7B;
    byte water_speed;
    byte land_speed;
    byte hill_speed;
    _gap _7F;
    _gap _80;
    _gap _81;
    _gap _82;
    _gap _83;
}; // 84

struct TTreasureMap {
    TEquipment;

    _gap _6C;
    _gap _6D;
    _gap _6E;
    _gap _6F;
    _gap _70;
    _gap _71;
    _gap _72;
    _gap _73;
    _gap _74;
    _gap _75;
    _gap _76;
    _gap _77;
    _gap _78;
    _gap _79;
    _gap _7A;
    _gap _7B;
    _gap _7C;
    _gap _7D;
    _gap _7E;
    _gap _7F;
}; // 80

struct TMicromodule {
    TEquipment;

    _gap _6C;
    _gap _6D;
    _gap _6E;
    _gap _6F;
}; // 70

struct TArtefact {
    TEquipmentWithActCode;
}; // 78

struct TUselessItem {
    TEquipmentWithActCode;

    WSTR custom_text;
    int data[3];
}; // 88

struct TProtoplasm {
    TCountableItem;
}; // 78

struct TArtefactTransmitter {
    TArtefact;

    int power;
}; // 7C

struct TArtefactTranctucator {
    TArtefact;

    _gap _78;
    _gap _79;
    _gap _7A;
    _gap _7B;
}; // 7C

struct TArtefactCustom {
    TArtefact;

    int data_2;
    int data_3;
    STR text_data_1;
    STR text_data_2;
    STR text_data_3;
    _gap _8C;
    _gap _8D;
    _gap _8E;
    _gap _8F;
    _gap _90;
    _gap _91;
    _gap _92;
    _gap _93;
}; // 94

struct TCustomWeapon {
    TWeapon;

    _gap _90;
    _gap _91;
    _gap _92;
    _gap _93;
}; // 94


