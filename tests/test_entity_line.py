#!/usr/bin/env python
#coding:utf-8
# Purpose: 
# Created: 21.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfexplorer.tags import Tags
from dxfexplorer.entitysection import EntitySection

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version


class TestLines(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(LINES)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

    def test_lines(self):
        self.assertEqual(len(self.entities), 4)

    def test_lines_data(self):
        line = self.entities[0]
        self.assertEqual(line.start, (0., 0., 0.))
        self.assertEqual(line.end, (1., 0., 0.))


LINES = """  0
SECTION
  2
ENTITIES
  0
LINE
  8
0
 10
0.0
 20
0.0
 30
0.0
 11
1.0
 21
0.0
 31
0.0
  0
LINE
  8
0
 10
1.0
 20
0.0
 30
0.0
 11
1.0
 21
1.0
 31
0.0
  0
LINE
  8
0
 10
1.0
 20
1.0
 30
0.0
 11
0.0
 21
1.0
 31
0.0
  0
LINE
  8
0
 10
0.0
 20
1.0
 30
0.0
 11
0.0
 21
0.0
 31
0.0
  0
ENDSEC
"""
