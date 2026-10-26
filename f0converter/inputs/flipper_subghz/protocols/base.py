from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ....formats.flipper.fileformat import FlipperBlock


@dataclass(frozen=True)
class SubGhzProtocol:
    name: str                           # Flipper protocol name
    encode: Callable[[FlipperBlock], tuple[list[int], str]]     # key file -> (values, description)


def key_bits(block: FlipperBlock, protocol: str) -> list[int]:
    """Bits of Key, highest first, as many as Bit says."""
    raise NotImplementedError
