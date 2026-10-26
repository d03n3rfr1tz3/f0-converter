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
        """Lines without ":" are ignored, comment lines end a block."""
        blocks = [FlipperBlock()]
        for line in text.lstrip("\ufeff").splitlines():
            line = line.strip()
            if line.startswith("#"):
                if blocks[-1].entries:
                    blocks.append(FlipperBlock())
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            blocks[-1].add(key.strip(), value.strip())
        return cls([block for block in blocks if block.entries])

    @classmethod
    def read(cls, path: str) -> FlipperFile:
        return cls.parse(read_text(path))

    def format(self) -> str:
        return "#\n".join("".join("%s: %s\n" % entry for entry in block.entries) for block in self.blocks)

    def write(self, path: str) -> None:
        with open(path, "w", encoding="utf-8", newline="\n") as file:
            file.write(self.format())


def read_text(path: str) -> str:
    """Text of a file; a BOM is dropped, invalid characters are replaced."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as file:
        return file.read()
