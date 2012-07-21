#!/usr/bin/env python
#coding:utf-8
# Purpose: tables contained in tables sections
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .defaultchunk import DefaultChunk
from .tags import TagGroups
from .classifiedtags import ClassifiedTags

TABLENAMES = {
    'layer': 'layers',
    'ltype': 'linetypes',
    'appid': 'appids',
    'dimstyle': 'dimstyles',
    'style': 'styles',
    'ucs': 'ucs',
    'view': 'views',
    'vport': 'viewports',
    'block_record': 'block_records',
}

def tablename(dxfname):
    """ Translate DXF-table-name to attribute-name. ('LAYER' -> 'layers') """
    name = dxfname.lower()
    return TABLENAMES.get(name, name+'s')

class GenericTable(DefaultChunk):
    @property
    def name(self):
        return tablename(self.tags[1].value)

class LayerTable:
    def __init__(self, tags, dxfversion):
        self._dxfversion = dxfversion
        self._layers = dict()
        self._build_table_entries(tags)

    # start public interface

    def get(self, name):
        return self._layers[name]

    def __contains__(self, name):
        return name in self._layers

    # end public interface

    def _build_table_entries(self, tags):
        groups = TagGroups(tags)
        assert groups.getname(0) == 'TABLE'
        assert groups.getname(-1) == 'ENDTAB'

        self._table_header = ClassifiedTags(groups[0][1:])
        for entrytags in groups[1:-1]:
            self._add_entry(ClassifiedTags(entrytags))

    def _add_entry(self, entry):
        """ Add table-entry to table and entitydb. """
        self._layers.append(entry)

    def get_entry(self, name):
        """ Get table-entry by name as WrapperClass(). """
        for entry in iter(self):
            if entry.dxf.name == name:
                return entry
        raise ValueError(name)

    def wrap(self, tags):
        return DXF12Layer(tags) if self._dxfversion == "AC1009" else DXFLayer(tags)
