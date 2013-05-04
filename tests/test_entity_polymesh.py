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

class TestPolymeshDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(POLYMESH_DXF12)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_entitysection(self):
        self.assertEqual(len(self.entities), 1, "VERTEX should be added to POLYLINE")

    def test_polymesh_properties(self):
        polymesh = self.entities[0]
        self.assertEqual(polymesh.dxftype, 'POLYMESH')
        self.assertEqual(polymesh.color, 256)
        self.assertEqual(polymesh.layer, '0')
        self.assertEqual(polymesh.linetype, None)
        self.assertEqual(polymesh.mcount, 3)
        self.assertEqual(polymesh.ncount, 3)
        self.assertFalse(polymesh.is_mclosed)
        self.assertFalse(polymesh.is_nclosed)
        self.assertFalse(polymesh.paperspace)

    def test_polymesh_first_vertex(self):
        polymesh = self.entities[0]
        v1 = polymesh.get_location((0,0))
        self.assertEqual(v1, (0., 0., 99.))

    def test_polymesh_last_vertex(self):
        polymesh = self.entities[0]
        v2 = polymesh.get_location((2,2))
        self.assertEqual(v2, (2., 2., 99.))

class TestPolymeshDXF13(TestPolymeshDXF12):
    def setUp(self):
        tags = Tags.fromtext(POLYMESH_DXF13)
        self.entities = EntitySection(tags, DrawingProxy('AC1024'))


POLYMESH_DXF12 = """  0
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
16
 71
3
 72
3
  0
VERTEX
  8
0
 10
0.0
 20
0.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
0.0
 20
1.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
0.0
 20
2.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
1.0
 20
0.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
1.0
 20
1.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
1.0
 20
2.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
2.0
 20
0.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
2.0
 20
1.0
 30
99.0
 70
64
  0
VERTEX
  8
0
 10
2.0
 20
2.0
 30
99.0
 70
64
  0
SEQEND
  0
ENDSEC
"""

POLYMESH_DXF13 = """  0
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
AcDbPolygonMesh
 66
     1
 10
0.0
 20
0.0
 30
0.0
 70
    16
 71
     3
 72
     3
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
AcDbPolygonMeshVertex
 10
0.0
 20
0.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
0.0
 20
1.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
0.0
 20
2.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
1.0
 20
0.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
1.0
 20
1.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
1.0
 20
2.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
2.0
 20
0.0
 30
99.0
 70
    64
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
AcDbPolygonMeshVertex
 10
2.0
 20
1.0
 30
99.0
 70
    64
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
100
AcDbVertex
100
AcDbPolygonMeshVertex
 10
2.0
 20
2.0
 30
99.0
 70
    64
  0
SEQEND
  5
B7
330
AD
100
AcDbEntity
  8
0
  0
ENDSEC
"""
