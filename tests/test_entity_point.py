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

class TestPointDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(POINT_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_point_data(self):
        entity = self.entity
        self.assertEqual(entity.dxftype, 'POINT')
        self.assertEqual(entity.point, (10., 20., 30.))
        self.assertEqual(entity.color, 256)
        self.assertEqual(entity.layer, '0')
        self.assertEqual(entity.linetype, None)
        self.assertFalse(entity.paperspace)

class TestPointDXF13(TestPointDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(POINT_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

POINT_DXF12 = """  0
POINT
  5
42F
  8
0
 10
10.0
 20
20.0
 30
30.0
"""

POINT_DXF13 = """  0
POINT
  5
42F
330
1F
100
AcDbEntity
  8
0
100
AcDbPoint
 10
10.0
 20
20.0
 30
30.0
"""
