# encoding: utf-8
# Purpose: entity classes, new implementation without dxf12/dxf13 layer
# Created: 17.04.2016
# Copyright (C) 2016, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from . import const
from .color import TrueColor
from .styles import default_text_style

SPECIAL_CHARS = {
    'd': '°'
}


class DXFEntity(object):
    def __init__(self):
        self.dxftype = 'ENTITY'
        self.handle = None
        self.owner = None
        self.paperspace = None
        self.layer = '0'
        self.linetype = None
        self.thickness = 0.0
        self.extrusion = None
        self.ltscale = 1.0
        self.line_weight = 0
        self.invisible = 0
        self.color = const.BYLAYER
        self.true_color = None
        self.transparency = None
        self.shadow_mode = None
        self.layout_tab_name = None

    def setup_attributes(self, tags):
        self.dxftype = tags.get_type()
        for code, value in tags.plain_tags():
            if code == 5:   # special case 105 handled by STYLE TABLE
                self.handle = value
            elif code == 6:
                self.linetype = value
            elif code == 8:
                self.layer = value
            elif code == 39:
                self.thickness = value
            elif code == 48:
                self.ltscale = value
            elif code == 62:
                self.color = value
            elif code == 67:
                self.paperspace = value
            elif code == 210:
                self.extrusion = value
            elif code == 284:
                self.shadow_mode = value
            elif code == 330:
                self.owner = value
            elif code == 370:
                self.line_weight = value
            elif code == 410:
                self.layout_tab_name = value
            elif code == 420:
                self.true_color = TrueColor(value)
            elif code == 440:
                self.transparency = 1. - float(value & 0xFF) / 255.
            else:
                yield code, value  # chain of generators

    def set_default_extrusion(self):  # call only for 2d entities with extrusion vector
        if self.extrusion is None:
            self.extrusion = (0., 0., 1.)


class Point(DXFEntity):
    def __init__(self):
        super(Point, self).__init__()
        self.point = (0, 0, 0)

    def setup_attributes(self, tags):
        for code, value in super(Point, self).setup_attributes(tags):
            if code == 10:
                self.point = value
            else:
                yield code, value  # chain of generators
        self.set_default_extrusion()


class Line(DXFEntity):
    def __init__(self):
        super(Line, self).__init__()
        self.start = (0, 0, 0)
        self.end = (0, 0, 0)

    def setup_attributes(self, tags):
        for code, value in super(Line, self).setup_attributes(tags):
            if code == 10:
                self.start = value
            elif code == 11:
                self.end = value
            else:
                yield code, value  # chain of generators


class Circle(DXFEntity):
    def __init__(self):
        super(Circle, self).__init__()
        self.center = (0, 0, 0)
        self.radius = 1.0

    def setup_attributes(self, tags):
        for code, value in super(Circle, self).setup_attributes(tags):
            if code == 10:
                self.center = value
            elif code == 40:
                self.radius = value
            else:
                yield code, value  # chain of generators
        self.set_default_extrusion()


class Arc(Circle):
    def __init__(self):
        super(Arc, self).__init__()
        self.startangle = 0.
        self.endangle = 360.

    def setup_attributes(self, tags):
        for code, value in super(Arc, self).setup_attributes(tags):
            if code == 50:
                self.startangle = value
            elif code == 51:
                self.endangle = value
            else:
                yield code, value  # chain of generators
        self.set_default_extrusion()

TRACE_CODES = frozenset((10, 11, 12, 13))


class Trace(DXFEntity):
    def __init__(self):
        super(Trace, self).__init__()
        self.points = []

    def setup_attributes(self, tags):
        for code, value in super(Trace, self).setup_attributes(tags):
            if code in TRACE_CODES:
                self.points.append(value)
            else:
                yield code, value  # chain of generators
        self.set_default_extrusion()


Solid = Trace


class Face(Trace):
    def __init__(self):
        super(Face, self).__init__()
        self.points = []
        self.invisible_edge = 0

    def setup_attributes(self, tags):
        for code, value in super(Face, self).setup_attributes(tags):
            if code == 70:
                self.invisible_edge = value
            else:
                yield code, value  # chain of generators
        self.set_default_extrusion()

    def is_edge_invisible(self, edge):
        # edges 0 .. 3
        return bool(self.invisible_edge & (1 << edge))


class Text(DXFEntity):
    def __init__(self):
        super(Text, self).__init__()
        self.insert = (0., 0.)
        self.height = 1.0
        self.text = ""
        self.rotation = 0.
        self.oblique = 0.
        self.style = "STANDARD"
        self.width = 1.
        self.is_backwards = False
        self.is_upside_down = False
        self.halign = 0
        self.valign = 0
        self.alignpoint = None
        self.font = ""
        self.bigfont = ""

    def setup_attributes(self, tags):
        for code, value in super(Text, self).setup_attributes(tags):
            if code == 10:
                self.insert = value
            elif code == 11:
                self.alignpoint = value
            elif code == 1:
                self.text = value
            elif code == 7:
                self.style = value
            elif code == 40:
                self.height = value
            elif code == 41:
                self.width = value
            elif code == 50:
                self.rotation = value
            elif code == 51:
                self.oblique = value
            elif code == 71:
                self.is_backwards = bool(value & 2)
                self.is_upside_down = bool(value & 4)
            elif code == 72:
                self.halign = value
            elif code == 73:
                self.valign = value
            else:
                yield code, value  # chain of generators
        self.set_default_extrusion()

    def resolve_text_style(self, text_styles):
        style = text_styles.get(self.style, None)
        if style is None:
            style = default_text_style
        if self.height == 0:
            self.height = style.height
        if self.width == 0:
            self.width = style.width
        if self.oblique is None:
            self.oblique = style.oblique
        if self.is_backwards is None:
            self.is_backwards = style.is_backwards
        if self.is_upside_down is None:
            self.is_upside_down = style.is_upside_down
        if self.font is None:
            self.font = style.font
        if self.bigfont is None:
            self.bigfont = style.bigfont

    def plain_text(self):
        chars = []
        raw_chars = list(reversed(self.text))  # text splitted into chars, in reversed order for efficient pop()
        while len(raw_chars):
            char = raw_chars.pop()
            if char == '%':  # formatting codes and special characters
                if len(raw_chars) and raw_chars[-1] == '%':
                    raw_chars.pop()  # '%'
                    if len(raw_chars):
                        special_char = raw_chars.pop()  # command char
                        chars.append(SPECIAL_CHARS.get(special_char, ""))
                else:  # char is just a single '%'
                    chars.append(char)
            else:  # char is what it is, a character
                chars.append(char)
        return "".join(chars)


class Attrib(Text):
    def __init__(self):
        super(Attrib, self).__init__()
        self.field_length = 0
        self.tag = ""

    def setup_attributes(self, tags):
        for code, value in super(Attrib, self).setup_attributes(tags):
            if code == 2:
                self.tag = value
            elif code == 73:
                self.field_length = value
            else:
                yield code, value


class Insert(DXFEntity):
    def __init__(self):
        super(Insert, self).__init__()
        self.name = ""
        self.insert = (0., 0., 0.)
        self.rotation = 0.
        self.scale = (1., 1., 1.)
        self.row_count = 1
        self.row_spacing = 0.
        self.col_count = 1
        self.col_spacing = 0.
        self.attribsfollow = False
        self.attribs = []

    def setup_attributes(self, tags):
        xscale = 1.
        yscale = 1.
        zscale = 1.
        for code, value in super(Insert, self).setup_attributes(tags):
            if code == 2:
                self.name = value
            elif code == 10:
                self.insert = value
            elif code == 41:
                xscale = value
            elif code == 42:
                yscale = value
            elif code == 43:
                zscale = value
            elif code == 44:
                self.col_spacing = value
            elif code == 45:
                self.row_spacing = value
            elif code == 50:
                self.rotation = value
            elif code == 66:
                self.attribsfollow = bool(value)
            elif code == 70:
                self.col_count = value
            elif code == 71:
                self.row_count = value
            else:
                yield code, value
        self.scale = (xscale, yscale, zscale)
        self.set_default_extrusion()

    def find_attrib(self, attrib_tag):
        for attrib in self.attribs:
            if attrib.tag == attrib_tag:
                return attrib
        return None

    def append_data(self, attribs):
        self.attribs = attribs


class Polyline(DXFEntity):
    LINE_TYPES = frozenset(('spline2d', 'polyline2d', 'polyline3d'))

    def __init__(self):
        super(Polyline, self).__init__()
        self.vertices = []  # set in append data
        self.points = []  # set in append data
        self.controlpoints = []  # set in append data
        self.width = []  # set in append data
        self.bulge = []  # set in append data
        self.tangents = []  # set in append data
        self.flags = 0
        self.mode = 'polyline2d'
        self.mcount = 0
        self.ncount = 0
        self.default_start_width = 0.
        self.default_end_width = 0.
        self.is_mclosed = False
        self.is_nclosed = False
        self.is_closed = False
        self.elevation = (0., 0., 0.)
        self.m_smooth_density = 0.
        self.n_smooth_density = 0.
        self.smooth_type = 0
        self.spline_type = None
        if self.mode == 'spline2d':
            if self.smooth_type == const.POLYMESH_CUBIC_BSPLINE:
                self.spline_type = 'cubic_bspline'
            elif self.smooth_type == const.POLYMESH_QUADRIC_BSPLINE:
                self.spline_type = 'quadratic_bspline'
            elif self.smooth_type == const.POLYMESH_BEZIER_SURFACE:
                self.spline_type = 'bezier_curve'  # is this a valid spline type for DXF12?

    def setup_attributes(self, tags):
        def get_mode():
            flags = self.flags
            if flags & const.POLYLINE_SPLINE_FIT_VERTICES_ADDED:
                return 'spline2d'
            elif flags & const.POLYLINE_3D_POLYLINE:
                return 'polyline3d'
            elif flags & const.POLYLINE_3D_POLYMESH:
                return 'polymesh'
            elif flags & const.POLYLINE_POLYFACE:
                return 'polyface'
            else:
                return 'polyline2d'

        for code, value in super(Polyline, self).setup_attributes(tags):
            if code == 10:
                self.elevation = value
            elif code == 40:
                self.default_start_width = value
            elif code == 41:
                self.default_end_width = value
            elif code == 70:
                self.flags = value
            elif code == 71:
                self.mcount = value
            elif code == 72:
                self.ncount = value
            elif code == 73:
                self.m_smooth_density = value
            elif code == 73:
                self.n_smooth_density = value
            elif code == 75:
                self.smooth_type = value
        self.mode = get_mode()
        if self.mode == 'spline2d':
            if self.smooth_type == const.POLYMESH_CUBIC_BSPLINE:
                self.spline_type = 'cubic_bspline'
            elif self.smooth_type == const.POLYMESH_QUADRIC_BSPLINE:
                self.spline_type = 'quadratic_bspline'
            elif self.smooth_type == const.POLYMESH_BEZIER_SURFACE:
                self.spline_type = 'bezier_curve'  # is this a valid spline type for DXF12?
        self.is_mclosed = bool(self.flags & const.POLYLINE_MESH_CLOSED_M_DIRECTION)
        self.is_nclosed = bool(self.flags & const.POLYLINE_MESH_CLOSED_N_DIRECTION)
        self.is_closed = self.is_mclosed
        self.set_default_extrusion()

    def __len__(self):
        return len(self.vertices)

    def __getitem__(self, item):
        return self.vertices[item]

    def __iter__(self):
        return iter(self.vertices)

    def append_data(self, vertices):
        def default_width(start_width, end_width):
            if start_width == 0.:
                start_width = self.default_start_width
            if end_width == 0.:
                end_width = self.default_end_width
            return start_width, end_width

        self.vertices = vertices
        if self.mode in Polyline.LINE_TYPES:
            for vertex in self.vertices:
                if vertex.flags & const.VTX_SPLINE_FRAME_CONTROL_POINT:
                    self.controlpoints.append(vertex.location)
                else:
                    self.points.append(vertex.location)
                    self.width.append(default_width(vertex.start_width, vertex.end_width))
                    self.bulge.append(vertex.bulge)
                    self.tangents.append(vertex.tangent if vertex.flags & const.VTX_CURVE_FIT_TANGENT else None)

    def cast(self):
        if self.mode == 'polyface':
            return PolyFace(self)
        elif self.mode == 'polymesh':
            return PolyMesh(self)
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


class PolyShape(object):
    def __init__(self, polyline, dxftype):
        # copy all dxf attributes from polyline
        for key, value in polyline.__dict__.items():
            self.__dict__[key] = value
        self.dxftype = dxftype


class PolyFace(PolyShape):
    def __init__(self, polyline):
        VERTEX_FLAGS = const.VTX_3D_POLYFACE_MESH_VERTEX + const.VTX_3D_POLYGON_MESH_VERTEX

        def is_vertex(flags):
            return flags & VERTEX_FLAGS == VERTEX_FLAGS

        super(PolyFace, self).__init__(polyline, 'POLYFACE')
        vertices = []
        face_records = []
        for vertex in polyline.vertices:
            (vertices if is_vertex(vertex.flags) else face_records).append(vertex)

        self._face_records = face_records

    def __getitem__(self, item):
        return SubFace(self._face_records[item], self.vertices)

    def __len__(self):
        return len(self._face_records)

    def __iter__(self):
        return (SubFace(f, self.vertices) for f in self._face_records)


class PolyMesh(PolyShape):
    def __init__(self, polyline):
        super(PolyMesh, self).__init__(polyline, 'POLYMESH')

    def __iter__(self):
        return iter(self.vertices)

    def get_location(self, pos):
        return self.get_vertex(pos).location

    def get_vertex(self, pos):
        m, n = pos
        if 0 <= m < self.mcount and 0 <= n < self.ncount:
            pos = m * self.ncount + n
            return self.vertices[pos]
        else:
            raise IndexError(repr(pos))


class Vertex(DXFEntity):
    def __init__(self):
        super(Vertex, self).__init__()
        self.location = (0., 0., 0.)
        self.flags = 0
        self.start_width = 0.
        self.end_width = 0.
        self.bulge = 0.
        self.tangent = None
        self.vtx = None

    def setup_attributes(self, tags):
        vtx0 = 0
        vtx1 = 0
        vtx2 = 0
        vtx3 = 0
        for code, value in super(Vertex, self).setup_attributes(tags):
            if code == 10:
                self.location = value
            elif code == 40:
                self.start_width = value
            elif code == 41:
                self.end_width = value
            elif code == 50:
                self.tangent = value
            elif code == 71:
                vtx0 = value
            elif code == 72:
                vtx1 = value
            elif code == 73:
                vtx2 = value
            elif code == 74:
                vtx3 = value
        indices = (vtx0, vtx1, vtx2, vtx3)
        if any(indices):
            self.vtx = indices

    def __getitem__(self, item):
        return self.location[item]

    def __iter__(self):
        return iter(self.location)


class Block(DXFEntity):
    pass


class LWPolyline(DXFEntity):
    pass


class Ellipse(DXFEntity):
    pass


class Ray(DXFEntity):
    pass


class XLine(DXFEntity):
    pass


class Spline(DXFEntity):
    pass


class Helix(DXFEntity):
    pass


class MText(DXFEntity):
    pass


class Mesh(DXFEntity):
    pass


class Light(DXFEntity):
    pass


class Body(DXFEntity):
    pass


class Solid3d(DXFEntity):
    pass


class Surface(DXFEntity):
    pass


EntityTable = {
    'LINE': Line,
    'POINT': Point,
    'CIRCLE': Circle,
    'ARC': Arc,
    'TRACE': Trace,
    'SOLID': Solid,
    '3DFACE': Face,
    'TEXT': Text,
    'INSERT': Insert,
    'SEQEND': DXFEntity,
    'ATTRIB': Attrib,
    'ATTDEF': Attrib,
    'POLYLINE': Polyline,
    'VERTEX': Vertex,
    'BLOCK': Block,
    'ENDBLK': DXFEntity,
    'LWPOLYLINE': LWPolyline,
    'ELLIPSE': Ellipse,
    'RAY': Ray,
    'XLINE': XLine,
    'SPLINE': Spline,
    'HELIX': Helix,
    'MTEXT': MText,
    'MESH': Mesh,
    'LIGHT': Light,
    'BODY': Body,
    'REGION': Body,
    '3DSOLID': Solid3d,
    'SURFACE': Surface,
    'PLANESURFACE': Surface,
}


def entity_factory(tags):
    dxftype = tags.get_type()
    cls = EntityTable.get(dxftype, DXFEntity)  # get entity class
    entity = cls()  # call constructor
    list(entity.setup_attributes(tags))  # setup dxf attributes - chain of generators
    if hasattr(entity, 'cast'):
        entity = entity.cast()
    return entity

