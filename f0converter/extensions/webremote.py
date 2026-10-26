from __future__ import annotations

from .base import Extension

COLOR = "#FFF"                          # button color of converted codes


class WebRemoteExtension(Extension):
    """Button color and label for a web remote: "#RGB Label"."""

    name = "webremote"
    description = "button color and label for a web remote (#RGB Label)"

    def annotate(self, signal, label: str) -> str | None:
        raise NotImplementedError

    def header_lines(self) -> list[str]:
        raise NotImplementedError
