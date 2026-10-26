from .base import IrProtocol, LircTiming

SAMSUNG_TIMING = LircTiming("SPACE_ENC|CONST_LENGTH", 38000, one=(550, 1650), zero=(550, 550), gap=108000,
                            header=(4500, 4500), ptrail=550)


def encode_samsung32(address: int, command: int) -> int:
    raise NotImplementedError


PROTOCOLS = [
    IrProtocol("Samsung32", 32, 16, SAMSUNG_TIMING, encode_samsung32),
]
