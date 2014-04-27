# Created: 27.04.14
# License: MIT License

from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory
from datetime import datetime

class TestSun(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(SUN)
        self.entity = entity_factory(tags, 'AC1024')

    def test_sun_properties(self):
        sun = self.entity
        self.assertEqual(sun.dxftype, 'SUN')
        self.assertEqual(sun.color, 256)
        self.assertEqual(sun.layer, '0')
        self.assertEqual(sun.linetype, None)
        self.assertFalse(sun.paperspace)

    def test_sun_data(self):
        sun = self.entity
        self.assertEqual(sun.version, 1)
        self.assertEqual(sun.status, 0)
        self.assertEqual(sun.sun_color, 0)
        self.assertEqual(sun.intensity, 0.75)
        self.assertTrue(sun.shadows)
        self.assertEqual(sun.date, datetime(2014, 4, 22, 0, 0, 0))
        self.assertTrue(sun.daylight_savings_time)
        self.assertEqual(sun.shadow_type, 0)
        self.assertEqual(sun.shadow_softness, 0)

SUN = """  0
SUN
  5
3D5
330
1F
100
AcDbEntity
  8
0
100
AcDbSun
 90
1
290
0
 63
0
 40
0.75
291
1
 91
2456770
 92
0
292
1
 70
0
280
0
"""
