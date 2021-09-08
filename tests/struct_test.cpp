// bit=32
#include <string>
#include <iostream>
#include <cstdint>
#include <stddef.h>

#include "../cpp-tools/structs/include.h"
#include "../cpp-tools/wrapped-classes/include.h"

using namespace std;

#define LOG(expr) cout<<#expr<<" = "<<(expr)<<endl;
#define ASSERT_TRUE(expr) if(!(expr)) {cout<<"Assert true error:\n\t"<<#expr<<" = "<<(expr)<<endl;}
#define ASSERT_FALSE(expr) if((expr)) {cout<<"Assert false error:\n\t"<<#expr<<" = "<<(expr)<<endl;}
#define ASSERT_EQ(expr,val) if((expr)!=(val)) {cout<<"Assert equal error:\n\t"<<#expr<<" === "<<(expr)<<" != "<<(val)<<" === " <<#val<<endl;}
#define ASSERT_NOT_EQ(expr,val) if((expr)==(val)) {cout<<"Assert not equal error:\n\t"<<#expr<<" === "<<(expr)<<" == "<<(val)<<" === " <<#val<<endl;}


int main() {

    ASSERT_EQ(sizeof(byte),    1);
    ASSERT_EQ(sizeof(word),    2);
    ASSERT_EQ(sizeof(dword),   4);

    ASSERT_EQ(sizeof(PTR),     4);
    ASSERT_EQ(sizeof(UNK),     sizeof(PTR));
    ASSERT_EQ(sizeof(STR),     sizeof(PTR));
    ASSERT_EQ(sizeof(WSTR),    sizeof(PTR));
    ASSERT_EQ(sizeof(FUNC),    sizeof(PTR));

    ASSERT_EQ(sizeof(_gap_8),  sizeof(byte));
    ASSERT_EQ(sizeof(_gap_16), sizeof(word));
    ASSERT_EQ(sizeof(_gap_32), sizeof(dword));
    ASSERT_EQ(sizeof(_gap),    sizeof(_gap_8));


    ASSERT_EQ(sizeof(TShip),            0x4D0);
    ASSERT_EQ(sizeof(TRuins),           0x568);
    ASSERT_EQ(sizeof(TTranclucator),    0x4EC);
    ASSERT_EQ(sizeof(TKling),           0x4DC);
    ASSERT_EQ(sizeof(TNormalShip),      0x510);
    ASSERT_EQ(sizeof(TPirate),          0x51C);
    ASSERT_EQ(sizeof(TWarrior),         0x514);
    ASSERT_EQ(sizeof(TTransport),       0x514);
    ASSERT_EQ(sizeof(TRanger),          0x560);
    ASSERT_EQ(sizeof(TPlayer),          0x990);

    ASSERT_EQ(sizeof(TGalaxy),          0x1D4);
    ASSERT_EQ(sizeof(TConstellation),   0x08c);
    ASSERT_EQ(sizeof(TStar),            0x114);
    ASSERT_EQ(sizeof(TPlanet),          0x16c);
    ASSERT_EQ(sizeof(THole),            0x034);
    ASSERT_EQ(sizeof(TAsteroid),        0x03c);
    ASSERT_EQ(sizeof(TMissile),         0x074);

    ASSERT_EQ(sizeof(TItem),                    0x38);
    ASSERT_EQ(sizeof(TGoods),                   0x40);
    ASSERT_EQ(sizeof(TEquipment),               0x6C);
    ASSERT_EQ(sizeof(THull),                    0x94);
    ASSERT_EQ(sizeof(TFuelTanks),               0x7C);
    ASSERT_EQ(sizeof(TEngine),                  0x7C);
    ASSERT_EQ(sizeof(TRadar),                   0x78);
    ASSERT_EQ(sizeof(TScaner),                  0x74);
    ASSERT_EQ(sizeof(TRepairRobot),             0x74);
    ASSERT_EQ(sizeof(TCargoHook),               0x84);
    ASSERT_EQ(sizeof(TDefGenerator),            0x78);
    ASSERT_EQ(sizeof(TWeapon),                  0x90);
    ASSERT_EQ(sizeof(TCountableItem),           0x78);
    ASSERT_EQ(sizeof(TEquipmentWithActCode),    0x78);
    ASSERT_EQ(sizeof(TCistern),                 0x78);
    ASSERT_EQ(sizeof(TSatellite),               0x84);
    ASSERT_EQ(sizeof(TTreasureMap),             0x80);
    ASSERT_EQ(sizeof(TMicromodule),             0x70);
    ASSERT_EQ(sizeof(TArtefact),                0x78);
    ASSERT_EQ(sizeof(TUselessItem),             0x88);
    ASSERT_EQ(sizeof(TProtoplasm),              0x78);
    ASSERT_EQ(sizeof(TArtefactTransmitter),     0x7C);
    ASSERT_EQ(sizeof(TArtefactTranclucator),    0x7C);
    ASSERT_EQ(sizeof(TArtefactCustom),          0x94);
    ASSERT_EQ(sizeof(TCustomWeapon),            0x94);

    ASSERT_EQ(sizeof(TGalaxyEvent),             0x014);

    return 0;
}

