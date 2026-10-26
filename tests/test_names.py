import argparse
import unittest

import support  # noqa: F401
from f0converter.names import (base_name, button_label, code_name, key_name, parse_rename, plain_name, remote_name,
                               unique_name)


class NamesTest(unittest.TestCase):
    def test_base_name(self):
        self.assertEqual(base_name("remotes/Light_On.sub"), "Light_On")
        self.assertEqual(base_name("TV.IR"), "TV")
        self.assertEqual(base_name("Old.sub.bak"), "Old")
        self.assertEqual(base_name("notes.txt"), "notes.txt")

    def test_plain_name(self):
        self.assertEqual(plain_name("Küche Licht (groß)", "X"), "Kueche_Licht_gross")
        self.assertEqual(plain_name("Ä-Ö ü", "X"), "Ae-Oe_ue")
        self.assertEqual(plain_name("  !! ", "X"), "X")

    def test_code_name_and_renames(self):
        renames = [parse_rename("On=an"), parse_rename("Off=aus")]
        self.assertEqual(code_name("Light_On", renames), "Light_an")
        self.assertEqual(code_name("Light_OFF", renames), "Light_aus")
        self.assertEqual(code_name("Moon", renames), "Moon")
        self.assertEqual(code_name("Light_On", []), "Light_On")
        self.assertEqual(code_name("", []), "New")

    def test_parse_rename_errors(self):
        for text in ("On", "=an", "On=", "O n=an", "On=a n"):
            with self.subTest(text=text), self.assertRaises(argparse.ArgumentTypeError):
                parse_rename(text)

    def test_remote_name(self):
        self.assertEqual(remote_name("ir/05. HDMI-Switcher.ir"), "HDMI-Switcher")
        self.assertEqual(remote_name("12 TV.ir"), "TV")
        self.assertEqual(remote_name("01..ir"), "Remote")

    def test_key_name_and_label(self):
        self.assertEqual(key_name("Vol+"), "KEY_VOL")
        self.assertEqual(key_name("ch-up"), "KEY_CH_UP")
        self.assertEqual(key_name("KEY_OK"), "KEY_OK")
        self.assertEqual(key_name("btn_left"), "BTN_LEFT")
        self.assertEqual(key_name("+"), "KEY_BUTTON")
        self.assertEqual(button_label("Vol__up "), "Vol up")
        self.assertEqual(button_label("_"), "?")

    def test_unique_name(self):
        used = set()
        self.assertEqual([unique_name("KEY_A", used) for _ in range(3)], ["KEY_A", "KEY_A_2", "KEY_A_3"])
        self.assertEqual(used, {"KEY_A", "KEY_A_2", "KEY_A_3"})


if __name__ == "__main__":
    unittest.main()
