#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 21.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version

class TestCircleDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(CIRCLE_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_circle_data(self):
        circle = self.entity
        self.assertEqual(circle.dxftype, 'CIRCLE')
        self.assertEqual(circle.center, (0., 0., 0.))
        self.assertEqual(circle.radius, 5.)
        self.assertEqual(circle.layer, 'mozman')
        self.assertEqual(circle.color, 256)
        self.assertEqual(circle.linetype, None)
        self.assertFalse(circle.paperspace)

class TestCircleDXF13(TestCircleDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(CIRCLE_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

CIRCLE_DXF13 = """  0
CIRCLE
  5
3D9
330
1F
100
AcDbEntity
  8
mozman
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
"""

CIRCLE_DXF12 = """  0
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
"""
