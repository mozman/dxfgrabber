# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.dxfentities import entity_factory


class TestLWPolyline(unittest.TestCase):
    def setUp(self):
        tags = Tags.from_text(LWPOLYLINE)
        self.entity = entity_factory(tags)

    def test_lwpolyline_properties(self):
        polyline = self.entity
        self.assertEqual(polyline.dxftype, 'LWPOLYLINE')
        self.assertTrue(polyline.is_closed)
        self.assertEqual(polyline.color, 256)
        self.assertEqual(polyline.layer, '0')
        self.assertEqual(polyline.linetype, None)
        self.assertEqual(polyline.elevation, 0.)
        self.assertEqual(polyline.thickness, 2.7)
        self.assertFalse(polyline.paperspace)

    def test_lwpolyline_first_point(self):
        polyline = self.entity
        self.assertEqual(0, polyline.const_width)
        self.assertEqual(len(polyline.points), 7)
        self.assertEqual(polyline.points[0], (5.24, 1.4))

    def test_lwpolyline_last_point(self):
        polyline = self.entity
        self.assertEqual(polyline.points[-1], (4.16, 0.29))


class TestLWPolyline2(unittest.TestCase):
    def setUp(self):
        tags = Tags.from_text(LWPOLYLINE2)
        self.entity = entity_factory(tags)

    def test_points(self):
        polyline = self.entity
        self.assertEqual([(1.0, 2.0), (2.0, 3.0), (3.0, 4.0)], polyline.points)

    def test_width(self):
        polyline = self.entity
        self.assertEqual([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)], polyline.width)

    def test_bulge(self):
        polyline = self.entity
        self.assertEqual([0.5, 0.75, 1.0], polyline.bulge)


LWPOLYLINE = """  0
LWPOLYLINE
  5
3DE
330
1F
100
AcDbEntity
  8
0
100
AcDbPolyline
 90
        7
 70
     1
 39
2.7
 43
0.0
 10
5.24
 20
1.40
 10
5.04
 20
2.93
 10
3.72
 20
3.73
 10
2.27
 20
3.20
 10
1.78
 20
1.74
 10
2.62
 20
0.44
 10
4.16
 20
0.29
999
coordinates never at the end of the file
"""


LWPOLYLINE2 = """  0
LWPOLYLINE
  5
3DE
330
1F
100
AcDbEntity
  8
0
100
AcDbPolyline
 90
     3
 70
     1
 39
2.7
 43
0.0
 10
1.00
 20
2.00
 40
1.0
 41
1.0
 42
0.5
 10
2.00
 20
3.00
 40
2.0
 41
2.0
 42
0.75
 10
3.00
 20
4.00
 40
3.0
 41
3.0
 42
1.00
"""