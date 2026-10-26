from __future__ import annotations

import collections
import os
from dataclasses import dataclass

from ...errors import ConvertError
from ...formats.lirc.protocols import PROTOCOLS
from ...formats.lirc.writer import (LircCode, LircParsedRemote, LircRawCode, LircRawRemote, format_parsed_remote,
                                    format_raw_remote)
from ...messages import Messages
from ...model import InputResult, IrParsedSignal, IrRawSignal
from ...names import base_name, button_label, key_name, remote_name, unique_name
from ..base import Document, Output, OutputOptions
from .keys import remote_names

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
        documents = []
        for result in results:
            where = os.path.basename(result.source)
            try:
                text = self.convert_file(result, options, messages)
            except ConvertError as error:
                messages.error(where, str(error))
                continue
            documents.append(Document(base_name(result.source) + ".lircd.conf", text))
        return documents

    def convert_file(self, result: InputResult, options: LircOptions, messages: Messages) -> str:
        where = os.path.basename(result.source)
        parsed: dict[str, list[LircCode]] = collections.OrderedDict()
        raw: dict[tuple[int, int], list[LircRawCode]] = collections.OrderedDict()
        keys: dict = collections.defaultdict(set)       # group: key names used
        trailing_pauses: dict[tuple[int, int], list[int]] = collections.defaultdict(list)
        for signal in self.accepted(result, messages):
            annotation = options.annotate(signal, button_label(signal.name))
            try:
                if isinstance(signal, IrParsedSignal):
                    protocol = PROTOCOLS.get(signal.protocol)
                    if protocol is None:
                        raise ConvertError("protocol %s is not supported yet" % (signal.protocol or "(none)"))
                    code = protocol.encode(signal.address, signal.command)
                    key = unique_name(key_name(signal.name), keys[signal.protocol])
                    parsed.setdefault(signal.protocol, []).append(LircCode(key, code, annotation))
                else:
                    group = (signal.frequency, signal.duty_cycle)
                    values = list(signal.values)
                    if len(values) % 2 == 0:
                        trailing_pauses[group].append(values.pop())
                    if len(values) > WBUF_SIZE - 1:
                        raise ConvertError("%d values, lircd sends at most %d, record it shorter"
                                           % (len(values), WBUF_SIZE - 1))
                    key = unique_name(key_name(signal.name), keys[group])
                    raw.setdefault(group, []).append(LircRawCode(key, tuple(values), annotation))
            except ConvertError as error:
                messages.error(where, "%s: %s" % (signal.name, error))
        if not parsed and not raw:
            raise ConvertError("no signal could be converted")

        # the biggest protocol gets the name of the remote, the others a suffix
        protocols = sorted(parsed, key=lambda name: -len(parsed[name]))
        names = remote_names(options.remote or remote_name(result.source), protocols, list(raw))
        lines = ["# converted from the Flipper Zero file \"%s\" with f0-converter" % where]
        lines += options.header_lines() + ["#", ""]
        summary = []
        for name, protocol in zip(names, protocols):
            lines += format_parsed_remote(self.parsed_remote(name, protocol, parsed[protocol]))
            summary.append("%s (%s, %d)" % (name, protocol, len(parsed[protocol])))
        for name, (group, codes) in zip(names[len(protocols):], raw.items()):
            pauses = trailing_pauses.get(group)
            gap = max(pauses) if pauses else RAW_GAP
            if pauses:
                messages.warning(where, "%d raw signals end with a pause, the longest (%d us) became the gap of %s"
                                 % (len(pauses), gap, name))
            lines += format_raw_remote(LircRawRemote(name, group[0], group[1], gap, codes))
            summary.append("%s (raw %d Hz, %d)" % (name, group[0], len(codes)))
        messages.info("%s: %s" % (where, ", ".join(summary)))
        return "\n".join(lines)

    @staticmethod
    def parsed_remote(name: str, protocol_name: str, codes: list[LircCode]) -> LircParsedRemote:
        """Leading bits that all codes share become pre_data."""
        protocol = PROTOCOLS[protocol_name]
        remote = LircParsedRemote(name, protocol.bits, protocol.timing, codes)
        prefix_bits = protocol.prefix_bits
        prefixes = {code.code >> (protocol.bits - prefix_bits) for code in codes}
        if prefix_bits and len(prefixes) == 1:
            remote.bits = protocol.bits - prefix_bits
            remote.pre_data_bits = prefix_bits
            remote.pre_data = prefixes.pop()
            mask = (1 << remote.bits) - 1
            remote.codes = [LircCode(code.name, code.code & mask, code.annotation) for code in codes]
        return remote
