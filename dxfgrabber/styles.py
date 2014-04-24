# Purpose: handle text styles
# Created: 06.01.2014
# Copyright (C) 2014, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .dxfentity import DXFEntity
from .layers import Table
from .dxfattr import DXFAttr, DXFAttributes, DefSubclass


class Style(object):
    def __init__(self, wrapper):
        self.name = wrapper.dxf.name
        self.height = wrapper.dxf.height
        self.width = wrapper.dxf.width
        self.oblique = wrapper.dxf.oblique
        self.backward = bool(wrapper.dxf.generation_flags and 2)
        self.mirror_y = bool(wrapper.dxf.generation_flags and 4)
        self.font = wrapper.dxf.font
        self.bigfont = wrapper.dxf.get('bigfont', "")


class StyleTable(Table):
    name = 'styles'

    @staticmethod
    def from_tags(tags, drawing):
        dxfversion = drawing.dxfversion
        styles = StyleTable()
        for entrytags in styles._classified_tags(tags):
            dxfstyle = styles.wrap(entrytags, dxfversion)
            styles._table_entries[dxfstyle.dxf.name] = Style(dxfstyle)
        return styles
    
    @staticmethod
    def wrap(tags, dxfversion):
        return DXF12Style(tags) if dxfversion == "AC1009" else DXF13Style(tags)


class DXF12Style(DXFEntity):
    DXFATTRIBS = DXFAttributes(DefSubclass(None, {
        'handle': DXFAttr(5, None),
        'name': DXFAttr(2, None),
        'flags': DXFAttr(70, None),
        'height': DXFAttr(40, None),  # fixed height, 0 if not fixed
        'width': DXFAttr(41, None),  # width factor
        'oblique': DXFAttr(50, None),  # oblique angle in degree, 0 = vertical
        'generation_flags': DXFAttr(71, None),  # 2 = backward, 4 = mirrored in Y
        'last_height': DXFAttr(42, None),  # last height used
        'font': DXFAttr(3, None),  # primary font file name
        'bigfont': DXFAttr(4, None),  # big font name, blank if none
    }))

none_subclass = DefSubclass(None, {'handle': DXFAttr(5, None)} )
symbol_subclass = DefSubclass('AcDbSymbolTableRecord', {})
style_subclass = DefSubclass('AcDbTextStyleTableRecord', {
    'name': DXFAttr(2, None),
    'flags': DXFAttr(70, None),
    'height': DXFAttr(40, None),  # fixed height, 0 if not fixed
    'width': DXFAttr(41, None),  # width factor
    'oblique': DXFAttr(50, None),  # oblique angle in degree, 0 = vertical
    'generation_flags': DXFAttr(71, None),  # 2 = backward, 4 = mirrored in Y
    'last_height': DXFAttr(42, None),  # last height used
    'font': DXFAttr(3, None),  # primary font file name
    'bigfont': DXFAttr(4, None),  # big font name, blank if none
})


class DXF13Style(DXF12Style):
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, style_subclass)
