from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PulseCode:
    """One frame of an OOK signal: values in µs, pulse first, ending with the pause after the frame."""

    values: tuple[int, ...]

    @property
    def duration(self) -> int:
        return sum(self.values)

    @property
    def pause(self) -> int:
        return self.values[-1]

    def describe(self) -> str:
        return "%d values, %.1f ms, pause %d us" % (len(self.values), self.duration / 1000, self.pause)
