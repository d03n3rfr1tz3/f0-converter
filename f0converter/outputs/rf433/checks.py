"""What the rf433 sender can send: limits of gpio-ir-tx, 433.92 MHz and OOK only."""

from __future__ import annotations

from ...model import PulseCode, SubGhzSignal

IR_MAX_DURATION = 500000                # in µs; maximum duration of one write
LIRCBUF_SIZE = 1024                     # maximum number of values of one write
FREQUENCY = 433920000                   # in Hz


def code_problems(code: PulseCode) -> list[str]:
    raise NotImplementedError


def signal_warnings(signal: SubGhzSignal) -> list[str]:
    """Frequency and modulation the sender cannot reproduce."""
    raise NotImplementedError
