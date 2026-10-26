import contextlib
import io
import os
import shutil
import tempfile
import unittest

from support import FIXTURES_DIR, fixture, run_cli

IR_FILE = fixture("01. Example TV.ir")


class CliTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.directory)

    def write(self, name: str, text: str) -> str:
        path = os.path.join(self.directory, name)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return path

    def test_codes_to_stdout_messages_to_stderr(self):
        code, stdout, stderr = run_cli("rf433", fixture("Shed_On.sub"), "--name", "Shed_an")
        self.assertEqual(code, 0)
        self.assertTrue(stdout.startswith("    # Shed_On.sub, RAW, 4 of 6 frames match\n    name Shed_an\n"))
        self.assertEqual(stderr, " --> Shed_an: Shed_On.sub, RAW, 4 of 6 frames match, 26 values, 24.0 ms, pause 9300 us\n")

    def test_output_folder(self):
        folder = os.path.join(self.directory, "out")
        code, stdout, stderr = run_cli("lirc", os.path.join(FIXTURES_DIR, "*.ir"), "--output", folder)
        self.assertEqual((code, stdout), (0, ""))
        target = os.path.join(folder, "01. Example TV.lircd.conf")
        self.assertIn(" --> written " + target, stderr)
        with open(target, encoding="utf-8") as file:
            self.assertIn("name  Example_TV\n", file.read())

        code, stdout, stderr = run_cli("lirc", IR_FILE, "--output", folder)
        self.assertEqual(code, 1)
        self.assertIn("Error: %s: exists, delete it first or choose another --output" % target, stderr)

    def test_remote_name_of_lirc(self):
        code, stdout, stderr = run_cli("lirc", IR_FILE, "--remote", "Living_TV")
        self.assertEqual(code, 0)
        self.assertIn("name  Living_TV\n", stdout)
        self.assertIn("name  Living_TV_raw_56000\n", stdout)

    def test_option_errors(self):
        for argv, message in ((("lirc", IR_FILE, IR_FILE), "2 files need --output"),
                              (("lirc", IR_FILE, IR_FILE, "--remote", "TV", "--output", self.directory),
                               "--remote needs exactly one file, got 2"),
                              (("rf433", os.path.join(FIXTURES_DIR, "*.sub"), "--name", "Light"),
                               "--name needs exactly one file, got 5"),
                              (("rf433", fixture("Shed_On.sub"), "--repeat", "5"), "--repeat needs --remote"),
                              (("rf433", os.path.join(self.directory, "*.sub")), "no files match "),
                              (("rf433", os.path.join(self.directory, "missing.sub")), "missing.sub")):
            with self.subTest(argv=argv):
                code, stdout, stderr = run_cli(*argv)
                self.assertEqual((code, stdout), (1, ""))
                self.assertIn(message, stderr)

    def test_argument_errors(self):
        for argv in (("rf433", "x.sub", "--rename-suffix", "On"), ("rf433", "x.sub", "--from", "pronto"),
                     ("lirc", "x.ir", "--extension", "unknown"), ()):
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    run_cli(*argv)
                self.assertEqual(raised.exception.code, 2)

    def test_wrong_output_for_the_input(self):
        code, stdout, stderr = run_cli("rf433", IR_FILE)
        self.assertEqual((code, stdout), (1, ""))
        self.assertIn("Error: 01. Example TV.ir: Power: not supported by the rf433 output, try another command", stderr)

    def test_unrecognized_file_and_from(self):
        path = self.write("notes.txt", "nothing to see\n")
        code, stdout, stderr = run_cli("rf433", path)
        self.assertEqual(code, 1)
        self.assertIn("Error: notes.txt: file format not recognized, choose one with --from (flipper-subghz, flipper-ir)",
                      stderr)

        code, stdout, stderr = run_cli("lirc", fixture("Shed_On.sub"), "--from", "flipper-ir")
        self.assertEqual(code, 1)
        self.assertIn("Error: Shed_On.sub: not a Flipper IR file (Filetype: Flipper SubGhz RAW File)", stderr)

    def test_good_files_are_converted_besides_bad_ones(self):
        bad = self.write("Bad.sub", "Filetype: Flipper SubGhz Key File\nVersion: 1\nProtocol: KeeLoq\n")
        code, stdout, stderr = run_cli("rf433", fixture("Patio_On.sub"), bad)
        self.assertEqual(code, 1)
        self.assertIn("name Patio_On\n", stdout)
        self.assertIn("Error: Bad.sub: KeeLoq is a rolling code", stderr)

    def test_same_code_name_twice(self):
        code, stdout, stderr = run_cli("rf433", fixture("Shed_On.sub"), fixture("Shed_On.sub"))
        self.assertEqual(code, 1)
        self.assertIn("Error: Shed_On.sub: code name Shed_On is used twice, convert this file alone with --name", stderr)
        self.assertEqual(stdout.count("name Shed_On\n"), 1)

    def test_formats(self):
        code, stdout, stderr = run_cli("formats")
        self.assertEqual(code, 0)
        for text in ("flipper-subghz", "RAW, Intertechno_V3, Princeton", "flipper-ir", "rf433", "lirc",
                     "NEC, NECext", "webremote"):
            self.assertIn(text, stdout)


if __name__ == "__main__":
    unittest.main()
