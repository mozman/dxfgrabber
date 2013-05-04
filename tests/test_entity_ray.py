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

class TestRay(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(RAY)
        self.entity = entity_factory(tags, 'AC1024')

    def test_ray_properties(self):
        ray = self.entity
        self.assertEqual(ray.dxftype, 'RAY')
        self.assertEqual(ray.color, 256)
        self.assertEqual(ray.layer, '0')
        self.assertEqual(ray.linetype, None)
        self.assertFalse(ray.paperspace)

    def test_ray_data(self):
        ray = self.entity
        self.assertEqual(ray.start, (3.0, 7.0, 0.0))
        self.assertEqual(ray.unitvector, (0.37, -0.92, 0.0))

RAY = """  0
RAY
  5
3E1
330
1F
100
AcDbEntity
  8
0
100
AcDbRay
 10
3.0
 20
7.0
 30
0.0
 11
0.37
 21
-0.92
 31
0.0
"""
