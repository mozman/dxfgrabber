#!/usr/bin/env python
#coding:utf-8
# Purpose: default chunk
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .tags import Tags

class DefaultChunk(object):
    def __init__(self, tags, drawing):
        assert isinstance(tags, Tags)
        self.tags = tags
        self._drawing = drawing

    @property
    def name(self):
        return self.tags[1].value.lower()

def iterchunks(tagreader, stoptag='EOF', endofchunk='ENDSEC'):
    while True:
        tag = next(tagreader)
        if tag == (0, stoptag):
            return
        tags = Tags([tag])
        while tag != (0, endofchunk):
            tag = next(tagreader)
            tags.append(tag)
        yield tags
