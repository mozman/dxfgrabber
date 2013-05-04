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
from .entities import entity_factory

class EntitySection(object):
    name = 'entities'

    def __init__(self, tags, drawing):
        self._entities = list()
        self._build(tags, drawing.dxfversion)

    def get_entities(self):
        return self._entities

    # start of public interface

    def __len__(self):
        return len(self._entities)

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, index):
        return self._entities[index]

    # end of public interface

    def _build(self, tags, dxfversion):
        assert tags[0] == (0, 'SECTION')
        assert tags[1] == (2, self.name.upper())
        assert tags[-1] == (0, 'ENDSEC')

        if len(tags) == 3: # empty entities section
            return
        groups = TagGroups(islice(tags, 2, len(tags)-1))
        self._entities = build_entities(groups, dxfversion)

def build_entities(tag_groups, dxfversion):
    def build_entity(group):
        try:
            entity = entity_factory(ClassifiedTags(group), dxfversion)
        except KeyError:
            entity = None # ignore unsupported entities
        return entity

    entities = list()
    collector = None
    for group in tag_groups:
        entity = build_entity(group)
        if entity is not None:
            if collector:
                if entity.dxftype == 'SEQEND':
                    collector.stop()
                    entities.append(collector.entity)
                    collector = None
                else:
                    collector.append(entity)
            elif entity.dxftype == 'POLYLINE':
                collector = _Collector(entity)
            elif entity.dxftype == 'INSERT' and entity.attribsfollow:
                collector = _Collector(entity)
            else:
                entities.append(entity)
    return entities

class _Collector:
    def __init__(self, entity):
        self.entity = entity
        self._data = list()

    def append(self, entity):
        self._data.append(entity)

    def stop(self):
        self.entity.append_data(self._data)
        if hasattr(self.entity, 'cast'):
            self.entity = self.entity.cast()
