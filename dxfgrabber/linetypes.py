# Purpose: handle linetypes table
# Created: 06.01.2014
# Copyright (C) 2014, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .dxfentity import DXFEntity
from .layers import Table
from .dxfattr import DXFAttr, DXFAttributes, DefSubclass


class Linetype(object):
    def __init__(self, wrapper):
        self.name = wrapper.dxf.name
        self.description = wrapper.dxf.description
        self.length = wrapper.dxf.length  # overall length of the pattern
        self.pattern = wrapper.get_pattern()  # list of floats: value>0: line, value<0: gap, value=0: dot


class LinetypeTable(Table):
    name = 'linetypes'

    @staticmethod
    def from_tags(tags, drawing):
        dxfversion = drawing.dxfversion
        styles = LinetypeTable()
        for entrytags in styles._classified_tags(tags):
            dxfstyle = styles.wrap(entrytags, dxfversion)
            styles._table_entries[dxfstyle.dxf.name] = Linetype(dxfstyle)
        return styles
    
    @staticmethod
    def wrap(tags, dxfversion):
        return DXF12Linetype(tags) if dxfversion == "AC1009" else DXF13Linetype(tags)


class DXF12Linetype(DXFEntity):
    DXFATTRIBS = DXFAttributes(DefSubclass(None, {
        'handle': DXFAttr(5, None),
        'name': DXFAttr(2, None),
        'description': DXFAttr(3, None),
        'length': DXFAttr(40, None),
        'items': DXFAttr(73, None),
    }))

    def get_pattern(self):
        items = self.dxf.items
        if items == 0:
            return []
        else:
            tags = self.tags.noclass
            return [pattern_tag.value for pattern_tag in tags.findall(49)]

none_subclass = DefSubclass(None, {'handle': DXFAttr(5, None)} )
symbol_subclass = DefSubclass('AcDbSymbolTableRecord', {})
linetype_subclass = DefSubclass('AcDbLinetypeTableRecord', {
    'name': DXFAttr(2,  None),
    'description': DXFAttr(3, None),
    'length': DXFAttr(40, None),
    'items': DXFAttr(73, None),
})


class DXF13Linetype(DXF12Linetype):
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, linetype_subclass)

    def get_pattern(self):
        items = self.dxf.items
        if items == 0:
            return []
        else:
            tags = self.tags.get_subclass('AcDbLinetypeTableRecord')
            return [pattern_tag.value for pattern_tag in tags.findall(49)]
