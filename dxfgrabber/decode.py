# Purpose: decode DXF proprietary data
# Created: 01.05.2014
# Copyright (C) 2014, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"


def decode(textlines):
    def _decode(text):
        s = ""
        skip = False
        for c in bytes(text, 'ascii'):
            if skip:
                skip = False
                continue
            if c == 0x20:
                s += ' '
            elif c == 0x40:
                s += '_'
            elif c == 0x5F:
                s += '@'
            elif 0x41 <= c <= 0x5E:
                s += chr(0x41 + (0x5E - c))
                if c == 0x5E:
                    skip = True
            else:
                s += chr(c ^ 0x5F)
        return s
    return [_decode(line) for line in textlines]