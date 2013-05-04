#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.entitysection import EntitySection

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version

class TestPolyfaceDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(POLYFACE_DXF12)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_entitysection(self):
        self.assertEqual(len(self.entities), 1, "VERTEX should be added to POLYLINE")

    def test_polyface_properties(self):
        polyface = self.entities[0]
        self.assertEqual(polyface.dxftype, 'POLYFACE')
        self.assertEqual(polyface.color, 256)
        self.assertEqual(polyface.layer, '0')
        self.assertEqual(polyface.linetype, None)
        self.assertFalse(polyface.paperspace)

    def test_face_count(self):
        polyface = self.entities[0]
        self.assertEqual(len(polyface), 2)

    def test_polymesh_first_face(self):
        polyface = self.entities[0]
        f1 = polyface[0]
        self.assertEqual(f1[0].location, (0., 0., 0.))
        self.assertEqual(f1[3].location, (1., 0., 0.))

    def test_polymesh_last_face(self):
        polyface = self.entities[0]
        f2 = polyface[-1]
        self.assertEqual(f2[0].location, (0., 0., 1.))
        self.assertEqual(f2[3].location, (1., 0., 1.))

POLYFACE_DXF12 = """  0
SECTION
  2
ENTITIES
  0
POLYLINE
  8
0
 66
1
 70
64
 71
8
 72
2
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
 70
192
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
 70
192
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
 70
192
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
 70
192
  0
VERTEX
  8
0
 10
0.0
 20
0.0
 30
1.0
 70
192
  0
VERTEX
  8
0
 10
0.0
 20
1.0
 30
1.0
 70
192
  0
VERTEX
  8
0
 10
1.0
 20
1.0
 30
1.0
 70
192
  0
VERTEX
  8
0
 10
1.0
 20
0.0
 30
1.0
 70
192
  0
VERTEX
 62
0
  8
0
 10
0.0
 20
0.0
 30
0.0
 70
128
 71
1
 72
2
 73
3
 74
4
  0
VERTEX
 62
0
  8
0
 10
0.0
 20
0.0
 30
0.0
 70
128
 71
5
 72
6
 73
7
 74
8
  0
SEQEND
  0
ENDSEC
"""

POLYFACE_DXF13 = """  0
SECTION
  2
ENTITIES
  0
POLYLINE
  5
AD
330
76
100
AcDbEntity
  8
0
100
AcDbPolyFaceMesh
 66
     1
 10
0.0
 20
0.0
 30
0.0
 70
    64
 71
     8
 72
     2
  0
VERTEX
  5
AE
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
0.0
 20
0.0
 30
0.0
 70
   192
  0
VERTEX
  5
AF
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
0.0
 20
1.0
 30
0.0
 70
   192
  0
VERTEX
  5
B0
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
1.0
 20
1.0
 30
0.0
 70
   192
  0
VERTEX
  5
B1
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
1.0
 20
0.0
 30
0.0
 70
   192
  0
VERTEX
  5
B2
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
0.0
 20
0.0
 30
1.0
 70
   192
  0
VERTEX
  5
B3
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
0.0
 20
1.0
 30
1.0
 70
   192
  0
VERTEX
  5
B4
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
1.0
 20
1.0
 30
1.0
 70
   192
  0
VERTEX
  5
B5
330
AD
100
AcDbEntity
  8
0
100
AcDbVertex
100
AcDbPolyFaceMeshVertex
 10
1.0
 20
0.0
 30
1.0
 70
   192
  0
VERTEX
  5
B6
330
AD
100
AcDbEntity
  8
0
 62
     0
100
AcDbFaceRecord
 10
0.0
 20
0.0
 30
0.0
 70
   128
 71
     1
 72
     2
 73
     3
 74
     4
  0
VERTEX
  5
B7
330
AD
100
AcDbEntity
  8
0
 62
     0
100
AcDbFaceRecord
 10
0.0
 20
0.0
 30
0.0
 70
   128
 71
     5
 72
     6
 73
     7
 74
     8
  0
SEQEND
  5
B8
330
AD
100
AcDbEntity
  8
0
  0
ENDSEC
"""
