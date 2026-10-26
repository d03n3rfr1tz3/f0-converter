from __future__ import annotations

from .base import Output
from .lirc import LircOutput
from .rf433 import Rf433Output

OUTPUTS: tuple[type[Output], ...] = (Rf433Output, LircOutput)
