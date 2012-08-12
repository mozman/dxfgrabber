#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test blocks section
# Created: 08.08.2012
# Copyright (C) 2012, Manfred Moitzi
# License: MIT-License
from __future__ import unicode_literals

import unittest

from dxfgrabber.tags import Tags
from dxfgrabber.blockssection import BlocksSection

class DrawingProxy:
    def __init__(self, version):
        self.grab_blocks = True
        self.dxfversion = version

class TestBlockSectionDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(BLOCKS_DXF12)
        self.blocks = BlocksSection(tags, DrawingProxy('AC1009'))

    def test_paperspace_block(self):
        block = self.blocks['$PAPER_SPACE']
        self.assertEqual(block.name, '$PAPER_SPACE')
        self.assertEqual(len(block), 0)

    def test_line_block(self):
        block = self.blocks['LINE-BLOCK']
        self.assertEqual(block.name, 'LINE-BLOCK')
        self.assertEqual(len(block), 1)
        line = block[0]
        self.assertEqual(line.layer, 'LOGO')

class TestBlockSectionDXF13(TestBlockSectionDXF12):
    def setUp(self):
        tags = Tags.fromtext(BLOCKS_DXF13)
        self.blocks = BlocksSection(tags, DrawingProxy('AC1024'))

class TestBlockWithAttributeDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(BLOCKS_WITH_ATTRIB_DXF12)
        self.blocks = BlocksSection(tags, DrawingProxy('AC1009'))

    def test_testblock(self):
        block = self.blocks['TESTBLOCK']
        self.assertEqual(block.name, 'TESTBLOCK')
        self.assertEqual(len(block), 2)

    def test_entity_polyline(self):
        block = self.blocks['TESTBLOCK']
        polyline = block[0]
        self.assertEqual(polyline.dxftype, 'POLYLINE')
        self.assertEqual(len(polyline), 4)

    def test_entity_attdef(self):
        block = self.blocks['TESTBLOCK']
        attdef = block[1]
        self.assertEqual(attdef.dxftype, 'ATTDEF')
        self.assertEqual(attdef.tag, 'TESTTAG')

class TestBlockWithAttributeDXF13(TestBlockWithAttributeDXF12):
    def setUp(self):
        tags = Tags.fromtext(BLOCKS_WITH_ATTRIB_DXF13)
        self.blocks = BlocksSection(tags, DrawingProxy('AC1024'))

    def test_entity_polyline(self):
        block = self.blocks['TESTBLOCK']
        polyline = block[0]
        self.assertEqual(polyline.dxftype, 'LWPOLYLINE')
        self.assertEqual(len(polyline), 4)

BLOCKS_DXF12 = """  0
SECTION
  2
BLOCKS
  0
BLOCK
 67
     1
  8
0
  2
$PAPER_SPACE
 70
     0
 10
0.0
 20
0.0
 30
0.0
  3
$PAPER_SPACE
  1

  0
ENDBLK
  5
16
 67
     1
  8
0
  0
BLOCK
  8
0
  2
LINE-BLOCK
 70
     0
 10
0.0
 20
0.0
 30
0.0
  3
LINE-BLOCK
  1

  0
LINE
  5
B2
  8
LOGO
 62
    53
 10
-1.0
 20
-2.0
 30
0.0
 11
-2.0
 21
-2.0
 31
0.0
  0
ENDBLK
  5
17
 67
     1
  8
0
  0
ENDSEC
"""

BLOCKS_DXF13 = """  0
SECTION
  2
BLOCKS
  0
BLOCK
  5
15
330
12
100
AcDbEntity
 67
     1
  8
0
100
AcDbBlockBegin
  2
$PAPER_SPACE
 70
     0
 10
0.0
 20
0.0
 30
0.0
  3
$PAPER_SPACE
  1

  0
ENDBLK
  5
16
330
12
100
AcDbEntity
 67
     1
  8
0
100
AcDbBlockEnd
  0
BLOCK
  5
B1
330
B0
100
AcDbEntity
  8
0
100
AcDbBlockBegin
  2
LINE-BLOCK
 70
     0
 10
0.0
 20
0.0
 30
0.0
  3
LINE-BLOCK
  1

  0
LINE
  5
B2
330
B0
100
AcDbEntity
  8
LOGO
 62
    53
100
AcDbLine
 10
-1.431005238184638
 20
-0.4479491225939683
 30
0.0
 11
-2.377047953427222
 21
-1.46785225886731
 31
0.0
  0
ENDBLK
  5
17
330
12
100
AcDbEntity
 67
     1
  8
0
100
AcDbBlockEnd
  0
ENDSEC
"""

BLOCKS_WITH_ATTRIB_DXF12 = """  0
SECTION
  2
BLOCKS
  0
BLOCK
  8
0
  2
TESTBLOCK
 70
     2
 10
0.0
 20
0.0
 30
0.0
  3
TESTBLOCK
  1

  0
POLYLINE
  5
3E9
  8
0
 66
     1
 10
0.0
 20
0.0
 30
0.0
 70
     1
  0
VERTEX
  5
4C4
  8
0
 10
0.0
 20
35.847412069643497
 30
0.0
  0
VERTEX
  5
4C5
  8
0
 10
53.273527067372527
 20
35.847412069643497
 30
0.0
  0
VERTEX
  5
4C6
  8
0
 10
53.273527067372527
 20
0.0
 30
0.0
  0
VERTEX
  5
4C7
  8
0
 10
0.0
 20
0.0
 30
0.0
  0
SEQEND
  5
4C8
  8
0
  0
ATTDEF
  5
3EA
  8
0
 10
2.5087256305691308
 20
3.392964828296527
 30
0.0
 40
3.0
  1
myText
  7
NOTES
  3
InputText
  2
TESTTAG
 70
     0
1001
ACADANNOTATIVE
1000
AnnotativeData
1002
{
1070
     1
1070
     1
1002
}
1001
ACADANNOPO
1070
     1
1001
AcDbAttr
1070
     0
1070
     1
  0
ENDBLK
  5
17
 67
     1
  8
0
  0
ENDSEC
"""

BLOCKS_WITH_ATTRIB_DXF13 = """  0
SECTION
  2
BLOCKS
  0
BLOCK
  5
3D7
330
3D6
100
AcDbEntity
  8
0
100
AcDbBlockBegin
  2
TESTBLOCK
 70
     2
 10
0.0
 20
0.0
 30
0.0
  3
TESTBLOCK
  1

  0
LWPOLYLINE
  5
3E9
330
3D6
100
AcDbEntity
  8
0
100
AcDbPolyline
 90
        4
 70
     1
 43
0.0
 10
0.0
 20
35.8474120696435
 10
53.27352706737253
 20
35.8474120696435
 10
53.27352706737253
 20
0.0
 10
0.0
 20
0.0
  0
ATTDEF
  5
3EA
102
{ACAD_XDICTIONARY
360
3EB
102
}
330
3D6
100
AcDbEntity
  8
0
100
AcDbText
 10
2.508725630569131
 20
3.392964828296527
 30
0.0
 40
3.0
  1
myText
  7
Notes
100
AcDbAttributeDefinition
  3
InputText
  2
TESTTAG
 70
     0
1001
AcadAnnotative
1000
AnnotativeData
1002
{
1070
     1
1070
     1
1002
}
1001
AcadAnnoPO
1070
     1
1001
AcDbAttr
1070
     0
1070
     1
  0
ENDBLK
  5
3D8
330
3D6
100
AcDbEntity
  8
0
100
AcDbBlockEnd
  0
ENDSEC
"""
