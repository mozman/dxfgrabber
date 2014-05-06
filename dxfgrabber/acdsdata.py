# Purpose: acdsdata section manager
# Created: 05.05.2014
# Copyright (C) 2014, Manfred Moitzi
# License: MIT License

from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from itertools import islice
from .tags import TagGroups, DXFStructureError, Tags, binary_encoded_data_to_bytes


class AcDsDataSection(object):
    name = 'acdsdata'

    def __init__(self):
        self.entities = []  # stores AcDsData objects
        # Standard_ACIS_Binary (SAB) data store, key = handle of DXF Entity in the ENTITIES section: BODY, 3DSOLID
        # SURFACE, PLANESURFACE, REGION
        self.sab_data = {}

    @classmethod
    def from_tags(cls, tags, drawing):
        data_section = cls()
        data_section._build(tags, drawing.dxfversion)
        return data_section

    def __iter__(self):
        return iter(self.entities)

    def _build(self, tags, dxfversion):
        if tags[0] != (0, 'SECTION') or tags[1] != (2, self.name.upper()) or tags[-1] != (0, 'ENDSEC'):
            raise DXFStructureError("Critical structure error in {} section.".format(self.name.upper()))

        if len(tags) == 3:  # empty entities section
            return

        start_index = 2
        while tags[start_index].code != 0:
            start_index += 1

        for group in TagGroups(islice(tags, start_index, len(tags)-1)):
            data_record = AcDsDataRecord(Tags(group))
            self.entities.append(data_record)  # tags have no subclasses
            if data_record.dxftype == 'ACDSRECORD':
                asm_data = data_record.get_section('ASM_Data', None)
                if asm_data is not None:
                    self.add_asm_data(data_record)

    def add_asm_data(self, acdsrecord):
        try:
            asm_data = acdsrecord.get_section('ASM_Data')
            entity_id = acdsrecord.get_section('AcDbDs::ID')
        except ValueError:
            return
        else:
            handle = entity_id[2].value
            binary_data_text = (tag.value for tag in asm_data if tag.code == 310)
            binary_data = binary_encoded_data_to_bytes(binary_data_text)
            self.sab_data[handle] = binary_data


class Section(Tags):
    @property
    def name(self):
        return self[0].value

    @property
    def type(self):
        return self[1].value

    @property
    def data(self):
        return self[2:]


class AcDsDataRecord(object):
    def __init__(self, tags):
        self.dxftype = tags[0].value
        start_index = 2
        while tags[start_index].code != 2:
            start_index += 1
        self.sections = [Section(tags) for tags in TagGroups(islice(tags, start_index, None), split_code=2)]

    def has_section(self, name):
        return self.get_section(name, default=None) is not None

    def get_section(self, name, default=KeyError):
        for section in self.sections:
            if section.name == name:
                return section
        if default is KeyError:
            raise KeyError(name)
        else:
            return default

    def __getitem__(self, name):
        return self.get_section(name)
