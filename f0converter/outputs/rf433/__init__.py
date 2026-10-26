from __future__ import annotations

from dataclasses import dataclass, field

from ...messages import Messages
from ...model import InputResult, SubGhzSignal
from ...signal.cluster import DEFAULT_TOLERANCE
from ..base import Document, Output, OutputOptions


@dataclass
class Rf433Options(OutputOptions):
    remote: str | None = None           # write a complete code file for this remote
    repeat: int | None = None           # repeat of the remote, only with remote
    name: str | None = None             # code name for a single signal
    renames: list[tuple[str, str]] = field(default_factory=list)    # suffixes of code names, e.g. ("On", "an")
    tolerance: float = DEFAULT_TOLERANCE


class Rf433Output(Output):
    """rf433 code files: one frame per code, recordings of one conversion cleaned together."""

    name = "rf433"
    description = "rf433 code file (433 MHz OOK)"

    def accepts(self, signal) -> bool:
        return isinstance(signal, SubGhzSignal)

    def convert(self, results: list[InputResult], options: Rf433Options, messages: Messages) -> list[Document]:
        raise NotImplementedError
