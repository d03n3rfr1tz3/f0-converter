from __future__ import annotations

import re

from ...errors import ConvertError
from ...formats.flipper.fileformat import FlipperFile
from ...model import InputResult, PulseCode, SubGhzSignal
from ...names import base_name
from ..base import Input, InputSettings
from .protocols import PROTOCOLS, ROLLING_PROTOCOLS
from .raw import convert_raw

FILETYPE = re.compile(r"^\s*Filetype:\s*Flipper SubGhz", re.MULTILINE)


class FlipperSubGhzInput(Input):
    """Flipper Zero SubGhz files (.sub): RAW recordings and keys of static protocols."""

    name = "flipper-subghz"
    description = "Flipper Zero SubGhz file (.sub)"

    def detect(self, text: str) -> bool:
        return bool(FILETYPE.search(text))

    def read(self, path: str, text: str, settings: InputSettings) -> InputResult:
        flipper = FlipperFile.parse(text)
        if not flipper.blocks:
            raise ConvertError("empty file")
        if not flipper.filetype.startswith("Flipper SubGhz"):
            raise ConvertError("not a Flipper SubGhz file (Filetype: %s)" % flipper.filetype)
        block = flipper.blocks[0]
        result = InputResult(path)

        frequency = None
        text_frequency = block.first("Frequency", "")
        if text_frequency.isdigit():
            frequency = int(text_frequency)
        elif text_frequency:
            result.warnings.append("invalid Frequency %s" % text_frequency)

        protocol = block.first("Protocol", "")
        if block.all("RAW_Data"):
            code, description = convert_raw(block, settings)
            raw = True
        elif protocol in PROTOCOLS:
            values, description = PROTOCOLS[protocol].encode(block)
            code, raw = PulseCode(tuple(values)), False
        elif protocol in ROLLING_PROTOCOLS:
            raise ConvertError("%s is a rolling code, a recording cannot be sent again" % protocol)
        else:
            raise ConvertError("protocol %s is not supported yet, please record as RAW" % (protocol or "(none)"))

        result.signals.append(SubGhzSignal(base_name(path), path, code, raw, description, frequency,
                                           block.first("Preset", "")))
        return result

    def protocols(self) -> list[str]:
        return ["RAW"] + sorted(PROTOCOLS)
