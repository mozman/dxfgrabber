#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test header section
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: GPLv3
from __future__ import unicode_literals

import unittest

from dxfgrabber.tags import Tags
from dxfgrabber.headersection import HeaderSection

class TestHeaderSection(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(TESTHEADER)
        self.header = HeaderSection(tags)

    def test_get_acadver(self):
        result = self.header['$ACADVER']
        self.assertEqual('AC1009', result)

    def test_get_insbase(self):
        result = self.header['$INSBASE']
        self.assertEqual((0., 0., 0.), result)

    def test_getitem_keyerror(self):
        with self.assertRaises(KeyError):
            var = self.header['$TEST']

    def test_get(self):
        result = self.header.get('$TEST', 'TEST')
        self.assertEqual('TEST', result)

    def test_contains(self):
        self.assertTrue('$ACADVER' in self.header)

    def test_not_contains(self):
        self.assertFalse('$MOZMAN' in self.header)

TESTHEADER = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1009
  9
$INSBASE
 10
0.0
 20
0.0
 30
0.0
  9
$EXTMIN
 10
1.0000000000000000E+020
 20
1.0000000000000000E+020
 30
1.0000000000000000E+020
  9
$EXTMAX
 10
-1.0000000000000000E+020
 20
-1.0000000000000000E+020
 30
-1.0000000000000000E+020
  0
ENDSEC
"""
