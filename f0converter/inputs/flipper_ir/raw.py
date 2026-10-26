from __future__ import annotations

from ...formats.flipper.fileformat import FlipperBlock
from ...model import IrRawSignal


def read_raw(block: FlipperBlock, name: str, source: str) -> IrRawSignal:
    raise NotImplementedError
