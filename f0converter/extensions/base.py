from __future__ import annotations


class Extension:
    """Adds comments for other tools to the output, e.g. buttons of a web remote."""

    name = ""                           # used by --extension
    description = ""

    def annotate(self, signal, label: str) -> str | None:
        """Comment for one code; the output decides where it goes. label is a readable name of the code."""
        return None

    def header_lines(self) -> list[str]:
        """Comment lines at the start of a generated file, explaining the annotations."""
        return []
