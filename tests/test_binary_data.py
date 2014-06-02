# Author:  mozman -- <mozman@gmx.at>
# Purpose: test body, region, solid3d
# Created: 03.05.2014
# Copyright (C) 2014, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals


import unittest

from dxfgrabber.tags import binary_encoded_data_to_bytes


class TestBinaryData(unittest.TestCase):
    def test_binary_encoded_data_to_bytes_1(self):
        result = binary_encoded_data_to_bytes(['FFFF'])
        self.assertEqual(b"\xff\xff", result)

    def test_binary_encoded_data_to_bytes_2(self):
        result = binary_encoded_data_to_bytes(['F0F0', '1A1C'])
        self.assertEqual(b"\xF0\xF0\x1A\x1C", result)


if __name__ == '__main__':
    unittest.main()
