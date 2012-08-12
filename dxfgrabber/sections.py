#!/usr/bin/env python
#coding:utf-8
# Purpose: sections module
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .codepage import toencoding
from .defaultchunk import DefaultChunk, iterchunks
from .headersection import HeaderSection
from .tablessection import TablesSection
from .entitysection import EntitySection
from .blockssection import BlocksSection

class Sections(object):
    def __init__(self, tagreader, drawing):
        self._sections = dict()
        self._setup_sections(tagreader, drawing)

    def _setup_sections(self, tagreader, drawing):
        def name(section):
            return section[1].value

        bootstrap = True
        for section in iterchunks(tagreader, stoptag='EOF', endofchunk='ENDSEC'):
            if bootstrap:
                new_section = HeaderSection(section)
                drawing.dxfversion = new_section['$ACADVER']
                codepage = new_section.get('$DWGCODEPAGE', 'ANSI_1252')
                drawing.encoding = toencoding(codepage)
                bootstrap = False
            else:
                section_class = get_section_class(name(section))
                new_section = section_class(section, drawing)
            self._sections[new_section.name] = new_section

    def __getattr__(self, key):
        try:
            return self._sections[key]
        except KeyError:
            raise AttributeError(key)

SECTIONMAP = {
    'TABLES': TablesSection,
    'ENTITIES': EntitySection,
    'BLOCKS': BlocksSection,
}

def get_section_class(name):
    return SECTIONMAP.get(name, DefaultChunk)
