# Created: 06.01.2014
# License: MIT License
from __future__ import unicode_literals

import unittest

from dxfgrabber.tags import Tags
from dxfgrabber.linetypes import LinetypeTable


class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version


class TestDXF12Style(unittest.TestCase):
    def setUp(self):
        tags = Tags.from_text(DXF12LTYPES)
        self.linetypes = LinetypeTable.from_tags(tags)

    def test_get_existing_style(self):
        style = self.linetypes.get("CONTINUOUS")
        self.assertEqual("CONTINUOUS", style.name)

    def test_contains(self):
        self.assertTrue("CONTINUOUS" in self.linetypes)

    def test_iter_styles(self):
        styles = list(self.linetypes)
        self.assertEqual(3, len(styles))

    def test_style_names(self):
        self.assertEqual(self.linetypes.names(), ["CONTINUOUS", "DASHDOT", "DASHED"])

    def test_style_attribs(self):
        style = self.linetypes.get("CONTINUOUS")
        self.assertEqual(style.description, "Solid line")
        self.assertEqual(style.length, 0.0)
        self.assertEqual(style.pattern, [])

    def test_dashed_pattern(self):
        style = self.linetypes.get("DASHED")
        self.assertEqual(style.description, "__ __ __ __ __ __ __ __ __ __ __ __ __ __ __")
        self.assertEqual(style.length, 0.75)
        # pattern: list of floats: value>0: line, value<0: gap, value=0: dot
        self.assertEqual(style.pattern, [0.5, -0.25])

    def test_dashdot_pattern(self):
        style = self.linetypes.get("DASHDOT")
        self.assertEqual(style.description, "__ . __ . __ . __ . __ . __ . __ . __ . __ . __")
        self.assertEqual(style.length, 1.0)
        # pattern: list of floats: value>0: line, value<0: gap, value=0: dot
        self.assertEqual(style.pattern, [0.5, -0.25, 0.0, -0.25])


class TestDXF13Style(TestDXF12Style):
    def setUp(self):
        tags = Tags.from_text(DXF13LTYPES)
        self.linetypes = LinetypeTable.from_tags(tags)


DXF13LTYPES = """  0
TABLE
  2
LTYPE
  5
21
330
0
100
AcDbSymbolTable
 70
     3
  0
LTYPE
  5
B
330
21
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
  2
CONTINUOUS
 70
     0
  3
Solid line
 72
    65
 73
     0
 40
0.0
  0
LTYPE
  5
3E1
330
21
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
  2
DASHED
 70
     0
  3
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __
 72
    65
 73
     2
 40
0.75
 49
0.5
 74
     0
 49
-0.25
 74
     0
  0
LTYPE
  5
51A7
330
21
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
  2
DASHDOT
 70
     0
  3
__ . __ . __ . __ . __ . __ . __ . __ . __ . __
 72
    65
 73
     4
 40
1.0
 49
0.5
 74
     0
 49
-0.25
 74
     0
 49
0.0
 74
     0
 49
-0.25
 74
     0
  0
ENDTAB
"""

DXF12LTYPES = """  0
TABLE
  2
LTYPE
 70
     3
  0
LTYPE
  2
CONTINUOUS
 70
     0
  3
Solid line
 72
    65
 73
     0
 40
0.0
  0
LTYPE
  2
DASHED
 70
     0
  3
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __
 72
    65
 73
     2
 40
0.75
 49
0.5
 49
-0.25
  0
LTYPE
  2
DASHDOT
 70
     0
  3
__ . __ . __ . __ . __ . __ . __ . __ . __ . __
 72
    65
 73
     4
 40
1.0
 49
0.5
 49
-0.25
 49
0.0
 49
-0.25
  0
ENDTAB
"""
