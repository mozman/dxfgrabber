#!/usr/bin/env python
#coding:utf-8
# Purpose: 
# Created: 21.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfexplorer.tags import Tags
from dxfexplorer.entitysection import EntitySection
from dxfexplorer.testtools import  DrawingProxy

LINES = """  0
SECTION
  2
ENTITIES
  0
LINE
  8
0
 10
0.0
 20
0.0
 30
0.0
 11
1.0
 21
0.0
 31
0.0
  0
LINE
  8
0
 10
1.0
 20
0.0
 30
0.0
 11
1.0
 21
1.0
 31
0.0
  0
LINE
  8
0
 10
1.0
 20
1.0
 30
0.0
 11
0.0
 21
1.0
 31
0.0
  0
LINE
  8
0
 10
0.0
 20
1.0
 30
0.0
 11
0.0
 21
0.0
 31
0.0
  0
ENDSEC
"""

CIRCLES = """  0
SECTION
  2
ENTITIES
  0
CIRCLE
  8
mozman
 10
0.0
 20
0.0
 30
0.0
 40
5.0
  0
CIRCLE
  8
mozman
 10
3.0
 20
3.0
 30
0.0
 40
3.0
  0
ENDSEC
"""

POLYLINE = """  0
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
class TestLines(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(LINES)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_lines(self):
        self.assertEqual(len(self.entities), 4)

    def test_lines_data(self):
        line = self.entities[0]
        self.assertEqual(line.start, (0., 0., 0.))
        self.assertEqual(line.end, (1., 0., 0.))

class TestCircles(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(CIRCLES)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_circles(self):
        self.assertEqual(len(self.entities), 2)

    def test_circle_data(self):
        circle = self.entities[0]
        self.assertEqual(circle.center, (0., 0., 0.))
        self.assertEqual(circle.radius, 5.)
        self.assertEqual(circle.layer, 'mozman')

class TestPolyline(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(POLYLINE)
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
