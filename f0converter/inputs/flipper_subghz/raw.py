"""RAW recordings: cut out the frame that repeats most often."""

from __future__ import annotations

from ...formats.flipper.fileformat import FlipperBlock
from ...model import PulseCode
from ..base import InputSettings


def raw_values(block: FlipperBlock) -> list[int]:
    """RAW_Data: +pulse -pause in µs over many lines; same signs are merged, leading pauses dropped."""
    raise NotImplementedError


def convert_raw(block: FlipperBlock, settings: InputSettings) -> tuple[PulseCode, str]:
    raise NotImplementedError
