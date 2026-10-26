from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class LircTiming:
    """Timing of a protocol family in lircd.conf; pairs are (pulse, space) in µs."""

    flags: str
    frequency: int
    one: tuple[int, int]
    zero: tuple[int, int]
    gap: int
    header: tuple[int, int] | None = None
    plead: int | None = None
    ptrail: int | None = None
    repeat: tuple[int, int] | None = None
    min_repeat: int | None = None
    toggle_bit_mask: int | None = None
    rc6_mask: int | None = None


@dataclass(frozen=True)
class IrProtocol:
    """A Flipper IR protocol and how its address and command become a LIRC code."""

    name: str                           # Flipper protocol name
    bits: int                           # bits of the LIRC code
    prefix_bits: int                    # leading bits that become pre_data when all codes share them
    timing: LircTiming
    encode: Callable[[int, int], int]   # (address, command) -> LIRC code


def lsb_first(data: int, bits: int) -> int:
    """The Flipper sends bit 0 of its data first, LIRC writes the first bit sent as the highest bit."""
    return int(format(data & ((1 << bits) - 1), "0%db" % bits)[::-1], 2)
