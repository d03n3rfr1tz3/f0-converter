from __future__ import annotations

from ....errors import ConvertError
from ....formats.flipper.fileformat import FlipperBlock
from .base import SubGhzProtocol, key_bits

# timing in µs (KlikAanKlikUit, Nexa)
SHORT = 270
LONG = 1300
SYNC = 2700
END = 10400


def encode(block: FlipperBlock) -> tuple[list[int], str]:
    """Sync, then two pulses per bit: 1 = long pause first, 0 = long pause second, pause at the end."""
    bits = key_bits(block, "Intertechno_V3")
    if len(bits) != 32:
        raise ConvertError("Intertechno_V3 with %d bit is not supported yet, please record as RAW" % len(bits))
    values = [SHORT, SYNC]
    for bit in bits:
        values.extend([SHORT, LONG, SHORT, SHORT] if bit else [SHORT, SHORT, SHORT, LONG])
    values.extend([SHORT, END])
    key = int("".join(str(bit) for bit in bits), 2)
    return values, "Intertechno_V3 id %d, %s %d, %s" % (key >> 6, "group" if key & 32 else "unit", key & 15,
                                                          "on" if key & 16 else "off")


PROTOCOL = SubGhzProtocol("Intertechno_V3", encode)
