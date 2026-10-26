from __future__ import annotations

from ...errors import ConvertError
from ...formats.flipper.fileformat import FlipperBlock
from ...model import IrRawSignal


def read_raw(block: FlipperBlock, name: str, source: str) -> IrRawSignal:
    """Values as recorded, pulse first; the duty cycle becomes percent."""
    try:
        frequency = int(block.first("frequency", ""))
        duty_cycle = int(round(float(block.first("duty_cycle", "0.33")) * 100))
        values = [int(part) for line in block.all("data") for part in line.split()]
    except ValueError:
        raise ConvertError("%s: invalid frequency, duty_cycle or data" % name) from None
    if not values or min(values) <= 0:
        raise ConvertError("%s: raw data is empty or contains zero or negative values" % name)
    return IrRawSignal(name, source, frequency, duty_cycle, tuple(values))
