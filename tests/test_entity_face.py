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

class TestFaceDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(FACE_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_face_data(self):
        entity = self.entity
        self.assertEqual(entity.dxftype, '3DFACE')
        self.assertEqual(entity.points[0], (0., 0., 0.))
        self.assertEqual(entity.points[1], (1., 0., 1.))
        self.assertEqual(entity.points[2], (1., 1., 1.))
        self.assertEqual(entity.points[3], (0., 1., 0.))
        self.assertEqual(entity.color, 256)
        self.assertEqual(entity.layer, '0')
        self.assertEqual(entity.linetype, None)
        self.assertFalse(entity.paperspace)

class TestFaceDXF13(TestFaceDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(FACE_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

FACE_DXF12 = """  0
3DFACE
  5
41F
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
1.0
 12
1.0
 22
1.0
 32
1.0
 13
0.0
 23
1.0
 33
0.0
"""

FACE_DXF13 = """  0
3DFACE
  5
41F
330
1F
100
AcDbEntity
  8
0
100
AcDbFace
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
1.0
 12
1.0
 22
1.0
 32
1.0
 13
0.0
 23
1.0
 33
0.0
"""
