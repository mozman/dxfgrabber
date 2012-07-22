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

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version

class TestCirclesDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(CIRCLES_DXF12)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_circles(self):
        self.assertEqual(len(self.entities), 2)

    def test_circle_data(self):
        circle = self.entities[0]
        self.assertEqual(circle.center, (0., 0., 0.))
        self.assertEqual(circle.radius, 5.)
        self.assertEqual(circle.layer, 'mozman')

class TestCirclesDXF13(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(CIRCLES_DXF13)
        self.entities = EntitySection(tags, DrawingProxy('AC1024'))

CIRCLES_DXF13 = """  0
SECTION
  2
ENTITIES
  0
ENDSEC
"""

CIRCLES_DXF12 = """  0
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
