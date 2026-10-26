import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from f0converter import __version__  # noqa: E402
from f0converter.cli import build_parser, main  # noqa: E402
from f0converter.commands import COMMANDS  # noqa: E402
from f0converter.extensions import EXTENSIONS  # noqa: E402
from f0converter.inputs import INPUTS  # noqa: E402
from f0converter.outputs import OUTPUTS  # noqa: E402


class SmokeTest(unittest.TestCase):
    def test_registries(self):
        self.assertEqual([command.name for command in COMMANDS], ["rf433", "lirc", "formats"])
        self.assertEqual([item.name for item in INPUTS], ["flipper-subghz", "flipper-ir"])
        self.assertEqual([item.name for item in OUTPUTS], ["rf433", "lirc"])
        self.assertEqual([item.name for item in EXTENSIONS], ["webremote"])

    def test_every_command_parses_its_help(self):
        parser = build_parser([command() for command in COMMANDS])
        for command in COMMANDS:
            with self.subTest(command=command.name), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    parser.parse_args([command.name, "--help"])
                self.assertEqual(raised.exception.code, 0)

    def test_version(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
            main(["--version"])
        self.assertIn(__version__, output.getvalue())


if __name__ == "__main__":
    unittest.main()
