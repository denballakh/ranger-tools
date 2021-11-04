from __future__ import annotations

from typing import Literal, Type, ClassVar
from types import TracebackType

import time
import json
import os
import statistics

from ..common import fmt_time, round_to_three_chars
from .mixins import PrintableMixin


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

    def __exit__(
        self,
        exc_type: Type[Exception],
        exc_value: Type[Exception] | Exception,
        traceback: TracebackType,
    ) -> Literal[False]:
        self.end_time = time.process_time()
        assert self.start_time is not None
        self.time = self.end_time - self.start_time
        return False


class AdaptiveTimer:
    start_time: float | None
    end_time: float | None
    real_time: float | None
    time: float | None

    atm: AdaptiveTimeMeasurer
    cnt: int
    case_id: str
    extra: float

    _calibration: ClassVar[float] = 0.0

    def __init__(
        self,
        atm: AdaptiveTimeMeasurer,
        case_id: str,
        cnt: int,
        extra: float = 1.0,
    ) -> None:
        self.atm = atm
        self.cnt = max(round(cnt * extra), 1)
        self.case_id = case_id
        self.extra = extra

        self.start_time = None
        self.end_time = None
        self.time = None
        self.real_time = None

    @classmethod
    def calibrate(cls, t: float) -> None:
        assert t >= 0
        cls._calibration = t

    def __enter__(self) -> int:
        self.start_time = time.perf_counter()
        return self.cnt

    def __exit__(
        self,
        exc_type: Type[Exception],
        exc_value: Type[Exception] | Exception,
        traceback: TracebackType,
    ) -> Literal[False]:
        self.end_time = time.perf_counter()
        assert self.start_time is not None
        self.time = self.end_time - self.start_time
        self.real_time = self.time
        self.time /= self.cnt
        self.time -= self._calibration

        stdev = self.atm.register(self)
        stdev, std_unit = fmt_time(stdev)
        stdev = round_to_three_chars(stdev)

        m_time, m_unit = fmt_time(self.time)
        m_time = round_to_three_chars(m_time)

        rt_time, rt_unit = fmt_time(self.real_time)
        rt_time = round_to_three_chars(rt_time)

        print(
            f'{self.case_id:35}{m_time:>4} {m_unit} +- {stdev:>3} {std_unit} '
            f'[{rt_time:>3} {rt_unit} / {self.cnt:>9}]'
        )

        return False


class AdaptiveTimeMeasurer:
    config: dict[str, tuple[int, list[float]]]
    target_time: float
    history_len: int
    growth_ratio: float
    adapt_ratio: float

    def __init__(
        self,
        config_file: str,
        target_time: float = 1.0,
        history_len: int = 5,
        growth_ratio: float = 5,
        adapt_ratio: float = 3,
    ) -> None:
        assert history_len > 2
        assert target_time > 0
        assert growth_ratio >= 2
        assert adapt_ratio >= 0

        self.config_file = config_file
        self.target_time = target_time
        self.history_len = history_len
        self.growth_ratio = growth_ratio
        self.adapt_ratio = adapt_ratio

        if not os.path.isfile(config_file):
            self.config = {}
        else:
            try:
                with open(config_file, 'rt', encoding='utf-8') as file:
                    self.config = json.load(file)
            except json.decoder.JSONDecodeError:
                self.config = {}

    def __call__(self, case_id: str, extra: float = 1.0) -> AdaptiveTimer:
        if case_id not in self.config:
            self.config[case_id] = (1, [])

        return AdaptiveTimer(self, case_id, self.config[case_id][0], extra=extra)

    def __enter__(self) -> AdaptiveTimeMeasurer:
        return self

    def __exit__(
        self,
        exc_type: Type[Exception],
        exc_value: Type[Exception] | Exception,
        traceback: TracebackType,
    ) -> Literal[False]:
        with open(self.config_file, 'wt', encoding='utf-8') as file:
            json.dump(self.config, file)

        return False

    def register(self, at: AdaptiveTimer) -> float:
        assert at.case_id in self.config
        assert at.real_time is not None

        case_id = at.case_id
        value = at.time
        assert value is not None

        cnt, history = self.config[at.case_id]
        rt = at.real_time / at.extra

        if not rt:
            cnt *= int(max(cnt * self.growth_ratio, 1))
        else:
            cnt = round(
                cnt * (self.target_time / rt * self.adapt_ratio + 1) / (self.adapt_ratio + 1)
            )
            cnt = max(round(cnt), 1)

        history = history + [value]
        history = history[: self.history_len]

        self.config[case_id] = cnt, history

        if len(history) >= 3:
            return statistics.stdev(history[1:])
        return 0.0
