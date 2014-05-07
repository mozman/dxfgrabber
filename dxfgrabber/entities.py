# Purpose: entity classes
# Created: 21.07.2012, parts taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from . import dxf12, dxf13
from . import const
from .juliandate import calendar_date
from datetime import datetime

import math


class SeqEnd(object):
    def __init__(self, wrapper):
        self.dxftype = wrapper.dxftype()


class Entity(SeqEnd):
    def __init__(self, wrapper):
        super(Entity, self).__init__(wrapper)
        self.paperspace = bool(wrapper.paperspace())


class Shape(Entity):
    def __init__(self, wrapper):
        super(Shape, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.layer = get_dxf('layer', '0')
        self.linetype = get_dxf('linetype', None)  # None=BYLAYER
        self.thickness = get_dxf('thickness', 0.0)
        self.ltscale = get_dxf('ltscale', 1.0)
        self.invisible = get_dxf('invisible', 0)  # 0=visible
        self.color = get_dxf('color', const.BYLAYER)  # 256=BYLAYER, 0=BYBLOCK
        # if adding additional DXF attributes, do it also for PolyShape


class PolyShape(object):
    """ Base class for Polyface and Polymesh, both are special cases of POLYLINE.
    """
    def __init__(self, polyline, dxftype):
        self.dxftype = dxftype
        self.paperspace = polyline.paperspace
        self.layer = polyline.layer
        self.linetype = polyline.linetype
        self.ltscale = polyline.ltscale
        self.invisible = polyline.invisible
        self.color = polyline.color


class Line(Shape):
    def __init__(self, wrapper):
        super(Line, self).__init__(wrapper)
        self.start = wrapper.get_dxf_attrib('start')
        self.end = wrapper.get_dxf_attrib('end')


class Point(Shape):
    def __init__(self, wrapper):
        super(Point, self).__init__(wrapper)
        self.point = wrapper.get_dxf_attrib('point')


class Circle(Shape):
    def __init__(self, wrapper):
        super(Circle, self).__init__(wrapper)
        self.center = wrapper.get_dxf_attrib('center')
        self.radius = wrapper.get_dxf_attrib('radius')


class Arc(Shape):
    def __init__(self, wrapper):
        super(Arc, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.center = get_dxf('center')
        self.radius = get_dxf('radius')
        self.startangle = get_dxf('startangle')
        self.endangle = get_dxf('endangle')


class Trace(Shape):
    def __init__(self, wrapper):
        super(Trace, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.points = [
            get_dxf(vname) for vname in const.VERTEXNAMES
        ]

Solid = Trace


class Face(Trace):
    def __init__(self, wrapper):
        super(Face, self).__init__(wrapper)
        self.invisible_edge = wrapper.get_dxf_attrib('invisible_edge', 0)

    def is_edge_invisible(self, edge):
        # edges 0 .. 3
        return bool(self.invisible_edge & (1 << edge))


class Text(Shape):
    def __init__(self, wrapper):
        super(Text, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.insert = get_dxf('insert')
        self.text = get_dxf('text')
        self.height = get_dxf('height', 1.)
        self.rotation = get_dxf('rotation', 0.)
        self.style = get_dxf('style', "")
        self.halign = get_dxf('halign', 0)
        self.valign = get_dxf('valign', 0)
        self.alignpoint = get_dxf('alignpoint', None)


class Insert(Shape):
    def __init__(self, wrapper):
        super(Insert, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.name = get_dxf('name')
        self.insert = get_dxf('insert')
        self.rotation = get_dxf('rotation', 0.)
        self.scale = get_dxf('xscale', 1.), get_dxf('yscale', 1.), get_dxf('zscale', 1.)
        self.attribsfollow = bool(get_dxf('attribsfollow', 0))
        self.attribs = []

    def find_attrib(self, attrib_tag):
        for attrib in self.attribs:
            if attrib.tag == attrib_tag:
                return attrib
        return None

    def append_data(self, attribs):
        self.attribs = attribs


class Attrib(Text):  # also ATTDEF
    def __init__(self, wrapper):
        super(Attrib, self).__init__(wrapper)
        self.tag = wrapper.get_dxf_attrib('tag')


class Polyline(Shape):
    def __init__(self, wrapper):
        super(Polyline, self).__init__(wrapper)
        self.vertices = None
        self.mode = wrapper.get_mode()
        self.flags = wrapper.flags
        get_dxf = wrapper.get_dxf_attrib
        self.mcount = get_dxf("mcount", 0)
        self.ncount = get_dxf("ncount", 0)
        self.default_start_width = get_dxf("defaultstartwidth", 0.)
        self.default_end_width = get_dxf("defaultendwidth", 0.)
        self.is_mclosed = wrapper.is_mclosed()
        self.is_nclosed = wrapper.is_nclosed()
        self.elevation = get_dxf('elevation', (0., 0., 0.))

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


class SubFace(object):
    def __init__(self, face_record, vertices):
        self._vertices = vertices
        self.face_record = face_record

    def __len__(self):
        return len(self.face_record.vtx)

    def __getitem__(self, item):
        return self._vertices[self._vertex_index(item)]

    def __iter__(self):
        return (self._vertices[index].location for index in self.indices())

    def _vertex_index(self, pos):
        return abs(self.face_record.vtx[pos]) - 1

    def indices(self):
        return tuple(abs(i)-1 for i in self.face_record.vtx if i != 0)

    def is_edge_visible(self, pos):
        return self.face_record.vtx[pos] > 0


class Polyface(PolyShape):
    def __init__(self, polyline):
        VERTEX_FLAGS = const.VTX_3D_POLYFACE_MESH_VERTEX + const.VTX_3D_POLYGON_MESH_VERTEX

        def is_vertex(flags):
            return flags & VERTEX_FLAGS == VERTEX_FLAGS

        super(Polyface, self).__init__(polyline, 'POLYFACE')
        vertices = []
        face_records = []
        for vertex in polyline.vertices:
            (vertices if is_vertex(vertex.flags) else face_records).append(vertex)

        self.vertices = vertices
        self._face_records = face_records

    def __getitem__(self, item):
        return SubFace(self._face_records[item], self.vertices)

    def __len__(self):
        return len(self._face_records)

    def __iter__(self):
        return (SubFace(f, self.vertices) for f in self._face_records)


class Polymesh(PolyShape):
    def __init__(self, polyline):
        super(Polymesh, self).__init__(polyline, 'POLYMESH')
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
        get_dxf = wrapper.get_dxf_attrib
        self.location = get_dxf('location')
        self.flags = get_dxf('flags', 0)
        self.bulge = get_dxf('bulge', 0)
        self.tangent = get_dxf('tangent', None)
        self.vtx = self._get_vtx(wrapper)

    def _get_vtx(self, wrapper):
        vtx = []
        get_dxf = wrapper.get_dxf_attrib
        for vname in const.VERTEXNAMES:
            try:
                vtx.append(get_dxf(vname))
            except ValueError:
                pass
        return tuple(vtx)


class LWPolyline(Shape):
    def __init__(self, wrapper):
        super(LWPolyline, self).__init__(wrapper)
        self.points = tuple(wrapper)
        self.is_closed = wrapper.is_closed()
        self.elevation = wrapper.get_dxf_attrib('elevation', (0., 0., 0.))

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        return self.points[item]

    def __iter__(self):
        return iter(self.points)

    def get_rstrip_points(self):
        last0 = 4
        for point in self.points:
            while point[last0] == 0 and last0 > 1:
                last0 -= 1
            yield tuple(point[:last0+1])


class Ellipse(Shape):
    def __init__(self, wrapper):
        super(Ellipse, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.center = get_dxf('center')
        self.majoraxis = get_dxf('majoraxis')
        self.ratio = get_dxf('ratio', 1.0)  # circle
        self.startparam = get_dxf('startparam', 0.)
        self.endparam = get_dxf('endparam', 6.283185307179586)  # 2*pi


class Ray(Shape):
    def __init__(self, wrapper):
        super(Ray, self).__init__(wrapper)
        self.start = wrapper.get_dxf_attrib('start')
        self.unitvector = wrapper.get_dxf_attrib('unitvector')

XLine = Ray


class Spline(Shape):
    def __init__(self, wrapper):
        super(Spline, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.normalvector = get_dxf('normalvector', None)
        self.flags = get_dxf('flags', 0)
        self.degree = get_dxf('degree', 3)
        self.starttangent = get_dxf('starttangent', None)
        self.endtangent = get_dxf('endtangent', None)
        self.knots = tuple(wrapper.knots())
        self.weights = tuple(wrapper.weights())
        self.tol_knot = get_dxf('knot_tolernace', .0000001)
        self.tol_controlpoint = get_dxf('controlpoint_tolerance', .0000001)
        self.tol_fitpoint = get_dxf('fitpoint_tolerance', .0000000001)
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


class Helix(Spline):
    def __init__(self, wrapper):
        super(Helix, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.helix_version = (get_dxf('helix_major_version', 1),
                              get_dxf('helix_maintainance_version', 1))
        self.axis_base_point = get_dxf('axis_base_point', None)
        self.start_point = get_dxf('start_point', None)
        self.axis_vector = get_dxf('axis_vector', None)
        self.radius = get_dxf('radius', 0)
        self.turns = get_dxf('turns', 0)
        self.turn_height = get_dxf('turn_height', 0)
        self.handedness = get_dxf('handedness', 0)  # 0 = left, 1 = right
        self.constrain = get_dxf('constrain', 0)
        # 0 = Constrain turn height;
        # 1 = Constrain turns;
        # 2 = Constrain height


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
        self.insert = wrapper.get_dxf_attrib('insert')
        self.rawtext = wrapper.rawtext()
        get_dxf = wrapper.get_dxf_attrib
        self.height = get_dxf('height', 1.0)
        self.linespacing = get_dxf('linespacing', 1.0)
        self.attachmentpoint = get_dxf('attachmentpoint', 1)
        self.style = get_dxf('style', 'STANDARD')
        self.extrusion = get_dxf('extrusion', (0., 0., 1.))
        try:
            xdir = wrapper.get_dxf_attrib('xdirection')
        except ValueError:
            xdir = deg2vec(get_dxf('rotation', 0.0))
        self.xdirection = normalized(xdir)

    def lines(self):
        return self.rawtext.split('\P')


class Block(Shape):
    def __init__(self, wrapper):
        super(Block, self).__init__(wrapper)
        self.basepoint = wrapper.get_dxf_attrib('basepoint')
        self.name = wrapper.get_dxf_attrib('name')
        self.flags = wrapper.get_dxf_attrib('flags', 0)
        self.xrefpath = wrapper.get_dxf_attrib('xrefpath', "")
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


def unpack_seconds(seconds):
    seconds = int(seconds / 1000)  # remove 1/1000 part
    hours = int(seconds / 3600)
    seconds = int(seconds % 3600)
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)
    return hours, minutes, seconds


class Sun(Entity):
    def __init__(self, wrapper):
        super(Sun, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.version = get_dxf('version', 1)
        self.status = bool(get_dxf('status', 0))  # on/off ?
        self.sun_color = get_dxf('sun_color', None)  # None is unset
        self.intensity = get_dxf('intensity', 0)
        self.shadows = bool(get_dxf('shadows', 0))
        julian_date = get_dxf('date', 0.)
        if julian_date > 0.:
            date = calendar_date(julian_date)
        else:
            date = datetime.now()
        hours, minutes, seconds = unpack_seconds(get_dxf('time', 0))
        self.date = datetime(date.year, date.month, date.day, hours, minutes, seconds)
        self.daylight_savings_time = bool(get_dxf('daylight_savings_time', 0))
        self.shadow_type = get_dxf('shadows_type', 0)
        self.shadow_map_size = get_dxf('shadow_map_size', 0)
        self.shadow_softness = get_dxf('shadow_softness', 0)


class Mesh(Shape):
    def __init__(self, wrapper):
        super(Mesh, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.version = get_dxf('version', 2)
        self.blend_crease = bool(get_dxf('blend_crease', 0))
        self.subdivision_levels = get_dxf('subdivision_levels', 1)
        # rest are mostly positional tags
        self.vertices = []
        self.faces = []
        self.edges = []
        self.edge_crease_list = []

        subdmesh_tags = wrapper.tags.get_subclass('AcDbSubDMesh')
        # for all blocks I ignore the count values, perhaps they are wrong,
        # but I use the count tags as indicator for the begin of the list
        try:
            pos = subdmesh_tags.tag_index(92)
        except ValueError:  # no vertices???
            return
        else:
            self.vertices = Mesh.get_vertices(subdmesh_tags, pos+1)
        try:
            pos = subdmesh_tags.tag_index(93)
        except ValueError:  # no faces???
            pass
        else:
            self.faces = Mesh.get_faces(subdmesh_tags, pos+1)
        try:
            pos = subdmesh_tags.tag_index(94)
        except ValueError:  # no edges
            pass
        else:
            self.edges = Mesh.get_edges(subdmesh_tags, pos+1)
        try:
            pos = subdmesh_tags.tag_index(95)
        except ValueError:  # no edges crease values
            pass
        else:
            self.edge_crease_list = Mesh.get_edge_crease_list(subdmesh_tags, pos+1)

    def get_face(self, index):
        return tuple(self.vertices[vertex_index] for vertex_index in self.faces[index])

    def get_edge(self, index):
        return tuple(self.vertices[vertex_index] for vertex_index in self.edges[index])

    @staticmethod
    def get_vertices(tags, pos):
        vertices = []
        itags = iter(tags[pos:])
        while True:
            try:
                tag = next(itags)
            except StopIteration:  # premature end of tags, return what you got
                break
            if tag.code == 10:
                vertices.append(tag.value)
            else:
                break
        return vertices

    @staticmethod
    def get_faces(tags, pos):
        faces = []
        face = []
        itags = iter(tags[pos:])
        try:
            while True:
                tag = next(itags)
                # loop until first tag.code != 90
                if tag.code != 90:
                    break
                count = tag.value  # count of vertex indices
                while count > 0:
                    tag = next(itags)
                    face.append(tag.value)
                    count -= 1
                faces.append(tuple(face))
                del face[:]
        except StopIteration:  # premature end of tags, return what you got
            pass
        return faces

    @staticmethod
    def get_edges(tags, pos):
        edges = []
        start_index = None
        for index in Mesh.get_raw_list(tags, pos, code=90):
            if start_index is None:
                start_index = index
            else:
                edges.append((start_index, index))
                start_index = None
        return edges

    @staticmethod
    def get_edge_crease_list(tags, pos):
        return Mesh.get_raw_list(tags, pos, code=140)

    @staticmethod
    def get_raw_list(tags, pos, code):
        raw_list = []
        itags = iter(tags[pos:])
        while True:
            try:
                tag = next(itags)
            except StopIteration:
                break
            if tag.code == code:
                raw_list.append(tag.value)
            else:
                break
        return raw_list


class Light(Shape):
    def __init__(self, wrapper):
        super(Light, self).__init__(wrapper)
        get_dxf = wrapper.get_dxf_attrib
        self.version = get_dxf('version', 1)
        self.name = get_dxf('name', "")
        self.light_type = get_dxf('light_type', 1)  # distant = 1; point = 2; spot = 3
        self.status = bool(get_dxf('status', 0))  # on/off ?
        self.light_color = get_dxf('light_color', None)  # 0 is unset
        self.true_color = get_dxf('true_color', None)  # None is unset
        self.plot_glyph = bool(get_dxf('plot_glyph', 0))
        self.intensity = get_dxf('intensity', 0)
        self.position = get_dxf('position', (0, 0, 1))
        self.target = get_dxf('target', (0, 0, 0))
        self.attenuation_type = get_dxf('attenuation_type', 0)  # 0 = None; 1 = Inverse Linear; 2 = Inverse Square
        self.use_attenuation_limits = bool(get_dxf('use_attenuation_limits', 0))
        self.attenuation_start_limit = get_dxf('attenuation_start_limit', 0)
        self.attenuation_end_limit = get_dxf('attenuation_end_limit', 0)
        self.hotspot_angle = get_dxf('hotspot_angle', 0)
        self.fall_off_angle = get_dxf('fall_off_angle', 0)
        self.cast_shadows = bool(get_dxf('cast_shadows', 0))
        self.shadow_type = get_dxf('shadow_type', 0)  # 0 = Ray traced shadows; 1 = Shadow maps
        self.shadow_map_size = get_dxf('shadow_map_size', 0)
        self.shadow_softness = get_dxf('shadow_softness', 0)


class Body(Shape):
    def __init__(self, wrapper):
        super(Body, self).__init__(wrapper)
        # need handle to get SAB data in DXF version AC1027 and later
        self.handle = wrapper.get_dxf_attrib('handle', None)
        self.version = wrapper.get_dxf_attrib('version', 1)
        self.acis = wrapper.get_acis_data()

    def set_sab_data(self, sab_data):
        self.acis = sab_data

    @property
    def is_sat(self):
        return isinstance(self.acis, list)  # but could be an empty list

    @property
    def is_sab(self):
        return not self.is_sat  # has binary encoded ACIS data

Solid3d = Body
# perhaps reading creation history is needed


class Surface(Body):
    def __init__(self, wrapper):
        super(Surface, self).__init__(wrapper)
        self.u_isolines = wrapper.get_dxf_attrib('u_isolines', 0)
        self.v_isolines = wrapper.get_dxf_attrib('v_isolines', 0)


EntityTable = {
    'LINE': (Line, dxf12.Line, dxf13.Line),
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
    'HELIX': (Helix, None, dxf13.Helix),
    'MTEXT': (MText, None, dxf13.MText),
    'SUN': (Sun, None, dxf13.Sun),
    'MESH': (Mesh, None, dxf13.Mesh),
    'LIGHT': (Light, None, dxf13.Light),
    'BODY': (Body, None, dxf13.Body),
    'REGION': (Body, None, dxf13.Body),
    '3DSOLID': (Solid3d, None, dxf13.Solid3d),
    'SURFACE': (Surface, None, dxf13.Surface),
    'PLANESURFACE': (Surface, None, dxf13.Surface),
}


def entity_factory(tags, dxfversion):
    dxftype = tags.get_type()
    cls, dxf12wrapper, dxf13wrapper = EntityTable[dxftype]
    wrapper = dxf12wrapper(tags) if dxfversion == "AC1009" else dxf13wrapper(tags)
    wrapper.post_read_correction()
    shape = cls(wrapper)
    return shape


