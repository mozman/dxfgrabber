#!/usr/bin/env python
#coding:utf-8
# Purpose: tables section
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .defaultchunk import iterchunks, DefaultChunk
from .layers import LayerTable

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

class TablesSection(object):
    name = 'tables'
    def __init__(self, tags, drawing):
        self._drawing = drawing
        self._tables = dict()
        self._setup_tables(tags)

    def _setup_tables(self, tags):
        def name(table):
            return table[1].value

        def skiptags(tags, count):
            for i in range(count):
                next(tags)
            return tags

        itertags = skiptags(iter(tags), 2) # (0, 'SECTION'), (2, 'TABLES')
        for table in iterchunks(itertags, stoptag='ENDSEC', endofchunk='ENDTAB'):
            table_class = table_factory(name(table))
            new_table = table_class(table, self._drawing)
            self._tables[new_table.name] = new_table

    def __getattr__(self, key):
        try:
            return self._tables[key]
        except KeyError:
            raise AttributeError(key)

# support for further tables types are possible
TABLESMAP = {
    'LAYER': LayerTable,
}

def table_factory(name):
    return TABLESMAP.get(name, GenericTable)
