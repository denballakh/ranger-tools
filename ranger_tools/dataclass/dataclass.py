raise NotImplementedError('dataclass module is deprecated')

from ..io import IBuffer, OBuffer


class NOT_SET_TYPE:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return 'NOT_SET'


NOT_SET = NOT_SET_TYPE()


class DataType:
    def __new__(cls):
        raise NotImplementedError

    @classmethod
    def to_buffer(cls, buf, obj, parent=None):
        raise NotImplementedError

    @classmethod
    def from_buffer(cls, buf, parent=None) -> object:
        raise NotImplementedError


def PrimitiveClass(typename, param=None):
    defaults = {
        'int': 0,
        'uint': 0,
        'byte': 0,
        'bool': False,
        'float': 0.0,
        'double': 0.0,
        'bytes': b'',
        'str': '',
        'wstr': '',
        'char': '',
        'wchar': '',
    }

    class primitiveclass(DataType):
        def __new__(cls):
            return defaults[typename]

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            buf.write_unknown(typename, obj, param)

        @classmethod
        def from_buffer(cls, buf, parent=None) -> object:
            return buf.read_unknown(typename, param)

    return primitiveclass


int_ = PrimitiveClass('int')
uint_ = PrimitiveClass('uint')
byte_ = PrimitiveClass('byte')
bool_ = PrimitiveClass('bool')
float_ = PrimitiveClass('float')
double_ = PrimitiveClass('double')
bytes_ = lambda l: PrimitiveClass('bytes', l)
str_ = PrimitiveClass('str')
wstr_ = PrimitiveClass('wstr')
char_ = PrimitiveClass('char')
wchar_ = PrimitiveClass('wchar')

null_ = bytes_(0)


def Optional(fields: list[tuple[lambda:..., DataType]]):
    class optional(DataType):
        def __new__(cls):
            return NOT_SET

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            for pred, field_type in fields:
                if pred(parent):
                    field_type.to_buffer(buf, obj, parent=parent)

        @classmethod
        def from_buffer(cls, buf, parent=None) -> object:
            for pred, field_type in fields:
                if pred(parent):
                    return field_type.from_buffer(buf, parent=parent)
            return NOT_SET

    return optional


def List(field_type):
    class list_(DataType):
        def __new__(cls):
            return []

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            buf.write_uint(len(obj))
            for elem in obj:
                field_type.to_buffer(buf, elem, parent=parent)

        @classmethod
        def from_buffer(cls, buf, parent=None) -> object:
            length = buf.read_uint()
            result = []
            for _ in range(length):
                result.append(field_type.from_buffer(buf, parent=parent))
            return result

    return list_


def Wrapped(field_type, decode, encode, default):
    class wrapped(DataType):
        def __new__(cls):
            return default

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            field_type.to_buffer(buf, decode(obj), parent=parent)

        @classmethod
        def from_buffer(cls, buf, parent=None) -> object:
            return encode(field_type.from_buffer(buf, parent=parent))

    return wrapped

def Calculated(field_type, f):
    class calculated(DataType):
        def __new__(cls):
            return field_type()

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            field_type.to_buffer(buf, f(parent, buf))

        @classmethod
        def from_buffer(cls, buf, parent=None) -> object:
            return field_type.from_buffer(buf)

    return calculated

def Constant(field_type, value):
    class constant(DataType):
        def __new__(cls):
            return value

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            assert obj == value
            field_type.to_buffer(buf, value, parent=parent)

        @classmethod
        def from_buffer(cls, buf, parent=None) -> object:
            assert field_type.from_buffer(buf, parent=parent) == value
            return value

    return constant


def DataClass(classname: str, fields: list[tuple[str, DataType]]):
    class dataclass(DataType):
        def __new__(cls):
            class _:
                def to_buffer(self, buf, parent=None):
                    dataclass.to_buffer(buf, self, parent=parent)

                def __repr__(self) -> str:
                    printed = set()
                    s = f'<{classname}:'
                    for name, _ in fields:
                        if name not in printed:
                            s += f' {name}={getattr(self, name)!r}'
                            printed |= {name}
                    s += '>'
                    return s

                def __len__(self) -> int:
                    buf = OBuffer()
                    self.to_buffer(buf)
                    return len(buf.data)

            elem = _()
            for field_name, field_type in fields:
                setattr(elem, field_name, field_type())
            return elem

        @classmethod
        def to_buffer(cls, buf, obj, parent=None):
            for field_name, field_type in fields:
                field_type.to_buffer(buf, getattr(obj, field_name), parent=obj)

        @classmethod
        def from_buffer(cls, buf: IBuffer, parent=None):
            e = cls()
            for field_name, field_type in fields:
                setattr(e, field_name, field_type())
            for field_name, field_type in fields:
                f = field_type.from_buffer(buf, parent=e)

                if f is not NOT_SET:
                    setattr(e, field_name, f)
            return e

    return dataclass



MinMax = DataClass('MinMax', [
    ('min', int_),
    ('max', int_),
])

Status = DataClass('Status', [
    ('trader', MinMax),
    ('warrior', MinMax),
    ('pirate', MinMax),
])
Point = DataClass('Point', [
    ('x', int_),
    ('y', int_),
])

Rect = DataClass('Rect', [
    ('top', int_),
    ('left', int_),
    ('right', int_),
    ('bottom', int_),
])
