from __future__ import annotations

import os
from dataclasses import dataclass, field

from ...formats.rf433.writer import Rf433Code, format_codes, format_remote
from ...messages import Messages
from ...model import InputResult, PulseCode, SubGhzSignal
from ...names import button_label, code_name
from ...signal.cluster import DEFAULT_TOLERANCE, clean_codes
from ..base import Document, Output, OutputOptions
from .checks import code_problems, signal_warnings


@dataclass
class Rf433Options(OutputOptions):
    remote: str | None = None           # write a complete code file for this remote
    repeat: int | None = None           # repeat of the remote, only with remote
    name: str | None = None             # code name for a single signal
    renames: list[tuple[str, str]] = field(default_factory=list)    # suffixes of code names, e.g. ("On", "an")
    tolerance: float = DEFAULT_TOLERANCE


@dataclass
class _Entry:
    name: str
    signal: SubGhzSignal
    code: PulseCode


class Rf433Output(Output):
    """rf433 code files: one frame per code, recordings of one conversion cleaned together."""

    name = "rf433"
    description = "rf433 code file (433 MHz OOK)"

    def accepts(self, signal) -> bool:
        return isinstance(signal, SubGhzSignal)

    def convert(self, results: list[InputResult], options: Rf433Options, messages: Messages) -> list[Document]:
        entries = self.collect(results, options, messages)

        # recordings of one remote get the same values (e.g. 268 and 271 become one of both)
        recorded = [entry for entry in entries if entry.signal.raw]
        for entry, values in zip(recorded, clean_codes([list(entry.code.values) for entry in recorded], options.tolerance)):
            entry.code = PulseCode(tuple(values))

        codes = []
        for entry in entries:
            problems = code_problems(entry.code)
            if problems:
                messages.error(entry.name, "; ".join(problems))
                continue
            comment = "%s, %s" % (os.path.basename(entry.signal.source), entry.signal.description)
            messages.info("%s: %s, %s" % (entry.name, comment, entry.code.describe()))
            codes.append(Rf433Code(entry.name, entry.code.values, comment=comment,
                                   annotation=options.annotate(entry.signal, button_label(entry.name))))
        if not codes:
            return []

        if options.remote is None:
            return [Document("codes.conf", "\n".join(format_codes(codes)) + "\n")]
        header = ["# %s, converted from Flipper Zero files with f0-converter" % options.remote,
                  "#",
                  "# One frame per code including the pause at the end: values in µs, pulse first.",
                  "# Check after editing: rf433 check"] + options.header_lines() + [""]
        lines = format_remote(options.remote, options.repeat, codes, header)
        return [Document(options.remote + ".conf", "\n".join(lines) + "\n")]

    def collect(self, results: list[InputResult], options: Rf433Options, messages: Messages) -> list[_Entry]:
        entries: list[_Entry] = []
        for result in results:
            where = os.path.basename(result.source)
            for signal in self.accepted(result, messages):
                name = options.name if options.name is not None else code_name(signal.name, options.renames)
                if any(entry.name == name for entry in entries):
                    messages.error(where, "code name %s is used twice, convert this file alone with --name" % name)
                    continue
                for warning in signal_warnings(signal):
                    messages.warning(where, warning)
                entries.append(_Entry(name, signal, signal.code))
        return entries
