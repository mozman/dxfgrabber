# Purpose: handle header section
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .tags import TagGroups


class HeaderSection(dict):
    name = "header"

    def __init__(self):
        super(HeaderSection, self).__init__()
        self._create_default_vars()

    @staticmethod
    def from_tags(tags):
        header = HeaderSection()
        if tags[1] == (2, 'HEADER'):  # DXF12 without a HEADER section is valid!
            header._build(tags)
        return header

    def _create_default_vars(self):
        self['$ACADVER'] = 'AC1009'
        self['$DWGCODEPAGE'] = 'ANSI_1252'

    def _build(self, tags):
        assert tags[0] == (0, 'SECTION')
        assert tags[1] == (2, 'HEADER')
        assert tags[-1] == (0, 'ENDSEC')
        if len(tags) == 3:  # empty header section!
            return
        groups = TagGroups(tags[2:-1], splitcode=9)
        for group in groups:
            name = group[0].value
            if len(group) > 2:
                value = tuple(group[1:])
            else:
                value = group[1]
            var = _HeaderVar(value)
            self[name] = var.get_point() if var.ispoint else var.value


class _HeaderVar:
    def __init__(self, tag):
        self.tag = tag

    @property
    def code(self):
        return self.tag[0]

    @property
    def value(self):
        return self.tag[1]

    @property
    def ispoint(self):
        return isinstance(self.tag[0], tuple)

    def get_point(self):
        if self.ispoint:
            return tuple([tag[1] for tag in self.tag])
        else:
            raise ValueError
