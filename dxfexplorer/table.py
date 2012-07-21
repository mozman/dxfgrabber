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

class Table(object):
    def __init__(self, tags, drawing):
        self._dxfname = tags[1].value
        self._drawing = drawing
        self._table_entries = list()
        self._table_header = None
        self._build_table_entries(tags)

    # start public interface

    def get(self, name):
        return self.get_entry(name)

    def __contains__(self, name):
        return self.entry_exists(name)

    def __len__(self):
        return len(self._table_entries)

    def __iter__(self):
        for handle in self._table_entries:
            yield self.get_table_entry_wrapper(handle)

    # end public interface

    @property
    def name(self):
        return tablename(self._dxfname)

    def _build_table_entries(self, tags):
        groups = TagGroups(tags)
        assert groups.getname(0) == 'TABLE'
        assert groups.getname(-1) == 'ENDTAB'

        self._table_header = ClassifiedTags(groups[0][1:])
        for entrytags in groups[1:-1]:
            self._add_entry(ClassifiedTags(entrytags))

    @property
    def entitydb(self):
        return self._drawing.entitydb

    @property
    def handles(self):
        return self.entitydb.handles

    @property
    def dxffactory(self):
        return self._drawing.dxffactory

    def _iter_table_entries_as_tags(self):
        """ Iterate over table-entries as Tags(). """
        return ( self.entitydb[handle] for handle in self._table_entries )

    def entry_exists(self, name):
        """ Check if an table-entry 'name' exists. """
        try:
            entry = self.get_entry(name)
            return True
        except ValueError:
            return False

    def new_entry(self, dxfattribs):
        """ Create new table-entry of type 'self._dxfname', and add new entry
        to table.

        Does not check if an entry dxfattribs['name'] already exists!
        Duplicate entries are possible for Viewports.
        """
        handle = self.handles.next()
        entry = self.dxffactory.new_entity(self._dxfname, handle, dxfattribs)
        self._add_entry(entry)
        return entry

    def _add_entry(self, entry):
        """ Add table-entry to table and entitydb. """
        if hasattr(entry, 'gethandle'):
            try:
                handle = entry.gethandle()
            except ValueError:
                handle = self.handles.next()
            tags = entry
        else:
            handle = entry.dxf.handle
            tags = entry.tags
        self.entitydb[handle] = tags
        self._table_entries.append(handle)

    def get_entry(self, name):
        """ Get table-entry by name as WrapperClass(). """
        for entry in iter(self):
            if entry.dxf.name == name:
                return entry
        raise ValueError(name)

    def get_table_entry_wrapper(self, handle):
        tags = self.entitydb[handle]
        return self.dxffactory.wrap_entity(tags)
