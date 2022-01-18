from __future__ import annotations

from typing import Generic, Literal, Iterator, TypeVar
from types import TracebackType

from .mixin import PrintableMixin

__all__ = ('switch',)

T = TypeVar('T')


class switch(PrintableMixin, Generic[T]):
    __slots__ = ('expr', 'triggered')
    expr: T
    triggered: bool

    def __init__(self, expr: T) -> None:
        self.expr = expr
        self.triggered = False

    def __call__(self, *args: object) -> bool:
        if self.triggered:
            return False

        if not len(args):
            self.triggered = True
            return True

        for arg in args:
            if arg == self.expr:
                self.triggered = True
                return True

        return False

    def __enter__(self) -> switch[T]:
        return self

    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: type[Exception] | Exception,
        traceback: TracebackType,
    ) -> Literal[False]:
        return False

    def __iter__(self) -> Iterator[switch[T]]:
        yield self
