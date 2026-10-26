"""RAW recordings: cut out the frame that repeats most often."""

from __future__ import annotations

from ...errors import ConvertError
from ...formats.flipper.fileformat import FlipperBlock
from ...model import PulseCode
from ...signal.cluster import clean_codes
from ...signal.frames import extract_frame
from ..base import InputSettings


def raw_values(block: FlipperBlock) -> list[int]:
    """RAW_Data: +pulse -pause in µs over many lines; same signs are merged, leading pauses dropped."""
    values: list[int] = []
    for line in block.all("RAW_Data"):
        for part in line.split():
            try:
                value = int(part)
            except ValueError:
                raise ConvertError("invalid value in RAW_Data: " + part) from None
            if value == 0 or (not values and value < 0):
                continue
            if values and (values[-1] > 0) == (value > 0):
                values[-1] += value
            else:
                values.append(value)
    return [abs(value) for value in values]


def convert_raw(block: FlipperBlock, settings: InputSettings) -> tuple[PulseCode, str]:
    """The cleaned frame and how it was found."""
    values, description = extract_frame(raw_values(block), settings.min_gap, settings.tolerance)
    return PulseCode(tuple(clean_codes([values], settings.tolerance)[0])), "RAW, " + description
