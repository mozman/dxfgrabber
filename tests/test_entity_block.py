#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfgrabber.classifiedtags import ClassifiedTags
from dxfgrabber.entities import entity_factory

class TestBlockDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(BLOCK_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_block_properties(self):
        block = self.entity
        self.assertEqual(block.dxftype, 'BLOCK')
        self.assertEqual(block.color, 256)
        self.assertEqual(block.layer, '0')
        self.assertEqual(block.linetype, None)
        self.assertFalse(block.paperspace)

    def test_block_data(self):
        block = self.entity
        self.assertEqual(block.basepoint, (10.0, 20.0, 30.0))
        self.assertEqual(block.name, "$MODEL_SPACE")
        self.assertEqual(block.flags, 0)
        self.assertEqual(block.xrefpath, "/x/ref.dxf")

class TestBlockEndDXF12(unittest.TestCase):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ENDBLK_DXF12)
        self.entity = entity_factory(tags, 'AC1009')

    def test_existence(self):
        self.assertEqual(self.entity.dxftype, 'ENDBLK')

class TestBlockDXF13(TestBlockDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(BLOCK_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

class TestBlockEndDXF13(TestBlockEndDXF12):
    def setUp(self):
        tags = ClassifiedTags.fromtext(ENDBLK_DXF13)
        self.entity = entity_factory(tags, 'AC1024')

BLOCK_DXF12 = """  0
BLOCK
  8
0
  2
$MODEL_SPACE
 70
     0
 10
10.0
 20
20.0
 30
30.0
  3
$MODEL_SPACE
  1
/x/ref.dxf
"""

BLOCK_DXF13 = """  0
BLOCK
  5
6
330
2
100
AcDbEntity
  8
0
100
AcDbBlockBegin
  2
$MODEL_SPACE
 70
     0
 10
10.0
 20
20.0
 30
30.0
  3
$MODEL_SPACE
  1
/x/ref.dxf
"""

ENDBLK_DXF12 = """  0
ENDBLK
  5
D
  8
0
"""

ENDBLK_DXF13 = """  0
ENDBLK
  5
D
330
2
100
AcDbEntity
  8
0
100
AcDbBlockEnd
"""
