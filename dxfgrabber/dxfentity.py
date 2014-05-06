# Purpose: generic tag wrapper
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"


class DXFNamespace(object):
    """ Provides the dxf namespace for DXFEntity.
    """
    def __init__(self, wrapper):
        self.wrapper = wrapper

    def get(self, key, default=ValueError):
        """
        DXFEntity.dxf.get('DXF_ATTRIBUTE_NAME') - raises ValueError, if not exists
        DXFEntity.dxf.get('DXF_ATTRIBUTE_NAME', defaultvalue)

        """
        return self.wrapper.get_dxf_attrib(key, default)

    def __getattr__(self, key):
        """ DXFEntity.dxf.DXF_ATTRIBUTE_NAME """
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
            return subclass_tags.get_value(dxfattr.code)

    def paperspace(self):
        return self.get_dxf_attrib('paperspace', default=0) == 1

    def post_read_correction(self):
        pass

    @staticmethod
    def _get_extented_type(tags, code, xtype):
        index = tags.tag_index(code)
        value = tags[index].value
        length = len(value)
        if length == 2:
            if xtype == 'Point3D':
                return value[0], value[1], 0.
        elif xtype == 'Point2D':
            return value[0], value[1]
        return value

