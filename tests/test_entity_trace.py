#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 22.07.12
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

import unittest
from dxfexplorer.tags import Tags
from dxfexplorer.entitysection import EntitySection

class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version

class TestTraceDXF12(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(TRACE_DXF12)
        self.entities = EntitySection(tags, DrawingProxy('AC1009'))

class TestTraceDXF13(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(TRACE_DXF13)
        self.entities = EntitySection(tags, DrawingProxy('AC1024'))

TRACE_DXF12 = """  0
SECTION
  2
ENTITIES
  0
ENDSEC
"""

TRACE_DXF13 = """  0
SECTION
  2
ENTITIES
  0
ENDSEC
"""
