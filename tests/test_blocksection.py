#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test blocks section
# Created: 08.08.2012
# Copyright (C) 2012, Manfred Moitzi
# License: GPLv3
from __future__ import unicode_literals

import unittest

from dxfgrabber.tags import Tags
from dxfgrabber.blockssection import BlocksSection

class DrawingProxy:
    def __init__(self, version):
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
