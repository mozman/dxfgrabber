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

class TestSpline(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(SPLINE)
        self.entity = entity_factory(tags, 'AC1024')

    def test_spline_properties(self):
        spline = self.entity
        self.assertEqual(spline.dxftype, 'SPLINE')
        self.assertEqual(spline.color, 256)
        self.assertEqual(spline.layer, '0')
        self.assertEqual(spline.linetype, None)
        self.assertFalse(spline.paperspace)

    def test_spline_data(self):
        spline = self.entity
        self.assertEqual(spline.normalvector, (0.0, 0.0, 1.0))
        self.assertEqual(spline.degree, 3)

    def test_spline_konts(self):
        spline = self.entity
        self.assertEqual(len(spline.knots), 10)
        self.assertEqual(spline.knots[0], 0)
        self.assertEqual(spline.knots[-1], 82.08)

    def test_spline_weights(self):
        spline = self.entity
        self.assertEqual(len(spline.weights), 6)
        self.assertEqual(spline.weights[0], 7.)
        self.assertEqual(spline.weights[-1], 3.)

    def test_spline_controlpoints(self):
        spline = self.entity
        self.assertEqual(len(spline.controlpoints), 6)
        self.assertEqual(spline.controlpoints[0], (28.40, 40.68, 0.))
        self.assertEqual(spline.controlpoints[-1], (97.78, 53.96, 0.))

    def test_spline_fitpoints(self):
        spline = self.entity
        self.assertEqual(len(spline.fitpoints), 4)
        self.assertEqual(spline.fitpoints[0], (28.40, 40.68, 0.))
        self.assertEqual(spline.fitpoints[-1], (97.78, 53.96, 0.))

SPLINE = """  0
SPLINE
  5
3D5
330
1F
100
AcDbEntity
  8
0
100
AcDbSpline
210
0.0
220
0.0
230
1.0
 70
     8
 71
     3
 72
    10
 73
     6
 74
     4
 42
0.0000000001
 43
0.0000000001
 44
0.0000000001
 40
0.0
 40
0.0
 40
0.0
 40
0.0
 40
29.56
 40
51.18
 40
82.08
 40
82.08
 40
82.08
 40
82.08
 10
28.40
 20
40.68
 30
0.0
 41
7.0
 10
37.78
 20
49.19
 30
0.0
 41
1.0
 10
54.02
 20
63.91
 30
0.0
 41
1.0
 10
71.78
 20
28.72
 30
0.0
 41
1.0
 10
88.15
 20
44.61
 30
0.0
 41
2.0
 10
97.78
 20
53.96
 30
0.0
 41
3.0
 11
28.40
 21
40.68
 31
0.0
 11
54.82
 21
53.96
 31
0.0
 11
70.62
 21
39.21
 31
0.0
 11
97.78
 21
53.96
 31
0.0
"""
