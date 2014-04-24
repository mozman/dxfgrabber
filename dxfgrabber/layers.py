# Purpose: handle layers
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .tags import TagGroups
from .classifiedtags import ClassifiedTags
from .dxfentity import DXFEntity

from .dxfattr import DXFAttr, DXFAttributes, DefSubclass


class Layer(object):
    def __init__(self, wrapper):
        self.name = wrapper.dxf.name
        self.color = wrapper.get_color()
        self.linetype = wrapper.dxf.linetype
        self.locked = wrapper.is_locked()
        self.frozen = wrapper.is_frozen()
        self.on = wrapper.is_on()


class Table(object):

    def __init__(self):
        self._table_entries = dict()

    # start public interface

    def get(self, name):
        return self._table_entries[name]

    def __getitem__(self, item):
        return self.get(item)

    def __contains__(self, name):
        return name in self._table_entries

    def __iter__(self):
        return iter(self._table_entries.values())

    def __len__(self):
        return len(self._table_entries)

    def names(self):
        return sorted(self._table_entries.keys())

    # end public interface

    def _classified_tags(self, tags):
        groups = TagGroups(tags)
        assert groups.getname(0) == 'TABLE'
        assert groups.getname(-1) == 'ENDTAB'
        for entrytags in groups[1:-1]:
            yield ClassifiedTags(entrytags)


class LayerTable(Table):
    name = 'layers'

    @staticmethod
    def from_tags(tags, drawing):
        dxfversion = drawing.dxfversion
        layers = LayerTable()
        for entrytags in layers._classified_tags(tags):
            dxflayer = layers.wrap(entrytags, dxfversion)
            layers._table_entries[dxflayer.dxf.name] = Layer(dxflayer)
        return layers

    @staticmethod
    def wrap(tags, dxfversion):
        return DXF12Layer(tags) if dxfversion == "AC1009" else DXF13Layer(tags)


class DXF12Layer(DXFEntity):
    DXFATTRIBS = DXFAttributes(DefSubclass(None, {
        'handle': DXFAttr(5, None),
        'name': DXFAttr(2, None),
        'flags': DXFAttr(70, None),
        'color': DXFAttr(62,  None), # dxf color index, if < 0 layer is off
        'linetype': DXFAttr(6, None),
        }))
    LOCK = 0b00000100
    FROZEN = 0b00000001

    def is_frozen(self):
        return self.dxf.flags & DXF12Layer.FROZEN > 0

    def is_locked(self):
        return self.dxf.flags & DXF12Layer.LOCK > 0

    def is_off(self):
        return self.dxf.color < 0

    def is_on(self):
        return not self.is_off()

    def get_color(self):
        return abs(self.dxf.color)

none_subclass = DefSubclass(None, {'handle': DXFAttr(5, None)} )
symbol_subclass = DefSubclass('AcDbSymbolTableRecord', {})
layer_subclass = DefSubclass('AcDbLayerTableRecord', {
    'name': DXFAttr(2, None), # layer name
    'flags': DXFAttr(70, None),
    'color': DXFAttr(62, None), # dxf color index
    'linetype': DXFAttr(6, None), # linetype name
})


class DXF13Layer(DXF12Layer):
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, layer_subclass)
