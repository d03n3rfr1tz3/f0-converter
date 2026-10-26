from .base import IrProtocol, LircTiming, lsb_first

NEC_TIMING = LircTiming("SPACE_ENC|CONST_LENGTH", 38000, one=(560, 1690), zero=(560, 560), gap=108000,
                        header=(9000, 4500), ptrail=560, repeat=(9000, 2250))
PIONEER_TIMING = LircTiming("SPACE_ENC", 40000, one=(500, 1500), zero=(500, 500), gap=26500,
                            header=(8500, 4225), ptrail=500, min_repeat=1)


def encode_nec(address: int, command: int) -> int:
    """8 bit address and command, each followed by its inverse."""
    address, command = address & 0xFF, command & 0xFF
    return lsb_first(address | (address ^ 0xFF) << 8 | command << 16 | (command ^ 0xFF) << 24, 32)


def encode_nec_ext(address: int, command: int) -> int:
    """16 bit address and command without inverse."""
    return lsb_first((address & 0xFFFF) | (command & 0xFFFF) << 16, 32)


def encode_nec42(address: int, command: int) -> int:
    """13 bit address and 8 bit command, each followed by its inverse."""
    address, command = address & 0x1FFF, command & 0xFF
    return lsb_first(address | (address ^ 0x1FFF) << 13 | command << 26 | (command ^ 0xFF) << 34, 42)


def encode_nec42_ext(address: int, command: int) -> int:
    """26 bit address and 16 bit command without inverse."""
    return lsb_first((address & 0x3FFFFFF) | (command & 0xFFFF) << 26, 42)


PROTOCOLS = [
    IrProtocol("NEC", 32, 16, NEC_TIMING, encode_nec),
    IrProtocol("NECext", 32, 16, NEC_TIMING, encode_nec_ext),
    IrProtocol("NEC42", 42, 26, NEC_TIMING, encode_nec42),
    IrProtocol("NEC42ext", 42, 26, NEC_TIMING, encode_nec42_ext),
    IrProtocol("Pioneer", 32, 16, PIONEER_TIMING, encode_nec),
]
