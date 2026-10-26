from .base import IrProtocol, LircTiming

RC6_TIMING = LircTiming("RC6", 36000, one=(444, 444), zero=(444, 444), gap=27000,
                        header=(2666, 889), toggle_bit_mask=0x10000, rc6_mask=0x10000)


def encode_rc6(address: int, command: int) -> int:
    """Mode 0: start bit, 3 mode bits, toggle bit (double length, rc6_mask), 8 bit address, 8 bit command."""
    return 1 << 20 | (address & 0xFF) << 8 | (command & 0xFF)


PROTOCOLS = [
    IrProtocol("RC6", 21, 0, RC6_TIMING, encode_rc6),
]
