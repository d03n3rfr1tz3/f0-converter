from __future__ import annotations

from ..errors import ConvertError
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
    raise NotImplementedError
