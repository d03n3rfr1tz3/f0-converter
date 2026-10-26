from __future__ import annotations

import sys
from typing import TextIO


class Messages:
    """Messages go to stderr, so stdout carries only the converted text."""

    def __init__(self, stream: TextIO | None = None):
        self.stream = stream
        self.errors = 0

    def info(self, text: str) -> None:
        print(" --> " + text, file=self.stream or sys.stderr)

    def warning(self, where: str, text: str) -> None:
        self.info("Warning: %s: %s" % (where, text))

    def error(self, where: str, text: str) -> None:
        self.errors += 1
        self.info("Error: %s: %s" % (where, text))
