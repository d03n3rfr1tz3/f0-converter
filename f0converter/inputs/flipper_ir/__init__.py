from __future__ import annotations

from ...model import InputResult
from ..base import Input, InputSettings


class FlipperIrInput(Input):
    """Flipper Zero IR files (.ir): parsed and raw signals."""

    name = "flipper-ir"
    description = "Flipper Zero IR file (.ir)"

    def detect(self, text: str) -> bool:
        raise NotImplementedError

    def read(self, path: str, text: str, settings: InputSettings) -> InputResult:
        raise NotImplementedError

    def protocols(self) -> list[str]:
        return ["parsed (any protocol)", "raw"]
