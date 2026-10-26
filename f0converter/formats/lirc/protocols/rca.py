from .base import IrProtocol, LircTiming

RCA_TIMING = LircTiming("SPACE_ENC", 38000, one=(500, 2000), zero=(500, 1000), gap=8000,
                        header=(4000, 4000), ptrail=500)


def encode_rca(address: int, command: int) -> int:
    raise NotImplementedError


PROTOCOLS = [
    IrProtocol("RCA", 24, 0, RCA_TIMING, encode_rca),
]
