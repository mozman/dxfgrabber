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

class TestLWPolyline(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(LWPOLYLINE)
        self.entity = entity_factory(tags, 'AC1024')

    def test_lwpolyline_properties(self):
        polyline = self.entity
        self.assertEqual(polyline.dxftype, 'LWPOLYLINE')
        self.assertTrue(polyline.is_closed)
        self.assertEqual(polyline.color, 256)
        self.assertEqual(polyline.layer, '0')
        self.assertEqual(polyline.linetype, None)
        self.assertFalse(polyline.paperspace)

    def test_lwpolyline_first_point(self):
        polyline = self.entity
        self.assertEqual(len(polyline.points), 7)
        self.assertEqual(polyline.points[0], (5.24, 1.40))

    def test_lwpolyline_first_point(self):
        polyline = self.entity
        self.assertEqual(polyline.points[-1], (4.16, 0.29))

LWPOLYLINE = """  0
LWPOLYLINE
  5
3DE
330
1F
100
AcDbEntity
  8
0
100
AcDbPolyline
 90
        7
 70
     1
 43
0.0
 10
5.24
 20
1.40
 10
5.04
 20
2.93
 10
3.72
 20
3.73
 10
2.27
 20
3.20
 10
1.78
 20
1.74
 10
2.62
 20
0.44
 10
4.16
 20
0.29
"""
