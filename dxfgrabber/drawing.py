#!/usr/bin/env python
#coding:utf-8
# Purpose: Manage drawing data of DXF files
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .tags import TagIterator
from .sections import Sections

DEFAULT_OPTIONS = {
    "grab_blocks": True
}

class Drawing(object):
    def __init__(self, stream, options=None):
        tagreader = TagIterator(stream)
        self.dxfversion = 'AC1009'
        self.encoding = 'cp1252'
        self.filename = None
        if options is None:
            options = DEFAULT_OPTIONS
        self.grab_blocks = options.get('grab_blocks', True)

        sections = Sections(tagreader, self)
        self.header = sections.header
        self.layers = sections.tables.layers
        self.entities = sections.entities
        self.blocks = sections.blocks

