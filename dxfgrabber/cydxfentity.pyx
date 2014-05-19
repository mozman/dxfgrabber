# cython: profile=True
# Purpose: generic tag wrapper
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .const import XTYPE_NONE, XTYPE_2D, XTYPE_3D, XTYPE_2D_3D

cdef enum:
    _XT_NONE = 0
    _XT_2D = 1
    _XT_3D = 2
    _XT_2D_3D = 3

assert _XT_NONE == XTYPE_NONE
assert _XT_2D == XTYPE_2D
assert _XT_3D == XTYPE_3D
assert _XT_2D_3D == XTYPE_2D_3D


class cyDXFEntity:
    DXFATTRIBS = {}

    def __init__(self, tags):
        self.tags = tags

    def dxftype(self):
        return self.tags.noclass[0].value

    def get_dxf_attrib(self, key, default=ValueError):
        # core function - every optimization is useful
        try:
            dxfattr = self.DXFATTRIBS[key]
        except KeyError:
            # attribute is not defined - returning the default value is useful
            # to query newer DXF attributes on older DXF files.
            # !! Problem: misspelled attributes with default values do not
            # raise an Exception !!
            if default is ValueError:
                raise ValueError("DXFAttrib '%s' is not defined." % key)
            else:
                return default
        try:
            return self._get_dxf_attrib(dxfattr)
        except ValueError:  # attribute is defined but no value is present
            if default is ValueError:
                raise ValueError("DXFAttrib '%s': value is not present." % key)
            else:
                return default

    def _get_dxf_attrib(self, dxfattr):
        # no subclass is subclass index 0
        subclass_tags = self.tags.subclasses[dxfattr.subclass]
        cdef int xtype = <int> dxfattr.xtype
        if xtype != _XT_NONE and xtype != _XT_2D_3D:
            return self._get_extented_type(subclass_tags, <int> dxfattr.code, xtype)
        else:
            return subclass_tags.get_value(<int> dxfattr.code)

    def paperspace(self):
        return self.get_dxf_attrib('paperspace', default=0) == 1

    def post_read_correction(self):
        pass

    @staticmethod
    def _get_extented_type(tags, int code, int xtype):
        value = tags.get_value(code)
        if <int> len(value) == 2:
            if xtype == _XT_3D:
                return value[0], value[1], 0.
        elif xtype == _XT_2D:
            return value[0], value[1]
        return value

