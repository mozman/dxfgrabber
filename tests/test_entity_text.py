# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.dxfentities import entity_factory


class TestTextDXF12(unittest.TestCase):
    def setUp(self):
        self.entity = entity_factory(Tags.from_text(TEXT_DXF12))

    def test_text_data(self):
        entity = self.entity
        self.assertEqual(entity.dxftype, 'TEXT')
        self.assertEqual(entity.text, "TEXT")
        self.assertEqual(entity.insert, (17., 17., 0.))
        self.assertEqual(entity.rotation, 0.0)
        self.assertEqual(entity.height, 3.0)
        self.assertEqual(entity.style.upper(), "NOTES")
        self.assertEqual(entity.color, 256)
        self.assertEqual(entity.layer, '0')
        self.assertEqual(entity.linetype, None)
        self.assertFalse(entity.paperspace)

    def test_text_alignment(self):
        entity = self.entity
        self.assertEqual(entity.halign, 0)
        self.assertEqual(entity.valign, 0)
        self.assertEqual(entity.align_point, None)

    def test_text_plain_text_old_formatting_code(self):
        text = self.entity
        text.text = "das ist %%u ein text mit %"
        expected = "das ist  ein text mit %"
        self.assertEqual(expected, text.plain_text())

    def test_mtext_plain_text_old_formatting_code_2(self):
        text = self.entity
        text.text = "%%u2 CAR GARAGE"
        self.assertEqual("2 CAR GARAGE", text.plain_text())


class TestTextDXF12(TestTextDXF12):
    def setUp(self):
        self.entity = entity_factory(Tags.from_text(TEXT_DXF13))

TEXT_DXF12 = """  0
TEXT
  5
470
  8
0
 10
17.0
 20
17.0
 30
0.0
 40
3.0
  1
TEXT
  7
NOTES
1001
ACADANNOPO
1070
     1
1001
ACADANNOTATIVE
1000
AnnotativeData
1002
{
1070
     1
1070
     0
1002
}
"""

TEXT_DXF13 = """  0
TEXT
  5
470
102
{ACAD_XDICTIONARY
360
471
102
}
330
1F
100
AcDbEntity
  8
0
100
AcDbText
 10
17.0
 20
17.0
 30
0.0
 40
3.0
  1
TEXT
  7
Notes
100
AcDbText
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
"""
