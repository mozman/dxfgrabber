#!/usr/bin/env python
#coding:utf-8
# dxfgrabber - copyright (C) 2012 by Manfred Moitzi (mozman)
# Purpose: grab information from DXF drawings - all DXF versions supported
# Created: 21.07.2012
# License: MIT License

version = (0, 4, 0)
VERSION = "%d.%d.%d"  % version

__author__ = "mozman <mozman@gmx.at>"
__doc__ = """A Python library to grab information from DXF drawings - all DXF versions supported."""


# Python27/3x support should be done here
import sys
PYTHON3 = sys.version_info[0] > 2

if PYTHON3:
    tostr = str
else: # PYTHON27
    tostr = unicode
# end of Python 27/3x adaption
# if tostr does not work, look at package 'dxfwrite' for escaping unicode chars

import io
from .tags import dxfinfo

def read(stream, options=None):
    if hasattr(stream, 'readline'):
        from .drawing import Drawing
        return Drawing(stream, options)
    else:
        raise AttributeError('stream object requires a readline() method.')

def readfile(filename, options=None):
    def get_encoding():
        with open(filename) as fp:
            info = dxfinfo(fp)
        return info.encoding

    from .drawing import Drawing
    with io.open(filename, encoding=get_encoding()) as fp:
        dwg = Drawing(fp, options)
    dwg.filename = filename
    return dwg
