#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 21.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory

class TestLineDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(LINE_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_lines_data(self):
        line = self.entity
        self.assertEqual(line.dxftype, 'LINE')
        self.assertEqual(line.start, (0., 0., 0.))
        self.assertEqual(line.end, (1., 0., 0.))
        self.assertEqual(line.color, 256)
        self.assertEqual(line.layer, '0')
        self.assertEqual(line.linetype, None)
        self.assertFalse(line.paperspace)

class TestLineDXF13(TestLineDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(LINE_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

LINE_DXF13 = """  0
LINE
  5
3D6
330
1F
100
AcDbEntity
  8
0
100
AcDbLine
 10
0.0
 20
0.0
 30
0.0
 11
1.0
 21
0.0
 31
0.0
"""

LINE_DXF12 = """  0
LINE
  8
0
 10
0.0
 20
0.0
 30
0.0
 11
1.0
 21
0.0
 31
0.0
"""
