"""Finding the frame that repeats most often in a recording."""

from __future__ import annotations

DEFAULT_MIN_GAP = 5000                  # in µs; pauses of at least this length end a frame
ABSOLUTE_TOLERANCE = 120                # in µs; short values may differ at least this much
MIN_FRAME_VALUES = 16                   # shorter frames are noise


def split_frames(values: list[int], min_gap: int) -> list[tuple[list[int], bool]]:
    """[(frame, ends with a gap)]"""
    raise NotImplementedError


def similar(first: list[int], second: list[int], tolerance: float) -> bool:
    raise NotImplementedError


def median(values: list[int]) -> int:
    raise NotImplementedError


def extract_frame(values: list[int], min_gap: int, tolerance: float) -> tuple[list[int], str]:
    """The median frame of the biggest group of similar frames, and a description."""
    raise NotImplementedError
