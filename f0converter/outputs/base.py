from __future__ import annotations

from dataclasses import dataclass, field

from ..extensions import Extension
from ..messages import Messages
from ..model import InputResult


@dataclass
class Document:
    name: str                           # file name when written to a folder
    text: str


@dataclass
class OutputOptions:
    extensions: list[Extension] = field(default_factory=list)

    def annotate(self, signal, label: str) -> str | None:
        """The annotations of all extensions for one code, None without any."""
        annotations = [text for text in (extension.annotate(signal, label) for extension in self.extensions) if text]
        return " ".join(annotations) if annotations else None

    def header_lines(self) -> list[str]:
        return [line for extension in self.extensions for line in extension.header_lines()]


class Output:
    """Writes signals of the model in one format."""

    name = ""
    description = ""

    def accepts(self, signal) -> bool:
        raise NotImplementedError

    def convert(self, results: list[InputResult], options: OutputOptions, messages: Messages) -> list[Document]:
        """Signals the output does not accept and codes it cannot write are reported as errors."""
        raise NotImplementedError
