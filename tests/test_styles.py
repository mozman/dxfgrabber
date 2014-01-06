# Created: 06.01.2014
# License: MIT License
from __future__ import unicode_literals

import unittest

from dxfgrabber.tags import Tags
from dxfgrabber.styles import StyleTable


class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version


class TestDXF12Style(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(DXF12STYLES)
        self.styles = StyleTable.from_tags(tags, DrawingProxy("AC1009"))

    def test_get_existing_style(self):
        style = self.styles.get("STANDARD")
        self.assertEqual("STANDARD", style.name)

    def test_contains(self):
        self.assertTrue("STANDARD" in self.styles)

    def test_iter_styles(self):
        styles = list(self.styles)
        self.assertEqual(1, len(styles))

    def test_style_names(self):
        self.assertEqual(self.styles.stylenames(), ["STANDARD"])

    def test_style_attribs(self):
        style = self.styles.get("STANDARD")
        self.assertEqual(style.height, 0)
        self.assertEqual(style.width, 1)
        self.assertEqual(style.oblique, 0)
        self.assertFalse(style.backward)
        self.assertFalse(style.mirror_y)
        self.assertEqual(style.font, 'txt')
        self.assertEqual(style.bigfont, '')


class TestDXF13Style(TestDXF12Style):
    def setUp(self):
        tags = Tags.fromtext(DXF13STYLES)
        self.styles = StyleTable.from_tags(tags, DrawingProxy("AC1024"))

DXF13STYLES = """  0
TABLE
  2
STYLE
  5
1E
330
0
100
AcDbSymbolTable
 70
    33
  0
STYLE
  5
1F
330
1E
100
AcDbSymbolTableRecord
100
AcDbTextStyleTableRecord
  2
STANDARD
 70
     0
 40
0.0
 41
1.0
 50
0.0
 71
     0
 42
0.2
  3
txt
  4

  0
ENDTAB
"""

DXF12STYLES = """  0
TABLE
  2
STYLE
 70
    33
  0
STYLE
  2
STANDARD
 70
     0
 40
0.0
 41
1.0
 50
0.0
 71
     0
 42
0.2
  3
txt
  4

  0
ENDTAB
"""
