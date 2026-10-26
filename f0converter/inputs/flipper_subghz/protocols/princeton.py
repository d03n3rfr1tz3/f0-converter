from __future__ import annotations

from ....errors import ConvertError
from ....formats.flipper.fileformat import FlipperBlock
from .base import SubGhzProtocol, key_bits

DEFAULT_TE = 390                        # in µs; when the key file has no TE (Flipper default)
DEFAULT_GUARD = 30                      # pause at the end in TE; when the key file has no Guard_time


def encode(block: FlipperBlock) -> tuple[list[int], str]:
    """Bit 1 = long pulse, short pause; bit 0 = short pulse, long pause; long = 3 TE."""
    bits = key_bits(block, "Princeton")
    try:
        te = int(block.first("TE", str(DEFAULT_TE)))
        guard = int(block.first("Guard_time", str(DEFAULT_GUARD)))
    except ValueError:
        raise ConvertError("Princeton key file with invalid TE or Guard_time") from None
    values = []
    for bit in bits:
        values.extend([3 * te, te] if bit else [te, 3 * te])
    values.extend([te, guard * te])
    return values, "Princeton %d bit, TE %d" % (len(bits), te)


PROTOCOL = SubGhzProtocol("Princeton", encode)
