import os
import shutil
import tempfile
import unittest

import support  # noqa: F401
from f0converter.formats.flipper.fileformat import FlipperBlock, FlipperFile


class FlipperFileTest(unittest.TestCase):
    def test_parse(self):
        flipper = FlipperFile.parse("﻿Filetype: IR signals file\nVersion: 1\n#\n# \n"
                                    "name: Power\ntype: parsed\nno colon here\n#\nname: Mute\n  data: 1 2 3  \n")
        self.assertEqual((flipper.filetype, flipper.version), ("IR signals file", "1"))
        self.assertEqual(len(flipper.blocks), 3)
        self.assertEqual(flipper.blocks[1].entries, [("name", "Power"), ("type", "parsed")])
        self.assertEqual(flipper.blocks[2].first("data"), "1 2 3")
        self.assertIsNone(flipper.blocks[2].first("type"))

    def test_values_may_contain_colons_and_repeat(self):
        block = FlipperFile.parse("RAW_Data: 1 -2\nRAW_Data: 3 -4\nNote: a: b\n").blocks[0]
        self.assertEqual(block.all("RAW_Data"), ["1 -2", "3 -4"])
        self.assertEqual(block.first("Note"), "a: b")

    def test_empty(self):
        flipper = FlipperFile.parse("# only a comment\n\n")
        self.assertEqual((flipper.blocks, flipper.filetype, flipper.version), ([], "", ""))

    def test_write_and_read_again(self):
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory)
        path = os.path.join(directory, "remote.ir")
        flipper = FlipperFile([FlipperBlock([("Filetype", "IR signals file"), ("Version", "1")]),
                               FlipperBlock([("name", "Power"), ("type", "parsed"), ("protocol", "NEC")])])
        flipper.blocks[1].add("address", "10 00 00 00")
        flipper.write(path)
        with open(path, encoding="utf-8") as file:
            self.assertEqual(file.read(), "Filetype: IR signals file\nVersion: 1\n#\nname: Power\ntype: parsed\n"
                                          "protocol: NEC\naddress: 10 00 00 00\n")
        self.assertEqual([block.entries for block in FlipperFile.read(path).blocks],
                         [block.entries for block in flipper.blocks])


if __name__ == "__main__":
    unittest.main()
