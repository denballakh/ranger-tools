from typing import Union

RACE = lambda *args: args
RACE_FLAG = lambda *args: args
OWNER_FLAG = lambda *args: args
SHIP_TYPE_FLAG = lambda *args: args
ECONOMY_FLAG = lambda *args: args
GOVERNMENT_FLAG = lambda *args: args
WEAPON = lambda *args: args
VAR_TYPE = lambda *args: args
FRIENDSHIP = lambda *args: args
PLACE_TYPE = lambda *args: args
MOVE_TYPE = lambda *args: args
OP_TYPE = lambda *args: args
RELATION = lambda *args: args
ETHER_TYPE = lambda *args: args
ITEM_TYPE = lambda *args: args
EQUIPMENT_TYPE = lambda *args: args

from ..io import IBuffer, OBuffer
from . import *

__all__ = ['SCR']


class Status:
    def __repr__(self) -> str:
        return f'<Status: trader={self.trader!r} warrior={self.warrior!r} pirate={self.pirate!r}>'

    def __init__(self, trader: tuple[int,int], warrior: tuple[int,int], pirate: tuple[int,int]):
        self.trader = trader
        self.warrior = warrior
        self.pirate = pirate

class SCRObj:
    name: str
    def __init__(self): pass
    def __repr__(self) -> str: pass
    @classmethod
    def from_buffer(cls, buf: IBuffer): pass
    def to_buffer(self, buf: OBuffer): pass

class Var(SCRObj):
    name: str
    type: VAR_TYPE
    value: Union[None, int, str, float]

    def __repr__(self) -> str:
        return f'<Var: name={self.name!r} type={self.type!r} value={self.value!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        var = cls()
        var.name = buf.read_wstr()
        var.type = VAR_TYPE(buf.read_byte())
        if var.type is VAR_TYPE.UNKNOWN:
            var.value = None

        if var.type is VAR_TYPE.INTEGER:
            var.value = buf.read_int()

        if var.type is VAR_TYPE.DWORD:
            var.value = buf.read_uint()

        if var.type is VAR_TYPE.FLOAT:
            var.value = buf.read_double()

        if var.type is VAR_TYPE.STRING:
            var.value = buf.read_wstr()

        if var.type is VAR_TYPE.ARRAY:
            var.value = buf.read_int()
            for _ in range(var.value):
                buf.read_wstr()
                buf.read_byte()

        return var

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_byte(int(self.type))
        if self.type is VAR_TYPE.UNKNOWN:
            pass

        if self.type is VAR_TYPE.INTEGER:
            buf.write_int(self.value)

        if self.type is VAR_TYPE.DWORD:
            buf.write_uint(self.value)

        if self.type is VAR_TYPE.FLOAT:
            buf.write_double(self.value)

        if self.type is VAR_TYPE.STRING:
            buf.write_wstr(self.value)

        if self.type is VAR_TYPE.ARRAY:
            buf.write_uint(self.value)
            for _ in range(self.value):
                buf.write_wstr('')
                buf.write_byte(0)

class StarLink(SCRObj):
    end_star: int
    distance: tuple[int, int]
    is_hole: bool

    def __repr__(self) -> str:
        return f'<StarLink: end_star={self.end_star!r} distance={self.distance!r} is_hole={self.is_hole!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        sl = cls()
        sl.end_star = buf.read_uint()
        sl.distance = (buf.read_int(), buf.read_int())
        sl.is_hole = buf.read_bool()
        return sl

    def to_buffer(self, buf: OBuffer):
        buf.write_uint(self.end_star)
        buf.write_int(self.distance[0])
        buf.write_int(self.distance[1])
        buf.write_bool(self.is_hole)

class Planet(SCRObj):
    name: str
    race: RACE_FLAG
    owner: OWNER_FLAG
    economy: ECONOMY_FLAG
    government: GOVERNMENT_FLAG
    range: tuple[int, int]
    dialog: str

    def __repr__(self) -> str:
        return f'<Planet: name={self.name!r} race={self.race!r} owner={self.owner!r} economy={self.economy!r} government={self.government!r} range={self.range!r} dialog={self.dialog!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        p = cls()
        p.name = buf.read_wstr()
        p.race = RACE_FLAG(buf.read_uint())
        p.owner = OWNER_FLAG(buf.read_uint())
        p.economy = ECONOMY_FLAG(buf.read_uint())
        p.government = GOVERNMENT_FLAG(buf.read_uint())
        p.range = (buf.read_int(), buf.read_int())
        p.dialog = buf.read_wstr()
        return p


    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_uint(int(self.race))
        buf.write_uint(int(self.owner))
        buf.write_uint(int(self.economy))
        buf.write_uint(int(self.government))
        buf.write_int(self.range[0])
        buf.write_int(self.range[1])
        buf.write_wstr(self.dialog)

class Ship(SCRObj):
    count: int
    owner: OWNER_FLAG
    type: SHIP_TYPE_FLAG
    is_player: bool
    speed: tuple[int,int]
    weapon: WEAPON
    cargohook: int
    emptyspace: int
    status: Status
    strength: tuple[int,int]
    ruins = ""

    def __repr__(self) -> str:
        return f'<Ship: count={self.count!r} owner={self.owner!r} type={self.type!r} is_player={self.is_player!r} speed={self.speed!r} weapon={self.weapon!r} cargohook={self.cargohook!r} emptyspace={self.emptyspace!r} status={self.status!r} strength={self.strength!r} ruins={self.ruins!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.count = buf.read_int()
        e.owner = OWNER_FLAG(buf.read_uint())
        e.type = SHIP_TYPE_FLAG(buf.read_uint())
        e.is_player = buf.read_bool()
        e.speed = (buf.read_int(), buf.read_int())
        e.weapon = WEAPON(buf.read_uint())
        e.cargohook = buf.read_int()
        e.emptyspace = buf.read_int()
        e.status = Status((buf.read_int(),buf.read_int()),(buf.read_int(),buf.read_int()),(buf.read_int(),buf.read_int()))
        e.strength = (buf.read_int(),buf.read_int())
        e.ruins = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_int(self.count)
        buf.write_uint(int(self.owner))
        buf.write_uint(int(self.type))
        buf.write_bool(self.is_player)
        buf.write_int(self.speed[0])
        buf.write_int(self.speed[1])
        buf.write_uint(int(self.weapon))
        buf.write_int(self.cargohook)
        buf.write_int(self.emptyspace)
        buf.write_int(self.status.trader[0])
        buf.write_int(self.status.trader[1])
        buf.write_int(self.status.warrior[0])
        buf.write_int(self.status.warrior[1])
        buf.write_int(self.status.pirate[0])
        buf.write_int(self.status.pirate[1])
        buf.write_int(self.strength[0])
        buf.write_int(self.strength[1])
        buf.write_wstr(self.ruins)

class Star(SCRObj):
    name: str
    constellation: int
    no_kling: bool
    no_come_kling: bool
    starlinks: list[StarLink]
    planets: list[Planet]
    ships: list[Ship]

    def __repr__(self) -> str:
        return f'<Star:  name={self.name!r} constellation={self.constellation!r} no_kling={self.no_kling!r} no_come_kling={self.no_come_kling!r} starlinks={self.starlinks!r} planets={self.planets!r} ships={self.ships!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        star = cls()
        star.name = buf.read_wstr()
        star.constellation = buf.read_int()
        star.no_kling = buf.read_bool()
        star.no_come_kling = buf.read_bool()

        star.starlinks = []
        star.planets = []
        star.ships = []

        for _ in range(buf.read_uint()):
            e = StarLink.from_buffer(buf)
            star.starlinks.append(e)

        for _ in range(buf.read_uint()):
            e = Planet.from_buffer(buf)
            star.planets.append(e)

        for _ in range(buf.read_uint()):
            e = Ship.from_buffer(buf)
            star.ships.append(e)

        return star


    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_int(self.constellation)
        buf.write_bool(self.no_kling)
        buf.write_bool(self.no_come_kling)

        buf.write_uint(len(self.starlinks))
        for e in self.starlinks:
            e.to_buffer(buf)

        buf.write_uint(len(self.planets))
        for e in self.planets:
            e.to_buffer(buf)

        buf.write_uint(len(self.ships))
        for e in self.ships:
            e.to_buffer(buf)

class Place(SCRObj):
    name: str
    star: str
    type: PLACE_TYPE
    object: str
    angle: float
    distance: float
    radius: int

    def __repr__(self) -> str:
        return f'<Place: name={self.name!r} star={self.star!r} type={self.type!r} object={self.object!r} angle={self.angle!r} distance={self.distance!r} radius={self.radius!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.name = buf.read_wstr()
        e.star = buf.read_wstr()
        e.type = PLACE_TYPE(buf.read_uint())
        if e.type is not PLACE_TYPE.FREE:
            e.object = buf.read_wstr()
        else:
            e.object = ''

        if e.type is PLACE_TYPE.FREE:
            e.angle = buf.read_float()
        else:
            e.angle = 0.0

        if e.type in {PLACE_TYPE.FREE, PLACE_TYPE.TO_STAR, PLACE_TYPE.FROM_SHIP}:
            e.distance = buf.read_float()
        else:
            e.distance = 0.0

        if e.type is not PLACE_TYPE.IN_PLANET:
            e.radius = buf.read_int()
        else:
            e.radius = 0

        if e.type in {PLACE_TYPE.TO_STAR, PLACE_TYPE.FROM_SHIP}:
            e.angle = buf.read_float()
        else:
            e.angle = 0.0

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_wstr(self.star)
        buf.write_uint(int(self.type))
        if self.type is not PLACE_TYPE.FREE:
            buf.write_wstr(self.object)
        if self.type is PLACE_TYPE.FREE:
            buf.write_float(self.angle)
        if self.type in {PLACE_TYPE.FREE, PLACE_TYPE.TO_STAR, PLACE_TYPE.FROM_SHIP}:
            buf.write_float(self.distance)
        if self.type is not PLACE_TYPE.IN_PLANET:
            buf.write_int(self.radius)
        if self.type in {PLACE_TYPE.TO_STAR, PLACE_TYPE.FROM_SHIP}:
            buf.write_float(self.angle)

class Item(SCRObj):
    name: str
    place: str
    kind: ITEM_TYPE
    type: int
    size: int
    level: int
    radius: int
    owner: RACE
    useless: str

    def __repr__(self) -> str:
        return f'<Item: name={self.name!r} place={self.place!r} kind={self.kind!r} type={self.type!r} size={self.size!r} level={self.level!r} radius={self.radius!r} owner={self.owner!r} useless={self.useless!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.name = buf.read_wstr()
        e.place = buf.read_wstr()
        e.kind = ITEM_TYPE(buf.read_uint())
        e.type = buf.read_uint()
        e.size = buf.read_int()
        e.level = buf.read_int()
        e.radius = buf.read_int()
        e.owner = RACE(buf.read_uint())
        e.useless = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_wstr(self.place)
        buf.write_uint(int(self.kind))
        buf.write_uint(self.type)
        buf.write_int(self.size)
        buf.write_int(self.level)
        buf.write_int(self.radius)
        buf.write_uint(int(self.owner))
        buf.write_wstr(self.useless)

class Group(SCRObj):
    name: str
    planet: str
    state: int
    owner: OWNER_FLAG
    type: SHIP_TYPE_FLAG
    count: tuple[int,int]
    speed: tuple[int,int]
    weapon: WEAPON
    cargohook: int
    emptyspace: int
    add_player: bool
    status: Status
    search_distance: int
    dialog: str
    strength: tuple[int,int]
    ruins: str


    def __repr__(self) -> str:
        return f'<Group: name={self.name!r} planet={self.planet!r} state={self.state!r} owner={self.owner!r} type={self.type!r} count={self.count!r} speed={self.speed!r} weapon={self.weapon!r} cargohook={self.cargohook!r} emptyspace={self.emptyspace!r} add_player={self.add_player!r} status={self.status!r} search_distance={self.search_distance!r} dialog={self.dialog!r} strength={self.strength!r} ruins={self.ruins!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.name = buf.read_wstr()
        e.planet = buf.read_wstr()
        e.state = buf.read_int()
        e.owner = OWNER_FLAG(buf.read_uint())
        e.type = SHIP_TYPE_FLAG(buf.read_uint())
        e.count = (buf.read_int(), buf.read_int())
        e.speed = (buf.read_int(), buf.read_int())
        e.weapon = WEAPON(buf.read_uint())
        e.cargohook = buf.read_int()
        e.emptyspace = buf.read_int()
        e.add_player = buf.read_bool()
        e.status = Status((buf.read_int(),buf.read_int()),(buf.read_int(),buf.read_int()),(buf.read_int(),buf.read_int()))
        e.search_distance = buf.read_int()
        e.dialog = buf.read_wstr()
        e.strength = (buf.read_float(), buf.read_float())
        e.ruins = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_wstr(self.planet)
        buf.write_int(self.state)
        buf.write_uint(int(self.owner))
        buf.write_uint(int(self.type))
        buf.write_int(self.count[0])
        buf.write_int(self.count[1])
        buf.write_int(self.speed[0])
        buf.write_int(self.speed[1])
        buf.write_uint(int(self.weapon))
        buf.write_int(self.cargohook)
        buf.write_int(self.emptyspace)
        buf.write_bool(self.add_player)
        buf.write_int(self.status.trader[0])
        buf.write_int(self.status.trader[1])
        buf.write_int(self.status.warrior[0])
        buf.write_int(self.status.warrior[1])
        buf.write_int(self.status.pirate[0])
        buf.write_int(self.status.pirate[1])
        buf.write_int(self.search_distance)
        buf.write_wstr(self.dialog)
        buf.write_float(self.strength[0])
        buf.write_float(self.strength[1])
        buf.write_wstr(self.ruins)

class GroupLink(SCRObj):
    begin: int
    end: int
    relations: tuple[RELATION, RELATION]
    war_weight: tuple[int,int]

    def __repr__(self) -> str:
        return f'<GroupLink>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.begin = buf.read_int()
        e.end = buf.read_int()
        e.relations = (RELATION(buf.read_uint()), RELATION(buf.read_uint()))
        e.war_weight = (buf.read_float(), buf.read_float())
        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_int(self.begin)
        buf.write_int(self.end)
        buf.write_uint(int(self.relations[0]))
        buf.write_uint(int(self.relations[1]))
        buf.write_float(self.war_weight[0])
        buf.write_float(self.war_weight[1])

class State(SCRObj):
    name: str
    type: MOVE_TYPE
    object: str
    attack: list[str]
    take_item: str
    take_all: bool
    out_msg: str
    in_msg: str
    ether: str
    code: str

    def __repr__(self) -> str:
        return f'<State: name={self.name!r} type={self.type!r} object={self.object!r} attack={self.attack!r} take_item={self.take_item!r} take_all={self.take_all!r} out_msg={self.out_msg!r} in_msg={self.in_msg!r} ether={self.ether!r} code={self.code!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.name = buf.read_wstr()
        e.type = MOVE_TYPE(buf.read_uint())
        if e.type not in {MOVE_TYPE.NONE, MOVE_TYPE.FREE}:
            e.object = buf.read_wstr()
        else:
            e.object = ""
        e.attack = []
        for _ in range(buf.read_uint()):
            e.attack.append(buf.read_wstr())
        e.take_item = buf.read_wstr()
        e.take_all = buf.read_bool()
        e.out_msg = buf.read_wstr()
        e.in_msg = buf.read_wstr()
        e.ether = buf.read_wstr()
        e.code = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_uint(int(self.type))
        if self.type not in {MOVE_TYPE.NONE, MOVE_TYPE.FREE}:
            buf.write_wstr(self.object)
        buf.write_uint(len(self.attack))
        for s in self.attack:
            buf.write_wstr(s)
        buf.write_wstr(self.take_item)
        buf.write_bool(self.take_all)
        buf.write_wstr(self.out_msg)
        buf.write_wstr(self.in_msg)
        buf.write_wstr(self.ether)
        buf.write_wstr(self.code)

class Dialog(SCRObj):
    name: str
    code: str

    def __repr__(self) -> str:
        return f'<Dialog: name={self.name!r} code={self.code!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.name = buf.read_wstr()
        e.code = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.name)
        buf.write_wstr(self.code)

class DialogMsg(SCRObj):
    command: str
    code: str

    def __repr__(self) -> str:
        return f'<DialogMsg: command={self.command!r} code={self.code!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.command = buf.read_wstr()
        e.code = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.command)
        buf.write_wstr(self.code)

class DialogAnswer(SCRObj):
    command: str
    answer: str
    code: str

    def __repr__(self) -> str:
        return f'<DialogAnswer: command={self.command!r} answer={self.answer!r} code={self.code!r}>'

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = cls()
        e.command = buf.read_wstr()
        e.answer = buf.read_wstr()
        e.code = buf.read_wstr()

        return e

    def to_buffer(self, buf: OBuffer):
        buf.write_wstr(self.command)
        buf.write_wstr(self.answer)
        buf.write_wstr(self.code)


class SCR:
    SUPPORTED_VERSIONS = {7}

    version: int
    globalvars: list[Var]
    globalcode: str
    localvars: list[Var]
    constellations: int
    stars: list[Star]
    places: list[Place]
    items: list[Item]
    groups: list[Group]
    grouplinks: list[GroupLink]
    initcode: str
    turncode: str
    dialogbegincode: str
    states: list[State]
    dialogs: list[Dialog]
    dialog_msgs: list[DialogMsg]
    dialog_answers: list[DialogAnswer]

    def __init__(self):
        self.version: int = 0
        self.globalvars = []
        self.globalcode = ''
        self.localvars = []
        self.constellations = 0
        self.stars = []
        self.places = []
        self.items = []
        self.groups = []
        self.grouplinks = []
        self.initcode = ''
        self.turncode = ''
        self.dialogbegincode = ''
        self.states = []
        self.dialogs = []
        self.dialog_msgs = []
        self.dialog_answers = []

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        scr = cls()

        scr.version = buf.read_uint()

        if scr.version not in SCR.SUPPORTED_VERSIONS:
            raise ValueError(f'Unsupported script vrrsion: {scr.version}')

        buf.read_uint()

        for _i in range(buf.read_uint()):
            e = Var.from_buffer(buf)
            scr.globalvars.append(e)

        scr.globalcode = buf.read_wstr()

        for _ in range(buf.read_uint()):
            e = Var.from_buffer(buf)
            scr.localvars.append(e)

        scr.constellations = buf.read_int()

        for _ in range(buf.read_uint()):
            e = Star.from_buffer(buf)
            scr.stars.append(e)

        for _ in range(buf.read_uint()):
            e = Place.from_buffer(buf)
            scr.places.append(e)

        for _ in range(buf.read_uint()):
            e = Item.from_buffer(buf)
            scr.items.append(e)

        for _ in range(buf.read_uint()):
            e = Group.from_buffer(buf)
            scr.groups.append(e)

        for _ in range(buf.read_uint()):
            e = GroupLink.from_buffer(buf)
            scr.grouplinks.append(e)

        scr.initcode = buf.read_wstr()
        scr.turncode = buf.read_wstr()
        scr.dialogbegincode = buf.read_wstr()

        for _ in range(buf.read_uint()):
            e = State.from_buffer(buf)
            scr.states.append(e)

        for _ in range(buf.read_uint()):
            e = Dialog.from_buffer(buf)
            scr.dialogs.append(e)

        for _ in range(buf.read_uint()):
            e = DialogMsg.from_buffer(buf)
            scr.dialog_msgs.append(e)

        for _ in range(buf.read_uint()):
            e = DialogAnswer.from_buffer(buf)
            scr.dialog_answers.append(e)

        return scr

    def to_buffer(self, buf: OBuffer):
        buf.write_uint(self.version)

        buf.write_uint(0)

        buf.write_uint(len(self.globalvars))
        for e in self.globalvars:
            e.to_buffer(buf)

        buf.write_wstr(self.globalcode)

        buf.data[4:8] = len(buf.data).to_bytes(4, 'little', signed=False)

        buf.write_uint(len(self.localvars))
        for e in self.localvars:
            e.to_buffer(buf)

        buf.write_int(self.constellations)

        buf.write_uint(len(self.stars))
        for e in self.stars:
            e.to_buffer(buf)

        buf.write_uint(len(self.places))
        for e in self.places:
            e.to_buffer(buf)

        buf.write_uint(len(self.items))
        for e in self.items:
            e.to_buffer(buf)

        buf.write_uint(len(self.groups))
        for e in self.groups:
            e.to_buffer(buf)

        buf.write_uint(len(self.grouplinks))
        for e in self.grouplinks:
            e.to_buffer(buf)

        buf.write_wstr(self.initcode)
        buf.write_wstr(self.turncode)
        buf.write_wstr(self.dialogbegincode)

        buf.write_uint(len(self.states))
        for e in self.states:
            e.to_buffer(buf)

        buf.write_uint(len(self.dialogs))
        for e in self.dialogs:
            e.to_buffer(buf)

        buf.write_uint(len(self.dialog_msgs))
        for e in self.dialog_msgs:
            e.to_buffer(buf)

        buf.write_uint(len(self.dialog_answers))
        for e in self.dialog_answers:
            e.to_buffer(buf)


    @classmethod
    def from_bytes(cls, data: bytes):
        buf = IBuffer.from_bytes(data)
        return cls.from_buffer(buf)

    def to_bytes(self) -> bytes:
        buf = OBuffer()
        self.to_buffer(buf)
        return buf.to_bytes()

    @classmethod
    def from_scr(cls, path: str):
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_scr(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())

