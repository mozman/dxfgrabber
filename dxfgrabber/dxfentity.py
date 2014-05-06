# Purpose: generic tag wrapper
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


class DXFEntity(object):
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
        except ValueError:  # attribute is defined but no value is present
            return get_default("DXFAttrib '%s': value is not present." % key)

    def _get_dxf_attrib(self, dxfattr):
        # no subclass is subclass index 0
        subclass_tags = self.tags.subclasses[dxfattr.subclass]
        if dxfattr.xtype is not None:
            return self._get_extented_type(subclass_tags, dxfattr.code, dxfattr.xtype)
        else:
            return subclass_tags.getvalue(dxfattr.code)

    def paperspace(self):
        return self.dxf.get('paperspace', 0) == 1

    def post_read_correction(self):
        pass

    @staticmethod
    def _get_extented_type(tags, code, xtype):
        def get_point():
            index = tags.tagindex(code)
            return tags[index].value

        if xtype == 'Point3D':
            value = get_point()
            if len(value) == 2:
                raise DXFStructureError("expected 3D point but found 2D point")
            return value
        elif xtype == 'Point2D':
            value = get_point()
            if len(value) == 3:
                raise DXFStructureError("expected 2D point but found 3D point")
            return value
        elif xtype == 'Point2D/3D':
            return get_point()
        else:
            raise TypeError('Unknown extended type: %s' % xtype)

