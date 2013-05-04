#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 21.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.entitysection import EntitySection

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version

class TestPolylineDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(POLYLINE_DXF12)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_polyline(self):
        self.assertEqual(len(self.entities), 1)

    def test_polyline_data(self):
        polyline = self.entities[0]
        self.assertEqual(len(polyline), 4)

    def test_polyline_points(self):
        polyline = self.entities[0]
        points = list(polyline.points())
        self.assertEqual(points[3], (0., 1., 0.))

class TestPolylineDXF13(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(POLYLINE_DXF13)
        self.entities = EntitySection(tags, DrawingProxy('AC1024'))

POLYLINE_DXF13 = """  0
SECTION
  2
ENTITIES
  0
ENDSEC
"""

POLYLINE_DXF12 = """  0
SECTION
  2
ENTITIES
  0
POLYLINE
 62
7
  8
mozman
 66
1
 10
0.0
 20
0.0
 30
0.0
 70
8
  0
VERTEX
  8
0
 10
0.0
 20
0.0
 30
0.0
  0
VERTEX
  8
0
 10
1.0
 20
0.0
 30
0.0
  0
VERTEX
  8
0
 10
1.0
 20
1.0
 30
0.0
  0
VERTEX
  8
0
 10
0.0
 20
1.0
 30
0.0
  0
SEQEND
  0
ENDSEC
"""
