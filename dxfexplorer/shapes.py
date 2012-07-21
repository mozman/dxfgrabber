#!/usr/bin/env python
#coding:utf-8
# Purpose: 
# Created: 21.07.2012, parts taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from . import graphics12, graphics13
from . import const


class BasicShape:
    def __init__(self, wrapper):
        self.dxftype = wrapper.dxftype()
        self.layer = wrapper.dxf.get('layer', '0')
        self.linetype = wrapper.dxf.get('linetype', "")
        self.color = wrapper.dxf.get('color', 0)
        self.paperspace = wrapper.paperspace() == 1

class Line(BasicShape):
    def __init__(self, wrapper):
        super(Line, self).__init__(wrapper)
        self.start = wrapper.dxf.start
        self.end = wrapper.dxf.end

class Point(BasicShape):
    def __init__(self, wrapper):
        super(Point, self).__init__(wrapper)
        self.point = wrapper.point

class Circle(BasicShape):
    def __init__(self, wrapper):
        super(Circle, self).__init__(wrapper)
        self.center = wrapper.dxf.center
        self.radius = wrapper.dxf.radius

class Arc(BasicShape):
    def __init__(self, wrapper):
        super(Arc, self).__init__(wrapper)
        self.center = wrapper.dxf.center
        self.radius = wrapper.dxf.radius
        self.startangle = wrapper.dxf.startangle
        self.endangle = wrapper.dxf.endangle

class Trace(BasicShape):
    def __init__(self, wrapper):
        super(Trace, self).__init__(wrapper)
        self.points = [
        wrapper.dxf.get(vname) for vname in const.VERTEXNAMES
        ]

Solid = Trace

class Face(Trace):
    def __init__(self, wrapper):
        super(Face, self).__init__(wrapper)
        self.invisible_edge = wrapper.dxf.invisible_edge

class Text(BasicShape):
    def __init__(self, wrapper):
        super(Text, self).__init__(wrapper)
        self.insert = wrapper.dxf.insert
        self.height = wrapper.dxf.height
        self.text = wrapper.dxf.text
        self.rotation = wrapper.dxf.rotation

class Insert(BasicShape):
    def __init__(self, wrapper):
        super(Insert, self).__init__(wrapper)
        self.name = wrapper.dxf.name
        self.insert = wrapper.dxf.insert
        self.rotation = wrapper.dxf.rotation
        self.attribsfollow = wrapper.dxf.attribsfollow
        self.attribs = []

    def append_data(self, attribs):
        self.attribs = attribs

class SeqEnd:
    def __init__(self, wrapper):
        self.dxftype = wrapper.dxftype()
        self.paperspace = wrapper.paperspace()

class Attrib(BasicShape):
    def __init__(self, wrapper):
        super(Attrib, self).__init__(wrapper)
        self.insert = wrapper.dxf.insert
        self.height = wrapper.dxf.height
        self.text = wrapper.dxf.text
        self.tag = wrapper.dxf.tag
        self.rotation = wrapper.dxf.rotation


class Polyline(BasicShape):
    def __init__(self, wrapper):
        super(Polyline, self).__init__(wrapper)
        self.vertices = None
        self.mode = wrapper.get_mode()
        self.flags = wrapper.dxf.flags
        self.mcount = wrapper.dxf.get("mcount", 0)
        self.ncount = wrapper.dxf.get("ncount", 0)
        self.is_mclosed = wrapper.is_mclosed()
        self.is_nclosed = wrapper.is_nclosed()
        self.elevation = wrapper.dxf.elevation

    def __len__(self):
        return len(self.vertices)

    def __getitem__(self, item):
        return self.vertices[item]

    def __iter__(self):
        return iter(self.vertices)

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

class _Face:
    def __init__(self, face):
        self._vertices = []
        self._face = face

    def add(self, vertex):
        self._vertices.append(vertex)

    def __getitem__(self, item):
        return self._vertices[item]

    def __iter__(self):
        return (vertex.location for vertex in self._vertices)

class Polyface:
    def __init__(self, polyline):
        self.dxftype = "POLYFACE"
        self.layer = polyline.layer
        self.linetype = polyline.linetype
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
            if flags & const.VTX_3D_POLYFACE_MESH_VERTEX > 0 and\
               flags & const.VTX_3D_POLYGON_MESH_VERTEX == 0:
                return True
            else:
                return False

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

class Polymesh:
    def __init__(self, polyline):
        self.dxftype = "POLYMESH"
        self.layer = polyline.layer
        self.linetype = polyline.linetype
        self.color = polyline.color
        self.paperspace = polyline.paperspace
        self.mcount = polyline.mcount
        self.ncount = polyline.ncount
        self.is_mclosed = polyline.is_mclosed()
        self.is_nclosed = polyline.is_nclosed()
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
            return self._vertices(pos)
        else:
            raise IndexError(repr(pos))

class Vertex(BasicShape):
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

class LWPolyline(BasicShape):
    def __init__(self, wrapper):
        super(LWPolyline, self).__init__(wrapper)
        self.points = list(wrapper)
        self.is_closed = wrapper.is_closed()

class Ellipse(BasicShape):
    def __init__(self, wrapper):
        super(Ellipse, self).__init__(wrapper)
        self.center = wrapper.dxf.center
        self.majoraxis = wrapper.dxf.majoraxis
        self.ratio = wrapper.dxf.ratio
        self.startparam = wrapper.dxf.startparam
        self.endparam = wrapper.dxf.endparam

class Ray(BasicShape):
    def __init__(self, wrapper):
        super(Ray, self).__init__(wrapper)
        self.start = wrapper.dxf.start
        self.unitvector = wrapper.dxf.unitvector

ShapeTable = {
    'LINE':( Line, graphics12.Line, graphics13.Line),
    'POINT': (Point, graphics12.Point, graphics13.Point),
    'CIRCLE': (Circle, graphics12.Circle, graphics13.Arc),
    'ARC': (Arc, graphics12.Arc, graphics13.Arc),
    'TRACE': (Trace, graphics12.Trace, graphics13.Trace),
    'SOLID': (Solid, graphics12.Solid, graphics13.Solid),
    'FACE': (Face, graphics12.Face, graphics13.Face),
    'TEXT': (Text, graphics12.Text, graphics13.Text),
    'INSERT': (Insert, graphics12.Insert, graphics13.Insert),
    'SEQEND': (SeqEnd, graphics12.SeqEnd, graphics13.SeqEnd),
    'ATTRIB': (Attrib, graphics12.Attrib, graphics13.Attrib),
    'POLYLINE': (Polyline, graphics12.Polyline, graphics13.Polyline),
    'VERTEX': (Vertex, graphics12.Vertex, graphics13.Vertex),
    'LWPOLYLINE': (LWPolyline, None, graphics13.LWPolyline),
    'ELLIPSE': (Ellipse, None, graphics13.Ellipse),
    'RAY': (Ray, None, graphics13.Ray),

}

def shape_factory(tags, dxfversion):
    dxftype = tags.get_type()
    cls, dxf12wrapper, dxf13wrapper = ShapeTable[dxftype]
    shape = cls(dxf12wrapper(tags) if dxfversion=="AC1009" else dxf13wrapper(tags))
    return shape
