from .base import IrProtocol, LircTiming

KASEIKYO_TIMING = LircTiming("SPACE_ENC", 38000, one=(432, 1296), zero=(432, 432), gap=130000,
                             header=(3456, 1728), ptrail=432)


def encode_kaseikyo(address: int, command: int) -> int:
    raise NotImplementedError


PROTOCOLS = [
    IrProtocol("Kaseikyo", 48, 24, KASEIKYO_TIMING, encode_kaseikyo),
]
