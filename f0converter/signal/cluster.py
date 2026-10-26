"""Merging values that differ only by jitter."""

from __future__ import annotations

DEFAULT_TOLERANCE = 0.25                # relative distance of values that count as equal


def cluster_values(values: list[int], tolerance: float) -> dict[int, int]:
    """Value -> the most frequent value of its group."""
    raise NotImplementedError


def clean_codes(codes: list[list[int]], tolerance: float) -> list[list[int]]:
    """Pulses and pauses are grouped separately, over all given codes together."""
    raise NotImplementedError
