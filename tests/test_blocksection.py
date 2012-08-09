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

class TestBlockSectionDXF12(unittest.TestCase):
    # TODO: write blocks section tests DXF12
    def setUp(self):
        self.tags = Tags(BLOCKS_DXF12)

class TestBlockSectionDXF13(TestBlockSectionDXF12):
    # TODO: write blocks section tests DXF13
    def setUp(self):
        self.tags = Tags(BLOCKS_DXF13)

BLOCKS_DXF12 = """  0
SECTION
  2
BLOCKS
  0
ENDSEC
"""

BLOCKS_DXF13 = """  0
SECTION
  2
BLOCKS
  0
ENDSEC
"""
