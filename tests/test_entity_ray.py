# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.dxfentities import entity_factory


class TestRay(unittest.TestCase):
    def setUp(self):
        tags = Tags.from_text(RAY)
        self.entity = entity_factory(tags)

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
        self.assertEqual(ray.unit_vector, (0.37, -0.92, 0.0))

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
