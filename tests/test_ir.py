import io
import os
import shutil
import tempfile
import unittest

from support import fixture, ir_file, ir_parsed, ir_raw
from f0converter.errors import ConvertError
from f0converter.formats.lirc.protocols import PROTOCOLS
from f0converter.formats.lirc.protocols.base import lsb_first
from f0converter.formats.lirc.writer import LircCode
from f0converter.inputs import InputSettings, read_input
from f0converter.messages import Messages
from f0converter.model import InputResult, IrParsedSignal, IrRawSignal
from f0converter.outputs.lirc import LircOptions, LircOutput


class EncoderTest(unittest.TestCase):
    def test_publicly_known_codes(self):
        # address, command -> code as found in common LIRC files
        for protocol, address, command, code in (("NEC", 0x00, 0x45, 0x00FFA25D),
                                                 ("Samsung32", 0x07, 0x02, 0xE0E040BF),
                                                 ("SIRC", 1, 21, 0xA90),
                                                 ("RC5", 0, 12, 0x100C)):
            with self.subTest(protocol=protocol):
                self.assertEqual(PROTOCOLS[protocol].encode(address, command), code)

    def test_lsb_first(self):
        self.assertEqual(lsb_first(0b0001, 4), 0b1000)
        self.assertEqual(lsb_first(0x1FF, 8), 0xFF)

    def test_every_protocol_fits_its_bits(self):
        for protocol in PROTOCOLS.values():
            with self.subTest(protocol=protocol.name):
                self.assertLess(protocol.encode(0xFFFFFFFF, 0xFFFFFFFF), 1 << protocol.bits)
                self.assertLessEqual(protocol.prefix_bits, protocol.bits)

    def test_shared_leading_bits_become_pre_data(self):
        nec = PROTOCOLS["NEC"]
        remote = LircOutput.parsed_remote("TV", "NEC", [LircCode("KEY_A", nec.encode(0x10, 1)),
                                                        LircCode("KEY_B", nec.encode(0x10, 2))])
        self.assertEqual((remote.bits, remote.pre_data_bits, remote.pre_data), (16, 16, 0x08F7))
        self.assertEqual([code.code for code in remote.codes], [0x807F, 0x40BF])

        remote = LircOutput.parsed_remote("TV", "NEC", [LircCode("KEY_A", nec.encode(0x10, 1)),
                                                        LircCode("KEY_B", nec.encode(0x11, 2))])
        self.assertEqual((remote.bits, remote.pre_data_bits), (32, 0))


class FlipperIrInputTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory)

    def read(self, text: str) -> InputResult:
        path = os.path.join(self.directory, "Test.ir")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return read_input(path, InputSettings())

    def test_fixture(self):
        result = read_input(fixture("01. Example TV.ir"), InputSettings())
        self.assertEqual(result.errors, [])
        self.assertEqual([signal.name for signal in result.signals],
                         ["Power", "Vol_up", "Vol_dn", "Input", "Sleep", "Mute", "Mute", "Light"])
        self.assertEqual(result.signals[3], IrParsedSignal("Input", fixture("01. Example TV.ir"), "Samsung32", 0x0E, 0x01))
        light = result.signals[7]
        self.assertEqual((light.frequency, light.duty_cycle, len(light.values)), (56000, 50, 21))

    def test_bad_signals_are_errors_of_their_own(self):
        result = self.read(ir_file(ir_parsed("Good", "NEC", 1, 2),
                                   ["name: Bad", "type: parsed", "protocol: NEC", "address: zz", "command: 01 00 00 00"],
                                   ["name: Empty", "type: parsed", "protocol: NEC", "command: 01 00 00 00"],
                                   ir_raw("Zero", [100, 0, 100]),
                                   ["name: Rubbish", "type: raw", "frequency: high", "data: 1 2"],
                                   ["name: Odd", "type: pronto"]))
        self.assertEqual([signal.name for signal in result.signals], ["Good"])
        self.assertEqual(result.errors, ["Bad: invalid address", "Empty: invalid address",
                                         "Zero: raw data is empty or contains zero or negative values",
                                         "Rubbish: invalid frequency, duty_cycle or data", "Odd: unknown type pronto"])

    def test_empty_file(self):
        with self.assertRaisesRegex(ConvertError, "no signals in the file"):
            self.read(ir_file())


class LircOutputTest(unittest.TestCase):
    def convert(self, *signals):
        stream = io.StringIO()
        messages = Messages(stream)
        documents = LircOutput().convert([InputResult("remotes/TV.ir", list(signals))], LircOptions(), messages)
        return documents, stream.getvalue(), messages.errors

    def test_unsupported_protocol_and_too_long_raw(self):
        documents, text, errors = self.convert(IrParsedSignal("Power", "TV.ir", "NEC", 1, 2),
                                               IrParsedSignal("Odd", "TV.ir", "Foo", 1, 2),
                                               IrRawSignal("Long", "TV.ir", 38000, 33, (500,) * 257),
                                               IrRawSignal("Fits", "TV.ir", 38000, 33, (500,) * 256))
        self.assertEqual(errors, 2)
        self.assertIn("Error: TV.ir: Odd: protocol Foo is not supported yet", text)
        self.assertIn("Error: TV.ir: Long: 257 values, lircd sends at most 255, record it shorter", text)
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].name, "TV.lircd.conf")
        self.assertIn("KEY_POWER", documents[0].text)
        self.assertIn("KEY_FITS", documents[0].text)
        self.assertIn("\n  gap            500\n", documents[0].text)     # the trailing pause of Fits

    def test_nothing_left(self):
        documents, text, errors = self.convert(IrParsedSignal("Odd", "TV.ir", "Foo", 1, 2))
        self.assertEqual((documents, errors), ([], 2))
        self.assertIn("Error: TV.ir: no signal could be converted", text)

    def test_other_signals_are_rejected(self):
        from f0converter.model import PulseCode, SubGhzSignal
        documents, text, errors = self.convert(SubGhzSignal("Light", "Light.sub", PulseCode((300, 900)), False, ""))
        self.assertIn("Light: not supported by the lirc output, try another command", text)


if __name__ == "__main__":
    unittest.main()
