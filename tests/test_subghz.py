import os
import shutil
import tempfile
import unittest

from support import OOK, fixture, frame, recording, subghz_key, subghz_raw
from f0converter.errors import ConvertError
from f0converter.inputs import InputSettings, read_input
from f0converter.model import PulseCode, SubGhzSignal
from f0converter.outputs.rf433.checks import code_problems, signal_warnings


class SubGhzTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory)

    def read(self, text: str, name: str = "Test.sub") -> SubGhzSignal:
        path = os.path.join(self.directory, name)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        result = read_input(path, InputSettings())
        self.assertEqual(len(result.signals), 1)
        return result.signals[0]

    def test_princeton(self):
        signal = read_input(fixture("Garden_Light_On.sub"), InputSettings()).signals[0]
        self.assertEqual(signal.name, "Garden_Light_On")
        self.assertFalse(signal.raw)
        self.assertEqual(signal.description, "Princeton 24 bit, TE 350")
        values = signal.code.values
        self.assertEqual(len(values), 50)
        self.assertEqual(values[:8], (350, 1050, 1050, 350, 350, 1050, 1050, 350))     # 0x5A starts with 0101
        self.assertEqual(values[-2:], (350, 10500))

    def test_princeton_defaults(self):
        signal = self.read(subghz_key("Princeton", 4, 0x9, ("Guard_time: 10",)))
        self.assertEqual(signal.code.values, (1170, 390, 390, 1170, 390, 1170, 1170, 390, 390, 3900))

    def test_intertechno_v3(self):
        signal = self.read(subghz_key("Intertechno_V3", 32, 0x0ABCDE90))
        values = signal.code.values
        self.assertEqual(signal.description, "Intertechno_V3 id 2814842, unit 0, on")
        self.assertEqual(len(values), 2 + 32 * 4 + 2)
        self.assertEqual(values[:2], (270, 2700))
        self.assertEqual(values[2:10], (270, 270, 270, 1300, 270, 270, 270, 1300))     # 0x0A starts with 00
        self.assertEqual(values[-2:], (270, 10400))

    def test_intertechno_v3_other_lengths(self):
        with self.assertRaisesRegex(ConvertError, "Intertechno_V3 with 24 bit is not supported yet"):
            self.read(subghz_key("Intertechno_V3", 24, 0xABCDEF))

    def test_rolling_and_unknown_protocols(self):
        with self.assertRaisesRegex(ConvertError, "KeeLoq is a rolling code"):
            self.read(subghz_key("KeeLoq", 64, 0x1234))
        with self.assertRaisesRegex(ConvertError, "protocol Foo is not supported yet"):
            self.read(subghz_key("Foo", 24, 0x1234))
        with self.assertRaisesRegex(ConvertError, "Princeton key file without valid Bit or Key"):
            self.read(subghz_key("Princeton", 24, 0x1234).replace("Bit: 24", "Bit: x"))

    def test_raw_gives_exactly_the_frame(self):
        for name, expected in (("Shed_On.sub", frame("101100111000")),
                               ("Shed_Off.sub", frame("101100110100", short=302, long=897))):
            with self.subTest(name=name):
                signal = read_input(fixture(name), InputSettings()).signals[0]
                self.assertTrue(signal.raw)
                self.assertEqual(signal.code.values, tuple(expected))
                # the noise joins the first frame and the last one is cut off
                self.assertEqual(signal.description, "RAW, 4 of 6 frames match")

    def test_raw_line_length_does_not_matter(self):
        signed = recording(frame("110011110000"), repeats=3)
        self.assertEqual(self.read(subghz_raw(signed, per_line=7)).code,
                         self.read(subghz_raw(signed, per_line=512), "Other.sub").code)

    def test_raw_errors(self):
        with self.assertRaisesRegex(ConvertError, "noise only"):
            self.read(subghz_raw([300, -900] * 30))
        with self.assertRaisesRegex(ConvertError, "invalid value in RAW_Data: x"):
            self.read(subghz_raw([300, -900]).replace("-900", "x"))

    def test_frequency_and_preset(self):
        signal = self.read(subghz_key("Princeton", 24, 0x5A5A51, frequency=868350000,
                                      preset="FuriHalSubGhzPreset2FSKDev238Async"))
        self.assertEqual(signal_warnings(signal),
                         ["frequency 868350000 Hz, the usual transmitter modules send on 433920000 Hz",
                          "preset FuriHalSubGhzPreset2FSKDev238Async is not OOK, rf433 sends OOK only"])
        self.assertEqual(signal_warnings(self.read(subghz_key("Princeton", 24, 1, preset=OOK))), [])

    def test_invalid_frequency(self):
        path = os.path.join(self.directory, "Test.sub")
        with open(path, "w", encoding="utf-8") as file:
            file.write(subghz_key("Princeton", 24, 1).replace("433920000", "433.92"))
        result = read_input(path, InputSettings())
        self.assertEqual(result.warnings, ["invalid Frequency 433.92"])
        self.assertIsNone(result.signals[0].frequency)

    def test_code_problems(self):
        self.assertEqual(code_problems(PulseCode((300, 900))), [])
        self.assertEqual(code_problems(PulseCode((300,))), ["code needs at least one pulse and one pause"])
        self.assertEqual(code_problems(PulseCode((300, 0, 300))),
                         ["code must end with a pause (even number of values, got 3)", "code contains zero values"])
        self.assertEqual(code_problems(PulseCode((30, 90) * 513)), ["code has 1026 values, at most 1025 fit into one write"])
        self.assertEqual(code_problems(PulseCode((250000, 250000, 1000, 9000))),
                         ["code is 501.0 ms long, at most 500 ms fit into one write"])


if __name__ == "__main__":
    unittest.main()
