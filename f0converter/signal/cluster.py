"""Merging values that differ only by jitter."""

from __future__ import annotations

import collections

DEFAULT_TOLERANCE = 0.25                # relative distance of values that count as equal


def cluster_values(values: list[int], tolerance: float) -> dict[int, int]:
    """Value -> the most frequent value of its group.

    Sorted values form one group while each is at most (1 + tolerance) times the previous one.
    """
    counts = collections.Counter(values)
    mapping = {}
    group: list[int] = []
    for value in sorted(counts) + [None]:
        if group and (value is None or value > group[-1] * (1 + tolerance)):
            best = max(group, key=lambda item: counts[item])
            for item in group:
                mapping[item] = best
            group = []
        if value is not None:
            group.append(value)
    return mapping


def clean_codes(codes: list[list[int]], tolerance: float) -> list[list[int]]:
    """Pulses and pauses are grouped separately, over all given codes together."""
    pulses = cluster_values([value for values in codes for value in values[0::2]], tolerance)
    pauses = cluster_values([value for values in codes for value in values[1::2]], tolerance)
    return [[pulses[value] if index % 2 == 0 else pauses[value] for index, value in enumerate(values)]
            for values in codes]
