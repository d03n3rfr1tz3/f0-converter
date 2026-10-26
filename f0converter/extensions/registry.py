from __future__ import annotations

from ..errors import ConvertError
from .base import Extension
from .webremote import WebRemoteExtension

EXTENSIONS: tuple[type[Extension], ...] = (WebRemoteExtension,)


def find_extension(name: str) -> Extension:
    for extension_class in EXTENSIONS:
        if extension_class.name == name:
            return extension_class()
    raise ConvertError("unknown extension %s, known: %s" % (name, ", ".join(item.name for item in EXTENSIONS)))
