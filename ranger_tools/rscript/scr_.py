# from typing import Union

# from ..io import IBuffer, OBuffer
from ..dataclass import *
from . import *

__all__ = ['SCR']



VarListItem = DataClass('VarListItem', [
    ('str', wstr_),
    ('byte', byte_),
])

Var = DataClass('Var', [
    ('name', wstr_),
    ('type', Wrapped(byte_, int, VAR_TYPE, VAR_TYPE.UNKNOWN)),
    ('value', Optional([
        (lambda var: var.type is VAR_TYPE.UNKNOWN, null_),
        (lambda var: var.type is VAR_TYPE.INTEGER, int_),
        (lambda var: var.type is VAR_TYPE.DWORD, uint_),
        (lambda var: var.type is VAR_TYPE.FLOAT, float_),
        (lambda var: var.type is VAR_TYPE.STRING, wstr_),
        (lambda var: var.type is VAR_TYPE.ARRAY, List(VarListItem)),
    ])),
])

StarLink = DataClass('StarLink', [
    ('end_star', int_),
    ('distance', MinMax),
    ('is_hole', bool_),
])

Planet = DataClass('Planet', [
    ('name', wstr_),
    ('race', Wrapped(uint_, int, RACE_FLAG, RACE_FLAG(0))),
    ('owner', Wrapped(uint_, int, OWNER_FLAG, OWNER_FLAG(0))),
    ('economy', Wrapped(uint_, int, ECONOMY_FLAG, ECONOMY_FLAG(0))),
    ('government', Wrapped(uint_, int, GOVERNMENT_FLAG, GOVERNMENT_FLAG(0))),
    ('range', MinMax),
    ('dialog', wstr_),
])

Ship = DataClass('Ship', [
    ('count', int_),
    ('owner', Wrapped(uint_, int, OWNER_FLAG, OWNER_FLAG(0))),
    ('type', Wrapped(uint_, int, SHIP_TYPE_FLAG, SHIP_TYPE_FLAG(0))),
    ('is_player', bool_),
    ('speed', MinMax),
    ('weapon', Wrapped(uint_, int, WEAPON, WEAPON(0))),
    ('cargohook', int_),
    ('emptyspace', int_),
    ('status', Status),
    ('strength', MinMax),
    ('ruins', wstr_),
])

Star = DataClass('Star', [
    ('name', wstr_),
    ('constellation', int_),
    ('no_kling', bool_),
    ('no_come_kling', bool_),
    ('starlinks', List(StarLink)),
    ('planets', List(Planet)),
    ('ships', List(Ship)),
])


Place = DataClass('Place', [
    ('name', wstr_),
    ('star', wstr_),
    ('type', Wrapped(int_, int, PLACE_TYPE, PLACE_TYPE.FREE)),
    ('object', Optional([(lambda place: place.type is not PLACE_TYPE.FREE, wstr_)])),
    ('angle', Optional([(lambda place: place.type is PLACE_TYPE.FREE, float_)])),
    ('distance', Optional([(lambda place: place.type in {PLACE_TYPE.FREE, PLACE_TYPE.TO_STAR, PLACE_TYPE.FROM_SHIP}, float_)])),
    ('radius', Optional([(lambda place: place.type is not PLACE_TYPE.IN_PLANET, int_)])),
    ('angle', Optional([(lambda place: place.type in {PLACE_TYPE.TO_STAR, PLACE_TYPE.FROM_SHIP}, float_)])),
])


Item = DataClass('Item', [
    ('name', wstr_),
    ('place', wstr_),
    ('kind', Wrapped(uint_, int, ITEM_TYPE, ITEM_TYPE(0))),
    ('type', uint_),
    ('size', int_),
    ('level', int_),
    ('radius', int_),
    ('owner', Wrapped(uint_, int, SHIP_TYPE_FLAG, SHIP_TYPE_FLAG(0))),
    ('useless', wstr_),
])

Group = DataClass('Group', [
    ('name', wstr_),
    ('planet', wstr_),
    ('state', int_),
    ('owner', Wrapped(uint_, int, OWNER_FLAG, OWNER_FLAG(0))),
    ('type', Wrapped(uint_, int, SHIP_TYPE_FLAG, SHIP_TYPE_FLAG(0))),
    ('count', MinMax),
    ('speed', MinMax),
    ('weapon', Wrapped(uint_, int, WEAPON, WEAPON(0))),
    ('cargohook', int_),
    ('emptyspace', int_),
    ('add_player', bool_),
    ('status', Status),
    ('search_distance', int_),
    ('dialog', wstr_),
    ('strength', MinMax),
    ('ruins', wstr_),
])

GroupLink = DataClass('GroupLink', [
    ('begin', int_),
    ('end', int_),
    ('relations', DataClass('relation_pair', [
        ('first', Wrapped(uint_, int, RELATION, RELATION(5))),
        ('second', Wrapped(uint_, int, RELATION, RELATION(5))),
    ])),
    ('war_weight', MinMax),
])

State = DataClass('State', [
    ('name', wstr_),
    ('type', Wrapped(uint_, int, MOVE_TYPE, MOVE_TYPE(0))),
    ('object', Optional([(lambda state: state.type not in {MOVE_TYPE.NONE, MOVE_TYPE.FREE}, wstr_)])),
    ('attack', List(wstr_)),
    ('take_item', wstr_),
    ('take_all', bool_),
    ('out_msg', wstr_),
    ('in_msg', wstr_),
    ('ether', wstr_),
    ('code', wstr_),
])


Dialog = DataClass('Dialog', [
    ('name', wstr_),
    ('code', wstr_),
])

DialogMsg = DataClass('DialogMsg', [
    ('command', wstr_),
    ('code', wstr_),
])

DialogAnswer = DataClass('DialogAnswer', [
    ('command', wstr_),
    ('answer', wstr_),
    ('code', wstr_),
])

SCR_ = DataClass('SCR', [
    ('version', Constant(int_, 7)),
    ('_offset', Calculated(uint_, lambda obj, buf: 4 + 4 + 4 + sum(len(v) for v in obj.globalvars) + 2 * len(obj.globalcode) + 2)),
    ('globalvars', List(Var)),
    ('globalcode', wstr_),
    ('localvars', List(Var)),
    ('constellations', int_),
    ('stars', List(Star)),
    ('places', List(Place)),
    ('items', List(Item)),
    ('groups', List(Group)),
    ('grouplinks', List(GroupLink)),
    ('initcode', wstr_),
    ('turncode', wstr_),
    ('dialogbegincode', wstr_),
    ('states', List(State)),
    ('dialogs', List(Dialog)),
    ('dialog_msgs', List(DialogMsg)),
    ('dialog_answers', List(DialogAnswer)),
])


class SCR(SCR_):
    SUPPORTED_VERSIONS = {7}

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
        scr = cls.from_bytes(data)
        assert scr.version in cls.SUPPORTED_VERSIONS, f'Invalid script version: {scr.version}'
        return scr

    def to_scr(self, path: str):
        with open(path, 'wb') as file:
            file.write(self.to_bytes())

    def to_buffer(self, buf):
        SCR_.to_buffer(buf, self)

    @classmethod
    def from_buffer(cls, buf: IBuffer):
        e = SCR_.from_buffer(buf)
        r = e.__repr__

        e.__class__ = cls
        e.__repr__ = r
        # e.__class__.__repr__ = r

        return e
