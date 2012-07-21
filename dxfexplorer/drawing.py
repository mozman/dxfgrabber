#!/usr/bin/env python
#coding:utf-8
# Purpose: Manage drawing data of DXF files
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .tags import TagIterator
from .sections import Sections

class Drawing(object):
    def __init__(self, stream):
        tagreader = TagIterator(stream)
        self.dxfversion = 'AC1009'
        self.encoding = 'cp1252'
        self.filename = None

        sections = Sections(tagreader, self)
        self.header = sections.tables.header
        self.layers = sections.tables.layers
        self.entities = sections.entities

