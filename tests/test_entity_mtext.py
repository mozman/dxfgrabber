#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory

class TestMText(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(MTEXT)
        self.entity = entity_factory(tags, 'AC1024')

    def test_mtext_properties(self):
        mtext = self.entity
        self.assertEqual(mtext.dxftype, 'MTEXT')
        self.assertEqual(mtext.color, 256)
        self.assertEqual(mtext.layer, '0')
        self.assertEqual(mtext.linetype, None)
        self.assertFalse(mtext.paperspace)

    def test_mtext_data(self):
        mtext = self.entity
        self.assertEqual(mtext.insert, (36.0, 65.0, 0.0))
        self.assertEqual(mtext.height, 3.0)
        self.assertEqual(mtext.attachmentpoint, 1)
        self.assertEqual(mtext.style, "Notes")
        self.assertEqual(mtext.extrusion, (0.0, 0.0, 1.0))
        self.assertEqual(mtext.xdirection, (1.0, 0.0, 0.0))
        self.assertEqual(mtext.linespacing, 1.0)

    def test_mtext_text(self):
        mtext = self.entity
        self.assertEqual(mtext.rawtext, "first 250 chars\Psecond 250 chars\Pand the rest")
        self.assertEqual(mtext.lines(), ["first 250 chars", "second 250 chars", "and the rest"])

MTEXT = """  0
MTEXT
  5
3D2
102
{ACAD_XDICTIONARY
360
3D3
102
}
330
1F
100
AcDbEntity
  8
0
100
AcDbMText
 10
36.0
 20
65.0
 30
0.0
 40
3.0
 41
50.0
 46
0.0
 71
     1
 72
     5
  3
first 250 chars\P
  3
second 250 chars\P
  1
and the rest
  7
Notes
 73
     1
 44
1.0
1001
AcadAnnotative
1000
AnnotativeData
1002
{
1070
     1
1070
     1
1002
}
1001
AcadAnnoPO
1070
     1
1001
ACAD
1000
ACAD_MTEXT_COLUMN_INFO_BEGIN
1070
    75
1070
     2
1070
    79
1070
     0
1070
    76
1070
     1
1070
    78
1070
     0
1070
    48
1040
50.0
1070
    49
1040
15.0
1070
    50
1070
     1
1040
0.0
1000
ACAD_MTEXT_COLUMN_INFO_END
"""
