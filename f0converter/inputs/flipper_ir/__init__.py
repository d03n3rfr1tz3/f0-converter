from __future__ import annotations

import re

from ...errors import ConvertError
from ...formats.flipper.fileformat import FlipperFile
from ...model import InputResult
from ..base import Input, InputSettings
from .parsed import read_parsed
from .raw import read_raw

FILETYPE = re.compile(r"^\s*Filetype:\s*IR ", re.MULTILINE)


class FlipperIrInput(Input):
    """Flipper Zero IR files (.ir): parsed and raw signals."""

    name = "flipper-ir"
    description = "Flipper Zero IR file (.ir)"

    def detect(self, text: str) -> bool:
        return bool(FILETYPE.search(text))

    def read(self, path: str, text: str, settings: InputSettings) -> InputResult:
        flipper = FlipperFile.parse(text)
        if not flipper.filetype.startswith("IR "):
            raise ConvertError("not a Flipper IR file (Filetype: %s)" % flipper.filetype)
        result = InputResult(path)
        for block in flipper.blocks:
            name = block.first("name")
            if name is None:
                continue
            kind = block.first("type", "")
            try:
                if kind == "parsed":
                    result.signals.append(read_parsed(block, name, path))
                elif kind == "raw":
                    result.signals.append(read_raw(block, name, path))
                else:
                    raise ConvertError("%s: unknown type %s" % (name, kind or "(none)"))
            except ConvertError as error:
                result.errors.append(str(error))
        if not result.signals and not result.errors:
            raise ConvertError("no signals in the file")
        return result

    def protocols(self) -> list[str]:
        return ["parsed (any protocol)", "raw"]
