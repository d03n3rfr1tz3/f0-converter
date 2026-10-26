from .base import IrProtocol, LircTiming

NEC_TIMING = LircTiming("SPACE_ENC|CONST_LENGTH", 38000, one=(560, 1690), zero=(560, 560), gap=108000,
                        header=(9000, 4500), ptrail=560, repeat=(9000, 2250))
PIONEER_TIMING = LircTiming("SPACE_ENC", 40000, one=(500, 1500), zero=(500, 500), gap=26500,
                            header=(8500, 4225), ptrail=500, min_repeat=1)


def encode_nec(address: int, command: int) -> int:
    raise NotImplementedError


def encode_nec_ext(address: int, command: int) -> int:
    raise NotImplementedError


def encode_nec42(address: int, command: int) -> int:
    raise NotImplementedError


def encode_nec42_ext(address: int, command: int) -> int:
    raise NotImplementedError


PROTOCOLS = [
    IrProtocol("NEC", 32, 16, NEC_TIMING, encode_nec),
    IrProtocol("NECext", 32, 16, NEC_TIMING, encode_nec_ext),
    IrProtocol("NEC42", 42, 26, NEC_TIMING, encode_nec42),
    IrProtocol("NEC42ext", 42, 26, NEC_TIMING, encode_nec42_ext),
    IrProtocol("Pioneer", 32, 16, PIONEER_TIMING, encode_nec),
]
