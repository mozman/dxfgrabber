#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .tags import TagGroups, TAG_STRING_FORMAT

class HeaderSection(object):
    name = 'header'
    def __init__(self, tags):
        self.hdrvars = dict()
        self._build(tags)

    def __contains__(self, key):
        return key in self.hdrvars

    def _build(self, tags):
        assert tags[0] == (0, 'SECTION')
        assert tags[1] == (2, 'HEADER')
        assert tags[-1] == (0, 'ENDSEC')
        groups = TagGroups(tags[2:-1], splitcode=9)
        for group in groups:
            name = group[0].value
            if len(group) > 2:
                value = tuple(group[1:])
            else:
                value = group[1]
            self.hdrvars[name] = HeaderVar(value)

    def __getitem__(self, key):
        var = self.hdrvars[key]
        if var.ispoint:
            return var.getpoint()
        else:
            return var.value

    def get(self, key, default=None):
        if key in self.hdrvars:
            return self.__getitem__(key)
        else:
            return default

class HeaderVar:
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

    def getpoint(self):
        if self.ispoint:
            return tuple( [tag[1] for tag in self.tag] )
        else:
            raise ValueError

    def __str__(self):
        if self.ispoint:
            return "".join([TAG_STRING_FORMAT % tag for tag in self.tag])
        else:
            return TAG_STRING_FORMAT % self.tag
