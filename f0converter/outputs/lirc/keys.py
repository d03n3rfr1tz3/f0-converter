"""Names of LIRC remotes for the groups of one file."""

from __future__ import annotations


def remote_names(base: str, protocols: list[str], raw_groups: list[tuple[int, int]]) -> list[str]:
    """The first group gets the base name, the others a suffix: base_NEC, base_raw, base_raw_38000 …

    Raw groups are (frequency, duty cycle); the duty cycle is only added when two groups share a frequency.
    """
    names = []
    for protocol in protocols:
        names.append(base if not names else "%s_%s" % (base, protocol))
    for frequency, duty_cycle in raw_groups:
        suffix = "_raw" if len(raw_groups) == 1 else "_raw_%d" % frequency
        if sum(1 for other in raw_groups if other[0] == frequency) > 1:
            suffix += "_%d" % duty_cycle
        names.append(base if not names else base + suffix)
    return names
