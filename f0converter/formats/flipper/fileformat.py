"""The Flipper Zero file format: "Key: value" lines, blocks separated by comment lines."""

from __future__ import annotations


class FlipperBlock:
    def __init__(self, entries: list[tuple[str, str]] | None = None):
        self.entries = list(entries or [])

    def first(self, key: str, default: str | None = None) -> str | None:
        for name, value in self.entries:
            if name == key:
                return value
        return default

    def all(self, key: str) -> list[str]:
        return [value for name, value in self.entries if name == key]

    def add(self, key: str, value) -> None:
        self.entries.append((key, str(value)))


class FlipperFile:
    """The first block holds Filetype and Version; IR files have one block per signal after it."""

    def __init__(self, blocks: list[FlipperBlock]):
        self.blocks = blocks

    @property
    def filetype(self) -> str:
        return self.blocks[0].first("Filetype", "") if self.blocks else ""

    @property
    def version(self) -> str:
        return self.blocks[0].first("Version", "") if self.blocks else ""

    @classmethod
    def parse(cls, text: str) -> FlipperFile:
        raise NotImplementedError

    @classmethod
    def read(cls, path: str) -> FlipperFile:
        raise NotImplementedError

    def format(self) -> str:
        raise NotImplementedError

    def write(self, path: str) -> None:
        raise NotImplementedError
