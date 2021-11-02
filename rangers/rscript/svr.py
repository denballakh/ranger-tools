from ..buffer import Buffer
from .enums import *


def rgb_to_dword(r, g, b):
    return (b << 16) | (g << 8) | r


def pos_gen(size, step=20):
    n = 0
    while True:
        y, x = divmod(n, size)
        n += 1
        yield Point(x * step, y * step)


class MinMax:
    __slots__ = ['min', 'max']

    def __repr__(self) -> str:
        return f'<MinMax: min={self.min!r} max={self.max!r}>'

    def __init__(self, mn, mx):
        self.min = mn
        self.max = mx


class Point:
    __slots__ = ['x', 'y']

    def __repr__(self) -> str:
        return f'<Point: x={self.x!r} y={self.y!r}>'

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Status:
    __slots__ = ['trader', 'warrior', 'pirate']

    def __repr__(self) -> str:
        return f'<Status: trader={self.trader!r} warrior={self.warrior!r} pirate={self.pirate!r}>'

    def __init__(self, trader: MinMax, warrior: MinMax, pirate: MinMax):
        self.trader = trader
        self.warrior = warrior
        self.pirate = pirate


class Rect:
    __slots__ = "top", "left", "right", "bottom"

    def __repr__(self):
        return f'<Rect: top={self.top!r} left={self.left!r} right={self.right!r} bottom={self.bottom!r}>'

    def __init__(self, top, left, right, bottom):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom


class GraphPoint:
    classname = "TGraphPoint"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r}>'

    def __init__(self, script, pos=None, text=""):
        self._script = script

        self.pos = Point(0, 0) if pos is None else pos
        self.text = text

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        buf.write_wstr(self.classname)
        buf.write_int(self.pos.x)
        buf.write_int(self.pos.y)
        buf.write_wstr(self.text)
        buf.write_int(-1)

    def from_buffer(self, buf: Buffer):
        self.pos.x = buf.read_int()
        self.pos.y = buf.read_int()
        self.text = buf.read_wstr()
        _int = buf.read_int()
        assert _int == -1, _int

        return self


class GraphLink:
    classname = "TGraphLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r}>'

    def __init__(self, script, begin=None, end=None, ord_num=0, has_arrow=True):
        self._script = script
        self.begin = begin
        self.end = end
        self.ord_num = ord_num
        self.has_arrow = has_arrow

    def __post_init__(self):
        self.begin = self._script.graphpoints[self.begin]
        self.end = self._script.graphpoints[self.end]

    def to_buffer(self, buf: Buffer):
        buf.write_wstr(self.classname)
        buf.write_int(self._script.index(self.begin))
        buf.write_int(self._script.index(self.end))
        buf.write_uint(self.ord_num)
        buf.write_bool(self.has_arrow)

    def from_buffer(self, buf: Buffer):
        self.begin = buf.read_int()
        self.end = buf.read_int()
        self.ord_num = buf.read_uint()
        self.has_arrow = buf.read_bool()
        return self


class GraphRect:
    classname = "TGraphRectText"

    def __repr__(self) -> str:
        return f'<{self.classname}: rect={self.rect!r} fill_style={self.fill_style!r} fill_color={self.fill_color!r} border_style={self.border_style!r} border_color={self.border_color!r} border_size={self.border_size!r} border_coef={self.border_coef!r} text_align_x={self.text_align_x!r} text_align_y={self.text_align_y!r} text_align_rect={self.text_align_rect!r} text={self.text!r} text_color={self.text_color!r} font={self.font!r} font_size={self.font_size!r} is_bold={self.is_bold!r} is_italic={self.is_italic!r} is_underline={self.is_underline!r}>'

    def __init__(self, script, rect=None, text=""):
        self._script = script

        self.rect = rect if rect is not None else Rect(0, 0, 100, 100)
        self.fill_style = 0
        self.fill_color = rgb_to_dword(34, 111, 163)
        self.border_style = 0
        self.border_color = rgb_to_dword(220, 220, 220)
        self.border_size = 1
        self.border_coef = 0.3
        self.text_align_x = 0
        self.text_align_y = 0
        self.text_align_rect = False
        self.text = text
        self.text_color = rgb_to_dword(255, 255, 255)
        self.font = "Arial"
        self.font_size = 10
        self.is_bold = False
        self.is_italic = False
        self.is_underline = False

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        buf.write_wstr(self.classname)
        buf.write_int(self.rect.top)
        buf.write_int(self.rect.left)
        buf.write_int(self.rect.right)
        buf.write_int(self.rect.bottom)
        buf.write_byte(self.fill_style)
        buf.write_uint(self.fill_color)
        buf.write_byte(self.border_style)
        buf.write_uint(self.border_color)
        buf.write_uint(self.border_size)
        buf.write_float(self.border_coef)
        buf.write_uint(self.text_align_x)
        buf.write_uint(self.text_align_y)
        buf.write_bool(self.text_align_rect)
        buf.write_wstr(self.text)
        buf.write_uint(self.text_color)
        buf.write_wstr(self.font)
        buf.write_uint(self.font_size)
        buf.write_bool(self.is_bold)
        buf.write_bool(self.is_italic)
        buf.write_bool(self.is_underline)

    def from_buffer(self, buf: Buffer):
        self.rect.top = buf.read_int()
        self.rect.left = buf.read_int()
        self.rect.right = buf.read_int()
        self.rect.bottom = buf.read_int()
        self.fill_style = buf.read_byte()
        self.fill_color = buf.read_uint()
        self.border_style = buf.read_byte()
        self.border_color = buf.read_uint()
        self.border_size = buf.read_uint()
        self.border_coef = buf.read_float()
        self.text_align_x = buf.read_uint()
        self.text_align_y = buf.read_uint()
        self.text_align_rect = buf.read_bool()
        self.text = buf.read_wstr()
        self.text_color = buf.read_uint()
        self.font = buf.read_wstr()
        self.font_size = buf.read_uint()
        self.is_bold = buf.read_bool()
        self.is_italic = buf.read_bool()
        self.is_underline = buf.read_bool()
        return self


class Star(GraphPoint):
    classname = "TStar"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} constellation={self.constellation!r} priority={self.priority!r} is_subspace={self.is_subspace!r} no_kling={self.no_kling!r} no_come_kling={self.no_come_kling!r}>'

    def __init__(self, script, pos=None, text="StarNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.constellation = 0
        self.priority = 0
        self.is_subspace = False
        self.no_kling = False
        self.no_come_kling = False

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_int(self.constellation)
        buf.write_uint(self.priority)
        buf.write_bool(self.is_subspace)
        buf.write_bool(self.no_kling)
        buf.write_bool(self.no_come_kling)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.constellation = buf.read_int()
        self.priority = buf.read_uint()
        self.is_subspace = buf.read_bool()
        self.no_kling = buf.read_bool()
        self.no_come_kling = buf.read_bool()

        return self


class Planet(GraphPoint):
    classname = "TPlanet"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} race={self.race!r} owner={self.owner!r} economy={self.economy!r} government={self.government!r} range={self.range!r} dialog={self.dialog!r}>'

    def __init__(self, script, pos=None, text="PlanetNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.race = RACE_FLAG(0b00111110)  # r
        self.owner = OWNER_FLAG(0b00111110)  # o
        self.economy = ECONOMY_FLAG(0b00001110)  # e
        self.government = GOVERNMENT_FLAG(0b00111110)  # g
        self.range = MinMax(0, 100)
        self.dialog = None

    def __post_init__(self):
        self.dialog = self._script.graphpoints[self.dialog] if self.dialog != -1 else None

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(int(self.race))
        buf.write_uint(int(self.owner))
        buf.write_uint(int(self.economy))
        buf.write_uint(int(self.government))
        buf.write_int(self.range.min)
        buf.write_int(self.range.max)
        buf.write_int(self._script.index(self.dialog))

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)

        self.race = RACE_FLAG(buf.read_uint())
        self.owner = OWNER_FLAG(buf.read_uint())
        self.economy = ECONOMY_FLAG(buf.read_uint())
        self.government = GOVERNMENT_FLAG(buf.read_uint())
        self.range.min = buf.read_int()
        self.range.max = buf.read_int()
        self.dialog = buf.read_int()

        return self


class Ship(GraphPoint):
    classname = "TStarShip"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} count={self.count!r} owner={self.owner!r} type={self.type!r} is_player={self.is_player!r} speed={self.speed!r} weapon={self.weapon!r} cargohook={self.cargohook!r} emptyspace={self.emptyspace!r} rating={self.rating!r} status={self.status!r} score={self.score!r} strength={self.strength!r} ruins={self.ruins!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.count = 1
        self.owner = OWNER_FLAG(0b00111110)  # o
        self.type = SHIP_TYPE_FLAG(0b01111110)  # t
        self.is_player = False
        self.speed = MinMax(0, 10000)
        self.weapon = WEAPON.UNDEF
        self.cargohook = 0
        self.emptyspace = 0
        self.rating = MinMax(0, 1000)
        self.status = Status(MinMax(0, 100), MinMax(0, 100), MinMax(0, 100))
        self.score = MinMax(0, 1000000)
        self.strength = MinMax(0, 0)
        self.ruins = ""

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_int(self.count)
        buf.write_uint(int(self.owner))
        buf.write_uint(int(self.type))
        buf.write_bool(self.is_player)
        buf.write_int(self.speed.min)
        buf.write_int(self.speed.max)
        buf.write_uint(int(self.weapon))
        buf.write_uint(self.cargohook)
        buf.write_int(self.emptyspace)
        buf.write_int(self.rating.min)
        buf.write_int(self.rating.max)
        buf.write_int(self.status.trader.min)
        buf.write_int(self.status.trader.max)
        buf.write_int(self.status.warrior.min)
        buf.write_int(self.status.warrior.max)
        buf.write_int(self.status.pirate.min)
        buf.write_int(self.status.pirate.max)
        buf.write_int(self.score.min)
        buf.write_int(self.score.max)
        buf.write_float(self.strength.min)
        buf.write_float(self.strength.max)
        buf.write_wstr(self.ruins)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.count = buf.read_int()
        self.owner = OWNER_FLAG(buf.read_uint())
        self.type = SHIP_TYPE_FLAG(buf.read_uint())
        self.is_player = buf.read_bool()
        self.speed = MinMax(buf.read_int(), buf.read_int())
        self.weapon = WEAPON(buf.read_uint())
        self.cargohook = buf.read_uint()
        self.emptyspace = buf.read_int()
        self.rating = MinMax(buf.read_int(), buf.read_int())
        self.status = Status(
            MinMax(buf.read_int(), buf.read_int()),
            MinMax(buf.read_int(), buf.read_int()),
            MinMax(buf.read_int(), buf.read_int()),
        )
        self.score = MinMax(buf.read_int(), buf.read_int())
        self.strength = MinMax(buf.read_int(), buf.read_int())
        self.ruins = buf.read_wstr()

        return self


class Item(GraphPoint):
    classname = "TItem"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} kind={self.kind!r} type={self.type!r} size={self.size!r} level={self.level!r} radius={self.radius!r} owner={self.owner!r} useless={self.useless!r}>'

    def __init__(self, script, pos=None, text="ItemNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.kind = 0  # ic
        self.type = 0  # Equipment, Weapon, Goods, Artefact
        self.size = 10
        self.level = 1
        self.radius = 150
        self.owner = RACE.MALOC
        self.useless = ""

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(self.kind)
        buf.write_uint(self.type)
        buf.write_int(self.size)
        buf.write_uint(self.level)
        buf.write_int(self.radius)
        buf.write_uint(int(self.owner))
        buf.write_wstr(self.useless)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.kind = buf.read_uint()
        self.type = buf.read_uint()
        self.size = buf.read_int()
        self.level = buf.read_uint()
        self.radius = buf.read_int()
        self.owner = RACE(buf.read_uint())
        self.useless = buf.read_wstr()

        return self


class Place(GraphPoint):
    classname = "TPlace"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} type={self.type!r} angle={self.angle!r} dist={self.dist!r} radius={self.radius!r} obj={self.obj!r}>'

    def __init__(self, script, pos=None, text="PlaceNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.type = 0  # pt
        self.angle = 0  # 0..360
        self.dist = 0.5  # 0..1
        self.radius = 300  # in pixels
        self.obj = None

    def __post_init__(self):
        self.obj = self._script.graphpoints[self.obj] if self.obj != -1 else None

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(self.type)
        buf.write_float(self.angle)
        buf.write_float(self.dist)
        buf.write_int(self.radius)
        buf.write_int(self._script.index(self.obj))

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.type = buf.read_uint()
        self.angle = buf.read_float()
        self.dist = buf.read_float()
        self.radius = buf.read_int()
        self.obj = buf.read_int()

        return self


class Group(GraphPoint):
    classname = "TGroup"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} owner={self.owner!r} type={self.type!r} count={self.count!r} speed={self.speed!r} weapon={self.weapon!r} cargohook={self.cargohook!r} emptyspace={self.emptyspace!r} friendship={self.friendship!r} add_player={self.add_player!r} rating={self.rating!r} status={self.status!r} score={self.score!r} search_dist={self.search_dist!r} dialog={self.dialog!r} strength={self.strength!r} ruins={self.ruins!r}>'

    def __init__(self, script, pos=None, text="GroupNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.owner = OWNER_FLAG(0b00111110)  # o
        self.type = SHIP_TYPE_FLAG(0b01111110)  # t
        self.count = MinMax(2, 3)
        self.speed = MinMax(100, 10000)
        self.weapon = WEAPON.UNDEF  # w
        self.cargohook = 0
        self.emptyspace = 0
        self.friendship = FRIENDSHIP.FREE  # f
        self.add_player = False
        self.rating = MinMax(0, 1000)
        self.status = Status(MinMax(0, 100), MinMax(0, 100), MinMax(0, 100))
        self.score = MinMax(0, 1000000)
        self.search_dist = 10000
        self.dialog = None
        self.strength = MinMax(0, 0)
        self.ruins = ""

    def __post_init__(self):
        self.dialog = self._script.graphpoints[self.dialog] if self.dialog != -1 else None

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(int(self.owner))
        buf.write_uint(int(self.type))
        buf.write_int(self.count.min)
        buf.write_int(self.count.max)
        buf.write_int(self.speed.min)
        buf.write_int(self.speed.max)
        buf.write_uint(int(self.weapon))
        buf.write_uint(self.cargohook)
        buf.write_int(self.emptyspace)
        buf.write_uint(int(self.friendship))
        buf.write_bool(self.add_player)
        buf.write_int(self.rating.min)
        buf.write_int(self.rating.max)
        buf.write_int(self.status.trader.min)
        buf.write_int(self.status.trader.max)
        buf.write_int(self.status.warrior.min)
        buf.write_int(self.status.warrior.max)
        buf.write_int(self.status.pirate.min)
        buf.write_int(self.status.pirate.max)
        buf.write_int(self.score.min)
        buf.write_int(self.score.max)
        buf.write_int(self.search_dist)
        buf.write_int(self._script.index(self.dialog))
        buf.write_float(self.strength.min)
        buf.write_float(self.strength.max)
        buf.write_wstr(self.ruins)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)

        self.owner = OWNER_FLAG(buf.read_uint())
        self.type = SHIP_TYPE_FLAG(buf.read_uint())
        self.count.min = buf.read_int()
        self.count.max = buf.read_int()
        self.speed.min = buf.read_int()
        self.speed.max = buf.read_int()
        self.weapon = WEAPON(buf.read_uint())
        self.cargohook = buf.read_uint()
        self.emptyspace = buf.read_int()
        self.friendship = FRIENDSHIP(buf.read_uint())
        self.add_player = buf.read_bool()
        self.rating.min = buf.read_int()
        self.rating.max = buf.read_int()
        self.status.trader.min = buf.read_int()
        self.status.trader.max = buf.read_int()
        self.status.warrior.min = buf.read_int()
        self.status.warrior.max = buf.read_int()
        self.status.pirate.min = buf.read_int()
        self.status.pirate.max = buf.read_int()
        self.score.min = buf.read_int()
        self.score.max = buf.read_int()
        self.search_dist = buf.read_int()
        self.dialog = buf.read_int()
        self.strength.min = buf.read_float()
        self.strength.max = buf.read_float()
        self.ruins = buf.read_wstr()

        return self


class State(GraphPoint):
    classname = "TState"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} type={self.type!r} obj={self.obj!r} attack_groups={self.attack_groups!r} item={self.item!r} take_all={self.take_all!r} out_msg={self.out_msg!r} in_msg={self.in_msg!r} ether_type={self.ether_type!r} ether_uid={self.ether_uid!r} ether_msg={self.ether_msg!r}>'

    def __init__(self, script, pos=None, text="StateNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.type = MOVE_TYPE.NONE
        self.obj = ""
        self.attack_groups = []
        self.item = ""
        self.take_all = False
        self.out_msg = ""
        self.in_msg = ""
        self.ether_type = ETHER_TYPE.GALAXY
        self.ether_uid = ""
        self.ether_msg = ""

    def __post_init__(self):
        self.obj = self._script.graphpoints[self.obj] if self.obj != -1 else None
        self.item = self._script.graphpoints[self.item] if self.item != -1 else None
        for i in range(len(self.attack_groups)):
            self.attack_groups[i] = (
                self._script.graphpoints[self.attack_groups[i]]
                if self.attack_groups[i] != -1
                else None
            )

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(int(self.type))
        buf.write_int(self._script.index(self.obj))
        buf.write_uint(len(self.attack_groups))
        for ag in self.attack_groups:
            buf.write_int(self._script.index(ag))
        buf.write_int(self._script.index(self.item))
        buf.write_bool(self.take_all)
        buf.write_wstr(self.out_msg)
        buf.write_wstr(self.in_msg)
        buf.write_uint(int(self.ether_type))
        buf.write_wstr(self.ether_uid)
        buf.write_wstr(self.ether_msg)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.type = MOVE_TYPE(buf.read_uint())
        self.obj = buf.read_int()
        self.attack_groups = []
        for _ in range(buf.read_uint()):
            self.attack_groups.append(buf.read_int())
        self.item = buf.read_int()
        self.take_all = buf.read_bool()
        self.out_msg = buf.read_wstr()
        self.in_msg = buf.read_wstr()
        self.ether_type = ETHER_TYPE(buf.read_uint())
        self.ether_uid = buf.read_wstr()
        self.ether_msg = buf.read_wstr()

        return self


class ExprOp(GraphPoint):
    classname = "Top"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} expression={self.expression!r} type={self.type!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.expression = ""
        self.type = OP_TYPE.NORMAL  # op

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_wstr(self.expression)
        buf.write_byte(int(self.type))

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.expression = buf.read_wstr()
        self.type = OP_TYPE(buf.read_byte())

        return self


class ExprIf(GraphPoint):
    classname = "Tif"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} expression={self.expression!r} type={self.type!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.expression = ""
        self.type = OP_TYPE.NORMAL  # op

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_wstr(self.expression)
        buf.write_byte(int(self.type))

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.expression = buf.read_wstr()
        self.type = OP_TYPE(buf.read_byte())

        return self


class ExprWhile(GraphPoint):
    classname = "Twhile"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} expression={self.expression!r} type={self.type!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.expression = ""
        self.type = OP_TYPE.NORMAL  # op

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_wstr(self.expression)
        buf.write_byte(int(self.type))

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.expression = buf.read_wstr()
        self.type = OP_TYPE(buf.read_byte())

        return self


class ExprVar(GraphPoint):
    classname = "TVar"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} type={self.type!r} init_value={self.init_value!r} is_global={self.is_global!r}>'

    def __init__(self, script, pos=None, text="VarNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.type = VAR_TYPE_S.UNKNOWN
        self.init_value = ""
        self.is_global = False

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(int(self.type))
        buf.write_wstr(str(self.init_value))
        buf.write_bool(self.is_global)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.type = VAR_TYPE_S(buf.read_uint())
        self.init_value = buf.read_wstr()
        self.is_global = buf.read_bool()

        return self


class Ether(GraphPoint):
    classname = "TEther"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} type={self.type!r} uid={self.uid!r} msg={self.msg!r} focus={self.focus!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.type = ETHER_TYPE.ETHER
        self.uid = ""
        self.msg = ""
        self.focus = ["", "", ""]

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_uint(int(self.type))
        buf.write_wstr(self.uid)
        buf.write_wstr(self.msg)
        for f in self.focus:
            buf.write_wstr(f)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)

        self.type = ETHER_TYPE(buf.read_uint())
        self.uid = buf.read_wstr()
        self.msg = buf.read_wstr()
        self.focus = []
        for _ in range(3):
            self.focus.append(buf.read_wstr())

        return self


class Dialog(GraphPoint):
    classname = "TDialog"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r}>'

    def __init__(self, script, pos=None, text="DialogNew"):
        GraphPoint.__init__(self, script, pos, text)

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)

        return self


class DialogMsg(GraphPoint):
    classname = "TDialogMsg"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} msg={self.msg!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.msg = ""

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_wstr(self.msg)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.msg = buf.read_wstr()

        return self


class DialogAnswer(GraphPoint):
    classname = "TDialogAnswer"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} msg={self.msg!r}>'

    def __init__(self, script, pos=None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.msg = ""

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphPoint.to_buffer(self, buf)
        buf.write_wstr(self.msg)

    def from_buffer(self, buf: Buffer):
        GraphPoint.from_buffer(self, buf)
        self.msg = buf.read_wstr()

        return self


class StarLink(GraphLink):
    classname = "TStarLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r} dist={self.dist!r} deviation={self.deviation!r} relation={self.relation!r} is_hole={self.is_hole!r}>'

    def __init__(self, script, begin=None, end=None, ord_num=0, has_arrow=False):
        GraphLink.__init__(self, script, begin, end, ord_num, has_arrow)
        self.dist = MinMax(0, 150)
        self.deviation = 25
        self.relation = MinMax(0, 100)
        self.is_hole = False

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphLink.to_buffer(self, buf)
        buf.write_int(self.dist.min)
        buf.write_int(self.dist.max)
        buf.write_int(self.deviation)
        buf.write_int(self.relation.min)
        buf.write_int(self.relation.max)
        buf.write_bool(self.is_hole)

    def from_buffer(self, buf: Buffer):
        GraphLink.from_buffer(self, buf)
        self.dist.min = buf.read_int()
        self.dist.max = buf.read_int()
        self.deviation = buf.read_int()
        self.relation.min = buf.read_int()
        self.relation.max = buf.read_int()
        self.is_hole = buf.read_bool()

        return self


class GroupLink(GraphLink):
    classname = "TGroupLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r} relations={self.relations!r} war_weight={self.war_weight!r}>'

    def __init__(self, script, begin=None, end=None, ord_num=0, has_arrow=True):
        GraphLink.__init__(self, script, begin, end, ord_num, has_arrow)
        self.relations = [RELATION.NOCHANGE, RELATION.NOCHANGE]
        self.war_weight = MinMax(0.0, 1000.0)

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphLink.to_buffer(self, buf)
        for r in self.relations:
            buf.write_uint(int(r))
        buf.write_float(self.war_weight.min)
        buf.write_float(self.war_weight.max)

    def from_buffer(self, buf: Buffer):
        GraphLink.from_buffer(self, buf)
        self.relations = [RELATION(buf.read_uint()), RELATION(buf.read_uint)]
        self.war_weight.min = buf.read_float()
        self.war_weight.max = buf.read_float()

        return self


class StateLink(GraphLink):
    classname = "TStateLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r} expression={self.expression!r} priority={self.priority!r}>'

    def __init__(self, script, begin=None, end=None, ord_num=0, has_arrow=True):
        GraphLink.__init__(self, script, begin, end, ord_num, has_arrow)
        self.expression = ""
        self.priority = 0

    def __post_init__(self):
        pass

    def to_buffer(self, buf: Buffer):
        GraphLink.to_buffer(self, buf)
        buf.write_wstr(self.expression)
        buf.write_int(self.priority)

    def from_buffer(self, buf: Buffer):
        GraphLink.from_buffer(self, buf)
        self.expression = buf.read_wstr()
        self.priority = buf.read_int()

        return self


class SVR:
    version = 7

    def __init__(self):
        self.viewpos = Point(0, 0)
        self.name = ""
        self.filename = ""

        self.textfilenames = []
        self.textfilenames.append(['rus', ''])
        self.translations = []
        # self.translations_id = []

        self.graphpoints = []
        self.graphlinks = []
        self.graphrects = []

        self.pos_gen = pos_gen(30, 20)

    def add(self, clsname, pos=None):
        if not pos:
            pos = next(self.pos_gen)

        gp = classnames_points[clsname](self, pos)
        self.graphpoints.append(gp)
        return gp

    def link(self, begin, end):
        if isinstance(begin, Star) and isinstance(end, Star):
            gl = StarLink(self, begin, end)
        elif isinstance(begin, Group) and isinstance(end, Group):
            gl = GroupLink(self, begin, end)
        elif isinstance(begin, State) and isinstance(end, State):
            gl = StateLink(self, begin, end)
        else:
            gl = GraphLink(self, begin, end)
        self.graphlinks.append(gl)
        return gl

    def get(self, classname, n):
        cnt = 0
        for gp in self.graphpoints:
            if gp.classname == classname:
                if cnt == n:
                    return gp
                cnt += 1
        return None

    def find(self, name):
        if name == "":
            return None
        for gp in self.graphpoints:
            if gp.text == name:
                return gp
        return None

    def index(self, gp):
        if isinstance(gp, str):
            gp = self.find(gp)
        if not gp:
            return -1
        if gp in self.graphpoints:
            return self.graphpoints.index(gp)
        return -1

    # def find_link_begin(self, gp, clsname):
    #     cls = classnames_points[clsname]
    #     for gl in self.graphlinks:
    #         if (gl.begin is gp) and isinstance(gl.end, cls):
    #             return gl

    def to_buffer(self, buf: Buffer):
        buf.write(b'\x55\x44\x33\x22')
        buf.write_uint(self.version)
        buf.write_int(self.viewpos.x)
        buf.write_int(self.viewpos.y)
        buf.write_wstr(self.name)
        buf.write_wstr(self.filename)

        buf.write_byte(0)
        buf.write_uint(len(self.textfilenames))
        for lang, filename in self.textfilenames:
            buf.write_byte(1)
            buf.write_wstr(lang)
            buf.write_wstr(filename)

        buf.write(b'\0' * 6)
        buf.write_uint(len(self.translations))
        for tr_id, tran in self.translations:
            buf.write_byte(1)
            buf.write_wstr(tr_id)
            buf.write_wstr(tran)

        # buf.write(b'\0' * 6)
        # buf.write_uint(len(self.translations_id))
        # for tr_id, tran in self.translations_id:
        #     buf.write_byte(1)
        #     buf.write_wstr(tr_id)
        #     buf.write_wstr(tran)

        buf.write_uint(len(self.graphpoints))
        for gp in self.graphpoints:
            gp.to_buffer(buf)

        buf.write_uint(len(self.graphlinks))
        for gl in self.graphlinks:
            gl.to_buffer(buf)

        buf.write_uint(len(self.graphrects))
        for gr in self.graphrects:
            gr.to_buffer(buf)

    @classmethod
    def from_buffer(cls, buf: Buffer):
        self = cls()
        _x = buf.read(4)
        assert _x == b'\x55\x44\x33\x22', _x
        self.version = buf.read_uint()
        self.viewpos.x = buf.read_int()
        self.viewpos.y = buf.read_int()
        self.name = buf.read_wstr()
        self.filename = buf.read_wstr()

        self.textfilenames = []
        _x = buf.read_byte()
        assert _x == 0, _x
        for _ in range(buf.read_uint()):
            _x = buf.read_byte()
            assert _x == 1, _x
            self.textfilenames.append([buf.read_wstr(), buf.read_wstr()])
        _x = buf.read(6)
        assert _x == b'\0' * 6

        self.translations = []
        for _ in range(buf.read_uint()):
            _x = buf.read_byte()
            assert _x == 1, _x
            self.translations.append([buf.read_wstr(), buf.read_wstr()])

        # self.translations_id = []
        # for _ in range(buf.read_uint()):
        #     _x = buf.read_byte()
        #     assert _x == 1, _x
        #     self.translations_id.append([buf.read_wstr(), buf.read_wstr()])

        self.graphpoints = []

        for _ in range(buf.read_uint()):
            t = buf.read_wstr()
            g = classnames_points[t](self)
            g.from_buffer(buf)
            self.graphpoints.append(g)

        self.graphlinks = []
        for _ in range(buf.read_uint()):
            t = buf.read_wstr()
            g = classnames_links[t](self)
            g.from_buffer(buf)
            self.graphlinks.append(g)

        self.graphrects = []
        for _ in range(buf.read_uint()):
            t = buf.read_wstr()
            g = classnames_rects[t](self)
            g.from_buffer(buf)
            self.graphrects.append(g)

        for gp in self.graphpoints:
            gp.__post_init__()

        for gl in self.graphlinks:
            gl.__post_init__()

        for gr in self.graphrects:
            gr.__post_init__()

        return self

    @classmethod
    def from_bytes(cls, data: bytes):
        buf = Buffer(data)
        return cls.from_buffer(buf)

    def to_bytes(self) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return bytes(buf)

    @classmethod
    def from_svr(cls, path: str):
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_svr(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())


classnames_points = {
    v.classname: v
    for v in (
        GraphPoint,
        Star,
        Planet,
        Ship,
        Item,
        Place,
        Group,
        State,
        ExprOp,
        ExprIf,
        ExprWhile,
        ExprVar,
        Ether,
        Dialog,
        DialogMsg,
        DialogAnswer,
    )
}

classnames_links = {
    v.classname: v
    for v in (
        GraphLink,
        GroupLink,
        StateLink,
        StarLink,
    )
}

classnames_rects = {v.classname: v for v in (GraphRect,)}
