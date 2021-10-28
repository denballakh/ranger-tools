from __future__ import annotations

from typing import Any, Literal, Iterator, Type
from types import TracebackType

import time

from .mixins import PrintableMixin

__all__ = ['Timer', 'switch']


class Timer(PrintableMixin):
    __slots__ = ('start_time', 'end_time', 'time')
    start_time: float | None
    end_time: float | None
    time: float | None

    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None
        self.time = None

    def __enter__(self) -> Timer:
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Type[Exception], exc_value: Type[Exception] | Exception, traceback: TracebackType) -> Literal[False]:
        self.end_time = time.perf_counter()
        assert self.start_time is not None
        self.time = self.end_time - self.start_time
        return False


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

    def __exit__(self, exc_type: Type[Exception], exc_value: Type[Exception] | Exception, traceback: TracebackType) -> Literal[False]:
        return False

    def __iter__(self) -> Iterator[switch]:
        yield self
