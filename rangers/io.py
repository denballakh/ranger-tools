"""!
@file
"""
from __future__ import annotations

from typing import (
    TypeVar,
    Generic,
)

__all__ = [
    'AbstractIBuffer',
    'Stack',
]

T = TypeVar('T')


class AbstractIBuffer(Generic[T]):
    data: list[T]
    pos: int

    def __init__(self, data: list[T]) -> None:
        self.data = data
        self.pos = 0

    def get(self) -> T:
        assert 0 <= self.pos < len(self.data)
        result = self.data[self.pos]
        self.pos += 1
        return result

    def end(self) -> bool:
        return 0 <= self.pos < len(self.data)


class Stack(Generic[T]):
    data: list[T]

    def __init__(self, lst: list[T] = None) -> None:
        if lst is None:
            self.data = []
        else:
            self.data = lst

    def __repr__(self) -> str:
        return str(self.data)

    def push(self, value: T) -> None:
        self.data.append(value)

    def pop(self) -> T:
        assert self.data, 'Stack underflow'
        return self.data.pop()
