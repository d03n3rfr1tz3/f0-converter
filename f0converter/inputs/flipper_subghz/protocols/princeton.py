from __future__ import annotations

from ....formats.flipper.fileformat import FlipperBlock
from .base import SubGhzProtocol

DEFAULT_TE = 390                        # in µs; when the key file has no TE (Flipper default)
DEFAULT_GUARD = 30                      # pause at the end in TE; when the key file has no Guard_time


def encode(block: FlipperBlock) -> tuple[list[int], str]:
    """Bit 1 = long pulse, short pause; bit 0 = short pulse, long pause; long = 3 TE."""
    raise NotImplementedError


PROTOCOL = SubGhzProtocol("Princeton", encode)
