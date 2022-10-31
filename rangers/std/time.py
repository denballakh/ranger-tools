from __future__ import annotations

from typing import Iterator, Literal, Type, ClassVar
from types import TracebackType
from pathlib import Path
from itertools import repeat

import time
import json
import statistics
import math


def fmt_time(t: float) -> tuple[float, str]:
    if not t or math.isinf(t) or math.isnan(t):
        return t, '  '

    sign, t = [-1, 1][t > 0], abs(t)

    units = {
        -5: 'fs',
        -4: 'ps',
        -3: 'ns',
        -2: 'μs',
        -1: 'ms',
        +0: 's ',
    }

    unit_p = 0

    while t >= 999.5 and unit_p + 1 in units:
        t /= 1000.0
        unit_p += 1

    while t < 0.995 and unit_p - 1 in units:
        t *= 1000.0
        unit_p -= 1

    return t * sign, units[unit_p]


def round_to_three_chars(f: float) -> float | int:
    if abs(f) >= 999.5:
        return float('inf')
    if abs(f) >= 9.95:
        return round(f)
    return round(f, 1)


def format_value(t: float, n: int = 3) -> str:
    value, unit = fmt_time(t)
    value = round_to_three_chars(value)
    return f'{value:>{n}} {unit}'


def format_result(key: str, avg: float, dev: float, rt: float, cnt: int) -> str:
    return f'{key:50}{format_value(avg, 4)} ± {format_value(dev)} [{format_value(rt)} / {cnt:>9}]'


def print_stats(file: Path | str) -> None:
    try:
        his: dict[str, tuple[int, float, list[float]]] = json.load(Path(file).open('rt', encoding='utf-8'))
    except OSError:
        return

    for key, (cnt, k, history) in his.items():
        if not history:
            t = float('nan')
        else:
            t = history[-1]


        stdev = statistics.stdev(history[1:]) if len(history) >= 3 else float('nan')

        print(format_result(key, t / k, stdev / k, t * cnt, cnt))


class AdaptiveTimer:
    start_time: float | None
    end_time: float | None
    real_time: float | None
    time: float | None

    atm: AdaptiveTimeMeasurer
    cnt: int
    case_id: str
    extra: float
    k: float

    _calibration: ClassVar[float] = 0.0

    def __init__(
        self,
        atm: AdaptiveTimeMeasurer,
        case_id: str,
        cnt: int,
        extra: float = 1.0,
        k: float = 1.0,
    ) -> None:
        self.atm = atm
        self.cnt = max(round(cnt * extra), 1)
        self.case_id = case_id
        self.extra = extra
        self.k = k

        self.start_time = None
        self.end_time = None
        self.time = None
        self.real_time = None

    @classmethod
    def calibrate(cls, t: float) -> None:
        assert t >= 0
        cls._calibration = t

    def __enter__(self) -> Iterator[None]:
        self.start_time = time.perf_counter()
        return repeat(None, self.cnt)

    def __exit__(
        self,
        exc_type: Type[Exception] | None,
        exc_value: Type[Exception] | Exception | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        if exc_type is None:
            self.end_time = time.perf_counter()
        else:

            self.end_time = float('inf')

        assert self.start_time is not None
        self.real_time = self.end_time - self.start_time
        self.time = self.real_time / self.cnt - self._calibration

        print(
            format_result(
                self.case_id,
                self.time / self.k,
                self.atm.register(self) / self.k,
                self.real_time,
                self.cnt,
            )
        )

        return False


class AdaptiveTimeMeasurer:
    config: dict[str, tuple[int, float, list[float]]]
    target_time: float
    history_len: int
    config_file: Path

    def __init__(
        self,
        config_file: str,
        target_time: float = 1.0,
        history_len: int = 5,
        flush: bool = False,
    ) -> None:
        assert history_len > 2
        assert target_time > 0

        self.config_file = Path(config_file)
        self.target_time = target_time
        self.history_len = history_len

        try:
            if flush:
                raise FileNotFoundError

            config = json.load(self.config_file.open('rt', encoding='utf-8'))
            self.config = {}
            for key, (cnt, k, history) in config.items():
                self.config[key] = cnt, k, history # ?

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            self.config = {}

    def __call__(self, case_id: str, extra: float = 1.0, k: float = 1.0) -> AdaptiveTimer:
        if case_id not in self.config:
            self.config[case_id] = (1, k, [])

        return AdaptiveTimer(self, case_id, self.config[case_id][0], extra=extra, k=k)

    def __enter__(self) -> AdaptiveTimeMeasurer:
        return self

    def __exit__(
        self,
        exc_type: Type[Exception],
        exc_value: Type[Exception] | Exception,
        traceback: TracebackType,
    ) -> Literal[False]:
        with open(self.config_file, 'wt', encoding='utf-8') as file:
            json.dump(self.config, file, indent=4)

        return False

    def register(self, at: AdaptiveTimer) -> float:
        assert at.case_id in self.config
        assert at.real_time is not None

        case_id = at.case_id
        value = at.time
        assert value is not None

        cnt, k, history = self.config[at.case_id]
        rt = at.real_time

        if math.isinf(value):
            self.config[case_id] = 1, at.k, []
            return float('nan')

        if not value:
            cnt *= int(max(cnt * 2, 1))

        else:
            cnt = round(cnt * (at.extra * self.target_time / rt * 2 + 1) / (2 + 1))
            cnt = max(round(cnt), 1)

        history = history + [value]
        history = history[-self.history_len :]

        self.config[case_id] = cnt, at.k, history

        if len(history) >= 3:
            return statistics.stdev(history[1:])
        return float('nan')
