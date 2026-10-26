from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IrParsedSignal:
    """An IR signal of a known protocol, in the terms of the Flipper Zero."""

    name: str
    source: str
    protocol: str                       # Flipper protocol name, e.g. NEC or Samsung32
    address: int
    command: int


@dataclass
class IrRawSignal:
    """An IR signal as recorded."""

    name: str
    source: str
    frequency: int                      # carrier in Hz
    duty_cycle: int                     # in percent
    values: tuple[int, ...]             # in µs, pulse first
