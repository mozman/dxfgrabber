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

class TestLWPolyline(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(LWPOLYLINE)
        self.entities = EntitySection(tags, DrawingProxy('AC1024'))

LWPOLYLINE = """  0
SECTION
  2
ENTITIES
  0
ENDSEC
"""
