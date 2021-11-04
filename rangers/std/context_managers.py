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
        self.start_time = time.process_time()
        return self

    def __exit__(self, exc_type: Type[Exception], exc_value: Type[Exception] | Exception, traceback: TracebackType) -> Literal[False]:
        self.end_time = time.process_time()
        assert self.start_time is not None
        self.time = self.end_time - self.start_time
        return False

class TimeMeasure(PrintableMixin):
    __slots__ = ('fmtstr', 'cnt', 'start_time', 'end_time', 'time')
    fmtstr: str
    cnt: int
    start_time: float | None
    end_time: float | None
    time: float | None

    def __init__(self, fmtstr: str, cnt: int = 1) -> None:
        self.fmtstr = fmtstr
        self.start_time = None
        self.end_time = None
        self.time = None
        self.cnt = cnt

    def __enter__(self) -> TimeMeasure:
        self.start_time = time.process_time()
        return self

    def __exit__(self, exc_type: Type[Exception], exc_value: Type[Exception] | Exception, traceback: TracebackType) -> Literal[False]:
        self.end_time = time.process_time()
        assert self.start_time is not None
        self.time = self.end_time - self.start_time
        self.time /= self.cnt

        unit = 0
        time1 = self.time
        if not time1:
            unit = None
        else:
            while time1 < 1:
                time1 *= 1000
                unit -= 1
            while time1 >= 1000:
                time1 /= 1000
                unit += 1

        time_s = str(round(time1, 2))

        unit_s = {
            None: '',
            -3: 'ns',
            -2: 'mcs',
            -1: 'ms',
            0: 's',
            1: 'ks',
            2: 'Ms',
            3: 'Gs',
        }

        print(self.fmtstr % (time_s + ' ' + unit_s[unit]))
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
