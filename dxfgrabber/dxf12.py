#!/usr/bin/env python
#coding:utf-8
# Purpose: DXF12 tag wrapper
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"


from .dxfattr import DXFAttr, DXFAttributes, DefSubclass
from .genericwrapper import GenericWrapper
from . import const


def make_attribs(additional=None):
    dxfattribs = {
        'handle': DXFAttr(5, None),
        'layer': DXFAttr(8, None), # layername as string, default is '0'
        'linetype': DXFAttr(6, None), # linetype as string, special names BYLAYER/BYBLOCK, default is BYLAYER
        'color': DXFAttr(62, None), # dxf color index, 0 .. BYBLOCK, 256 .. BYLAYER, default is 256
        'paperspace': DXFAttr(67, None), # 0 .. modelspace, 1 .. paperspace, default is 0
    }
    if additional:
        dxfattribs.update(additional)
    return DXFAttributes(DefSubclass(None, dxfattribs))


class Line(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'start': DXFAttr(10, 'Point2D/3D'),
        'end': DXFAttr(11, 'Point2D/3D'),
    })


class Point(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'point': DXFAttr(10, 'Point2D/3D'),
    })


class Circle(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'center': DXFAttr(10, 'Point2D/3D'),
        'radius': DXFAttr(40, None),
    })


class Arc(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'center': DXFAttr(10, 'Point2D/3D'),
        'radius': DXFAttr(40, None),
        'startangle': DXFAttr(50, None),
        'endangle': DXFAttr(51, None),
    })


class Trace(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'vtx0' : DXFAttr(10, 'Point2D/3D'),
        'vtx1' : DXFAttr(11, 'Point2D/3D'),
        'vtx2' : DXFAttr(12, 'Point2D/3D'),
        'vtx3' : DXFAttr(13, 'Point2D/3D'),
    })


Solid = Trace


class Face(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'vtx0' : DXFAttr(10, 'Point2D/3D'),
        'vtx1' : DXFAttr(11, 'Point2D/3D'),
        'vtx2' : DXFAttr(12, 'Point2D/3D'),
        'vtx3' : DXFAttr(13, 'Point2D/3D'),
        'invisible_edge': DXFAttr(70, None),
    })


class Text(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'insert': DXFAttr(10, 'Point2D/3D'),
        'height': DXFAttr(40,  None),
        'text': DXFAttr(1,  None),
        'rotation': DXFAttr(50, None), # in degrees (circle = 360deg)
        'oblique': DXFAttr(51, None), # in degrees, vertical = 0deg
        'style': DXFAttr(7, None), # text style
        'width': DXFAttr(41, None), # width FACTOR!
        'textgenerationflag': DXFAttr(71, None), # 2 = backward (mirr-x), 4 = upside down (mirr-y)
        'halign': DXFAttr(72, None), # horizontal justification
        'valign': DXFAttr(73,  None), # vertical justification
        'alignpoint': DXFAttr(11, 'Point2D/3D'),
    })


class Insert(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'attribsfollow': DXFAttr(66, None),
        'name': DXFAttr(2, None),
        'insert': DXFAttr(10, 'Point2D/3D'),
        'xscale': DXFAttr(41, None),
        'yscale': DXFAttr(42, None),
        'zscale': DXFAttr(43, None),
        'rotation': DXFAttr(50, None),
        'colcount': DXFAttr(70, None),
        'rowcount': DXFAttr(71, None),
        'colspacing': DXFAttr(44, None),
        'rowspacing': DXFAttr(45, None),
    })


class SeqEnd(GenericWrapper):
    DXFATTRIBS = DXFAttributes(DefSubclass(None, { 'handle': DXFAttr(5, None),
                   'paperspace': DXFAttr(67, None),}))


class Attrib(GenericWrapper): # also ATTDEF
    DXFATTRIBS = make_attribs({
        'insert': DXFAttr(10, 'Point2D/3D'),
        'height': DXFAttr(40, None),
        'text': DXFAttr(1, None),
        'prompt': DXFAttr(3, None), # just in ATTDEF not ATTRIB
        'tag': DXFAttr(2, None),
        'flags': DXFAttr(70, None),
        'fieldlength': DXFAttr(73, None),
        'rotation': DXFAttr(50, None),
        'oblique': DXFAttr(51, None),
        'width': DXFAttr(41, None), # width factor
        'style': DXFAttr(7, None),
        'textgenerationflag': DXFAttr(71, None), # 2 = backward (mirr-x), 4 = upside down (mirr-y)
        'halign': DXFAttr(72, None), # horizontal justification
        'valign': DXFAttr(74, None), # vertical justification
        'alignpoint': DXFAttr(11, 'Point2D/3D'),
    })

class Polyline(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'elevation': DXFAttr(10, 'Point2D/3D'),
        'flags': DXFAttr(70, None),
        'defaultstartwidth': DXFAttr(40, None),
        'defaultendwidth': DXFAttr(41, None),
        'mcount': DXFAttr(71, None),
        'ncount': DXFAttr(72, None),
        'msmoothdensity': DXFAttr(73, None),
        'nsmoothdensity': DXFAttr(74, None),
        'smoothtype': DXFAttr(75, None),
    })

    def get_vertex_flags(self):
        return const.VERTEX_FLAGS[self.get_mode()]

    @property
    def flags(self):
        return self.dxf.get('flags', 0)

    def get_mode(self):
        flags = self.flags
        if flags & const.POLYLINE_3D_POLYLINE > 0:
            return 'polyline3d'
        elif flags & const.POLYLINE_3D_POLYMESH > 0:
            return 'polymesh'
        elif flags & const.POLYLINE_POLYFACE > 0:
            return 'polyface'
        else:
            return 'polyline2d'

    def is_mclosed(self):
        return bool(self.flags & const.POLYLINE_MESH_CLOSED_M_DIRECTION)

    def is_nclosed(self):
        return bool(self.flags & const.POLYLINE_MESH_CLOSED_N_DIRECTION)


class Vertex(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'location': DXFAttr(10, 'Point2D/3D'),
        'startwidth': DXFAttr(40, None),
        'endwidth': DXFAttr(41, None),
        'bulge': DXFAttr(42, None),
        'flags': DXFAttr(70, None),
        'tangent': DXFAttr(50, None),
        'vtx0': DXFAttr(71, None),
        'vtx1': DXFAttr(72, None),
        'vtx2': DXFAttr(73, None),
        'vtx3': DXFAttr(74, None),
    })

class Block(GenericWrapper):
    DXFATTRIBS = make_attribs({
        'name': DXFAttr(2, None),
        'name2': DXFAttr(3, None),
        'flags': DXFAttr(70, None),
        'basepoint': DXFAttr(10, 'Point2D/3D'),
        'xrefpath': DXFAttr(1, None),
        })

class EndBlk(SeqEnd):
    DXFATTRIBS = DXFAttributes(DefSubclass(None, { 'handle': DXFAttr(5, None) }))
