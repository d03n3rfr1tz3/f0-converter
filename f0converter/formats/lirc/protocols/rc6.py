from .base import IrProtocol, LircTiming

RC6_TIMING = LircTiming("RC6", 36000, one=(444, 444), zero=(444, 444), gap=27000,
                        header=(2666, 889), toggle_bit_mask=0x10000, rc6_mask=0x10000)


def encode_rc6(address: int, command: int) -> int:
    raise NotImplementedError


PROTOCOLS = [
    IrProtocol("RC6", 21, 0, RC6_TIMING, encode_rc6),
]
