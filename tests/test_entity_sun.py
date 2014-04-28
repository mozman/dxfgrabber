# Created: 27.04.14
# License: MIT License

from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
import dxfgrabber

from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory
from datetime import datetime
import os


class TestSun(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(SUN)
        self.entity = entity_factory(tags, 'AC1024')

    def test_sun_properties(self):
        sun = self.entity
        self.assertEqual(sun.dxftype, 'SUN')

    def test_sun_data(self):
        sun = self.entity
        self.assertEqual(sun.version, 1)
        self.assertEqual(sun.status, 1)
        self.assertEqual(sun.sun_color, 7)
        self.assertEqual(sun.intensity, 1.)
        self.assertTrue(sun.shadows)
        self.assertEqual(sun.date, datetime(2014, 9, 21, 15, 0, 0))
        self.assertFalse(sun.daylight_savings_time)
        self.assertEqual(sun.shadow_type, 0)
        self.assertEqual(sun.shadow_map_size, 256)
        self.assertEqual(sun.shadow_softness, 1)


EXT_FILE = r"D:\source\dxftest\SunLight.dxf"


class TestFromFile(unittest.TestCase):
    def test_read_from_objects_section(self):
        if os.path.exists(EXT_FILE):
            dwg = dxfgrabber.readfile(EXT_FILE)
            # take first sun
            sun = [obj for obj in dwg.objects if obj.dxftype == 'SUN'][0]
            self.assertEqual(sun.date, datetime(2014, 9, 21, 15, 0, 0))

SUN = """  0
SUN
  5
34D
330
EA
100
AcDbSun
 90
        1
290
     1
 63
     7
421
 16777215
 40
1.0
291
     1
 91
  2456922
 92
 54000000
292
     0
 70
     0
 71
   256
280
     1
"""
