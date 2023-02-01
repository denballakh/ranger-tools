from __future__ import annotations
from typing import Any, Final, Literal, cast, TypedDict

from .std.mixin import DataMixin, JSONMixin
from .std.buffer import OBuffer, IBuffer
from .std.dataclass import (
    compile,
    # base
    DataClass,
    # atomic
    DNone,
    Bool,
    Bool32,
    UInt8,
    UInt16,
    Int32,
    UInt32,
    Int64,
    Float,
    Double,
    WStr,
    # sequences
    Maybe,
    Pair,
    Sequence,
    List,
    Repeat,
    # namespaces
    NamedSequence,
    # game
    ZL,
    BufEC,
    CryptedRand31pm,
    # other
    Const,
    ShadowedConst,
    Converted,
    HexBytes,
    Nested,
    Selector,
    # memo
    AddToMemo,
    GetFromMemo,
    # debugging
    Raise,
    AssertOnEnd,
    _Log,
    _Hide,
    _PrintMsg,
    _PrintMemo,
    _LogOnException,
    _Wait,
    _Print,
    _Skip,
    _DumpTo,
    _Breakpoint,
    #
    get_memo,
)

__all__ = ('SAV',)

SAVE_VERSION: Final[int] = 166

MONEY_XOR: Final[int] = 0xA4A576AD

ID: Final = UInt32
SEED: Final = UInt32
TURN: Final = UInt32

TItem = NamedSequence(
    id=ID,
    item_type=UInt8,
    pos=Pair(Float),
    size=Int32,
    race=UInt8,
    cost=UInt32,
    _30=Int32,
    _24=Maybe(WStr),
    no_drop=Bool,
)

TGoods = NamedSequence(
    TItem,
    _38=Int32,
    natural=Bool,
)
TEquipment = NamedSequence(
    TItem,
    custom_faction=Maybe(WStr),
    sys_name=Maybe(WStr),
    explotable=Bool,
    duration=Float,
    broken=Bool,
    equip_slot_num=UInt8,
    bonus=Selector(Int32, {0: DNone, ...: UInt32}),
    special=Selector(Int32, {0: DNone, ...: UInt32}),
    spec_acrins=List(
        Sequence(
            Selector(Int32, {0: DNone, ...: UInt32}),
            Int32,
        ),
        UInt32,
    ),
    _64=UInt8,
)

TCargoHook = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    pick_up_size=UInt16,
    radius=UInt16,
    speed_min_max=Pair(Float),
)
TDefGenerator = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    def_factor=Float,
)
TEngine = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    speed=Int32,
    parsec=UInt8,
    _75=UInt8,
)
TFuelTanks = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    fuel=UInt16,
    capacity=UInt8,
)
TRadar = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    radius=UInt16,
)
TRepairRobot = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    recover_hp=UInt8,
)
TScaner = NamedSequence(
    TEquipment,
    tech_level=UInt8,
    scan_protect=UInt8,
)
THull = NamedSequence(
    TEquipment,
    hp=Int32,
    tech_level=UInt8,
    hit_protect=UInt8,
    hull_type=UInt8,
    series=Selector(Int32, {-1: DNone, ...: UInt32}),
    _7D=Bool,
    _7C=UInt8,
    _7E=Bool,
    _7F=AddToMemo('_7F', Bool),
    _80=Int32,
    _84=Int32,
    _7F_=Maybe(Sequence(ID, UInt8, UInt8), GetFromMemo[bool]('_7F')),
)


class TWeaponType(DataClass[dict[str, Any]]):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> dict[str, Any]:
        obj = TEquipment.read(buf)
        obj['tech_level'] = buf.read_byte()
        obj['radius'] = buf.read_i16()
        obj['dmg'] = buf.read_i32(), buf.read_i32()
        target_type = buf.read_byte()
        assert target_type in range(5), target_type
        target_id: int | None = None
        if target_type:
            target_id = ID.read(buf)
        obj['target'] = target_type, target_id

        memo = get_memo()
        assert 'weapon-infos' in memo

        if (
            obj['item_type'] in {53, 64, 67}
            or obj['item_type'] == 68
            and list(
                filter(
                    lambda x, /: x['name'] == memo['_this_weapon_type'],
                    memo['weapon-infos'],
                ),
            )[0]['shot_type']
            in {5, 6, 7}
        ):
            obj['ammo'] = buf.read_u32()
            obj['max_ammo'] = buf.read_u32()

        return obj

    def write(self, buf: OBuffer, obj: dict[str, Any], /) -> None:
        TEquipment.write(buf, obj)
        buf.write_byte(obj['tech_level'])
        buf.write_i16(obj['radius'])
        buf.write_i32(obj['dmg'][0])
        buf.write_i32(obj['dmg'][1])
        target_type, target_id = obj['target']
        buf.write_byte(target_type)
        if target_type:
            ID.write(buf, target_id)

        memo = get_memo()
        if (
            obj['item_type'] in {53, 64, 67}
            or obj['item_type'] == 68
            and list(
                filter(
                    lambda x, /: x['name'] == memo['_this_weapon_type'],
                    memo['weapon-infos'],
                ),
            )[0]['shot_type']
            in {5, 6, 7}
        ):
            buf.write_u32(obj['ammo'])
            buf.write_u32(obj['max_ammo'])


TWeapon = TWeaponType()

TCustomWeapon = Sequence(
    AddToMemo('_this_weapon_type', WStr),
    TWeaponType(),
)

TCistern = NamedSequence(
    TEquipment,
    fuel=UInt8,
    capacity=Int32,
)
TCountableItem = NamedSequence(
    TEquipment,
    _6c=Int32,
    _70=Bool,
)
TEquipmentWithActCode = NamedSequence(
    TEquipment,
)
TMicromodule = NamedSequence(
    TEquipment,
)
TSatellite = NamedSequence(
    TEquipment,
    _6c=UInt8,
    _74=Int32,
    cur_planet_id=ID,
    water_speed=UInt8,
    land_speed=UInt8,
    hill_speed=UInt8,
    _78=Float,
)
TTreasureMap = NamedSequence(
    TEquipment,
    planet_id=ID,
    _70=WStr,
    _74=WStr,
    _78=WStr,
)

TProtoplasm = NamedSequence(
    TCountableItem,
)

TUselessItem = NamedSequence(
    TEquipmentWithActCode,
    data_1=WStr,
    _i0=Int32,
    _i1=Int32,
    _i2=Int32,
)
TArtefact = NamedSequence(
    TEquipmentWithActCode,
)
TArtefactCustom = NamedSequence(
    TArtefact,
    _d0=Int32,
    _d1=Int32,
    _d2=Int32,
    _s0=Maybe(WStr),
    _s1=Maybe(WStr),
    _s2=Maybe(WStr),
)
TArtefactTranclucator = NamedSequence(
    TArtefact,
    tranc_ship=Raise(RuntimeError('tranc_ship is not replaced!')),
    # will be replaced after definition of TTranclucator
)
TArtefactTransmitter = NamedSequence(
    TArtefact,
    power=Int32,
)

VirtualItem: Any = Selector(
    UInt8,
    {
        0: TGoods,
        1: TGoods,
        2: TGoods,
        3: TGoods,
        4: TGoods,
        5: TGoods,
        6: TGoods,
        7: TGoods,
        8: TArtefactCustom,
        9: TArtefactCustom,
        10: TArtefact,
        11: TArtefact,
        12: TArtefact,
        13: TArtefact,
        14: TArtefact,
        15: TArtefact,
        16: TArtefact,
        17: TArtefact,
        18: TArtefact,
        19: TArtefact,
        20: TArtefact,
        21: TArtefact,
        22: TArtefact,
        23: TArtefactTransmitter,
        24: TArtefact,
        25: TArtefactTranclucator,
        26: TArtefact,
        27: TArtefact,
        28: TArtefact,
        29: TArtefact,
        30: TArtefact,
        31: TArtefact,
        32: TArtefact,
        33: TArtefact,
        34: TArtefact,
        35: TArtefact,
        36: TArtefact,
        37: TArtefact,
        38: TArtefact,
        39: TArtefact,
        40: TArtefact,
        41: TArtefact,
        42: THull,
        43: TFuelTanks,
        44: TEngine,
        45: TRadar,
        46: TScaner,
        47: TRepairRobot,
        48: TCargoHook,
        49: TDefGenerator,
        50: TWeapon,
        51: TWeapon,
        52: TWeapon,
        53: TWeapon,
        54: TWeapon,
        55: TWeapon,
        56: TWeapon,
        57: TWeapon,
        58: TWeapon,
        59: TWeapon,
        60: TWeapon,
        61: TWeapon,
        62: TWeapon,
        63: TWeapon,
        64: TWeapon,
        65: TWeapon,
        66: TWeapon,
        67: TWeapon,
        68: TCustomWeapon,
        69: TProtoplasm,
        70: TUselessItem,
        71: TMicromodule,
        72: TCistern,
        73: TSatellite,
        74: TTreasureMap,
        75: TCountableItem,
    },
)

TShip = NamedSequence(
    id=ID,
    name=WStr,
    custom_type_name=WStr,
    type=UInt8,
    owner=UInt8,
    pos=Pair(Float),
    prev_star_id=ID,
    cur_planet_id=ID,
    cur_ship_id=ID,
    home_planet_id=ID,
    goods=Repeat(
        NamedSequence(
            cnt=UInt32,
            cost=UInt32,
            _8=UInt32,
            _C=UInt32,
        ),
        8,
    ),
    money=UInt32,
    gen_seed=SEED,
    rnd_seed=SEED,
    _088=UInt32,
    face=Int32,
    pilot_race=UInt8,
    items=List(VirtualItem, UInt16),
    arts=List(VirtualItem, UInt16),
    drop_items=List(VirtualItem, UInt16),
    _3C4=List(Sequence(UInt8, Int32), UInt16),
    _3C8=List(Sequence(UInt8, Float, UInt32), UInt16),
    custom_infos=List(
        NamedSequence(
            _s0=WStr,
            _s1=WStr,
            _i0=Int32,
            _i1=Int32,
            _i2=Int32,
            _s2=WStr,
            _s3=WStr,
            _s4=WStr,
        ),
        UInt32,
    ),
    _3D8=List(UInt32, UInt16),
    recently_dropped_items=List(UInt32, UInt16),
    ship_bad_id=ID,
    _3F8_id=ID,
    partner_id_and_days=Selector(ID, {0: DNone, ...: UInt32}),
    _3B5=Bool,
    _420=Float,
    order=UInt8,
    _42c=UInt32,
    order_dest_id=ID,
    dest_pos=Pair(Float),
    _43c=Bool,
    _445=Bool,
    _448=Int32,
    script_order_absolute=UInt8,
    _458=Bool,
    skin=WStr,
    _byte=UInt8,
    in_hyper_space=Bool,
    _45c=Float,
    relation_to_rangers=List(UInt8, UInt16),
    rewards=List(UInt8, UInt8),
    destroy=Bool,
    skills=Repeat(UInt8, 6),
    protoplasm=UInt16,
    points=UInt32,
    free_points=UInt32,
    _3b0=UInt16,
    money_ciphered=Converted(UInt32, decode=MONEY_XOR.__xor__, encode=MONEY_XOR.__xor__),
    _3d4=UInt16,
    _unk_list=Repeat(Sequence(Float, Int32, Int32, Int32), 24),
    _08c=Int32,
    _094=Int32,
    _461=Bool,
    _462=UInt8,
    _463=UInt8,
    _464=Int32,
    _unk0=Repeat(Sequence(Bool, Int32), 3),
    _unk=Sequence(Float, Int32, Int32, Int32),
    tech_level_knowledge=UInt8,
    _334=Int32,
    _338=Int32,
    _33c=Int32,
    _3ec=Int32,
    no_drop=Bool,
    no_target=UInt8,
    no_talk=Bool,
    no_scan=Bool,
    _49c=Bool,
    _49d=Bool,
    _49e=UInt16,
    _4a0=AddToMemo('_4a0', Int32),
    _unk_id=ID,
    _4a0_str=Maybe(
        WStr,
        Converted(
            GetFromMemo[int]('_4a0'),
            decode=bool,
            encode=int,
        ),
    ),
    cur_standing=UInt8,
    _4b4=Sequence(
        Int32,
        Int32,
        Float,
        Int32,
        Float,
        Float,
        Float,
    ),
)
TKling = NamedSequence(
    TShip,
    sub_type=UInt8,
    sub_race=UInt8,
    _4d4=Int32,
    _4d8=UInt8,
)
TRuins = NamedSequence(
    TShip,
    equipment_shop=List(VirtualItem, UInt16),
    _4d4_4e0=Repeat(Sequence(Int32, Float, Int32, Int32), 8),
    _554=Int32,
    dest_star_id=ID,
    _55c=Int32,
    _satellite=TSatellite,
    _565=Bool,
    _564=Bool,
    _566=Bool,
    _567=Bool,
)
TTranclucator = NamedSequence(
    TShip,
    proprietor_id=ID,
    _4dc=Bool,
    _4dd=Bool,
    _4de=Bool,
    _4d0=Int32,
    _4d4=Maybe(WStr),
    _4e0=Repeat(Bool, 7),
    _4e6=Repeat(Bool, 2),
    _4df=Bool,
)
# patching...
TArtefactTranclucator.kwargs['tranc_ship'] = TTranclucator

TNormalShip = NamedSequence(
    TShip,
    _4d4=Int32,
    _4d8=Int32,
    _4dc=Int32,
    _4e0=Int32,
    _4e4=Int32,
    _4e8=Int32,
    _4ec=Int32,
    _4f2=UInt16,
    _4f4=UInt16,
    _4f0=UInt16,
    _4f6=UInt16,
    _4f8_id=ID,
    _4fc=Int32,
    _500=UInt8,
    _502=UInt16,
    _508=UInt8,
    _50c=UInt32,
    _4d0_id=ID,
    _504=Int32,
)

TPirate = NamedSequence(
    TNormalShip,
    in_prison=Bool32,
    sub_type=UInt8,
    _518=Float,
)
TTransport = NamedSequence(
    TNormalShip,
    sub_type=UInt8,
)
TWarrior = NamedSequence(
    TNormalShip,
    sub_type=UInt8,
)
TRanger = NamedSequence(
    TNormalShip,
    status=Repeat(UInt8, 3),
    _516=UInt8,
    _517=UInt8,
    _518=UInt8,
    _51c=UInt8,
    _51d=UInt8,
    _520=List(
        NamedSequence(
            _b0=UInt8,
            _w0=UInt16,
            _i0=Int32,
            _i1=Int32,
            _id0=ID,
            _id1=ID,
            _b1=Bool,
            _s0=WStr,
            _s1=WStr,
            _s2=WStr,
        ),
        UInt16,
    ),
    _519=UInt8,
    _51a=UInt8,
    _51b=UInt8,
    in_prison=Bool32,
    _528_id=ID,
    base_nod_cur=Int32,
    programs=Repeat(Int32, 12),
    _512=Bool,
)
TPlayer = NamedSequence(
    TRanger,
    _560=Bool,
    _561=Bool,
    _562=Bool,
    _564=Int32,
    _568=Int32,
    _56c=Repeat(Int32, 8),
    _98c=Repeat(UInt8, 3),
    item_storage=List(
        NamedSequence(
            storage_type=UInt8,
            storage_id=ID,
            item_id=ID,
            item=VirtualItem,
        ),
        UInt32,
    ),
    debt=Int32,
    debt_date=Int32,
    debt_cnt=Int32,
    deposit=Int32,
    deposit_date=Int32,
    deposit_day=Int32,
    deposit_percent=Float,
    med_policy=Int32,
    _5c0=Int32,
    _5c4=Int32,
    _5c8=Int32,
    dest_star_id=ID,
    _5d0=Repeat(Int32, 12),
    _5fc=Repeat(WStr, 24),
    _660=UInt8,
    _664=Repeat(Int32, 12),
    _694=Int32,
    _698=Int32,
    satellites=List(TSatellite, UInt32),
    _6a0=List(Repeat(Int32, 10), UInt32),
    _6a4=Int32,
    _6a8=Int32,
    reject_pb=Bool,
    _6ae=UInt16,
    _6b0=UInt16,
    _6b2=UInt16,
    _6b4=Int32,
    _6b8=UInt16,
    _6bc=UInt16,
    _6c0=UInt8,
    _strange_list_of_lists=List(
        Sequence(
            List(Int32, UInt16),
            List(Int32, UInt16),
        ),
        Const(UInt8, 10),
    ),
    pirate_partners=List(ID, UInt8),
    _948=List(Bool, Const(UInt8, 6)),
    _950=List(Sequence(Int32, WStr), UInt32),
    _954=List(Sequence(UInt32, UInt32, UInt8, WStr), UInt16),
    _958=UInt8,
    _959=Bool,
    pirate_clan_real=Bool,
    _95c=NamedSequence(
        _i0=UInt32,
        _i1=UInt32,
        _i2=UInt32,
        _i3=UInt32,
        _b0=UInt8,
        _i4=UInt32,
        _i5=UInt32,
        _i6=UInt32,
        _i7=UInt32,
        _i8=UInt32,
        _i9=UInt32,
    ),
    exp_points_dom_kills=Int32,
    exp_points_pir_kills=Int32,
    exp_points_good_kills=Int32,
    exp_points_trade=Int32,
    bridge=Selector(
        UInt8,
        {
            0: TRuins,
            ...: NamedSequence(
                bridge=TRuins,
                cur_ship_id=ID,
                cur_planet_id=ID,
            ),
        },
    ),
    _980=WStr,
    _984_blockpar=List(WStr, UInt32),
)

VirtualShip: DataClass[tuple[int, dict[str, Any]]] = Selector(
    UInt8,
    {
        0: TKling,
        1: TRanger,
        2: TTransport,
        3: TPirate,
        4: TWarrior,
        5: TTranclucator,
        6: TRuins,
        7: TRuins,
        8: TRuins,
        9: TRuins,
        10: TRuins,
        11: TRuins,
        12: TRuins,
        13: TRuins,
        255: TPlayer,
    },
)

TConstellation = NamedSequence(
    id=ID,
    _09=Bool,
    _88=UInt16,
    _0C=Float,
    _10=Float,
    stars_id=List(ID, UInt16),
    constellations_id=List(ID, UInt16),
    p_bound=List(Repeat(Float, 4), UInt16),
    p_bound_hidden=List(Repeat(Float, 4), UInt16),
    rect=Repeat(Int32, 4),
    point=Repeat(Int32, 2),
    lines=List(Repeat(Float, 4), UInt16),
    _80=List(
        NamedSequence(
            _l0=List(Pair(Float), UInt16),
            _d0=Float,
            _d1=Float,
            _d2=Float,
            _d3=Float,
            _d4=Float,
            _d5=Float,
        ),
        UInt16,
    ),
    _84=List(
        NamedSequence(
            _l0=List(Pair(Float), UInt16),
            _d0=Float,
            _d1=Float,
            _d2=Float,
            _d3=Float,
            _d4=Float,
            _d5=Float,
        ),
        UInt16,
    ),
)

TPlanet = NamedSequence(
    id=ID,
    gen_seed=SEED,
    rnd_seed=SEED,
    name=WStr,
    pos=Pair(Float),
    angle_speed=Float,
    _030=Int32,
    radius=Int32,
    water_total=Int32,
    water_complete=Int32,
    land_total=Int32,
    land_complete=Int32,
    hill_total=Int32,
    hill_complete=Int32,
    orbit_cnt=UInt8,
    is_visited=Bool,
    invention_levels=Repeat(UInt8, 20),
    cur_invention=UInt8,
    cur_invention_points=Float,
    _064=UInt8,
    _065=UInt8,
    population=UInt32,
    eco=UInt8,
    _070=UInt32,
    owner=UInt8,
    race=UInt8,
    gov=UInt8,
    goods=Repeat(
        NamedSequence(
            count=Int32,
            e_price=Float,
            sell_price=Int32,
            buy_price=Int32,
            count_2=UInt8,
            _100=UInt8,
        ),
        8,
    ),
    relation_to_rangers=List(UInt8, UInt16),
    equipment_store_items=List(VirtualItem, UInt16),
    warriors=List(
        VirtualShip,
        UInt16,
    ),
    spawned_rangers_count=UInt16,
    _11C=UInt16,
    _120=UInt16,
    _124=UInt16,
    _128=UInt16,
    graph_radius=UInt16,
    graph_name=WStr,
    graph_planet_14=UInt16,
    graph_planet_type=Int32,
    graph_planet_3C=UInt8,
    _108=Int32,
    sputniks=List(
        NamedSequence(
            index=Int32,
            graph_name=WStr,
            buf=Nested(
                BufEC(),
                NamedSequence(
                    _b0=UInt8,
                    _f0=Float,
                    _f1=Float,
                    _f2=Float,
                    _i0=Int32,
                    _f3=Float,
                    _i1=Int32,
                    _i2=Int32,
                    _i3=Int32,
                    _i4=Int32,
                    __end_check=AssertOnEnd(),
                ),
            ),
            _f=Float,
        ),
        UInt16,
    ),
    gone_items=List(
        NamedSequence(
            pos=Pair(UInt8),
            terrain_type=UInt8,
            terrain_needed=Int32,
            _8=Bool,
            item=VirtualItem,
        ),
        UInt16,
    ),
    no_landing=Bool,
    no_shop_update=Bool,
    is_rogeria=Bool,
    _164_s=WStr,
)

TAsteroid = NamedSequence(
    id=ID,
    graph_type=WStr,
    pos=Pair(Int32),
    speed=Pair(Float),
    _24=Float,
    minerals=Int32,
)

TMissile = NamedSequence(
    id=ID,
    type=UInt32,
    _b0=UInt8,
    _b1=UInt8,
    _i0=Int32,
    _i1=Int32,
    _i2=Selector(Int32, {0: DNone, ...: UInt32}),
    _i3=Selector(Int32, {0: DNone, ...: UInt32}),
    _f0=Float,
    _f1=Float,
    _f2=Float,
    _f3=Float,
    _id0=ID,
    _id1=ID,
    _id2=Selector(UInt8, {0: DNone, ...: ID}),
    _b2=UInt8,
    _i4=Int32,
    _f4=Float,
    _f5=Float,
    _f6=Float,
    _i5=Selector(UInt8, {0: DNone, ...: ID}),
    _f7=Float,
    _f8=Float,
    _f9=Float,
)
TCustomMissile = Sequence(WStr, TMissile)

VirtualMissile: Any = Selector(
    UInt8,
    {
        53: TMissile,
        64: TMissile,
        67: TMissile,
        68: TCustomMissile,
    },
)

THole = NamedSequence(
    id=ID,
    star1_id=ID,
    pos1=Pair(Float),
    star2_id=ID,
    pos2=Pair(Float),
    open_turn=TURN,
    status=Int32,
    graph=WStr,
    map_name=WStr,
)

TStar = NamedSequence(
    id=ID,
    gen_seed=SEED,
    rnd_seed=SEED,
    name=WStr,
    pos=Pair(Float),
    _01C=UInt16,
    fon_image=UInt8,
    planets=List(TPlanet, UInt16),
    asteroids=List(TAsteroid, UInt16),
    ships=List(VirtualShip, UInt16),
    items_in_space=List(VirtualItem, UInt16),
    drop_list=List(
        NamedSequence(
            pos=Pair(Float),
            _2=Int32,
            _3=UInt8,
            item=VirtualItem,
        ),
        UInt16,
    ),
    missiles=List(VirtualMissile, UInt16),
    con_id=ID,
    _032=WStr,
    battle=Bool,
    _040=UInt8,
    _041=UInt8,
    owner=UInt8,
    _04A=UInt8,
    series=UInt8,
    custom_faction=WStr,
    safe_radius=Float,
    damage_radius=Float,
    radius=UInt16,
    graph_object_type=WStr,
    _0F1=Bool,
    _080=UInt8,
    _070=Int32,
    _074=Int32,
    _084=Int32,
    _088=Int32,
    _08C=Int32,
    _078=Int32,
    no_come_kling=Bool,
    _0DC=ID,
    _0E0=WStr,
    _0E4=List(
        NamedSequence(
            _s0=WStr,
            _s1=WStr,
            _s2=WStr,
            _s3=WStr,
            _i0=Int32,
        ),
        UInt16,
    ),
)

TVarEC = NamedSequence(
    name=_Print(WStr),
    value=Selector(
        UInt8,
        {
            0: DNone,
            1: Int32,
            2: UInt32,
            3: Double,
            # 3: Float,
            4: WStr,
            # 6: Sequence(Const(UInt8, 6), WStr),
            # 6: WStr,
            6: DNone,
            9: List(Raise(RuntimeError('TVarEC')), UInt32),
        },
    ),
)

cast(List[dict[str, Any]], cast(Selector[int, Any], TVarEC.kwargs['value']).dclss[9]).dcls = TVarEC

TEther = List(Sequence(WStr, Int32), UInt32)

TScript = NamedSequence(
    name=WStr,
    __log=_Log(before=100),
    ether=TEther,
    vars1=List(TVarEC, UInt16),
    vars2=List(TVarEC, UInt16),
    _10=List(
        NamedSequence(
            _s=WStr,
            _d=Int32,
            _l=List(Sequence(WStr, Int32), UInt32),
            _zero=Const(Int32, 0),
        ),
        UInt32,
    ),
    _18=List(
        NamedSequence(
            _s0=WStr,
            _b0=UInt8,
            _i0=Int32,
            _i1=Int32,
            _i2=Int32,
            _s1=WStr,
            _s2=WStr,
            _s3=WStr,
            _s4=WStr,
            _s5=WStr,
            _id=ID,
        ),
        UInt32,
    ),
    ships=List(
        NamedSequence(
            id=ID,
            _i0=Int32,
            _i1=Int32,
            _i2=Int32,
            _i3=Int32,
            _i4=Int32,
            state=UInt32,
            _s=WStr,
            _b0=UInt8,
            _b1=UInt8,
        ),
        UInt16,
    ),
    _5c=List(WStr, UInt16),
)

CustomWeaponInfos = AddToMemo(
    'weapon-infos',
    List(
        NamedSequence(
            name=WStr,
            _b0=UInt8,
            _b1=UInt8,
            _f0=Float,
            _d1=Int32,
            _d2=Int32,
            _d3=Int32,
            _d4=Int32,
            _d5=Int32,
            _d6=Int32,
            _d7=Int32,
            _d8=Int32,
            _b2=UInt8,
            _d9=UInt32,
            shot_type=UInt8,
            _b4=UInt8,
            _b5=UInt8,
            _d10=Float,
            _d11=Float,
            _lst=Repeat(Float, 8),
            _s1=Maybe(WStr),
            _s2=Maybe(WStr),
            _s3=Maybe(WStr),
            _d12=Int32,
            _b6=UInt8,
            _b7=UInt8,
        ),
        UInt16,
    ),
)


AA = NamedSequence(
    enabled=Bool,
    kling_strength=UInt8,
    kling_aggro=UInt8,
    kling_spawn=UInt8,
    pirate_aggro=UInt8,
    coal_aggro=UInt8,
    asteroid_mod=UInt8,
    sun_damage_mod=UInt8,
    extra_inventions=UInt8,
    akrin_mod=UInt8,
    node_drop_mod=UInt8,
    AB_drop_value_mod=UInt8,
    drop_value_mod=UInt8,
    ag_planets=UInt8,
    mi_planets=UInt8,
    in_planets=UInt8,
    extra_rangers=UInt8,
    AB_hitpoints_mod=UInt8,
    AB_damage_mod=UInt8,
    AI_tolerate_junk=UInt8,
    rnd_chaotic=Bool,
    eq_knowledge_restricted=Bool,
    ruins_near_stars=Bool,
    ruins_targetting_full=Bool,
    special_ships_in_game=Bool,
    zero_start_exp=Bool,
    AB_battle_royale=Bool,
    kling_racial_weapons=Bool,
    start_center=Bool,
    max_range_missiles=Bool,
    old_hyper=Bool,
    pirate_nodes=Bool,
    AI_use_shops=Bool,
    ruins_use_shops=Bool,
    duplicate_arts=Bool,
    hull_growth=UInt8,
    _aa_0=UInt8,
    _aa_1=UInt8,
    _aa_2=UInt8,
)


TGalaxy = NamedSequence(
    curform=Int32,
    starmapposview=Pair(Int32),
    _b0=UInt8,
    _b1=Const(UInt8, 0),
    _b2=UInt8,
    _b3=Const(UInt8, 0),
    _b4=Const(UInt8, 0),
    _b5=Const(UInt8, 0),
    _protection_byte=UInt8,
    _b6=UInt8,
    _tips=Int32,
    _i1=Const(Int32, 0),
    ethers=List(
        NamedSequence(
            _s0=WStr,
            _b0=UInt8,
            _d0=UInt32,
            _d1=UInt32,
            _s1=WStr,
            _b1=UInt8,
            _d2=UInt32,
            _d3=UInt32,
            _d4=UInt32,
            _d5=UInt32,
            _d6=UInt32,
            _d7=UInt32,
            _b2=UInt8,
            _b3=UInt8,
            _s2=WStr,
        ),
        UInt32,
    ),
    _l1=List(
        Sequence(UInt8, UInt8, UInt32),
        UInt16,
    ),
    enabled_mods=WStr,
    gen_seed=SEED,
    rnd_seed=SEED,
    rangers_average_capital=Int32,
    _064=Int32,
    rangers_average_strength=Float,
    _06C=Float,
    _T_b0=Bool,
    _T_b1=Bool,
    _d0=Const(Int32, 0),
    cheat_points=UInt32,
    save_count=UInt32,
    _174=UInt32,
    custom_weapon_infos=CustomWeaponInfos,
    cons=List(TConstellation, UInt16),
    stars=List(TStar, UInt16),
    holes=List(THole, UInt16),
    _034s=List(Sequence(WStr, VirtualItem), UInt16),
    _158s=List(
        NamedSequence(
            pos=Pair(Float),
            _b0=UInt8,
            _w0=UInt16,
            _s0=WStr,
        ),
        UInt16,
    ),
    planets=List(ID, UInt16),
    rangers=List(ID, UInt16),
    delta_wins=Repeat(Int32, 5),
    keller_attack_star_id=ID,
    _0C0=UInt32,
    _weapons=List(
        NamedSequence(
            _b0=UInt8,
            _b1=UInt8,
            _s=Selector(UInt8, {0: DNone, 1: VirtualItem}),
        ),
        UInt16,
    ),
    global_vars=List(
        TVarEC,
        UInt32,
    ),
    _l0=List(
        NamedSequence(
            name=WStr,
            _w=UInt16,
            _i0=Int32,
            _i1=Int32,
        ),
        UInt16,
    ),
    scripts=List(TScript, UInt16),
    _154=List(
        NamedSequence(
            _w0=UInt16,
            _i0=Int32,
            _i1=Int32,
            _b0=UInt8,
            _l0=List(Int32, UInt16),
            _l1=List(
                NamedSequence(
                    type=UInt8,
                    id=ID,
                    _pos=Pair(Float),
                    _b0=UInt8,
                    _i0=Int32,
                ),
                UInt16,
            ),
        ),
        UInt16,
    ),
    _zero1=Const(UInt8, 0),
    _zero2=Const(Int32, 0),
    pirate_cnt=UInt16,
    _044=UInt16,
    _048=UInt16,
    turn=TURN,
    diff_levels=Repeat(UInt8, 8),
    player_id=ID,
    auto_battle_ship_id=ID,
    blazer_id=ID,
    keller_id=ID,
    terron_id=ID,
    _dword_862324_id=UInt32,
    terron_star_id=ID,
    eminent_rangers_id=Repeat(ID, 3),
    _gvar_0085EC0C=List(
        NamedSequence(
            id=ID,
            _b0=UInt8,
            _w0=UInt16,
            _s0=WStr,
            _b1=Bool,
            _b2=Bool,
        ),
        UInt16,
    ),
    planet_news=List(
        NamedSequence(
            id=ID,
            turn=TURN,
            _b0=UInt8,
            _s0=WStr,
        ),
        UInt16,
    ),
    _gvar_00857408=UInt32,
    _gvar_0085740C=UInt32,
    _0c4=Float,
    dom_researches=Repeat(
        NamedSequence(
            progress=Float,
            material=UInt32,
        ),
        3,
    ),
    _0ec=Float,
    klings_delta_win=Int32,
    pirates_delta_win=Int32,
    _0f8=Int32,
    _score_buf=HexBytes(BufEC()),
    _16c=List(
        NamedSequence(
            _i0=Int32,
            _f0=Float,
            _f1=Float,
            _f2=Float,
            _f3=Float,
            _f4=Float,
            _f5=Float,
            _f6=Float,
            _f7=Float,
            _f8=Float,
            _f9=Float,
            _i1=Int32,
        ),
        UInt32,
    ),
    _gvar_0085F060=Repeat(UInt32, 9),
    _T_1=Int32,
    _T_2=Int32,
    _T_3=Int32,
    _T_4=Float,
    _15c_ids=List(ID, UInt16),
    terron_weapon_lock_turn=TURN,
    terron_grow_lock_turn=TURN,
    terron_landing_lock_turn=TURN,
    terron_to_star=TURN,
    keller_leave=TURN,
    keller_new_research=TURN,
    blazer_landing=TURN,
    blazer_self_destruction=TURN,
    terron_turn_win=TURN,
    keller_turn_win=TURN,
    blazer_turn_win=TURN,
    pirate_win_turn=TURN,
    pirate_win_type=Int32,
    coalition_defeat_turn=TURN,
    _14c=Bool,
    _14c_2=UInt8,
    iron_will=Bool,  # cheats:
    kling_strength=UInt8,
    technic=UInt8,
    _17f=UInt8,
    _180=UInt8,
    ultrascan=UInt8,
    zawarudo=UInt8,
    _0bc=UInt32,
    _1ac=Int32,
    events=List(
        NamedSequence(
            type=WStr,
            turn=TURN,
            _l0=List(Int32, UInt32),
            _l1=List(WStr, UInt32),
        ),
        UInt16,
    ),
    interface_state_overrides=List(
        NamedSequence(
            form=WStr,
            elem=WStr,
            _b0=UInt8,
            _b1=UInt8,
        ),
        UInt16,
    ),
    interface_text_overrides=List(
        NamedSequence(
            form=WStr,
            elem=WStr,
            _b0=WStr,
            _b1=WStr,
        ),
        UInt16,
    ),
    interface_image_overrides=List(
        NamedSequence(
            form=WStr,
            elem=WStr,
            _b0=WStr,
            _b1=WStr,
        ),
        UInt16,
    ),
    interface_pos_overrides=List(
        NamedSequence(
            form=WStr,
            elem=WStr,
            _i0=Int32,
            _i1=Int32,
            _q0=Int64,
            _i2=Int32,
            _i3=Int32,
            _q1=Int64,
        ),
        UInt16,
    ),
    interface_size_overrides=List(
        NamedSequence(
            form=WStr,
            elem=WStr,
            _i0=Int32,
            _i1=Int32,
            _i2=Int32,
            _i3=Int32,
        ),
        UInt16,
    ),
    max_ship_id=ID,
    _020=Int32,
    _1cc=Int32,
    _T_b2=UInt8,
    finalization_name=WStr,
    AA=AA,
    _zeros=Const(Converted(Repeat(UInt8, 5), decode=tuple, encode=tuple), (0,) * 5),
    __end_check=AssertOnEnd(),
)


class SavImageData(TypedDict):
    _a: int
    _b: int
    _c: int
    data: str


class SavImage(DataClass[SavImageData]):
    __slots__ = ()

    def read(self, buf: IBuffer, /) -> SavImageData:
        data: SavImageData = {}  # type: ignore[typeddict-item]
        data['_a'] = buf.read_u32()
        data['_b'] = buf.read_u32()
        data['_c'] = buf.read_u32()
        data['data'] = buf.read(data['_b'] * data['_c']).hex(' ', -3)
        # assert buf, (buf.pos, len(buf))
        return data

    def write(self, buf: OBuffer, obj: SavImageData, /) -> None:
        buf.write_u32(obj['_a'])
        buf.write_u32(obj['_b'])
        buf.write_u32(obj['_c'])
        data = bytes.fromhex(obj['data'])
        buf.write(data)
        assert len(data) == obj['_a'] * obj['_b'] * 3, (len(data), obj['_a'] * obj['_b'] * 3)


Data1Obj: DataClass[SavImageData] = Nested(
    ZL(1, optional=True),
    SavImage(),
)
Data2Obj: DataClass[SavImageData] = Nested(
    ZL(1, optional=True),
    SavImage(),
)
Data3Obj = Nested(
    Nested(
        CryptedRand31pm(
            key=0,
            seed=0,
            prepend_size=True,
        ),
        ZL(1),
    ),
    TGalaxy,
)
Data4Obj = HexBytes(ZL(1, length=-1, optional=True))


SAVObj: DataClass[dict[str, Any]] = NamedSequence(
    _magic=Const(WStr, 'RSG', 'invalid save magic'),
    version=Const(
        Converted(
            WStr,
            decode=lambda s, /: int(s[1:]),
            encode=lambda i, /: 'v' + str(i),
        ),
        SAVE_VERSION,
        'unsupported save version',
    ),
    save_name=WStr,
    turn=Converted(
        WStr,
        decode=int,
        encode=str,
    ),
    money=Converted(
        WStr,
        decode=int,
        encode=str,
    ),
    name=WStr,
    race=WStr,
    _EZ=Const(WStr, 'EZ'),
    data1=Data1Obj,
    data2=Data2Obj,
    data3=Data3Obj,
    data4=Data4Obj,
)

# SAVObj = compile(SAVObj)


class SAV(DataMixin, JSONMixin):
    data: dict[str, Any]

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = {} if data is None else data

    @classmethod
    def from_buffer(cls, buf: IBuffer, **kwargs: Any) -> SAV:
        return cls(SAVObj.read_with_memo(buf))

    def to_buffer(self, buf: OBuffer, **kwargs: Any) -> None:
        SAVObj.write_with_memo(buf, self.data)
