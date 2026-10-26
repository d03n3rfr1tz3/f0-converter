"""What the rf433 sender can send: limits of gpio-ir-tx, 433.92 MHz and OOK only."""

from __future__ import annotations

from ...model import PulseCode, SubGhzSignal

IR_MAX_DURATION = 500000                # in µs; maximum duration of one write
LIRCBUF_SIZE = 1024                     # maximum number of values of one write
FREQUENCY = 433920000                   # in Hz


def code_problems(code: PulseCode) -> list[str]:
    values = code.values
    if len(values) < 2:
        return ["code needs at least one pulse and one pause"]
    problems = []
    if len(values) % 2 != 0:
        problems.append("code must end with a pause (even number of values, got %d)" % len(values))
    if 0 in values:
        problems.append("code contains zero values")
    if len(values) - 1 > LIRCBUF_SIZE:
        problems.append("code has %d values, at most %d fit into one write" % (len(values), LIRCBUF_SIZE + 1))
    if sum(values[:-1]) > IR_MAX_DURATION:
        problems.append("code is %.1f ms long, at most %d ms fit into one write"
                        % (sum(values[:-1]) / 1000, IR_MAX_DURATION // 1000))
    return problems


def signal_warnings(signal: SubGhzSignal) -> list[str]:
    """Frequency and modulation the sender cannot reproduce."""
    warnings = []
    if signal.frequency is not None and signal.frequency != FREQUENCY:
        warnings.append("frequency %d Hz, the usual transmitter modules send on %d Hz" % (signal.frequency, FREQUENCY))
    if signal.preset and not signal.preset.startswith("FuriHalSubGhzPresetOok"):
        warnings.append("preset %s is not OOK, rf433 sends OOK only" % signal.preset)
    return warnings
