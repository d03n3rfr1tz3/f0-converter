from .base import IrProtocol, LircTiming, lsb_first

RCA_TIMING = LircTiming("SPACE_ENC", 38000, one=(500, 2000), zero=(500, 1000), gap=8000,
                        header=(4000, 4000), ptrail=500)


def encode_rca(address: int, command: int) -> int:
    """4 bit address, 8 bit command, then both inverted."""
    address, command = address & 0xF, command & 0xFF
    return lsb_first(address | command << 4 | (address ^ 0xF) << 12 | (command ^ 0xFF) << 16, 24)


PROTOCOLS = [
    IrProtocol("RCA", 24, 0, RCA_TIMING, encode_rca),
]
