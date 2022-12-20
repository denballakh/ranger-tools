from __future__ import annotations
from typing import Any, Final, TypeVar, cast
import copy

from .std.mixin import DataMixin, JSONMixin
from .std.buffer import IBuffer, OBuffer
from .std.dataclass import (
    # base
    DataClass,
    Memo,
    # atomic
    DNone,
    Bool,
    Bool32,
    Byte,
    Int32,
    UInt32,
    Double,
    Bytes,
    # sequences
    Pair,
    List,
    Repeat,
    # namespaces
    NamedSequence,
    # other
    ConstValue,
    AnyOf,
    MemoSelectedDataClass,
    Converted,
    HexBytes,
    # memo
    AddToMemo,
    GetFromMemo,
    #
    AssertOnEnd,
)

__all__ = ('QM',)

T = TypeVar('T')


class MaybeUndefinedSizedWStr(DataClass[str | None]):
    """
    0000 -> None
    1000 ui32 wstr -> str
    """

    def read(self, buf: IBuffer, /) -> str | None:
        flag = buf.read_u32()
        if not flag:
            return None
        size = buf.read_u32()
        return buf.read_wstr(size)

    def write(self, buf: OBuffer, obj: str | None, /) -> None:
        if obj is None:
            buf.write_u32(0)
            return
        buf.write_u32(1)
        buf.write_u32(len(obj))
        buf.write_wstr(obj, length=len(obj))


VER_BASE: Final = 1_111_111_111

# VER_QM_1: Final = 10  # ?
VER_QM_2: Final = 11
VER_QM_3: Final = 12
VER_QM_4: Final = 13
# VER_QM_5: Final = 14  # ?
VER_QMM_6: Final = 15
VER_QMM_7: Final = 16

SUPPORTED_VERSIONS: Final = {
    VER_QM_2,
    VER_QM_3,
    VER_QM_4,
    VER_QMM_6,
    VER_QMM_7,
}

VER_QM: Final = {v for v in SUPPORTED_VERSIONS if v < VER_QMM_6}
VER_QMM: Final = {v for v in SUPPORTED_VERSIONS if v >= VER_QMM_6}


# must be different
# used internally, doesnt affect the result
TAG_VERSION: Final = 'version'
TAG_PAR_CNT: Final = 'parameters_cnt'
TAG_LOCATIONS_CNT: Final = 'locations_cnt'
TAG_JUMPS_CNT: Final = 'jumps_cnt'

UNK: Final = Int32  # any 4 bytes
VER: Final = GetFromMemo[int](TAG_VERSION)
USTR: Final = MaybeUndefinedSizedWStr()

PAR_CNT: Final[DataClass[int]] = MemoSelectedDataClass(
    lambda memo: cast(
        dict[int, DataClass[int]],
        {
            VER_QM_2: ConstValue(24),
            VER_QM_3: ConstValue(48),
            VER_QM_4: ConstValue(96),
            VER_QMM_6: GetFromMemo(TAG_PAR_CNT),
            VER_QMM_7: GetFromMemo(TAG_PAR_CNT),
        },
    )[memo[TAG_VERSION]],
)

# depending on the version will choose the option for QM or QMM
# if version >= minversion, then return the second parameter, otherwise - the first
def VER_SEL(qm: DataClass[T], qmm: DataClass[T], minversion: int = VER_QMM_6) -> DataClass[T]:
    return MemoSelectedDataClass(
        lambda memo: {
            False: qm,
            True: qmm,
        }[memo[TAG_VERSION] >= minversion],
    )


QM_LOCATION_TEXTS: Final = 10

QMHeader = NamedSequence(
    _unk0=UNK,
    giving_race=Byte,
    when_done=Byte,
    _unk1=UNK,
    planet_race=Byte,
    _unk2=UNK,
    player_status=Byte,
    _unk3=UNK,
    player_race=Byte,
    reputation_change=Int32,
    screen_size=Pair(Int32),
    grid_size=Pair(Int32),
    _unk4=UNK,
    default_jump_count_limit=Int32,
    complexity=Int32,
)
QMMHeader = NamedSequence(
    VER_SEL(
        NamedSequence(),
        NamedSequence(
            major_ver=UInt32,
            minor_ver=UInt32,
            changelog=USTR,
        ),
        minversion=VER_QMM_7,
    ),
    giving_race=Byte,
    when_done=Byte,
    planet_race=Byte,
    player_status=Byte,
    player_race=Byte,
    reputation_change=Int32,
    screen_size=Pair(Int32),
    grid_size=Pair(Int32),
    default_jump_count_limit=Int32,
    complexity=Int32,
    param_count=AddToMemo(TAG_PAR_CNT, UInt32),
)


QMParameterInit = NamedSequence(
    minmax=Pair(Int32),
    _average=Int32,
    type=Byte,
    _unk0=UNK,
    show_when_zero=Bool,
    critical_type=Byte,
    active=Bool,
    linecnt=AddToMemo('_line_cnt', Int32),
    is_money=Bool,
    name=USTR,
    lines=List(
        NamedSequence(
            diap=Pair(Int32),
            content=USTR,
        ),
        GetFromMemo[int]('_line_cnt'),
    ),
    crit_text=USTR,
    start_value=USTR,
)
QMMParameterInit = NamedSequence(
    minmax=Pair(Int32),
    type=Int32,
    show_when_zero=Bool,
    critical_type=Byte,
    active=Bool,
    linecnt=AddToMemo('_line_cnt', Int32),
    is_money=Bool,
    name=USTR,
    lines=List(
        NamedSequence(
            diap=Pair(Int32),
            content=USTR,
        ),
        GetFromMemo[int]('_line_cnt'),
    ),
    crit_text=USTR,
    img=USTR,
    sound=USTR,
    track=USTR,
    start_value=USTR,
)


QMLocation = NamedSequence(
    day_passed=Bool32,
    coord=Pair(Int32),
    id=Int32,
    type_start=Bool,
    type_win=Bool,
    type_lose=Bool,
    type_die=Bool,
    type_empty=Bool,
    pars=List(
        NamedSequence(
            _unk0=UNK,
            _unk1=UNK,
            _unk2=UNK,
            change=Int32,
            show_type=Byte,
            _unk3=UNK,
            percentQ=Bool,
            valueQ=Bool,
            exprQ=Bool,
            expression=USTR,
            _unk4=HexBytes(Bytes(10)),
            crit_text=USTR,
        ),
        PAR_CNT,
    ),
    texts=Repeat(USTR, QM_LOCATION_TEXTS),
    is_text_by_formula=Bool,
    _unk0=UNK,
    _unkstr1=USTR,
    _unkstr2=USTR,
    text_select_formula=USTR,
)
QMMLocation = NamedSequence(
    day_passed=Bool32,
    coord=Pair(Int32),
    id=Int32,
    max_visits=Int32,
    type=Byte,
    pars=List(
        NamedSequence(
            id=Int32,
            change=Int32,
            show_type=Byte,
            change_type=Byte,
            expression=USTR,
            crit_text=USTR,
            img=USTR,
            sound=USTR,
            track=USTR,
        ),
        UInt32,
    ),
    texts=List(
        NamedSequence(
            text=USTR,
            img=USTR,
            sound=USTR,
            track=USTR,
        ),
        UInt32,
    ),
    is_text_by_formula=Bool,
    text_select_formula=USTR,
)


QMJump = NamedSequence(
    priority=Double,
    day_passed=Bool32,
    id=Int32,
    from_to=Pair(Int32),
    _color=Byte,
    always_show=Bool,
    jump_count_limit=Int32,
    show_order=Int32,
    parameters=List(
        NamedSequence(
            _unk1=UNK,
            diap=Pair(Int32),
            change=Int32,
            show_type=Int32,
            _unk2=Byte,
            percentQ=Bool,
            valueQ=Bool,
            exprQ=Bool,
            expression=USTR,
            must_equal_cnt=AddToMemo('_must_equal_cnt', Int32),
            must_equalQ=Bool,
            must_equal=List(
                Int32,
                GetFromMemo('_must_equal_cnt'),
            ),
            must_mod_cnt=AddToMemo('_must_mod_cnt', Int32),
            must_modQ=Bool,
            must_mod=List(
                Int32,
                GetFromMemo('_must_mod_cnt'),
            ),
            crit_text=USTR,
        ),
        PAR_CNT,
    ),
    formula_to_pass=USTR,
    text=USTR,
    description=USTR,
)
QMMJump = NamedSequence(
    priority=Double,
    day_passed=Bool32,
    id=Int32,
    from_to=Pair(Int32),
    always_show=Bool,
    jump_count_limit=Int32,
    show_order=Int32,
    param_conditions=List(
        NamedSequence(
            id=UInt32,
            diap=Pair(Int32),
            must_equal_cnt=AddToMemo('_must_equal_cnt', Int32),
            must_equalQ=Bool,
            must_equal=List(
                Int32,
                GetFromMemo('_must_equal_cnt'),
            ),
            must_mod_cnt=AddToMemo('_must_mod_cnt', Int32),
            must_modQ=Bool,
            must_mod=List(
                Int32,
                GetFromMemo('_must_mod_cnt'),
            ),
        ),
        UInt32,
    ),
    param_changes=List(
        NamedSequence(
            id=UInt32,
            change=Int32,
            show_type=Byte,
            change_type=Byte,
            expression=USTR,
            crit_text=USTR,
            img=USTR,
            sound=USTR,
            track=USTR,
        ),
        UInt32,
    ),
    formula_to_pass=USTR,
    text=USTR,
    description=USTR,
    img=USTR,
    sound=USTR,
    track=USTR,
)


QuestObj: DataClass[dict[str, Any]] = NamedSequence(
    version=AddToMemo(
        TAG_VERSION,
        AnyOf(
            Converted(
                UInt32,
                decode=lambda v: v - VER_BASE,
                encode=lambda v: v + VER_BASE,
            ),
            SUPPORTED_VERSIONS,
            'Unsupported version',
        ),
    ),
    header=VER_SEL(QMHeader, QMMHeader),
    parameters=List(
        VER_SEL(QMParameterInit, QMMParameterInit),
        PAR_CNT,
    ),
    tostar=USTR,
    parsec=VER_SEL(USTR, DNone),
    artefact=VER_SEL(USTR, DNone),
    toplanet=USTR,
    date=USTR,
    money=USTR,
    fromplanet=USTR,
    fromstar=USTR,
    ranger=USTR,
    locations_cnt=AddToMemo(TAG_LOCATIONS_CNT, Int32),
    jumps_cnt=AddToMemo(TAG_JUMPS_CNT, Int32),
    success_text=USTR,
    task_text=USTR,
    unknown_text=VER_SEL(USTR, DNone),
    locations=List(
        VER_SEL(QMLocation, QMMLocation),
        GetFromMemo(TAG_LOCATIONS_CNT),
    ),
    jumps=List(
        VER_SEL(QMJump, QMMJump),
        GetFromMemo(TAG_JUMPS_CNT),
    ),
    __end=AssertOnEnd(),
)


class QM(DataMixin, JSONMixin):
    data: dict[str, Any]

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = {} if data is None else data

    @classmethod
    def from_buffer(cls, buf: IBuffer, **kwargs: Any) -> QM:
        self = cls()
        self.data = QuestObj.read(buf)
        return self

    def to_buffer(self, buf: OBuffer, **kwargs: Any) -> None:
        QuestObj.write(buf, self.data)

    def __deepcopy__(self, memo: Any) -> QM:
        return QM(copy.deepcopy(self.data, memo))

    def update(self) -> QM:
        OLD_VER: int = self.data['version']
        NEW_VER = VER_QMM_7

        new = copy.deepcopy(self)
        new.data['version'] = NEW_VER

        return new
