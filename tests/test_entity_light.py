# Created: 28.04.14
# License: MIT License

from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory


class TestLight(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(LIGHT)
        self.entity = entity_factory(tags, 'AC1024')

    def test_sun_properties(self):
        sun = self.entity
        self.assertEqual(sun.dxftype, 'LIGHT')
        self.assertEqual(sun.color, 256)
        self.assertEqual(sun.layer, '0')
        self.assertEqual(sun.linetype, None)
        self.assertFalse(sun.paperspace)

    def test_sun_data(self):
        sun = self.entity
        self.assertEqual(sun.version, 1)

LIGHT = """  0
LIGHT
  5
3D5
330
1F
100
AcDbEntity
  8
0
100
AcDbLight
 90
1
"""
