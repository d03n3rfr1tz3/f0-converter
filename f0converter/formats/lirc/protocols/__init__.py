"""LIRC knowledge of the IR protocols the Flipper Zero knows, one file per protocol family."""

from . import kaseikyo, nec, rc5, rc6, rca, samsung, sirc
from .base import IrProtocol, LircTiming

PROTOCOLS = {protocol.name: protocol
             for family in (nec, samsung, rca, sirc, kaseikyo, rc5, rc6) for protocol in family.PROTOCOLS}

__all__ = ["PROTOCOLS", "IrProtocol", "LircTiming"]
