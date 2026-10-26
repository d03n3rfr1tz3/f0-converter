from __future__ import annotations

from typing import Callable

from .base import IrProtocol, LircTiming

RC5_TIMING = LircTiming("RC5|CONST_LENGTH", 36000, one=(889, 889), zero=(889, 889), gap=113792,
                        plead=889, toggle_bit_mask=0x800)


def rc5_encoder(field: int) -> Callable[[int, int], int]:
    """Field bit (1 = RC5, 0 = RC5X), toggle bit, 5 bit address, 6 bit command; the first start bit is plead."""
    def encode(address: int, command: int) -> int:
        return field << 12 | (address & 0x1F) << 6 | (command & 0x3F)
    return encode


PROTOCOLS = [
    IrProtocol("RC5", 13, 0, RC5_TIMING, rc5_encoder(1)),
    IrProtocol("RC5X", 13, 0, RC5_TIMING, rc5_encoder(0)),
]
