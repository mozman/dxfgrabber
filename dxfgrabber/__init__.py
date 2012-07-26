#!/usr/bin/env python
#coding:utf-8
# dxfgrabber - copyright (C) 2012 by Manfred Moitzi (mozman)
# Purpose: read and explore DXF drawings - all DXF versions supported
# Created: 21.07.2012
# License: MIT License

version = (0, 1, 0)
VERSION = "%d.%d.%d"  % version

__author__ = "mozman <mozman@gmx.at>"
__doc__ = """A Python library to read and explore DXF drawings - all DXF versions supported."""

import io

# Python2/3 support should be done here
import sys
if sys.version_info[0] == 3:
    # for Python 3
    tostr = str
else:
    # for Python 2
    tostr = unicode
# end of Python2/3 support

from .tags import dxfinfo

def read(stream):
    from .drawing import Drawing
    return Drawing(stream)

def readfile(filename):
    def get_encoding():
        with open(filename) as fp:
            info = dxfinfo(fp)
        return info.encoding

    from .drawing import Drawing
    with io.open(filename, encoding=get_encoding()) as fp:
        dwg = Drawing(fp)
    dwg.filename = filename
    return dwg
