from __future__ import annotations
from pathlib import Path
from typing import Final

from .std.dataclass import (
    DataClass,
    DNone,
    Bool,
    UInt8,
    Int32,
    UInt32,
    Float,
    Double,
    WStr,
    #
    AddToMemo,
    MemoSelectedDataClass,
    #
    AnyOf,
    ConstValue,
    Converted,
    CustomCallable,
    List,
    NamedSequence,
    Sequence,
    #
    # _Print,
    # _Log,
    # _Wait,
)
from .std.bidict import bidict

SUPPORTED_VERSIONS: Final = {7, 8}


def EnumDCls(d: dict[int, str], base: DataClass[int]) -> DataClass[str]:
    bd = bidict(d)
    return Converted(
        base,
        decode=lambda vi: bd[vi],
        encode=lambda vs: bd.inv[vs],
    )


Var = NamedSequence(
    name=WStr,
    type=AddToMemo(
        '_var_type',
        EnumDCls(
            {
                0: 'none',
                1: 'int',
                2: 'dword',
                3: 'float',
                4: 'str',
                9: 'array',
            },
            base=UInt8,
        ),
    ),
    value=MemoSelectedDataClass(
        lambda memo: {
            'none': DNone,
            'int': Int32,
            'dword': UInt32,
            'float': Double,
            'str': WStr,
            'array': List(Var),
        }[memo['_var_type']]
    ),
)

MinMax = NamedSequence(
    min=Int32,
    max=Int32,
)

Status = Sequence(MinMax, MinMax, MinMax)

Planet = NamedSequence(
    name=WStr,
    race=UInt32,
    owner=UInt32,
    economy=UInt32,
    government=UInt32,
    range=MinMax,
    dialog=WStr,
)

Ship = NamedSequence(
    count=UInt32,
    owner=UInt32,
    type=UInt32,
    is_player=Bool,
    speed=MinMax,
    weapon=UInt32,
    cargohook=Int32,
    emptyspace=Int32,
    status=Status,
    strength=MinMax,
    ruins=WStr,
)

StarLink = NamedSequence(
    end_star=UInt32,
    distance=MinMax,
    is_hole=Bool,
)

Star = NamedSequence(
    name=WStr,
    constellation=Int32,
    no_kling=Bool,
    no_come_kling=Bool,
    starlinks=List(StarLink),
    planets=List(Planet),
    ships=List(Ship),
)

Place = NamedSequence(
    name=WStr,
    star=WStr,
    type=AddToMemo(
        '_place_type',
        EnumDCls(
            {
                0: 'free',
                1: 'near_planet',
                2: 'in_planet',
                3: 'to_star',
                4: 'near_item',
                5: 'from_ship',
                6: 'from_coords',
            },
            base=UInt32,
        ),
    ),
    data=MemoSelectedDataClass(
        lambda memo: {
            'free': NamedSequence(
                angle=Float,
                distance=Float,
                radius=Int32,
            ),
            'near_planet': NamedSequence(
                object=WStr,
                radius=Int32,
            ),
            'in_planet': NamedSequence(
                object=WStr,
            ),
            'to_star': NamedSequence(
                object=WStr,
                distance=Float,
                radius=Int32,
                angle=Float,
            ),
            'near_item': NamedSequence(
                object=WStr,
                radius=Int32,
            ),
            'from_ship': NamedSequence(
                object=WStr,
                distance=Float,
                radius=Int32,
                angle=Float,
            ),
            'from_coords': NamedSequence(
                var_X=WStr,
                var_Y=WStr,
                radius=Int32,
            ),
        }[memo['_place_type']]
    ),
)

Item = NamedSequence(
    name=WStr,
    place=WStr,
    kind=UInt32,
    type=UInt32,
    size=Int32,
    level=Int32,
    radius=Int32,
    owner=UInt32,
    useless=WStr,
)

Group = NamedSequence(
    name=WStr,
    planet=WStr,
    state=Int32,
    owner=UInt32,
    type=UInt32,
    count=MinMax,
    speed=MinMax,
    weapon=UInt32,
    cargohook=Int32,
    emptyspace=Int32,
    add_player=Bool,
    status=Status,
    search_distance=Int32,
    dialog=WStr,
    strength=Sequence(Float, Float),
    ruins=WStr,
)

GroupLink = NamedSequence(
    begin=Int32,
    end=Int32,
    relations=MinMax,
    war_weigth=Sequence(Float, Float),
)

State = NamedSequence(
    name=WStr,
    type=AddToMemo(
        '_state_type',
        EnumDCls(
            {
                0: 'none',
                1: 'move',
                2: 'follow',
                3: 'jump',
                4: 'landing',
                5: 'free',
            },
            base=UInt32,
        ),
    ),
    object=MemoSelectedDataClass(
        lambda memo: WStr if memo['_state_type'] not in {'none', 'free'} else ConstValue(''),
    ),
    attack=List(WStr),
    take_item=WStr,
    take_all=Bool,
    out_msg=WStr,
    in_msg=WStr,
    ether=WStr,
    code=WStr,
)

Dialog = NamedSequence(
    name=WStr,
    code=WStr,
)

DialogMsg = NamedSequence(
    command=WStr,
    code=WStr,
)

DialogAnswer = NamedSequence(
    command=WStr,
    answer=WStr,
    code=WStr,
)

SCR = NamedSequence(
    version=AnyOf(AddToMemo('version', UInt32), SUPPORTED_VERSIONS),
    __localvars_offset_1=Converted(UInt32, decode=lambda x: 0, encode=lambda x: 0),
    globalvars=List(Var),
    globalcode=WStr,
    __localvars_offset_2=CustomCallable(
        decode=lambda buf: None,
        encode=lambda buf, _: (
            p := buf.pos,
            buf.push_pos(4),
            buf.write_u32(p),  # type: ignore[func-returns-value]
            buf.pop_pos(),
        ),
    ),
    localvars=List(Var),
    constellations=Int32,
    stars=List(Star),
    places=List(Place),
    items=List(Item),
    groups=List(Group),
    grouplinks=List(GroupLink),
    initcode=WStr,
    turncode=WStr,
    dialogbegincode=WStr,
    states=List(State),
    dialogs=List(Dialog),
    dialog_messages=List(DialogMsg),
    dialog_answers=List(DialogAnswer),
)
