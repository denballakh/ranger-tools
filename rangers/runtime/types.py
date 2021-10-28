from ctypes import (
    Structure as struct,
    c_bool,
    c_char,
    c_wchar,
    c_byte,
    c_ubyte,
    c_short,
    c_ushort,
    c_int,
    c_uint,
    c_long,
    c_ulong,
    c_longlong,
    c_ulonglong,
    c_size_t,
    c_ssize_t,
    c_float,
    c_double,
    c_longdouble,
    c_char_p,
    c_wchar_p,
    c_void_p,
    POINTER,
)


class _pair_byte(struct): pass
class _pair_int(struct): pass
class _pair_float(struct): pass
class _pair_double(struct): pass

class TList(struct): pass
class TObjectList(struct): pass

class TPlanetTempl(struct): pass
class TStarDist(struct): pass
class TShipGoodsItem(struct): pass
class TGoodsShopItem(struct): pass
class TGoneItem(struct): pass
class TDomResearchProgress(struct): pass
class TGalaxyEvent(struct): pass
class TSetItem(struct): pass
class TMessagePlayer(struct): pass
class TStorageUnit(struct): pass
class TQuestGameContent(struct): pass
class TTextField(struct): pass
class TQuestParameter(struct): pass
class TArrayRectGR(struct): pass
class TShopSlot(struct): pass
class TStoredItem(struct): pass
class TPlayerHoldUnit(struct): pass
class TJournalRecord(struct): pass
class TPlanetNews(struct): pass
class TBonus(struct): pass
class TBonusSpecial(struct): pass

class THashEC(struct): pass
class TCodeEC(struct): pass
class TBufEC(struct): pass
class TFileEC(struct): pass
class TBlockParEC(struct): pass
class TBlockParElEC(struct): pass
class TDataElEC(struct): pass
class TDataEC(struct): pass
class TPackFileEC(struct): pass
class TPackCollectionEC(struct): pass
class TBlockMemUnitEC(struct): pass
class TBlockMemEC(struct): pass
class TStringsElEC(struct): pass
class TStringsEC(struct): pass
class TVarEC(struct): pass
class TVarArrayEC(struct): pass
class TCodeAnalyzerUnitEC(struct): pass
class TCodeAnalyzerEC(struct): pass
class TExpressionEC(struct): pass
class TExpressionInstrEC(struct): pass
class TExpressionVarEC(struct): pass

class TCCInterface(struct): pass
class TCBufEC(struct): pass
class TCBufControlEC(struct): pass
class TCCInterface_El(struct): pass
class TThreadEC(struct): pass
class TSaver(struct): pass


class TScript(struct): pass
class TScriptShip(struct): pass
class TScriptPlace(struct): pass
class TScriptItem(struct): pass
class TScriptState(struct): pass
class TScriptGroup(struct): pass
class TScriptStar(struct): pass
class TScriptConstellation(struct): pass
class TScriptDialog(struct): pass
class TScriptDialogMsg(struct): pass
class TScriptDialogAnswer(struct): pass


class TMissile(struct): pass
class TCustomMissile(struct): pass
class TAsteroid(struct): pass
class TGalaxy(struct): pass
class TStar(struct): pass
class TPlanet(struct): pass
class THole(struct): pass
class TConstellation(struct): pass
class TObjectSE(struct): pass


class TItem(struct): pass
class TGoods(TItem): pass
class TEquipment(TItem): pass

class THull(TEquipment): pass
class TFuelTanks(TEquipment): pass
class TEngine(TEquipment): pass
class TRadar(TEquipment): pass
class TScaner(TEquipment): pass
class TRepairRobot(TEquipment): pass
class TCargoHook(TEquipment): pass
class TDefGenerator(TEquipment): pass
class TWeapon(TEquipment): pass
class TCountableItem(TEquipment): pass
class TEquipmentWithActCode(TEquipment): pass
class TCistern(TEquipment): pass
class TSatellite(TEquipment): pass
class TTreasureMap(TEquipment): pass
class TMicromodule(TEquipment): pass

class TArtefact(TEquipmentWithActCode): pass
class TUselessItem(TEquipmentWithActCode): pass

class TArtefactTransmitter(TArtefact): pass
class TArtefactTranclucator(TArtefact): pass
class TArtefactCustom(TArtefact): pass

class TProtoplasm(TCountableItem): pass
class TCustomWeapon(TWeapon): pass


class TShip(struct): pass
class TRuins(TShip): pass
class TTranclucator(TShip): pass
class TKling(TShip): pass
class TNormalShip(TShip): pass

class TPirate(TNormalShip): pass
class TWarrior(TNormalShip): pass
class TTransport(TNormalShip): pass
class TRanger(TNormalShip): pass

class TPlayer(TRanger): pass



TVarEC._fields_ = [
    ('cls', c_void_p),
    ('name', c_void_p),
    ('type', c_int),

    ('val_int', c_int),
    ('val_dword', c_uint),
    ('val_float', c_float),
    ('val_str', c_wchar_p),
    ('val_externfun', c_void_p),
    ('val_libraryfun', c_void_p),
    ('val_fun', c_void_p),
    ('val_class', c_void_p),
    ('val_array', c_void_p),
    ('val_ref', c_void_p),
]

T = TVarEC
