"""Text of rf433 code files (see the rf433 project, docs/code-files.md)."""

from __future__ import annotations

from dataclasses import dataclass

VALUES_PER_LINE = 16


@dataclass
class Rf433Code:
    name: str
    values: tuple[int, ...]
    repeat: int | None = None
    comment: str = ""                   # comment line above the code
    annotation: str | None = None       # comment starting with #, written directly above the name


def format_codes(codes: list[Rf433Code], indent: str = "    ") -> list[str]:
    """The name blocks, ready to be pasted into "begin raw_codes"."""
    lines = []
    for code in codes:
        if code.comment:
            lines.append("%s# %s" % (indent, code.comment))
        if code.annotation:
            lines.append(indent + code.annotation)
        lines.append("%sname %s" % (indent, code.name))
        if code.repeat is not None:
            lines.append("%s  repeat %d" % (indent, code.repeat))
        for start in range(0, len(code.values), VALUES_PER_LINE):
            lines.append("%s  %s" % (indent, " ".join(str(value) for value in code.values[start:start + VALUES_PER_LINE])))
    return lines


def format_remote(name: str, repeat: int | None, codes: list[Rf433Code], header: list[str]) -> list[str]:
    """A complete code file with one remote; header are comment lines at the start."""
    lines = list(header) + ["begin remote", "  name    " + name]
    if repeat is not None:
        lines.append("  repeat  %d" % repeat)
    lines += ["", "  begin raw_codes"] + format_codes(codes) + ["  end raw_codes", "end remote"]
    return lines
