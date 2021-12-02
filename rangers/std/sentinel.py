from __future__ import annotations

from typing import ClassVar, Final, final

from enum import Enum

__all__ = ('sentinel', 'SentinelType')


@final
class SentinelType(Enum):
    instance = None

    def __repr__(self) -> str:
        return '<sentinel>'


sentinel: Final = SentinelType.instance
