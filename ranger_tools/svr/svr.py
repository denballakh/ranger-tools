from ..io import IBuffer, OBuffer
from ..scr import *

def rgb_to_dword(r, g, b):
    return (b << 16) | (g << 8) | r

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
    __slots__ = "top", "left", "width", "height"
    def __repr__(self):
        return f'<Rect: top={self.top!r} left={self.left!r} width={self.width!r} height={self.height!r}>'

    def __init__(self, top, left, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height


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

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.classname)
        buf.write_int(self.pos.x)
        buf.write_int(self.pos.y)
        buf.write_wstr(self.text)
        buf.write_int(-1)

    def from_buffer(self, buf: IBuffer):
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

    def to_buffer(self, s):
        s.write_wstr(self.classname)
        s.write_int(self._script.index(self.begin))
        s.write_int(self._script.index(self.end))
        s.write_uint(self.ord_num)
        s.write_bool(self.has_arrow)

    def from_buffer(self, buf: IBuffer):
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

    def to_buffer(self, s):
        s.write_wstr(self.classname)
        s.write_int(self.rect.top)
        s.write_int(self.rect.left)
        s.write_int(self.rect.right)
        s.write_int(self.rect.bottom)
        s.write_byte(self.fill_style)
        s.write_uint(self.fill_color)
        s.write_byte(self.border_style)
        s.write_uint(self.border_color)
        s.write_uint(self.border_size)
        s.write_float(self.border_coef)
        s.write_uint(self.text_align_x)
        s.write_uint(self.text_align_y)
        s.write_bool(self.text_align_rect)
        s.write_wstr(self.text)
        s.write_uint(self.text_color)
        s.write_wstr(self.font)
        s.write_uint(self.font_size)
        s.write_bool(self.is_bold)
        s.write_bool(self.is_italic)
        s.write_bool(self.is_underline)

    def from_buffer(self, s: IBuffer):
        self.classname = s.read_wstr()
        self.rect.top = s.read_int()
        self.rect.left = s.read_int()
        self.rect.right = s.read_int()
        self.rect.bottom = s.read_int()
        self.fill_style = s.read_byte()
        self.fill_color = s.read_uint()
        self.border_style = s.read_byte()
        self.border_color = s.read_uint()
        self.border_size = s.read_uint()
        self.border_coef = s.read_float()
        self.text_align_x = s.read_uint()
        self.text_align_y = s.read_uint()
        self.text_align_rect = s.read_bool()
        self.text = s.read_wstr()
        self.text_color = s.read_uint()
        self.font = s.read_wstr()
        self.font_size = s.read_uint()
        self.is_bold = s.read_bool()
        self.is_italic = s.read_bool()
        self.is_underline = s.read_bool()
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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(self.constellation)
        s.write_uint(self.priority)
        s.write_bool(self.is_subspace)
        s.write_bool(self.no_kling)
        s.write_bool(self.no_come_kling)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.constellation = s.read_uint()
        self.priority = s.read_uint()
        self.is_subspace = s.read_bool()
        self.no_kling = s.read_bool()
        self.no_come_kling = s.read_bool()

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(int(self.race))
        s.write_uint(int(self.owner))
        s.write_uint(int(self.economy))
        s.write_uint(int(self.government))
        s.write_int(self.range.min)
        s.write_int(self.range.max)
        s.write_int(self._script.index(self.dialog))

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)

        self.race = RACE_FLAG(s.read_uint())
        self.owner = OWNER_FLAG(s.read_uint())
        self.economy = ECONOMY_FLAG(s.read_uint())
        self.government = GOVERNMENT_FLAG(s.read_uint())
        self.range.min = s.read_int()
        self.range.max = s.read_int()
        self.dialog = s.read_int()

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
        self.status = Status(MinMax(0, 100),
                             MinMax(0, 100),
                             MinMax(0, 100))
        self.score = MinMax(0, 1000000)
        self.strength = MinMax(0, 0)
        self.ruins = ""

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_int(self.count)
        s.write_uint(int(self.owner))
        s.write_uint(int(self.type))
        s.write_bool(self.is_player)
        s.write_int(self.speed.min)
        s.write_int(self.speed.max)
        s.write_uint(int(self.weapon))
        s.write_uint(self.cargohook)
        s.write_int(self.emptyspace)
        s.write_int(self.rating.min)
        s.write_int(self.rating.max)
        s.write_int(self.status.trader.min)
        s.write_int(self.status.trader.max)
        s.write_int(self.status.warrior.min)
        s.write_int(self.status.warrior.max)
        s.write_int(self.status.pirate.min)
        s.write_int(self.status.pirate.max)
        s.write_int(self.score.min)
        s.write_int(self.score.max)
        s.write_float(self.strength.min)
        s.write_float(self.strength.max)
        s.write_wstr(self.ruins)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.count = s.read_int()
        self.owner = OWNER_FLAG(s.read_uint())
        self.type = SHIP_TYPE_FLAG(s.read_uint())
        self.is_player = s.read_bool()
        self.speed = MinMax(s.read_int(), s.read_int())
        self.weapon = WEAPON(s.read_uint())
        self.cargohook = s.read_uint()
        self.emptyspace = s.read_int()
        self.rating = MinMax(s.read_int(), s.read_int())
        self.status = Status(MinMax(s.read_int(), s.read_int()), MinMax(s.read_int(), s.read_int()), MinMax(s.read_int(), s.read_int()))
        self.score = MinMax(s.read_int(), s.read_int())
        self.strength = MinMax(s.read_int(), s.read_int())
        self.ruins = s.read_wstr()

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(self.kind)
        s.write_uint(self.type)
        s.write_int(self.size)
        s.write_uint(self.level)
        s.write_int(self.radius)
        s.write_uint(int(self.owner))
        s.write_wstr(self.useless)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.kind = s.read_uint()
        self.type = s.read_uint()
        self.size = s.read_int()
        self.level = s.read_uint()
        self.radius = s.read_int()
        self.owner = RACE(s.read_uint())
        self.useless = s.read_wstr()

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(self.type)
        s.write_float(self.angle)
        s.write_float(self.dist)
        s.write_int(self.radius)
        s.write_int(self._script.index(self.obj))

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.type = s.read_uint()
        self.angle = s.read_float()
        self.dist = s.read_float()
        self.radius = s.read_int()
        self.obj = s.read_int()

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
        self.status = Status(MinMax(0, 100),
                             MinMax(0, 100),
                             MinMax(0, 100))
        self.score = MinMax(0, 1000000)
        self.search_dist = 10000
        self.dialog = None
        self.strength = MinMax(0, 0)
        self.ruins = ""

    def __post_init__(self):
        self.dialog = self._script.graphpoints[self.dialog] if self.dialog != -1 else None

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(int(self.owner))
        s.write_uint(int(self.type))
        s.write_int(self.count.min)
        s.write_int(self.count.max)
        s.write_int(self.speed.min)
        s.write_int(self.speed.max)
        s.write_uint(int(self.weapon))
        s.write_uint(self.cargohook)
        s.write_int(self.emptyspace)
        s.write_uint(int(self.friendship))
        s.write_bool(self.add_player)
        s.write_int(self.rating.min)
        s.write_int(self.rating.max)
        s.write_int(self.status.trader.min)
        s.write_int(self.status.trader.max)
        s.write_int(self.status.warrior.min)
        s.write_int(self.status.warrior.max)
        s.write_int(self.status.pirate.min)
        s.write_int(self.status.pirate.max)
        s.write_int(self.score.min)
        s.write_int(self.score.max)
        s.write_int(self.search_dist)
        s.write_int(self._script.index(self.dialog))
        s.write_float(self.strength.min)
        s.write_float(self.strength.max)
        s.write_wstr(self.ruins)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)

        self.owner = OWNER_FLAG(s.read_uint())
        self.type = SHIP_TYPE_FLAG(s.read_uint())
        self.count.min = s.read_int()
        self.count.max = s.read_int()
        self.speed.min = s.read_int()
        self.speed.max = s.read_int()
        self.weapon = WEAPON(s.read_uint())
        self.cargohook = s.read_uint()
        self.emptyspace = s.read_int()
        self.friendship = FRIENDSHIP(s.read_uint())
        self.add_player = s.read_bool()
        self.rating.min = s.read_int()
        self.rating.max = s.read_int()
        self.status.trader.min = s.read_int()
        self.status.trader.max = s.read_int()
        self.status.warrior.min = s.read_int()
        self.status.warrior.max = s.read_int()
        self.status.pirate.min = s.read_int()
        self.status.pirate.max = s.read_int()
        self.score.min = s.read_int()
        self.score.max = s.read_int()
        self.search_dist = s.read_int()
        self.dialog = s.read_int()
        self.strength.min = s.read_float()
        self.strength.max = s.read_float()
        self.ruins = s.read_wstr()

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
            self.attack_groups[i] = self._script.graphpoints[self.attack_groups[i]] if self.attack_groups[i] != -1 else None


    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(int(self.type))
        s.write_int(self._script.index(self.obj))
        s.write_uint(len(self.attack_groups))
        for ag in self.attack_groups:
            s.write_int(self._script.index(ag))
        s.write_int(self._script.index(self.item))
        s.write_bool(self.take_all)
        s.write_wstr(self.out_msg)
        s.write_wstr(self.in_msg)
        s.write_uint(int(self.ether_type))
        s.write_wstr(self.ether_uid)
        s.write_wstr(self.ether_msg)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.type = MOVE_TYPE(s.read_uint())
        self.obj = s.read_int()
        self.attack_groups = []
        for _ in range(s.read_uint()):
            self.attack_groups.append(s.read_int())
        self.item = s.read_int()
        self.take_all = s.read_bool()
        self.out_msg = s.read_wstr()
        self.in_msg = s.read_wstr()
        self.ether_type = ETHER_TYPE(s.read_uint())
        self.ether_uid = s.read_wstr()
        self.ether_msg = s.read_wstr()

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_wstr(self.expression)
        s.write_byte(int(self.type))

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.expression = s.read_wstr()
        self.type = OP_TYPE(s.read_byte())

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_wstr(self.expression)
        s.write_byte(int(self.type))

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.expression = s.read_wstr()
        self.type = OP_TYPE(s.read_byte())

        return self



class ExprWhile(GraphPoint):
    classname = "Twhile"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} expression={self.expression!r} type={self.type!r}>'


    def __init__(self, script, pos= None, text=""):
        GraphPoint.__init__(self, script, pos, text)
        self.expression = ""
        self.type = OP_TYPE.NORMAL  # op

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_wstr(self.expression)
        s.write_byte(int(self.type))

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.expression = s.read_wstr()
        self.type = OP_TYPE(s.read_byte())

        return self



class ExprVar(GraphPoint):
    classname = "TVar"

    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r} type={self.type!r} init_value={self.init_value!r} is_global={self.is_global!r}>'


    def __init__(self, script, pos=None, text="VarNew"):
        GraphPoint.__init__(self, script, pos, text)
        self.type = VAR_TYPE_S.UNKNOWN  # svar
        self.init_value = ""
        self.is_global = False

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(int(self.type))
        s.write_wstr(self.init_value)
        s.write_bool(self.is_global)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.type = VAR_TYPE_S(s.read_uint())
        self.init_value = s.read_wstr()
        self.is_global = s.read_bool()

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_uint(int(self.type))
        s.write_wstr(self.uid)
        s.write_wstr(self.msg)
        for f in self.focus:
            s.write_wstr(f)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)

        self.type = ETHER_TYPE(s.read_uint())
        self.uid = s.read_wstr()
        self.msg = s.read_wstr()
        self.focus = []
        for _ in range(3):
            self.focus.append(s.read_wstr())

        return self



class Dialog(GraphPoint):
    classname = "TDialog"
    def __repr__(self) -> str:
        return f'<{self.classname}: pos={self.pos!r} text={self.text!r}>'

    def __init__(self, script, pos=None, text="DialogNew"):
        GraphPoint.__init__(self, script, pos, text)

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_wstr(self.msg)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.msg = s.read_wstr()

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

    def to_buffer(self, s):
        GraphPoint.to_buffer(self, s)
        s.write_wstr(self.msg)

    def from_buffer(self, s: IBuffer):
        GraphPoint.from_buffer(self, s)
        self.msg = s.read_wstr()

        return self



class StarLink(GraphLink):
    classname = "TStarLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r} dist={self.dist!r} deviation={self.deviation!r} relation={self.relation!r} is_hole={self.is_hole!r}>'


    def __init__(self, script, begin=None, end=None, ord_num=0,
                 has_arrow=False):
        GraphLink.__init__(self, script, begin, end, ord_num, has_arrow)
        self.dist = MinMax(0, 150)
        self.deviation = 25
        self.relation = MinMax(0, 100)
        self.is_hole = False

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphLink.to_buffer(self, s)
        s.write_int(self.dist.min)
        s.write_int(self.dist.max)
        s.write_int(self.deviation)
        s.write_int(self.relation.min)
        s.write_int(self.relation.max)
        s.write_bool(self.is_hole)

    def from_buffer(self, s: IBuffer):
        GraphLink.from_buffer(self, s)
        self.dist.min = s.read_int()
        self.dist.max = s.read_int()
        self.deviation = s.read_int()
        self.relation.min = s.read_int()
        self.relation.max = s.read_int()
        self.is_hole = s.read_bool()

        return self



class GroupLink(GraphLink):
    classname = "TGroupLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r} relations={self.relations!r} war_weight={self.war_weight!r}>'


    def __init__(self, script, begin=None, end=None, ord_num=0,
                 has_arrow=True):
        GraphLink.__init__(self, script, begin, end, ord_num, has_arrow)
        self.relations = [rel_.NOCHANGE, rel_.NOCHANGE]
        self.war_weight = MinMax(0.0, 1000.0)

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphLink.to_buffer(self, s)
        for r in self.relations:
            s.write_uint(int(r))
        s.write_float(self.war_weight.min)
        s.write_float(self.war_weight.max)


    def from_buffer(self, s: IBuffer):
        GraphLink.from_buffer(self, s)
        self.relations = [RELATION(s.read_uint()), RELATION(s.read_uint)]
        self.war_weight.min = s.read_float()
        self.war_weight.max = s.read_float()

        return self

class StateLink(GraphLink):
    classname = "TStateLink"

    def __repr__(self) -> str:
        return f'<{self.classname}: begin={self.begin!r} end={self.end!r} ord_num={self.ord_num!r} has_arrow={self.has_arrow!r} expression={self.expression!r} priority={self.priority!r}>'


    def __init__(self, script, begin=None, end=None, ord_num=0,
                 has_arrow=True):
        GraphLink.__init__(self, script, begin, end, ord_num, has_arrow)
        self.expression = ""
        self.priority = 0

    def __post_init__(self):
        pass

    def to_buffer(self, s):
        GraphLink.to_buffer(self, s)
        s.write_wstr(self.expression)
        s.write_int(self.priority)


    def from_buffer(self, s: IBuffer):
        GraphLink.from_buffer(self, s)
        self.expression = s.read_wstr()
        self.priority = s.read_int()

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
        self.translations_id = []

        self.graphpoints = []
        self.graphlinks = []
        self.graphrects = []

    # def add(self, clsname, pos=None):
    #     if not pos:
    #         pos = random_point()
    #     gp = classnames[clsname](self, pos)
    #     self.graphpoints.append(gp)
    #     return gp

    # def link(self, begin, end):
    #     if isinstance(begin, Star) and isinstance(end, Star):
    #         gl = StarLink(self, begin, end)
    #     elif isinstance(begin, Group) and isinstance(end, Group):
    #         gl = GroupLink(self, begin, end)
    #     elif isinstance(begin, State) and isinstance(end, State):
    #         gl = StateLink(self, begin, end)
    #     else:
    #         gl = GraphLink(self, begin, end)
    #     self.graphlinks.append(gl)
    #     # end.pos = near_point(begin.pos)
    #     return gl

    def find(self, name):
        if name == "": return None
        for gp in self.graphpoints:
            if gp.text == name:
                return gp
        return None

    def index(self, gp):
        if isinstance(gp, str):
            gp = self.find(gp)
        if not gp:
            return -1
        return self.graphpoints.index(gp)

    def find_link_begin(self, gp, clsname):
        cls = classnames[clsname]
        for gl in self.graphlinks:
            if (gl.begin is gp) and isinstance(gl.end, cls):
                return gl

    def to_buffer(self, s):
        # s = stream.from_io(f)

        s.write_bytes(b'\x55\x44\x33\x22')
        s.write_uint(self.version)
        s.write_int(self.viewpos.x)
        s.write_int(self.viewpos.y)
        s.write_wstr(self.name)
        s.write_wstr(self.filename)

        # self.textfilenames.save(s)
        # self.translations.save(s)
        # self.translations_id.save(s)

        s.write_uint(len(self.graphpoints))
        for gp in self.graphpoints:
            gp.to_buffer(s)

        s.write_uint(len(self.graphlinks))
        for gl in self.graphlinks:
            gl.to_buffer(s)

        s.write_uint(len(self.graphrects))
        for gr in self.graphrects:
            gr.to_buffer(s)

    def from_buffer(self, s):
        try:
            _x = s.read(4)
            assert _x == b'\x55\x44\x33\x22', _x
            self.version = s.read_uint()
            self.viewpos.x = s.read_int()
            self.viewpos.y = s.read_int()
            self.name = s.read_wstr()
            self.filename = s.read_wstr()
            s.read(6)
            self.textfilenames = []
            for _ in range(1):
                self.textfilenames.append([s.read_wstr(), s.read_wstr()])
            s.read(6)

            self.translations = []
            self.translations_id = []

            self.graphpoints = []
            c = s.read_uint()
            if c == 0:
                c = s.read_uint()
            else:
                s.read(1)
            print(c)
            for _ in range(c):
                t = s.read_wstr()
                g = classnames_points[t](self)
                g.from_buffer(s)
                self.graphpoints.append(g)

            self.graphlinks = []
            for _ in range(s.read_uint()):
                t = s.read_wstr()
                g = classnames_links[t](self)
                g.from_buffer(s)
                self.graphlinks.append(g)

            self.graphrects = []
            for _ in range(s.read_uint()):
                t = s.read_wstr()
                g = classnames_rects[t](self)
                g.from_buffer(s)
                self.graphrects.append(g)

            for gp in self.graphpoints:
                gp.__post_init__()

            for gl in self.graphlinks:
                gl.__post_init__()

            for gr in self.graphrects:
                gr.__post_init__()

        except:
            print(hex(s.pos))
            print(vars(self))
            1/0

        return self

    @classmethod
    def from_bytes(cls, data: bytes):
        buf = IBuffer.from_bytes(data)
        return cls().from_buffer(buf)

    def to_bytes(self) -> bytes:
        buf = OBuffer()
        self.to_buffer(buf)
        return buf.to_bytes()

    @classmethod
    def from_svr(cls, path: str):
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_svr(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())


classnames_points = {v.classname: v for v in (
    Star, Planet, Ship, Item, Place, Group, State, ExprOp, ExprIf, ExprWhile,
    ExprVar, Ether, Dialog, DialogMsg, DialogAnswer
)}
classnames_links = {v.classname: v for v in (
    GraphLink, GroupLink, StateLink, StarLink
)}
classnames_rects = {v.classname: v for v in (
    GraphRect,
)}
