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


class Insert(DXFEntity):
    pass


class SeqEnd(DXFEntity):
    pass


class Attrib(DXFEntity):
    pass


class AttDef(DXFEntity):
    pass


class Polyline(DXFEntity):
    pass


class Vertex(DXFEntity):
    pass


class Block(DXFEntity):
    pass


class BlockEnd(DXFEntity):
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


class Sun(DXFEntity):
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
    'SEQEND': SeqEnd,
    'ATTRIB': Attrib,
    'ATTDEF': AttDef,
    'POLYLINE': Polyline,
    'VERTEX': Vertex,
    'BLOCK': Block,
    'ENDBLK': BlockEnd,
    'LWPOLYLINE': LWPolyline,
    'ELLIPSE': Ellipse,
    'RAY': Ray,
    'XLINE': XLine,
    'SPLINE': Spline,
    'HELIX': Helix,
    'MTEXT': MText,
    'SUN': Sun,
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
    return entity

