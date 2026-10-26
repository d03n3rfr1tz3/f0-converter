from __future__ import annotations

from typing import Callable

from .base import IrProtocol, LircTiming, lsb_first

SIRC_TIMING = LircTiming("SPACE_ENC|CONST_LENGTH", 40000, one=(1200, 600), zero=(600, 600), gap=45000,
                         header=(2400, 600), min_repeat=2)


def sirc_encoder(address_bits: int) -> Callable[[int, int], int]:
    """7 bit command, then the address."""
    def encode(address: int, command: int) -> int:
        return lsb_first((command & 0x7F) | (address & ((1 << address_bits) - 1)) << 7, 7 + address_bits)
    return encode


PROTOCOLS = [
    IrProtocol("SIRC", 12, 0, SIRC_TIMING, sirc_encoder(5)),
    IrProtocol("SIRC15", 15, 0, SIRC_TIMING, sirc_encoder(8)),
    IrProtocol("SIRC20", 20, 0, SIRC_TIMING, sirc_encoder(13)),
]
