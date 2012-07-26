#!/usr/bin/env python
#coding:utf-8
# Purpose: entity module
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .tags import DXFStructureError

class DXFNamespace(object):
    """ Provides the dxf namespace for GenericWrapper.

    """
    __slots__ = ('wrapper', )
    def __init__(self, wrapper):
        self.wrapper = wrapper

    def get(self, key, default=ValueError):
        """
        GenericWrapper.dxf.get('DXF_ATTRIBUTE_NAME') - raises ValueError, if not exists
        GenericWrapper.dxf.get('DXF_ATTRIBUTE_NAME', defaultvalue)

        """
        return self.wrapper.get_dxf_attrib(key, default)

    def __getattr__(self, key):
        """ GenericWrapper.dxf.DXF_ATTRIBUTE_NAME """
        return self.wrapper.get_dxf_attrib(key)

class GenericWrapper:
    DXFATTRIBS = {}

    def __init__(self, tags):
        self.tags = tags
        self.dxf = DXFNamespace(self)

    def dxftype(self):
        return self.tags.noclass[0].value

    def get_dxf_attrib(self, key, default=ValueError):
        def get_default(msg):
            if default is ValueError:
                raise ValueError(msg)
            else:
                return default
        try:
            dxfattr = self.DXFATTRIBS[key]
        except KeyError:
            # attribute is not defined - returning the default value is useful
            # to query newer DXF attributes on older DXF files.
            # !! Problem: misspelled attributes with default values do not
            # raise an Exception !!
            return get_default("DXFAttrib '%s' is not defined." % key)

        try:
            return self._get_dxf_attrib(dxfattr)
        except ValueError: # attribute is defined but no value is present
            return get_default("DXFAttrib '%s': value is not present." % key)

    def _get_dxf_attrib(self, dxfattr):
        # no subclass is subclass index 0
        subclasstags = self.tags.subclasses[dxfattr.subclass]
        if dxfattr.xtype is not None:
            tags = ExtendedType(subclasstags)
            return tags.get_value(dxfattr.code, dxfattr.xtype)
        else:
            return subclasstags.getvalue(dxfattr.code)

    def _get_extended_type(self, code, xtype):
        tags = ExtendedType(self.tags)
        return tags.get_value(code, xtype)

    def paperspace(self):
        return self.dxf.get('paperspace', 0) == 1

class ExtendedType:
    def __init__(self, tags):
        self.tags = tags

    def get_value(self, code, xtype):
        if xtype == 'Point2D':
            return self._get_fix_point(code, axis=2)
        elif xtype == 'Point3D':
            return self._get_fix_point(code, axis=3)
        elif xtype == 'Point2D/3D':
            return self._get_flexible_point(code)
        else:
            raise TypeError('Unknown extended type: %s' % xtype)

    def _get_fix_point(self, code, axis):
        point = self._get_point(code)
        if len(point) != axis:
            raise DXFStructureError('Invalid axis count for code: %d' % code)
        return point

    def _get_point(self, code):
        index = self._point_index(code)
        return tuple(
            ( tag.value for x, tag in enumerate(self.tags[index:index+3])
              if tag.code == code + x*10 )
        )

    def _point_index(self, code):
        return self.tags.tagindex(code)

    def _get_flexible_point(self, code):
        point = self._get_point(code)
        if len(point) in (2, 3):
            return point
        else:
            raise DXFStructureError('Invalid axis count for code: %d' % code)
