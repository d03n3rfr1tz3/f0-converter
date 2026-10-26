"""Finding the frame that repeats most often in a recording."""

from __future__ import annotations

import collections

from ..errors import ConvertError

DEFAULT_MIN_GAP = 5000                  # in µs; pauses of at least this length end a frame
ABSOLUTE_TOLERANCE = 120                # in µs; short values may differ at least this much
MIN_FRAME_VALUES = 16                   # shorter frames are noise


def split_frames(values: list[int], min_gap: int) -> list[tuple[list[int], bool]]:
    """[(frame, ends with a gap)]; a frame ends with a pause of at least min_gap."""
    frames = []
    frame: list[int] = []
    for index in range(0, len(values) - 1, 2):
        frame.extend(values[index:index + 2])
        if values[index + 1] >= min_gap:
            frames.append((frame, True))
            frame = []
    if len(values) % 2:
        frame.append(values[-1])
    if frame:
        frames.append((frame, False))
    return frames


def similar(first: list[int], second: list[int], tolerance: float) -> bool:
    """Same length and every value within the tolerance; the pause at the end is not compared."""
    if len(first) != len(second):
        return False
    for a, b in zip(first[:-1], second[:-1]):
        if abs(a - b) > max(tolerance * max(a, b), ABSOLUTE_TOLERANCE):
            return False
    return True


def median(values: list[int]) -> int:
    values = sorted(values)
    return values[len(values) // 2]


def extract_frame(values: list[int], min_gap: int, tolerance: float) -> tuple[list[int], str]:
    """The median frame of the biggest group of similar frames, and a description.

    The last frame of a recording is usually cut off, so it is not used.
    """
    parts = split_frames(values, min_gap)
    if len(parts) == 1 and parts[0][1] and len(parts[0][0]) >= MIN_FRAME_VALUES:
        return parts[0][0], "single frame taken as is"
    frames = [frame for frame, ends_with_gap in parts[:-1] if ends_with_gap and len(frame) >= MIN_FRAME_VALUES]
    if not frames:
        raise ConvertError("no frame with at least %d values and a pause of %d us found (noise only?)"
                           % (MIN_FRAME_VALUES, min_gap))

    # every frame joins the first group of its length whose first frame it matches
    groups: dict[int, list[list[list[int]]]] = collections.defaultdict(list)
    for frame in frames:
        for group in groups[len(frame)]:
            if similar(group[0], frame, tolerance):
                group.append(frame)
                break
        else:
            groups[len(frame)].append([frame])
    best = max((group for same_length in groups.values() for group in same_length), key=len)
    if len(best) < 2:
        raise ConvertError("no frame repeats in %d frames, record longer or try --min-gap" % len(frames))

    return [median(list(column)) for column in zip(*best)], "%d of %d frames match" % (len(best), len(parts))
