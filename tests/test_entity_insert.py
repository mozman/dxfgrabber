#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.entitysection import EntitySection

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version

class TestInsertDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(INSERT_DXF12)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_section_setup(self):
        self.assertEqual(len(self.entities), 1, "ATTRIB should be appended to INSERT")

    def test_insert(self):
        insert = self.entities[0]
        self.assertEqual(insert.dxftype, 'INSERT')
        self.assertTrue(insert.attribsfollow)
        self.assertEqual(insert.insert, (999.0, 999., 0.))
        self.assertEqual(insert.name, "TEST")
        self.assertEqual(insert.rotation, 0.)
        self.assertEqual(insert.color, 256)
        self.assertEqual(insert.layer, '0')
        self.assertEqual(insert.linetype, None)
        self.assertFalse(insert.paperspace)

    def test_attribs(self):
        insert = self.entities[0]
        self.assertEqual(len(insert.attribs), 1)
        attrib = insert.find_attrib('MYATTRIB')
        self.assertEqual(attrib.text, 'TestInput')

class TestInsertDXF13(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(INSERT_DXF13)
        self.entities = EntitySection(tags, DrawingProxy('AC1024'))

INSERT_DXF12 = """  0
SECTION
  2
ENTITIES
  0
INSERT
  5
51B
  8
0
 66
     1
  2
TEST
 10
999.0
 20
999.0
 30
0.0
  0
ATTRIB
  5
51C
  8
0
 10
77.01095802080232
 20
2.6882932565357289
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
  0
SEQEND
  0
ENDSEC
"""

INSERT_DXF13 = """  0
SECTION
  2
ENTITIES
  0
INSERT
  5
510
330
1F
100
AcDbEntity
  8
0
100
AcDbBlockReference
 66
     1
  2
Test
 10
999.0
 20
999.0
 30
0.0
  0
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
77.01095802080232
 20
2.688293256535729
 30
0.0
 40
3.0
  1
TestInput
  7
Notes
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
  0
SEQEND
  0
ENDSEC
"""
