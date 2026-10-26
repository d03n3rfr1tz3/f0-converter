from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Callable

from ....errors import ConvertError

from ....formats.flipper.fileformat import FlipperBlock


@dataclass(frozen=True)
class SubGhzProtocol:
    name: str                           # Flipper protocol name
    encode: Callable[[FlipperBlock], tuple[list[int], str]]     # key file -> (values, description)


def key_bits(block: FlipperBlock, protocol: str) -> list[int]:
    """Bits of Key, highest first, as many as Bit says."""
    try:
        bits = int(block.first("Bit", ""))
        key = int(re.sub(r"\s+", "", block.first("Key", "")), 16)
    except ValueError:
        raise ConvertError("%s key file without valid Bit or Key" % protocol) from None
    return [(key >> index) & 1 for index in range(bits - 1, -1, -1)]
