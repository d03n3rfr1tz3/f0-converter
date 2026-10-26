"""Names of codes, keys and remotes derived from file and signal names."""

from __future__ import annotations


def base_name(path: str) -> str:
    """File name without folder and without .sub, .ir or .bak."""
    raise NotImplementedError


def plain_name(text: str, fallback: str) -> str:
    """Only letters, digits, _ and -; umlauts are written out."""
    raise NotImplementedError


def parse_rename(text: str) -> tuple[str, str]:
    """"On=an" for --rename-suffix."""
    raise NotImplementedError


def code_name(name: str, renames: list[tuple[str, str]], fallback: str = "New") -> str:
    """Plain name with renamed suffixes, e.g. Light_On -> Light_an with ("On", "an")."""
    raise NotImplementedError


def remote_name(path: str) -> str:
    """"05. HDMI-Switcher.ir" -> HDMI-Switcher"""
    raise NotImplementedError


def key_name(name: str) -> str:
    """LIRC key name: KEY_ and upper case."""
    raise NotImplementedError


def button_label(name: str) -> str:
    raise NotImplementedError


def unique_name(name: str, used: set[str]) -> str:
    """name, name_2, name_3 … whichever is not used yet; it is added to used."""
    raise NotImplementedError
