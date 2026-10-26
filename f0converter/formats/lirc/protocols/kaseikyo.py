from .base import IrProtocol, LircTiming, lsb_first

KASEIKYO_TIMING = LircTiming("SPACE_ENC", 38000, one=(432, 1296), zero=(432, 432), gap=130000,
                             header=(3456, 1728), ptrail=432)


def encode_kaseikyo(address: int, command: int) -> int:
    """address = id (2 bit), vendor (16 bit), genre1 and genre2 (4 bit each); parities as in the Flipper encoder."""
    vendor = (address >> 8) & 0xFFFF
    data = [vendor & 0xFF, vendor >> 8]
    parity = data[0] ^ data[1]
    data.append(((parity & 0xF) ^ (parity >> 4)) | ((address >> 4) & 0xF) << 4)
    data.append((address & 0xF) | (command & 0xF) << 4)
    data.append((((address >> 24) & 3) << 6 | command >> 4) & 0xFF)
    data.append(data[2] ^ data[3] ^ data[4])
    return lsb_first(sum(byte << (8 * index) for index, byte in enumerate(data)), 48)


PROTOCOLS = [
    IrProtocol("Kaseikyo", 48, 24, KASEIKYO_TIMING, encode_kaseikyo),
]
