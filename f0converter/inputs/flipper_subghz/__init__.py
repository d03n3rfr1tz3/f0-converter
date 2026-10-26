from __future__ import annotations

from ...model import InputResult
from ..base import Input, InputSettings
from .protocols import PROTOCOLS


class FlipperSubGhzInput(Input):
    """Flipper Zero SubGhz files (.sub): RAW recordings and keys of static protocols."""

    name = "flipper-subghz"
    description = "Flipper Zero SubGhz file (.sub)"

    def detect(self, text: str) -> bool:
        raise NotImplementedError

    def read(self, path: str, text: str, settings: InputSettings) -> InputResult:
        raise NotImplementedError

    def protocols(self) -> list[str]:
        return ["RAW"] + sorted(PROTOCOLS)
