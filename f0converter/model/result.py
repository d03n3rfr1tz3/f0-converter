from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class InputResult:
    """What an input read from one file: the signals and what went wrong."""

    source: str
    signals: list = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)     # signals that could not be read
