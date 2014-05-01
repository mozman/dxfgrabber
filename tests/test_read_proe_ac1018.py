# encoding: utf-8
# Copyright (C) 2014, Manfred Moitzi
# License: MIT-License

import unittest

import dxfgrabber
import os
FILE = "D:\Source\dxftest\ProE_AC1018.dxf"


def test_file_not_exists():
    return not os.path.exists(FILE)


@unittest.skipIf(test_file_not_exists(), "Skip reading ProE AC1018: test file '{}' not available.".format(FILE))
class TestReadProE_AC1018(unittest.TestCase):
    def test_open_proe_ac1018(self):
        dwg = dxfgrabber.readfile("D:\Source\dxftest\ProE_AC1018.dxf")
        modelspace = list(dwg.modelspace())

        # are there entities in model space
        self.assertEqual(17, len(modelspace))

        # can you get entities
        lines = [entity for entity in modelspace if entity.dxftype == 'LINE']
        self.assertEqual(12, len(lines))


if __name__ == '__main__':
    unittest.main()
