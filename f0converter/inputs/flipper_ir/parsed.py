from __future__ import annotations

from ...formats.flipper.fileformat import FlipperBlock
from ...model import IrParsedSignal


def read_number(block: FlipperBlock, key: str, name: str) -> int:
    """"07 00 00 00": bytes, lowest first."""
    raise NotImplementedError


def read_parsed(block: FlipperBlock, name: str, source: str) -> IrParsedSignal:
    raise NotImplementedError
