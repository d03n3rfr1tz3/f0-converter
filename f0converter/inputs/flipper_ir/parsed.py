from __future__ import annotations

from ...errors import ConvertError
from ...formats.flipper.fileformat import FlipperBlock
from ...model import IrParsedSignal


def read_number(block: FlipperBlock, key: str, name: str) -> int:
    """"07 00 00 00": bytes, lowest first."""
    try:
        parts = block.first(key, "").split()
        if not parts:
            raise ValueError
        return sum(int(part, 16) << (8 * index) for index, part in enumerate(parts))
    except ValueError:
        raise ConvertError("%s: invalid %s" % (name, key)) from None


def read_parsed(block: FlipperBlock, name: str, source: str) -> IrParsedSignal:
    """The protocol is not checked here, outputs know which protocols they can write."""
    return IrParsedSignal(name, source, block.first("protocol", ""), read_number(block, "address", name),
                          read_number(block, "command", name))
