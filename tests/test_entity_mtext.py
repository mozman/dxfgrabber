# encoding: utf-8
# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.dxfentities import entity_factory

class TestMText(unittest.TestCase):
    def setUp(self):
        tags = Tags.from_text(MTEXT)
        self.entity = entity_factory(tags)

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
        self.assertEqual(mtext.attachment_point, 1)
        self.assertEqual(mtext.style, "Notes")
        self.assertEqual(mtext.extrusion, (0.0, 0.0, 1.0))
        self.assertEqual(mtext.xdirection, (1.0, 0.0, 0.0))
        self.assertEqual(mtext.line_spacing, 1.0)
        self.assertEqual(mtext.rect_width, 50.0)
        self.assertEqual(mtext.horizontal_width, 45.0)
        self.assertEqual(mtext.vertical_height, 99.0)

    def test_mtext_text(self):
        mtext = self.entity
        self.assertEqual(mtext.raw_text, r"first 250 chars\Psecond 250 chars\Pand the rest")
        self.assertEqual(mtext.lines(), ["first 250 chars", "second 250 chars", "and the rest"])

    def test_mtext_plain_text(self):
        mtext = self.entity
        mtext.raw_text = r"\A1;Das ist eine MText\PZeile mit {\LFormat}ierung\Pänder die Farbe\P\pi-7.5,l7.5,t7.5;1.^INummerierung\P2.^INummerierung\P\pi0,l0,tz;\P{\H0.7x;\S1/2500;}  ein Bruch"
        expected = "Das ist eine MText\nZeile mit Formatierung\nänder die Farbe\n1.^INummerierung\n2.^INummerierung\n\n1/2500  ein Bruch"
        self.assertEqual(expected, mtext.plain_text())

    def test_mtext_plain_text_special_char(self):
        mtext = self.entity
        mtext.raw_text = "%%d"
        self.assertEqual("°", mtext.plain_text())

MTEXT = r"""  0
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
 42
45.0
 43
99.0
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
