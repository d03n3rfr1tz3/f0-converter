"""Names of LIRC remotes for the groups of one file."""

from __future__ import annotations


def remote_names(base: str, protocols: list[str], raw_groups: list[tuple[int, int]]) -> list[str]:
    """The first group gets the base name, the others a suffix: base_NEC, base_raw, base_raw_38000 …"""
    raise NotImplementedError
