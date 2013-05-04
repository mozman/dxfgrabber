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


class TestTextDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(TEXT_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

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

class TestTextDXF12(TestTextDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(TEXT_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

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
