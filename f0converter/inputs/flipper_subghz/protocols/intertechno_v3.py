from __future__ import annotations

from ....formats.flipper.fileformat import FlipperBlock
from .base import SubGhzProtocol

# timing in µs (KlikAanKlikUit, Nexa)
SHORT = 270
LONG = 1300
SYNC = 2700
END = 10400


def encode(block: FlipperBlock) -> tuple[list[int], str]:
    """Sync, then two pulses per bit: 1 = long pause first, 0 = long pause second, pause at the end."""
    raise NotImplementedError


PROTOCOL = SubGhzProtocol("Intertechno_V3", encode)
