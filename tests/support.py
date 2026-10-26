"""Made-up Flipper Zero files for the tests; no recordings of real remotes.

The files in tests/fixtures are written from FIXTURES; test_goldens.py checks that they are current.
"""

from __future__ import annotations

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from f0converter.cli import main  # noqa: E402

TESTS = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS, "fixtures")
GOLDENS_DIR = os.path.join(TESTS, "goldens")

SHORT = 300
LONG = 900
GAP = 9300
OOK = "FuriHalSubGhzPresetOok650Async"


def frame(bits: str, short: int = SHORT, long: int = LONG, gap: int = GAP) -> list[int]:
    """A frame of a typical fixed code socket: 0 = short pulse and long pause, 1 = the other way round."""
    values = []
    for bit in bits:
        values += [long, short] if bit == "1" else [short, long]
    return values + [short, gap]


def jitter(values: list[int], offset: int = 0, deviations: tuple[int, ...] = (12, -8, 5, -15)) -> list[int]:
    """Every 7th value differs a little, starting at offset; the gap at the end stays."""
    result = list(values)
    for count, index in enumerate(range(3 + offset % 7, len(values) - 1, 7)):
        result[index] += deviations[count % len(deviations)]
    return result


def recording(values: list[int], repeats: int = 5) -> list[int]:
    """RAW_Data as the Flipper records a button held down: noise before the first frame, every frame with
    other jitter, one pulse split in two, a zero value and the last frame cut off. Pauses are negative."""
    signed = [-2500, 140, -90, 210, -3100]
    for repeat in range(repeats):
        signed += [value if index % 2 == 0 else -value for index, value in enumerate(jitter(values, repeat))]
    signed[7:8] = [signed[7] // 2, 0, signed[7] - signed[7] // 2]
    return signed + [value if index % 2 == 0 else -value for index, value in enumerate(values[:len(values) // 2])]


def lines(key: str, values: list[int], per_line: int) -> list[str]:
    return ["%s: %s" % (key, " ".join(str(value) for value in values[start:start + per_line]))
            for start in range(0, len(values), per_line)]


def subghz_key(protocol: str, bits: int, key: int, extra: tuple[str, ...] = (), frequency: int = 433920000,
               preset: str = OOK) -> str:
    return "\n".join(["Filetype: Flipper SubGhz Key File", "Version: 1", "Frequency: %d" % frequency,
                      "Preset: " + preset, "Protocol: " + protocol, "Bit: %d" % bits,
                      "Key: " + " ".join("%02X" % ((key >> shift) & 0xFF) for shift in range(56, -8, -8))]
                     + list(extra)) + "\n"


def subghz_raw(signed: list[int], frequency: int = 433920000, preset: str = OOK, per_line: int = 20) -> str:
    return "\n".join(["Filetype: Flipper SubGhz RAW File", "Version: 1", "Frequency: %d" % frequency,
                      "Preset: " + preset, "Protocol: RAW"] + lines("RAW_Data", signed, per_line)) + "\n"


def ir_parsed(name: str, protocol: str, address: int, command: int) -> list[str]:
    def number(value: int) -> str:
        return " ".join("%02X" % ((value >> shift) & 0xFF) for shift in range(0, 32, 8))
    return ["name: " + name, "type: parsed", "protocol: " + protocol, "address: " + number(address),
            "command: " + number(command)]


def ir_raw(name: str, values: list[int], frequency: int = 38000, duty_cycle: str = "0.330000") -> list[str]:
    return ["name: " + name, "type: raw", "frequency: %d" % frequency, "duty_cycle: " + duty_cycle] \
        + lines("data", values, 512)


def ir_file(*signals: list[str]) -> str:
    result = ["Filetype: IR signals file", "Version: 1"]
    for signal in signals:
        result += ["# "] + signal
    return "\n".join(result) + "\n"


IR_PULSES = [9000, 4500] + [560, 560, 560, 1690] * 4 + [560]

FIXTURES = {
    "Garden_Light_On.sub": subghz_key("Princeton", 24, 0x5A5A51, ("TE: 350",)),
    "Garden_Light_Off.sub": subghz_key("Princeton", 24, 0x5A5A54),
    "Shed_On.sub": subghz_raw(recording(frame("101100111000"))),
    "Shed_Off.sub": subghz_raw(recording(frame("101100110100", short=302, long=897))),
    "Patio_On.sub": subghz_key("Intertechno_V3", 32, 0x0ABCDE90),
    "01. Example TV.ir": ir_file(
        ir_parsed("Power", "NEC", 0x10, 0x08),
        ir_parsed("Vol_up", "NEC", 0x10, 0x02),
        ir_parsed("Vol_dn", "NEC", 0x10, 0x03),
        ir_parsed("Input", "Samsung32", 0x0E, 0x01),
        ir_parsed("Sleep", "RC5", 0x01, 0x26),
        ir_raw("Mute", IR_PULSES),
        ir_raw("Mute", IR_PULSES[:-1] + [600, 40000]),
        ir_raw("Light", [1000, 500] * 10 + [1000], 56000, "0.500000"),
    ),
}


def write_fixtures(folder: str = FIXTURES_DIR) -> None:
    os.makedirs(folder, exist_ok=True)
    for name, text in FIXTURES.items():
        with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as file:
            file.write(text)


def fixture(name: str) -> str:
    return os.path.join(FIXTURES_DIR, name)


def run_cli(*argv: str) -> tuple[int, str, str]:
    """Exit code, stdout and stderr of one call."""
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = main(list(argv))
    return code, stdout.getvalue(), stderr.getvalue()


if __name__ == "__main__":
    write_fixtures()
