#!/usr/bin/env python
#coding:utf-8
# Purpose: entity section
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from itertools import islice

from .tags import TagGroups
from .classifiedtags import ClassifiedTags
from .shapes import shape_factory

class EntitySpace(list):
    """
    An EntitySpace is a collection of drawing entities.
    """
    def add(self, entity):
        self.append(entity)

class EntitySection(object):
    name = 'entities'
    def __init__(self, tags, drawing):
        self._entityspace = EntitySpace()
        dxfversion = drawing.dxfversion
        self._build_first_pass(tags, dxfversion)
        self._build_second_pass()

    def get_entityspace(self):
        return self._entityspace

    # start of public interface

    def __len__(self):
        return len(self._entityspace)

    def __iter__(self):
        return iter(self._entityspace)

    def __getitem__(self, index):
        if isinstance(index, int):
            raise ValueError('Integer index required')
        return self._entityspace[index]

    # end of public interface

    def _build_first_pass(self, tags, dxfversion):
        assert tags[0] == (0, 'SECTION')
        assert tags[1] == (2, self.name.upper())
        assert tags[-1] == (0, 'ENDSEC')

        if len(tags) == 3: # empty entities section
            return

        for group in TagGroups(islice(tags, 2, len(tags)-1)):
            try:
                entity = shape_factory(ClassifiedTags(group), dxfversion)
                self._entityspace.add(entity)
            except KeyError:
                pass # ignore unsupported entity types

    def _build_second_pass(self):
        collector = None
        new_entity_space = EntitySpace()
        for entity in self._entityspace:
            if collector:
                if entity.dxftype == 'SEQEND':
                    collector.stop()
                    new_entity_space.add(collector.entity)
                    collector = False
                else:
                    collector.add(entity)
            elif entity.dxftype == 'POLYLINE':
                collector = Collector(entity)
            elif entity.dxftype == 'INSERT' and entity.attribsfollow:
                collector = Collector(entity)
            else:
                new_entity_space.add(entity)
        self._entityspace = new_entity_space

class Collector:
    def __init__(self, entity):
        self.entity = entity
        self._data = list()

    def add(self, entity):
        self._data.append(entity)

    def stop(self):
        self.entity.append_data(self._data)
        if hasattr(self.entity, 'cast'):
            self.entity = self.entity.cast()
