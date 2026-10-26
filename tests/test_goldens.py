"""Whole conversions of the fixtures compared with tests/goldens.

UPDATE_GOLDENS=1 writes the goldens anew; check the difference before committing them.
"""

import os
import unittest

from support import FIXTURES, FIXTURES_DIR, GOLDENS_DIR, fixture, run_cli

SUB_FILES = os.path.join(FIXTURES_DIR, "*.sub")
IR_FILE = fixture("01. Example TV.ir")
REMOTE = ("--remote", "Garden", "--repeat", "15", "--rename-suffix", "On=an", "--rename-suffix", "Off=aus")
WEBREMOTE = ("--extension", "webremote")

CASES = {
    "rf433_codes.conf": ("rf433", SUB_FILES),
    "rf433_codes_webremote.conf": ("rf433", SUB_FILES) + WEBREMOTE,
    "rf433_remote.conf": ("rf433", SUB_FILES) + REMOTE,
    "rf433_remote_webremote.conf": ("rf433", SUB_FILES) + REMOTE + WEBREMOTE,
    "lirc.lircd.conf": ("lirc", IR_FILE),
    "lirc_webremote.lircd.conf": ("lirc", IR_FILE) + WEBREMOTE,
}


class GoldensTest(unittest.TestCase):
    def test_fixtures_are_current(self):
        self.assertEqual(sorted(name for name in os.listdir(FIXTURES_DIR)), sorted(FIXTURES))
        for name, text in FIXTURES.items():
            with self.subTest(name=name), open(fixture(name), encoding="utf-8", newline="") as file:
                self.assertEqual(file.read(), text, "run python tests/support.py")

    def test_conversions(self):
        for name, argv in CASES.items():
            with self.subTest(name=name):
                code, stdout, stderr = run_cli(*argv)
                self.assertEqual(code, 0, stderr)
                path = os.path.join(GOLDENS_DIR, name)
                if os.environ.get("UPDATE_GOLDENS"):
                    with open(path, "w", encoding="utf-8", newline="\n") as file:
                        file.write(stdout)
                with open(path, encoding="utf-8", newline="") as file:
                    self.assertEqual(stdout, file.read())


if __name__ == "__main__":
    unittest.main()
