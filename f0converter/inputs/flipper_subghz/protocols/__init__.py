"""Static SubGhz protocols, encoded from their key; one file per protocol."""

from . import intertechno_v3, princeton
from .base import SubGhzProtocol
from .rolling import ROLLING_PROTOCOLS

PROTOCOLS = {protocol.name: protocol for protocol in (princeton.PROTOCOL, intertechno_v3.PROTOCOL)}

__all__ = ["PROTOCOLS", "ROLLING_PROTOCOLS", "SubGhzProtocol"]
