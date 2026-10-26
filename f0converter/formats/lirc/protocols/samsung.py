from .base import IrProtocol, LircTiming, lsb_first

SAMSUNG_TIMING = LircTiming("SPACE_ENC|CONST_LENGTH", 38000, one=(550, 1650), zero=(550, 550), gap=108000,
                            header=(4500, 4500), ptrail=550)


def encode_samsung32(address: int, command: int) -> int:
    """8 bit address twice, 8 bit command and its inverse."""
    address, command = address & 0xFF, command & 0xFF
    return lsb_first(address | address << 8 | command << 16 | (command ^ 0xFF) << 24, 32)


PROTOCOLS = [
    IrProtocol("Samsung32", 32, 16, SAMSUNG_TIMING, encode_samsung32),
]
