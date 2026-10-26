from __future__ import annotations

from .base import Extension

COLOR = "#FFF"                          # button color of converted codes


class WebRemoteExtension(Extension):
    """Button color and label for a web remote: "#RGB Label"."""

    name = "webremote"
    description = "button color and label for a web remote (#RGB Label)"

    def annotate(self, signal, label: str) -> str | None:
        return "%s %s" % (COLOR, label)

    def header_lines(self) -> list[str]:
        return ["# web remote: button color and label (#RGB Label) behind each code, or in the line",
                "# above the name of raw codes; empty lines between codes are spacers"]
