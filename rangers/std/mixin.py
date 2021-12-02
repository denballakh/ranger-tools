from __future__ import annotations
from typing import (
    Any,
    Container,
    Sequence,
    Type,
    TypeVar,
    Iterable,
    final,
    Final,
    ClassVar,
    Literal,
)

import sys

# from functools import wraps
from ..common import get_attributes
from ..buffer import Buffer

__all__ = [
    'PrintableMixin',
    'DataMixin',
    'UniqueMixin',
]

T = TypeVar('T')


class Mixin:
    """Base class for all mixins"""

    __slots__ = ()


class PrintFormat:
    fmt: str
    fmt_empty: str
    attr_sep: str
    value_sep: str
    use_private_attrs: bool
    attrs: tuple[str, ...]
    pos_only_attrs: tuple[str, ...]

    def __init__(
        self,
        *,
        fmt: str = '<{class_name}: {attrs}>',
        fmt_empty: str | None = None,
        attr_sep: str = ' ',
        value_sep: str = '=',
        use_private_attrs: bool = False,
        attrs: Sequence[str] = (),
        pos_only_attrs: Sequence[str] = (),
    ) -> None:
        assert frozenset(pos_only_attrs) <= frozenset(attrs), (attrs, pos_only_attrs)
        self.fmt = fmt
        # print(fmt_empty)
        self.fmt_empty = fmt_empty if fmt_empty is not None else fmt
        # print(self.fmt_empty)
        self.attr_sep = attr_sep
        self.value_sep = value_sep
        self.use_private_attrs = use_private_attrs
        self.attrs = tuple(attrs)
        self.pos_only_attrs = tuple(pos_only_attrs)

    def format(self, obj: object) -> str:
        # print(self.fmt_empty)
        assert frozenset(self.pos_only_attrs) <= frozenset(self.attrs), (
            self.attrs,
            self.pos_only_attrs,
        )

        attrs: Iterable[tuple[str, object]] = get_attributes(obj)

        if self.attrs:
            attrs = filter(lambda pair: pair[0] in self.attrs, attrs)

        if not self.use_private_attrs:
            attrs = filter(
                lambda pair: not pair[0].startswith('_')
                or pair[0] in self.pos_only_attrs
                or pair[0] in self.attrs,
                attrs,
            )

        if self.pos_only_attrs:
            attrs = sorted(
                attrs,
                key=lambda pair: (
                    pair[0] not in self.pos_only_attrs,
                    self.pos_only_attrs.index(pair[0])
                    if pair[0] in self.pos_only_attrs
                    else self.attrs.index(pair[0])
                    if pair[0] in self.attrs
                    else 0,
                    pair[0],
                ),
            )

        attrs_l: Iterable[str] = (
            f'{value!r}' if attr in self.pos_only_attrs else f'{attr!s}{self.value_sep}{value!r}'
            for attr, value in attrs
        )

        attrs_s: str = self.attr_sep.join(attrs_l)

        if attrs_s:
            fmt = self.fmt
        else:
            fmt = self.fmt_empty

        return fmt.replace('{class_name}', obj.__class__.__qualname__).replace('{attrs}', attrs_s)

    def as_dict(self) -> dict[str, Any]:
        return {
            'fmt': self.fmt,
            'fmt_empty': self.fmt_empty,
            'attr_sep': self.attr_sep,
            'value_sep': self.value_sep,
            'use_private_attrs': self.use_private_attrs,
            'attrs': self.attrs,
            'pos_only_attrs': self.pos_only_attrs,
        }

    def replace(self, **kwargs: Any) -> PrintFormat:
        return self.__class__(**{**self.as_dict(), **kwargs})


class PrintableMixin(Mixin):
    __slots__ = ()

    __repr_fmt__: ClassVar[PrintFormat] = PrintFormat(
        fmt='{class_name}({attrs})',
        attr_sep=', ',
        value_sep='=',
    )
    __str_fmt__: ClassVar[PrintFormat] = PrintFormat(
        fmt='<{class_name}: {attrs}>',
        fmt_empty='<{class_name}>',
        attr_sep=' ',
        value_sep='=',
    )

    @final
    def __str__(self) -> str:
        return self.__str_fmt__.format(self)

    @final
    def __repr__(self) -> str:
        return self.__repr_fmt__.format(self)


DMT = TypeVar('DMT', bound='DataMixin')


class DataMixin(Mixin):
    __slots__ = ()

    @classmethod
    def from_buffer(cls: Type[DMT], buf: Buffer) -> DMT:
        raise NotImplementedError(f'Method {cls.__name__}.from_buffer is abstract')

    @classmethod
    def from_bytes(cls: Type[DMT], data: bytes) -> DMT:
        buf = Buffer(data)
        return cls.from_buffer(buf)

    @classmethod
    def from_file(cls: Type[DMT], path: str) -> DMT:
        with open(path, 'rb') as file:
            data = file.read()
        return cls.from_bytes(data)

    def to_buffer(self: DMT, buf: Buffer):
        raise NotImplementedError(f'Method {type(self).__name__}.to_buffer is abstract.')

    def to_bytes(self: DMT) -> bytes:
        buf = Buffer()
        self.to_buffer(buf)
        return buf.to_bytes()

    def to_file(self: DMT, path: str) -> None:
        with open(path, 'wb') as file:
            file.write(self.to_bytes())


class UniqueMixin(Mixin):
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return self is other

    def __ne__(self, other: object) -> bool:
        return self is not other

    def __hash__(self) -> int:
        return id(self)
