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

class TestAttribDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ATTRIB_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_attrib_data(self):
        entity = self.entity
        self.assertEqual(entity.dxftype, 'ATTRIB')
        self.assertEqual(entity.text, "TestInput")
        self.assertEqual(entity.tag, "MYATTRIB")
        self.assertEqual(entity.insert, (17., 17., 0.))
        self.assertEqual(entity.rotation, 0.0)
        self.assertEqual(entity.height, 3.0)
        self.assertEqual(entity.style, "NOTES")
        self.assertEqual(entity.color, 256)
        self.assertEqual(entity.layer, '0')
        self.assertEqual(entity.linetype, None)
        self.assertFalse(entity.paperspace)

class TestAttribDXF13(TestAttribDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ATTRIB_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

ATTRIB_DXF12 = """  0
ATTRIB
  5
51C
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
TestInput
  7
NOTES
  2
MYATTRIB
 70
     0
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
1001
AcDbAttr
1070
     0
1070
     1
"""

ATTRIB_DXF13 = """  0
ATTRIB
  5
511
102
{ACAD_XDICTIONARY
360
512
102
}
330
510
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
TestInput
  7
NOTES
100
AcDbAttribute
280
     0
  2
MYATTRIB
 70
     0
280
     1
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
