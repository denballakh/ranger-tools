from __future__ import annotations

from typing import Any, Literal, Iterator, Type
from types import TracebackType

from .mixins import PrintableMixin

__all__ = ['switch']


from .time import Timer # FIXME
__all__.append('Timer')

class switch(PrintableMixin):
    __slots__ = ('expr', 'triggered')
    expr: Any
    triggered: bool

    def __init__(self, expr: Any):
        self.expr = expr
        self.triggered = False

    def __call__(self, *args: Any) -> bool:
        if self.triggered:
            return False

        if len(args) == 0 or any(
            arg(self.expr) if callable(arg) else self.expr == arg for arg in args
        ):
            self.triggered = True
            return True

        return False

    def __enter__(self) -> switch:
        return self

    def __exit__(
        self,
        exc_type: Type[Exception],
        exc_value: Type[Exception] | Exception,
        traceback: TracebackType,
    ) -> Literal[False]:
        return False

    def __iter__(self) -> Iterator[switch]:
        yield self
