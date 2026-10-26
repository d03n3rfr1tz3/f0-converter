from __future__ import annotations

from dataclasses import dataclass

from .pulses import PulseCode


@dataclass
class SubGhzSignal:
    name: str                           # original name, e.g. the file name without extension
    source: str                         # file the signal comes from
    code: PulseCode
    raw: bool                           # recorded (True) or encoded from a protocol key (False)
    description: str                    # how the code came about, e.g. "RAW, 5 of 7 frames match"
    frequency: int | None = None        # in Hz
    preset: str = ""                    # Flipper modulation preset
