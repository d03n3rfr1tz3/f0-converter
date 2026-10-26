from __future__ import annotations

from ..errors import ConvertError
from ..formats.flipper.fileformat import read_text
from ..model import InputResult
from .base import Input, InputSettings
from .flipper_ir import FlipperIrInput
from .flipper_subghz import FlipperSubGhzInput

INPUTS: tuple[type[Input], ...] = (FlipperSubGhzInput, FlipperIrInput)


def find_input(name: str) -> Input:
    for input_class in INPUTS:
        if input_class.name == name:
            return input_class()
    raise ConvertError("unknown input %s, known: %s" % (name, ", ".join(item.name for item in INPUTS)))


def read_input(path: str, settings: InputSettings, name: str | None = None) -> InputResult:
    """Reads a file with the input of the given name, or the input that recognizes its content."""
    text = read_text(path)
    if name is not None:
        return find_input(name).read(path, text, settings)
    for input_class in INPUTS:
        item = input_class()
        if item.detect(text):
            return item.read(path, text, settings)
    raise ConvertError("file format not recognized, choose one with --from (%s)" % ", ".join(item.name for item in INPUTS))
