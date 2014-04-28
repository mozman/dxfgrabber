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
        light = self.entity
        self.assertEqual(light.dxftype, 'LIGHT')
        self.assertEqual(light.layer, '*ADSK_SYSTEM_LIGHTS')

    def test_sun_data(self):
        light = self.entity
        self.assertEqual(light.version, 1)
        self.assertEqual(light.light_color, 7)
        self.assertEqual(light.true_color, 16777215)
        self.assertEqual(light.name, 'Pointlight_Test')
        self.assertEqual(light.light_type, 2)
        self.assertEqual(light.intensity, 1.0)
        self.assertEqual(light.position, (1700, 1095, 0))
        self.assertEqual(light.target, (1700, 1095, -10))
        self.assertEqual(light.attenuation_type, 0)
        self.assertFalse(light.use_attenuation_limits)
        self.assertEqual(light.attenuation_start_limit, 1)
        self.assertEqual(light.attenuation_end_limit, 10)
        self.assertEqual(light.hotspot_angle, 45)
        self.assertEqual(light.fall_off_angle, 50)
        self.assertTrue(light.cast_shadows)
        self.assertEqual(light.shadow_type, 0)
        self.assertEqual(light.shadow_map_size, 256)
        self.assertEqual(light.shadow_softness, 1)

LIGHT = """  0
LIGHT
  5
34F
102
{ACAD_XDICTIONARY
360
350
102
}
330
1F
100
AcDbEntity
  8
*ADSK_SYSTEM_LIGHTS
160
                 8
310
0800000000000000
100
AcDbLight
 90
        1
  1
Pointlight_Test
 70
     2
290
     1
 63
     7
421
 16777215
291
     0
 40
1.0
 10
1700
 20
1095
 30
0.0
 11
1700
 21
1095
 31
-10.0
 72
     0
292
     0
 41
1.0
 42
10.0
 50
45.0
 51
50.0
293
     1
 73
     0
 91
      256
280
     1
"""
