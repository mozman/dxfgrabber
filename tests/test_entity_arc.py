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


class TestArcDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ARC_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_arc_data(self):
        entity = self.entity
        self.assertEqual(entity.dxftype, 'ARC')
        self.assertEqual(entity.center, (0., 0., 0.))
        self.assertEqual(entity.radius, 5.0)
        self.assertEqual(entity.startangle, 0.0)
        self.assertEqual(entity.endangle, 90.0)
        self.assertEqual(entity.color, 256)
        self.assertEqual(entity.layer, '0')
        self.assertEqual(entity.linetype, None)
        self.assertFalse(entity.paperspace)

class TestArcDXF13(TestArcDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ARC_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

ARC_DXF12 = """  0
ARC
  5
3E5
  8
0
 10
0.0
 20
0.0
 30
0.0
 40
5.0
 50
0.0
 51
90.0
"""

ARC_DXF13 = """  0
ARC
  5
3E5
330
1F
100
AcDbEntity
  8
0
100
AcDbCircle
 10
0.0
 20
0.0
 30
0.0
 40
5.0
100
AcDbArc
 50
0.0
 51
90.0
"""
