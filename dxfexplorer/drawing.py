#!/usr/bin/env python
#coding:utf-8
# Purpose: Manage drawing data of DXF files
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .tags import TagIterator
from .codepage import toencoding
from .sections import Sections

class Drawing(object):
    def __init__(self, stream):
        tagreader = TagIterator(stream)
        self.dxfversion = 'AC1009'
        self.encoding = 'cp1252'
        self.filename = None
        self.emtitydb = ""
        self.sections = Sections(tagreader, self)


    def _bootstraphook(self, header):
        # called from HeaderSection() object to update important dxf properties
        # before processing sections, which depends on this properties.
        self.dxfversion = header['$ACADVER']
        codepage = header.get('$DWGCODEPAGE', 'ANSI_1252')
        self.encoding = toencoding(codepage)

    @property
    def header(self):
        return self.sections.header

    @property
    def layers(self):
        return self.sections.tables.layers

    @property
    def blocks(self):
        return self.sections.blocks

    @property
    def entities(self):
        return self.sections.entities

