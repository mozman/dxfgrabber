# Created: 2014-05-09
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.color import TrueColor


class TestTrueColor(unittest.TestCase):
    def test_rgb(self):
        t = TrueColor(0xA0B0C0)
        r, g, b = t.rgb()
        self.assertTrue(0xA0, r)
        self.assertTrue(0xB0, g)
        self.assertTrue(0xC0, b)

    def test_r_g_b(self):
        t = TrueColor(0xA0B0C0)
        self.assertTrue(0xA0, t.r)
        self.assertTrue(0xB0, t.g)
        self.assertTrue(0xC0, t.b)

    def test_unpack(self):
        t = TrueColor(0xA0B0C0)
        r, g, b = t
        self.assertTrue(0xA0, r)
        self.assertTrue(0xB0, g)
        self.assertTrue(0xC0, b)

    def test_from_rgb(self):
        t = TrueColor.from_rgb(0xA0, 0xB0, 0xC0)
        self.assertEqual(0xA0B0C0, t)

    def test_from_aci(self):
        self.assertEqual(0xFF0000, TrueColor.from_aci(1))
        self.assertEqual(0xFFFFFF, TrueColor.from_aci(7))

    def test_0(self):
        with self.assertRaises(IndexError):
            TrueColor.from_aci(0)

    def test_256(self):
        with self.assertRaises(IndexError):
            TrueColor.from_aci(256)