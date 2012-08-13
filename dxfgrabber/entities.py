#!/usr/bin/env python
#coding:utf-8
# Purpose:
# Created: 21.07.2012, parts taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from . import dxf12, dxf13
from . import const
import math

class SeqEnd(object):
    def __init__(self, wrapper):
        self.dxftype = wrapper.dxftype()

class Entity(SeqEnd):
    def __init__(self, wrapper):
        super(Entity, self).__init__(wrapper)
        self.paperspace = wrapper.paperspace()

class Shape(Entity):
    def __init__(self, wrapper):
        super(Shape, self).__init__(wrapper)
        self.layer = wrapper.dxf.get('layer', '0')
        self.linetype = wrapper.dxf.get('linetype', None) # None=BYLAYER
        self.ltscale = wrapper.dxf.get('ltscale', 1.0)
        self.invisible = wrapper.dxf.get('invisible', 0) # 0=visible
        self.color = wrapper.dxf.get('color', const.BYLAYER) # 256=BYLAYER, 0=BYBLOCK

class Line(Shape):
    def __init__(self, wrapper):
        super(Line, self).__init__(wrapper)
        self.start = wrapper.dxf.start
        self.end = wrapper.dxf.end

class Point(Shape):
    def __init__(self, wrapper):
        super(Point, self).__init__(wrapper)
        self.point = wrapper.dxf.point

class Circle(Shape):
    def __init__(self, wrapper):
        super(Circle, self).__init__(wrapper)
        self.center = wrapper.dxf.center
        self.radius = wrapper.dxf.radius

class Arc(Shape):
    def __init__(self, wrapper):
        super(Arc, self).__init__(wrapper)
        self.center = wrapper.dxf.center
        self.radius = wrapper.dxf.radius
        self.startangle = wrapper.dxf.startangle
        self.endangle = wrapper.dxf.endangle

class Trace(Shape):
    def __init__(self, wrapper):
        super(Trace, self).__init__(wrapper)
        self.points = [
        wrapper.dxf.get(vname) for vname in const.VERTEXNAMES
        ]

Solid = Trace

class Face(Trace):
    def __init__(self, wrapper):
        super(Face, self).__init__(wrapper)
        self.invisible_edge = wrapper.dxf.get('invisible_edge', 0)

    def is_edge_invisible(self, edge):
        # edges 0 .. 3
        return bool(self.invisible_edge & (1 << edge))

class Text(Shape):
    def __init__(self, wrapper):
        super(Text, self).__init__(wrapper)
        self.insert = wrapper.dxf.insert
        self.text = wrapper.dxf.text
        self.height = wrapper.dxf.get('height', 1.)
        self.rotation = wrapper.dxf.get('rotation', 0.)
        self.style = wrapper.dxf.get('style', "")

class Insert(Shape):
    def __init__(self, wrapper):
        super(Insert, self).__init__(wrapper)
        self.name = wrapper.dxf.name
        self.insert = wrapper.dxf.insert
        self.rotation = wrapper.dxf.get('rotation', 0.)
        self.attribsfollow = bool(wrapper.dxf.get('attribsfollow', 0))
        self.attribs = []

    def find_attrib(self, attrib_tag):
        for attrib in self.attribs:
            if attrib.tag == attrib_tag:
                return attrib
        return None

    def append_data(self, attribs):
        self.attribs = attribs

class Attrib(Text): # also ATTDEF
    def __init__(self, wrapper):
        super(Attrib, self).__init__(wrapper)
        self.tag = wrapper.dxf.tag

class Polyline(Shape):
    def __init__(self, wrapper):
        super(Polyline, self).__init__(wrapper)
        self.vertices = None
        self.mode = wrapper.get_mode()
        self.flags = wrapper.flags
        self.mcount = wrapper.dxf.get("mcount", 0)
        self.ncount = wrapper.dxf.get("ncount", 0)
        self.is_mclosed = wrapper.is_mclosed()
        self.is_nclosed = wrapper.is_nclosed()
        self.elevation = wrapper.dxf.get('elevation', (0., 0., 0.))

    def __len__(self):
        return len(self.vertices)

    def __getitem__(self, item):
        return self.vertices[item]

    def __iter__(self):
        return iter(self.vertices)

    @property
    def is_closed(self):
        return self.is_mclosed

    def points(self):
        return (vertex.location for vertex in self.vertices)

    def append_data(self, vertices):
        self.vertices = vertices

    def cast(self):
        if self.mode == 'polyface':
            return Polyface(self)
        elif self.mode == 'polymesh':
            return Polymesh(self)
        else:
            return self

class _Face(object):
    def __init__(self, face):
        self._vertices = []
        self._face = face

    def add(self, vertex):
        self._vertices.append(vertex)

    def __getitem__(self, item):
        return self._vertices[item]

    def __iter__(self):
        return (vertex.location for vertex in self._vertices)

class Polyface(object):
    def __init__(self, polyline):
        self.dxftype = "POLYFACE"
        self.layer = polyline.layer
        self.linetype = polyline.linetype
        self.ltscale = polyline.ltscale
        self.invisible = polyline.invisible
        self.color = polyline.color
        self.paperspace = polyline.paperspace
        self._faces = list(self._iterfaces(polyline.vertices))

    def __getitem__(self, item):
        return self._faces[item]

    def __len__(self):
        return len(self._faces)

    def __iter__(self):
        return iter(self._faces)

    def _iterfaces(self, vertices):
        def isface(vertex):
            flags = vertex.flags
            return flags & const.VTX_3D_POLYFACE_MESH_VERTEX and \
                   not flags & const.VTX_3D_POLYGON_MESH_VERTEX

        def getface(vertex):
            face = _Face(vertex)
            for index in vertex.vtx:
                if index != 0:
                    index = abs(index) - 1
                    face.add(vertices[index])
                else:
                    break
            return face

        for vertex in vertices:
            if isface(vertex):
                yield getface(vertex)

class Polymesh(object):
    def __init__(self, polyline):
        self.dxftype = "POLYMESH"
        self.layer = polyline.layer
        self.linetype = polyline.linetype
        self.ltscale = polyline.ltscale
        self.invisible = polyline.invisible
        self.color = polyline.color
        self.paperspace = polyline.paperspace
        self.mcount = polyline.mcount
        self.ncount = polyline.ncount
        self.is_mclosed = polyline.is_mclosed
        self.is_nclosed = polyline.is_nclosed
        self._vertices = polyline.vertices

    def __iter__(self):
        return iter(self._vertices)

    def get_location(self, pos):
        return self.get_vertex(pos).location

    def get_vertex(self, pos):
        mcount = self.mcount
        ncount = self.ncount
        m, n = pos
        if 0 <= m < mcount and 0 <= n < ncount:
            pos = m * ncount + n
            return self._vertices[pos]
        else:
            raise IndexError(repr(pos))

class Vertex(Shape):
    def __init__(self, wrapper):
        super(Vertex, self).__init__(wrapper)
        self.location = wrapper.dxf.location
        self.flags = wrapper.dxf.get('flags', 0)
        self.bulge = wrapper.dxf.get('bulge', 0)
        self.tangent = wrapper.dxf.get('tangent', None)
        self.vtx = self._get_vtx(wrapper)

    def _get_vtx(self, wrapper):
        vtx = []
        for vname in const.VERTEXNAMES:
            try:
                vtx.append(wrapper.dxf.get(vname))
            except ValueError:
                pass
        return tuple(vtx)

class LWPolyline(Shape):
    def __init__(self, wrapper):
        super(LWPolyline, self).__init__(wrapper)
        self.points = tuple(wrapper)
        self.is_closed = wrapper.is_closed()

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        return self.points[item]

    def __iter__(self):
        return iter(self.points)

class Ellipse(Shape):
    def __init__(self, wrapper):
        super(Ellipse, self).__init__(wrapper)
        self.center = wrapper.dxf.center
        self.majoraxis = wrapper.dxf.majoraxis
        self.ratio = wrapper.dxf.get('ratio', 1.0) # circle
        self.startparam = wrapper.dxf.get('startparam', 0.)
        self.endparam = wrapper.dxf.get('endparam', 6.283185307179586) # 2*pi

class Ray(Shape):
    def __init__(self, wrapper):
        super(Ray, self).__init__(wrapper)
        self.start = wrapper.dxf.start
        self.unitvector = wrapper.dxf.unitvector

XLine = Ray

class Spline(Shape):
    def __init__(self, wrapper):
        super(Spline, self).__init__(wrapper)
        self.normalvector = wrapper.dxf.get('normalvector', None)
        self.flags = wrapper.dxf.get('flags', 0)
        self.degree = wrapper.dxf.get('degree', 3)
        self.starttangent = wrapper.dxf.get('starttangent', None)
        self.endtangent = wrapper.dxf.get('endtangent', None)
        self.knots = tuple(wrapper.knots())
        self.weights = tuple(wrapper.weights())
        self.tol_knot = wrapper.dxf.get('knot_tolernace', .0000001)
        self.tol_controlpoint = wrapper.dxf.get('controlpoint_tolernace', .0000001)
        self.tol_fitpoint = wrapper.dxf.get('fitpoint_tolernace', .0000000001)
        self.controlpoints = tuple(wrapper.controlpoints())
        self.fitpoints = tuple(wrapper.fitpoints())
        if len(self.weights) == 0:
            self.weights = tuple([1.0] * len(self.controlpoints))

    @property
    def is_closed(self):
        return bool(self.flags & const.SPLINE_CLOSED)

    @property
    def is_periodic(self):
        return bool(self.flags & const.SPLINE_PERIODIC)

    @property
    def is_rational(self):
        return bool(self.flags & const.SPLINE_RATIONAL)

    @property
    def is_planar(self):
        return bool(self.flags & const.SPLINE_PLANAR)

    @property
    def is_linear(self):
        return bool(self.flags & const.SPLINE_LINEAR)

def deg2vec(deg):
    rad = float(deg) * math.pi / 180.0
    return math.cos(rad), math.sin(rad), 0.

def normalized(vector):
    x, y, z = vector
    m = (x**2 + y**2 + z**2)**0.5
    return x/m, y/m, z/m

class MText(Shape):
    def __init__(self, wrapper):

        super(MText, self).__init__(wrapper)
        self.insert = wrapper.dxf.insert
        self.rawtext = wrapper.rawtext()
        self.height = wrapper.dxf.get('height', 1.0)
        self.linespacing = wrapper.dxf.get('linespacing', 1.0)
        self.attachmentpoint = wrapper.dxf.get('attachmentpoint', 1)
        self.style = wrapper.dxf.get('style', 'STANDARD')
        self.extrusion = wrapper.dxf.get('extrusion', (0., 0., 1.))
        try:
            xdir = wrapper.dxf.xdirection
        except ValueError:
            xdir = deg2vec(wrapper.dxf.get('rotation', 0.0))
        self.xdirection = normalized(xdir)

    def lines(self):
        return self.rawtext.split('\P')

class Block(Shape):
    def __init__(self, wrapper):
        super(Block, self).__init__(wrapper)
        self.basepoint = wrapper.dxf.basepoint
        self.name = wrapper.dxf.name
        self.flags = wrapper.dxf.get('flags', 0)
        self.xrefpath = wrapper.dxf.get('xrefpath', "")
        self._entities = list()

    @property
    def is_xref(self):
        return bool(self.flags & const.BLK_XREF)

    @property
    def is_xref_overlay(self):
        return bool(self.flags & const.BLK_XREF_OVERLAY)

    @property
    def is_anonymous(self):
        return bool(self.flags & const.BLK_ANONYMOUS)

    def set_entities(self, entities):
        self._entities = entities

    def __iter__(self):
        return iter(self._entities)

    def __getitem__(self, item):
        return self._entities[item]

    def __len__(self):
        return len(self._entities)

class BlockEnd(SeqEnd):
    pass

EntityTable = {
    'LINE':( Line, dxf12.Line, dxf13.Line),
    'POINT': (Point, dxf12.Point, dxf13.Point),
    'CIRCLE': (Circle, dxf12.Circle, dxf13.Arc),
    'ARC': (Arc, dxf12.Arc, dxf13.Arc),
    'TRACE': (Trace, dxf12.Trace, dxf13.Trace),
    'SOLID': (Solid, dxf12.Solid, dxf13.Solid),
    '3DFACE': (Face, dxf12.Face, dxf13.Face),
    'TEXT': (Text, dxf12.Text, dxf13.Text),
    'INSERT': (Insert, dxf12.Insert, dxf13.Insert),
    'SEQEND': (SeqEnd, dxf12.SeqEnd, dxf13.SeqEnd),
    'ATTRIB': (Attrib, dxf12.Attrib, dxf13.Attrib),
    'ATTDEF': (Attrib, dxf12.Attrib, dxf13.Attdef),
    'POLYLINE': (Polyline, dxf12.Polyline, dxf13.Polyline),
    'VERTEX': (Vertex, dxf12.Vertex, dxf13.Vertex),
    'BLOCK': (Block, dxf12.Block, dxf13.Block),
    'ENDBLK': (BlockEnd, dxf12.EndBlk, dxf13.EndBlk),
    'LWPOLYLINE': (LWPolyline, None, dxf13.LWPolyline),
    'ELLIPSE': (Ellipse, None, dxf13.Ellipse),
    'RAY': (Ray, None, dxf13.Ray),
    'XLINE': (XLine, None, dxf13.XLine),
    'SPLINE': (Spline, None, dxf13.Spline),
    'MTEXT': (MText, None, dxf13.MText),
}

def entity_factory(tags, dxfversion):
    dxftype = tags.get_type()
    cls, dxf12wrapper, dxf13wrapper = EntityTable[dxftype]
    shape = cls(dxf12wrapper(tags) if dxfversion=="AC1009" else dxf13wrapper(tags))
    return shape
