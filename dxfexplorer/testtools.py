#!/usr/bin/env python
#coding:utf-8
# Purpose: test tools
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .tags import Tags

class DrawingProxy:
    """ a lightweight drawing proxy for testing
    """
    def __init__(self, version):
        self.dxfversion = version

    def _bootstraphook(self, header):
        pass

def normlines(text):
    lines = text.split('\n')
    return [line.strip() for line in lines]
