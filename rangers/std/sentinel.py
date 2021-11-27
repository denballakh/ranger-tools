from __future__ import annotations

from typing import ClassVar
import sys

__all__ = ('sentinel',)


class sentinel:
    _cache: ClassVar[dict[str, sentinel]] = {}

    name: str

    def __new__(cls, name: str) -> sentinel:
        if name not in cls._cache:
            cls._cache[name] = super().__new__(cls)

        return cls._cache[name]

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f'<{self.name!s}>'

    def __repr__(self) -> str:
        return f'{type(self).__name__!s}({self.name!s})'

    def __eq__(self, other: object) -> bool:
        return self is other
