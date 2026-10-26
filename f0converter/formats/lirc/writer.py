"""Text of lircd.conf remotes."""

from __future__ import annotations

from dataclasses import dataclass, field

from .protocols import LircTiming

EPS = 30
AEPS = 100
DUTY_CYCLE = 33                         # duty cycle of parsed remotes in percent
RAW_PER_LINE = 8                        # values per line in raw_codes


@dataclass
class LircCode:
    name: str
    code: int
    annotation: str | None = None       # written behind the code


@dataclass
class LircParsedRemote:
    name: str
    bits: int
    timing: LircTiming
    codes: list[LircCode] = field(default_factory=list)
    pre_data_bits: int = 0
    pre_data: int = 0


@dataclass
class LircRawCode:
    name: str
    values: tuple[int, ...]
    annotation: str | None = None       # written as a comment line above the name


@dataclass
class LircRawRemote:
    name: str
    frequency: int
    duty_cycle: int
    gap: int
    codes: list[LircRawCode] = field(default_factory=list)


def format_parsed_remote(remote: LircParsedRemote) -> list[str]:
    raise NotImplementedError


def format_raw_remote(remote: LircRawRemote) -> list[str]:
    raise NotImplementedError
