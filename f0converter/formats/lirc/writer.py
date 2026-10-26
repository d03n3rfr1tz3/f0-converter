"""Text of lircd.conf remotes."""

from __future__ import annotations

from dataclasses import dataclass, field

from .protocols import LircTiming

EPS = 30
AEPS = 100
DUTY_CYCLE = 33                         # duty cycle of parsed remotes in percent
RAW_PER_LINE = 8                        # values per line in raw_codes


@dataclass
class LircCode:
    name: str
    code: int
    annotation: str | None = None       # comment starting with #, written behind the code


@dataclass
class LircParsedRemote:
    name: str
    bits: int
    timing: LircTiming
    codes: list[LircCode] = field(default_factory=list)
    pre_data_bits: int = 0
    pre_data: int = 0


@dataclass
class LircRawCode:
    name: str
    values: tuple[int, ...]
    annotation: str | None = None       # comment starting with #, written as a line of its own above the name


@dataclass
class LircRawRemote:
    name: str
    frequency: int
    duty_cycle: int
    gap: int
    codes: list[LircRawCode] = field(default_factory=list)


def setting(key: str, value) -> str:
    if isinstance(value, tuple):
        return "  %-12s %5d %5d" % (key, value[0], value[1])
    return "  %-12s %5s" % (key, value)


def hex_code(value: int, bits: int) -> str:
    return "0x%0*X" % ((bits + 3) // 4, value)


def timing_settings(remote: LircParsedRemote) -> list[str]:
    """header one zero plead ptrail repeat pre_data_bits pre_data gap min_repeat toggle_bit_mask rc6_mask"""
    timing = remote.timing
    entries = [("header", timing.header), ("one", timing.one), ("zero", timing.zero), ("plead", timing.plead),
               ("ptrail", timing.ptrail), ("repeat", timing.repeat)]
    if remote.pre_data_bits:
        entries += [("pre_data_bits", remote.pre_data_bits), ("pre_data", hex_code(remote.pre_data, remote.pre_data_bits))]
    entries += [("gap", timing.gap), ("min_repeat", timing.min_repeat)]
    for key, mask in (("toggle_bit_mask", timing.toggle_bit_mask), ("rc6_mask", timing.rc6_mask)):
        entries.append((key, None if mask is None else "0x%X" % mask))
    return [setting(key, value) for key, value in entries if value is not None]


def format_parsed_remote(remote: LircParsedRemote) -> list[str]:
    lines = ["begin remote", "", "  name  " + remote.name, setting("bits", remote.bits),
             "  flags " + remote.timing.flags, setting("eps", EPS), setting("aeps", AEPS),
             setting("frequency", remote.timing.frequency), setting("duty_cycle", DUTY_CYCLE), ""]
    lines += timing_settings(remote)
    lines += ["", "      begin codes"]
    for code in remote.codes:
        line = "          %-24s %-12s %s" % (code.name, hex_code(code.code, remote.bits), code.annotation or "")
        lines.append(line.rstrip())
    lines += ["      end codes", "", "end remote", ""]
    return lines


def format_raw_remote(remote: LircRawRemote) -> list[str]:
    lines = ["begin remote", "", "  name  " + remote.name, "  flags RAW_CODES", setting("eps", EPS),
             setting("aeps", AEPS), setting("frequency", remote.frequency), setting("duty_cycle", remote.duty_cycle),
             "", setting("gap", remote.gap), "", "      begin raw_codes"]
    for code in remote.codes:
        # a comment line of its own: lircd warns about anything behind the name
        if code.annotation:
            lines.append("          " + code.annotation)
        lines.append("          name " + code.name)
        for start in range(0, len(code.values), RAW_PER_LINE):
            lines.append("            " + " ".join("%6d" % value for value in code.values[start:start + RAW_PER_LINE]))
    lines += ["      end raw_codes", "", "end remote", ""]
    return lines
