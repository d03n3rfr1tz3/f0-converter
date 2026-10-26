"""Names of codes, keys and remotes derived from file and signal names."""

from __future__ import annotations

import argparse
import os
import re

UMLAUTS = (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss"))
SUFFIXES = (".bak", ".sub", ".ir")


def base_name(path: str) -> str:
    """File name without folder and without .sub, .ir or .bak."""
    name = os.path.basename(path)
    for suffix in SUFFIXES:
        if name.lower().endswith(suffix):
            name = name[:-len(suffix)]
    return name


def plain_name(text: str, fallback: str) -> str:
    """Only letters, digits, _ and -; umlauts are written out."""
    for umlaut, replacement in UMLAUTS:
        text = text.replace(umlaut, replacement)
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text).strip("_") or fallback


def parse_rename(text: str) -> tuple[str, str]:
    """"On=an" for --rename-suffix."""
    old, separator, new = text.partition("=")
    if not (separator and old and new) or plain_name(old, "") != old or plain_name(new, "") != new:
        raise argparse.ArgumentTypeError("expected OLD=NEW with letters, digits, _ and -, got %s" % text)
    return old, new


def code_name(name: str, renames: list[tuple[str, str]], fallback: str = "New") -> str:
    """Plain name with renamed suffixes, e.g. Light_On -> Light_an with ("On", "an")."""
    name = plain_name(name, fallback)
    for old, new in renames:
        if name.lower().endswith("_" + old.lower()):
            return name[:-len(old)] + new
    return name


def remote_name(path: str) -> str:
    """"05. HDMI-Switcher.ir" -> HDMI-Switcher"""
    return plain_name(re.sub(r"^\d+\.?\s*", "", base_name(path)), "Remote")


def key_name(name: str) -> str:
    """LIRC key name: KEY_ and upper case."""
    key = plain_name(name, "BUTTON").replace("-", "_").upper()
    return key if key.startswith(("KEY_", "BTN_")) else "KEY_" + key


def button_label(name: str) -> str:
    return " ".join(name.replace("_", " ").split()) or "?"


def unique_name(name: str, used: set[str]) -> str:
    """name, name_2, name_3 … whichever is not used yet; it is added to used."""
    candidate, number = name, 1
    while candidate in used:
        number += 1
        candidate = "%s_%d" % (name, number)
    used.add(candidate)
    return candidate
