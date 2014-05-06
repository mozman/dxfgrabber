# Purpose: handle drawing data of DXF files
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .tags import TagIterator
from .sections import Sections

DEFAULT_OPTIONS = {
    "grab_blocks": True,
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
        self.styles = sections.tables.styles
        self.linetypes = sections.tables.linetypes
        self.blocks = sections.blocks
        self.entities = sections.entities
        self.objects = sections.objects if ('objects' in sections) else []
        if 'acdsdata' in sections:
            self.acdsdata = sections.acdsdata
            # sab data introduced with DXF version AC1027 (R2013)
            if self.dxfversion >= 'AC1027':
                self.collect_sab_data()

    def modelspace(self):
        return (entity for entity in self.entities if not entity.paperspace)

    def paperspace(self):
        return (entity for entity in self.entities if entity.paperspace)

    def collect_sab_data(self):
        for entity in self.entities:
            if hasattr(entity, 'set_sab_data'):
                sab_data = self.acdsdata.sab_data[entity.handle]
                entity.set_sab_data(sab_data)
