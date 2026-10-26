"""Text of rf433 code files (see the rf433 project, docs/code-files.md)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rf433Code:
    name: str
    values: tuple[int, ...]
    repeat: int | None = None
    comment: str = ""                   # comment line above the code
    annotation: str | None = None       # comment line directly above the name


def format_codes(codes: list[Rf433Code], indent: str = "    ") -> list[str]:
    """The name blocks, ready to be pasted into "begin raw_codes"."""
    raise NotImplementedError


def format_remote(name: str, repeat: int | None, codes: list[Rf433Code], header: list[str]) -> list[str]:
    """A complete code file with one remote."""
    raise NotImplementedError
