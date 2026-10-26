from __future__ import annotations

from dataclasses import dataclass

from ..model import InputResult
from ..signal.cluster import DEFAULT_TOLERANCE
from ..signal.frames import DEFAULT_MIN_GAP


@dataclass
class InputSettings:
    min_gap: int = DEFAULT_MIN_GAP      # in µs; pauses of at least this length end a recorded frame
    tolerance: float = DEFAULT_TOLERANCE


class Input:
    """Reads one kind of file into signals of the model."""

    name = ""                           # used by --from
    description = ""

    def detect(self, text: str) -> bool:
        """True if the file content is of this kind."""
        raise NotImplementedError

    def read(self, path: str, text: str, settings: InputSettings) -> InputResult:
        raise NotImplementedError

    def protocols(self) -> list[str]:
        """Protocols this input understands, for the formats command."""
        return []
