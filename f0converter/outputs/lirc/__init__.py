from __future__ import annotations

from dataclasses import dataclass

from ...messages import Messages
from ...model import InputResult, IrParsedSignal, IrRawSignal
from ..base import Document, Output, OutputOptions

WBUF_SIZE = 256                         # send buffer of lircd; a raw signal has at most WBUF_SIZE - 1 values
RAW_GAP = 100000                        # in µs; gap of raw_codes when no signal ends with a pause


@dataclass
class LircOptions(OutputOptions):
    remote: str | None = None           # name of the remote, only for one file


class LircOutput(Output):
    """lircd.conf remote files, one per input file: a remote per protocol and per raw carrier."""

    name = "lirc"
    description = "LIRC remote file (lircd.conf)"

    def accepts(self, signal) -> bool:
        return isinstance(signal, (IrParsedSignal, IrRawSignal))

    def convert(self, results: list[InputResult], options: LircOptions, messages: Messages) -> list[Document]:
        raise NotImplementedError
