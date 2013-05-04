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

class TestEllipse(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ELLIPSE)
        self.entity = entity_factory(tags, 'AC1024')

    def test_ellipse_data(self):
        entity = self.entity
        self.assertEqual(entity.dxftype, 'ELLIPSE')
        self.assertEqual(entity.center, (0., 0., 0.))
        self.assertEqual(entity.majoraxis, (2.60, 1.50, 0.))
        self.assertEqual(entity.ratio, 0.33)
        self.assertEqual(entity.startparam, 0.0)
        self.assertEqual(entity.endparam, 6.28)
        self.assertEqual(entity.color, 256)
        self.assertEqual(entity.layer, '0')
        self.assertEqual(entity.linetype, None)
        self.assertFalse(entity.paperspace)

ELLIPSE = """  0
ELLIPSE
  5
3D2
330
1F
100
AcDbEntity
  8
0
100
AcDbEllipse
 10
0.0
 20
0.0
 30
0.0
 11
2.60
 21
1.50
 31
0.0
210
0.0
220
0.0
230
1.0
 40
0.33
 41
0.0
 42
6.28
"""
