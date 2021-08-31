// bit=32
#include <string>
#include <iostream>
#include <cstdint>

#include "structs/include.h"

using namespace std;

#define LOG(expr) cout<<#expr<<" = "<<(expr)<<endl;
#define ASSERT_TRUE(expr) if(!(expr)) {cout<<"Assert true error:\n\t"<<#expr<<" = "<<(expr)<<endl;}
#define ASSERT_FALSE(expr) if((expr)) {cout<<"Assert false error:\n\t"<<#expr<<" = "<<(expr)<<endl;}
#define ASSERT_EQ(expr,val) if((expr)!=(val)) {cout<<"Assert equal error:\n\t"<<#expr<<" === "<<(expr)<<" != "<<(val)<<" === " <<#val<<endl;}
#define ASSERT_NOT_EQ(expr,val) if((expr)==(val)) {cout<<"Assert not equal error:\n\t"<<#expr<<" === "<<(expr)<<" == "<<(val)<<" === " <<#val<<endl;}

#define STRUCT_MEMBER_OFFSET(srt, fld) ((int)((int8_t*)((int8_t*)&(srt.fld))-(int8_t*)(&srt)))




#define SET_EXPR(lhs, expr)                   *(uint32_t*)lhs = (uint32_t)(expr);
#define SET_VAR(lhs, rhs)                     *(int8_t**)&lhs = (int8_t*)&rhs;
#define SET_VAR_WITH_OFFSET(lhs, rhs, offset) *(int8_t**)&lhs = (int8_t*)&rhs + (offset);

VMT_TList* vmt_TList = nullptr;

void*     (__fastcall *TObject_Create)    (__cls* cls, int8_t flag);

TList*    (__fastcall *TList_Create)      (VMT_TList* cls, int8_t flag);
int       (__fastcall *TList_Destroy)     (TList* list, int8_t flag);
void      (__fastcall *TList_Add)         (TList* list, uint32_t value);
void      (__fastcall *TList_Clear)       (TList* list);
void      (__fastcall *TList_Delete)      (TList* list, int32_t index);
void      (__fastcall *TList_Error)       (TList* list, int32_t, int32_t);
void      (__fastcall *TList_Error_0)     (TList* list, int32_t, int32_t);
void      (__fastcall *TList_Exchange)    (TList* list, int32_t index1, int32_t index2);
void      (__fastcall *TList_Expand)      (TList* list);
uint32_t  (__fastcall *TList_First)       (TList* list);
uint32_t  (__fastcall *TList_Get)         (TList* list, int32_t index);
void      (__fastcall *TList_Grow)        (TList* list);
int32_t   (__fastcall *TList_IndexOf)     (TList* list, uint32_t value);
void      (__fastcall *TList_Insert)      (TList* list, int32_t index, uint32_t value);
uint32_t  (__fastcall *TList_Last)        (TList* list);
void      (__fastcall *TList_Put)         (TList* list, int32_t index, uint32_t value);
void      (__fastcall *TList_Remove)      (TList* list, uint32_t value);
void      (__fastcall *TList_SetCapacity) (TList* list, int32_t new_capacity);
void      (__fastcall *TList_SetCount)    (TList* list, int32_t new_count);
void      (__fastcall *TList_Notify)      (TList* list);



// TScriptShip* (__fastcall *TScriptShip_Create)  (VMT_TScriptShip* cls, int8_t flag);
// int          (__fastcall *TScriptShip_Destroy) (TScriptShip* list, int8_t flag);
// SET_VAR            (TScriptShip_Destroy, vmt_TScriptShip->destroy);
// SET_VAR_WITH_OFFSET(TScriptShip_Create, TScriptShip_Destroy, 0x52C - 0x570);

// Возвращает корабль в системе по индексу
TShip* StarShips(TStar* star, int index) {
    TList* ships = star->ships;
    if(index < 0) return (TShip*)ships->items[ships->count + index];
    else return (TShip*)ships->items[index];
}
// Возвращает количество кораблей в системе
int StarShips(TStar* star) {
    return star->ships->count;
}


void TList_methods_init(TList* list) {
    vmt_TList = list->cls;

    SET_EXPR           (TObject_Create   , 0x403FA8);
    SET_VAR            (TList_Destroy    , vmt_TList->destroy);
    SET_VAR_WITH_OFFSET(TList_Clear      , TList_Destroy, 0xAD0 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Delete     , TList_Destroy, 0xAE8 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Error      , TList_Destroy, 0xB4C - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Error_0    , TList_Destroy, 0xB84 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Exchange   , TList_Destroy, 0xBD8 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Expand     , TList_Destroy, 0xC28 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_First      , TList_Destroy, 0xC40 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Get        , TList_Destroy, 0xC48 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Grow       , TList_Destroy, 0xC70 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_IndexOf    , TList_Destroy, 0xCA4 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Insert     , TList_Destroy, 0xCC4 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Last       , TList_Destroy, 0xD30 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Put        , TList_Destroy, 0xD3C - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Remove     , TList_Destroy, 0xD8C - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_SetCapacity, TList_Destroy, 0xDAC - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_SetCount   , TList_Destroy, 0xDE8 - 0xA7C);
    SET_VAR_WITH_OFFSET(TList_Notify     , TList_Destroy, 0xE58 - 0xA7C);
}

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

    TGalaxy galaxy;
    cout << STRUCT_MEMBER_OFFSET(galaxy, scripts) << endl;

    return 0;
}

