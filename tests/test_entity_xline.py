# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.tags import Tags
from dxfgrabber.dxfentities import entity_factory

class TestXLine(unittest.TestCase):
    def setUp(self):
        tags = Tags.from_text(XLINE)
        self.entity = entity_factory(tags)

    def test_xline_properties(self):
        xline = self.entity
        self.assertEqual(xline.dxftype, 'XLINE')
        self.assertEqual(xline.color, 256)
        self.assertEqual(xline.layer, '0')
        self.assertEqual(xline.linetype, None)
        self.assertFalse(xline.paperspace)

    def test_xline_data(self):
        xline = self.entity
        self.assertEqual(xline.start, (40.0, 45.0, 0.0))
        self.assertEqual(xline.unit_vector, (0.66, 0.74, 0.0))

XLINE = """  0
XLINE
  5
3D2
330
1F
100
AcDbEntity
  8
0
100
AcDbXline
 10
40.0
 20
45.0
 30
0.0
 11
0.66
 21
0.74
 31
0.0
"""
