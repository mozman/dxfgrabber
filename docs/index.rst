.. dxfgrabber documentation master file, created by
   sphinx-quickstart on Mon Aug 13 09:33:38 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dxfgrabber |version| documentation
==================================

last updated |today|.

*dxfgrabber* is a Python library to grab information from DXF drawings - all DXF versions supported.

Python compatibility: *dxfgrabber* is tested with CPython 2.7, CPython3.4 and PyPy.

License: *dxfgrabber* is licensed under the MIT license.

simple usage::

    dxf = dxfgrabber.readfile("drawing.dxf")
    print("DXF version: {}".format(dxf.dxfversion))
    header_var_count = len(dxf.header) # dict of dxf header vars
    layer_count = len(dxf.layers) # collection of layer definitions
    block_definition_count(len(dxf.blocks)) #  dict like collection of block definitions
    entitiy_count = len(dxf.entities) # list like collection of entities

Read DXF files
==============

.. function:: readfile(filename[, options=None])

    Read DXF file `filename` from the file system, and returns an object
    :class:`Drawing`. `options` is a dict with options for reading DXF files.

.. function:: read(stream[, options=None])

    Like :func:`readfile`, but reads the DXF data from a `stream`. `stream`
    only requires a method :meth:`readline()`

Options dict for reading DXF files
----------------------------------

default options::

    DEFAULT_OPTIONS = {
        "grab_blocks": True
    }

================ ==========================================================
key              description
================ ==========================================================
grab_blocks      if ``True`` read block definitions from DXF file, else the
                 dict :attr:`Drawing.blocks` is empty.
================ ==========================================================



Drawing Content
===============

.. class:: Drawing

    Contains all collected data from the DXF file.

.. attribute:: Drawing.dxfversion

    DXF version as *string*.

    =========== ===============
    DXF         AutoCAD Version
    =========== ===============
    ``AC1009``  AutoCAD R12
    ``AC1015``  AutoCAD R2000
    ``AC1018``  AutoCAD R2004
    ``AC1021``  AutoCAD R2007
    ``AC1024``  AutoCAD R2010
    ``AC1027``  AutoCAD R2013
    =========== ===============

.. attribute:: Drawing.encoding

    content encoding, default is ``cp1252``

.. attribute:: Drawing.filename

    *filename* if read from a file.

.. attribute:: Drawing.header

    Contains all the DXF header vars in a *dict* like object.
    For explanation of DXF header vars and their content see the DXF
    specifications from `Autodesk`_. Header var content are basic Python types
    like *string*, *int*, and *float* as simple types and *tuples of float values*
    for 2D- and 3D points.

.. attribute:: Drawing.layers

    Contains all layer definitions in an object of type :class:`LayerTable`.

.. attribute:: Drawing.styles

    Contains all text style definitions in an object of type :class:`StyleTable`.

.. attribute:: Drawing.linetypes

    Contains all linetype definitions in an object of type :class:`LinetypeTable`.

.. attribute:: Drawing.blocks

    Contains all block definitions in a *dict* like object of type :class:`BlocksSection`.

.. attribute:: Drawing.entities

    Contains all drawing entities in a *list* like object of type :class:`EntitySection`.

.. attribute:: Drawing.objects

    Contains DXF objects from the objects section in a *list* like object of type :class:`EntitySection`.

.. method:: Drawing.modelspace()

    Iterate over all DXF entities in *modelspace*.

.. method:: Drawing.paperspace()

    Iterate over all DXF entities in *paperspace*.

Layer Table
-----------

.. class:: LayerTable

    Contains all layer definitions as objects of type :class:`Layer`.

.. method:: LayerTable.get(name)

    Return layer *name* as object of type :class:`Layer`. Raises *KeyError*

.. method:: LayerTable.__getitem__(name)

    Support for index operator: :code:`dwg.layers[name]`

.. method:: LayerTable.names(name)

    Returns a sorted list of all layer names.

.. method:: LayerTable.__iter__()

    Iterate over all layers, yields :class:`Layer` objects.

.. method:: LayerTable.__len__()

    Returns count of layers, support for standard :func:`len()` function.

Layer
-----

.. class:: Layer

.. attribute:: Layer.name

    Layer name as *string*

.. attribute:: Layer.color

    Layer color as *int* in range 1 to 255.

.. attribute:: Layer.linetype

    Layer linetype as *string*.

.. attribute:: Layer.locked

    type is *bool*

.. attribute:: Layer.frozen

    type is *bool*

.. attribute:: Layer.on

    type is *bool*

Style Table
-----------

.. class:: StyleTable

    Contains all text style definitions as objects of type :class:`Style`.

.. method:: StyleTable.get(name)

    Return text style *name* as object of type :class:`Style`. Raises *KeyError*

.. method:: StyleTable.__getitem__(name)

    Support for index operator: :code:`dwg.styles[name]`

.. method:: StyleTable.names(name)

    Returns a sorted list of all text style names.

.. method:: StyleTable.__iter__()

    Iterate over all text styles, yields :class:`Style` objects.

.. method:: StyleTable.__len__()

    Returns count of text styles, support for standard :func:`len()` function.

Style
-----

.. class:: Style

**TODO**

Linetype Table
--------------

.. class:: LinetypeTable

    Contains all linetype definitions as objects of type :class:`Linetype`.

.. method:: LinetypeTable.get(name)

    Return linetype *name* as object of type :class:`Linetype`. Raises *KeyError*

.. method:: LinetypeTable.__getitem__(name)

    Support for index operator: :code:`dwg.linetypes[name]`

.. method:: LinetypeTable.names(name)

    Returns a sorted list of all linetype names.

.. method:: LinetypeTable.__iter__()

    Iterate over all linetypes, yields :class:`Linetype` objects.

.. method:: LinetypeTable.__len__()

    Returns count of linetypes, support for standard :func:`len()` function.

Linetype
--------

.. class:: Linetype

**TODO**

Blocks Section
--------------

.. class:: BlocksSection

    Contains all block definitions as objects of type :class:`Block`.

.. method:: BlocksSection.__len__()

    Returns count of blocks, support for standard :func:`len()` function.

.. method:: BlocksSection.__iter__()

    Iterates over blocks, yields :class:`Block` objects.

.. method:: BlocksSection.__contains__(self, name)

   Returns ``True`` if a block *name* exists, support for standard ``in``
   operator.

.. method:: BlocksSection.__getitem__(name)

   Returns block *name*, support for the index operator: :code:`block = dwg.blocks[name]`.
   Raises *KeyError*

.. method:: BlocksSection.get(name[, default=None])

   Returns block *name* if exists or *default*.

Entity Section
--------------

.. class:: EntitySection

    Contains all drawing entities.

.. method:: EntitySection.__len__()

    Returns count of entities, support for standard :func:`len()` function.

.. method:: EntitySection.__iter__()

    Iterates over all entities.

.. method:: EntitySection.__getitem__(index)

   Returns entity a location *index*, *slicing* is possible, support for
   the index operator :code:`dwg.entity = entities[index]`. Raises *IndexError*

example for accessing entities::

    dwg = dxfgrabber.readfile('test.dxf')
    all_layer_0_entities = [entity for entity in dwg.entities if entity.layer == '0']


Entity Types
============

Base Class Shape
----------------

.. class:: Shape

    Base class for all drawing entities.

.. attribute:: Shape.paperspace

    ``True`` for *paperspace* and ``False`` for *modelspace*.

.. attribute:: Shape.dxftype

    DXF entity name, like ``CIRCLE`` or ``LINE``

.. attribute:: Shape.layer

    Layer name as *string*

.. attribute:: Shape.linetype

    Linetype as *string* or *None*, *None* means linetype by layer.

.. attribute:: Shape.thickness

    Element thickness as *float*.

.. attribute:: Shape.ltscale

    Linetype scale as *float*

.. attribute:: Shape.invisible

    ``True`` if entity is invisible.

.. attribute:: Shape.color

    Entity color as *int*, where 256 means color by layer and 0 means color by
    block.

.. attribute:: Shape.true_color

    Entity color as 0x00RRGGBB 24-bit integer value, return a :class:`TrueColor`. Value is *None* if not set.

.. attribute:: Shape.transparency

    Entity transparency as float from 0.0 to 1.0, 0.0 is opaque and 1.0 is 100% transparent. Value is *None* if not set.

.. attribute:: Shape.shadow_mode

===== ===========
Value Description
===== ===========
0     Casts and receives shadows
1     Casts shadows
2     Receives shadows
3     Ignores shadows
None  if not set
===== ===========

.. class:: TrueColor(int)

.. method:: TrueColor.rgb()

   Returns a tuple (red, green, blue) each value in range 0 to 255. (255, 255, 255) = white.

Block
-----

.. class:: Block(Shape)

.. attribute:: Block.basepoint

    Base point of block definition as 2D- or 3D point of type *tuple*.

.. attribute:: Block.name

    Block name as *string*

.. attribute:: Block.flags

    Block flags as int, for explanation see the DXF specifications from
    `Autodesk`_ and see also ``Block.is_...`` properties.

.. attribute:: Block.xrefpath

    Path to external reference as *string*

.. attribute:: Block.is_xref

    ``True`` if block is an external reference.

.. attribute:: Block.is_xref_overlay

    ``True`` if block is an external overlay reference.


.. attribute:: Block.is_anonymous

    ``True`` if block is an anonymous block, created by hatch or dimension.

.. method:: Block.__iter__:

    Support for iterator protocol, iterates over all block entities.

.. method:: Block.__getitem__(index):

    Returns block entity at location *index*, *slicing* is supported.

.. method:: Block.__len__():

    Returns count of block entities, support for standard :func:`len()` function.

Line
----

.. class:: Line(Shape)

.. attribute:: Line.start

    Start point of line (x, y[, z]) as *tuple*

.. attribute:: Line.end

    End point of line (x, y[, z]) as *tuple*

Point
-----

.. class:: Point(Shape)

.. attribute:: Point.point

    Location of point (x, y[, z]) as *tuple*

Circle
------

.. class:: Circle(Shape)

.. attribute:: Circle.center

    Location of circle center point (x, y[, z]) as *tuple*

.. attribute:: Circle.radius

    Circle radius as *float*

Arc
----

.. class:: Arc(Shape)

.. attribute:: Arc.center

    Location of arc center point (x, y[, z]) as *tuple*

.. attribute:: arc.radius

    Arc radius as *float*

.. attribute:: arc.startangle

    Arc startangle in degrees as *float*. (full circle = 360 degrees)

.. attribute:: arc.endangle

    Arc endangle in degrees as *float*. (full circle = 360 degrees)

Solid
-----

.. class:: Solid(Shape)

    A solid filled shape with 4 points. For Triangles point 3 and point 4 has
    the same location.

.. attribute:: Solid.points

    *List* of points (x, y[, z]) as *tuple*.

Trace
-----

.. class:: Trace(Solid)

    Same as :class:`Solid`.

Face
-----

.. class:: Face(Trace)

    A solid filled 3D shape with 4 points. For Triangles point 3 and point 4 has
    the same location. *DXF entity 3DFACE*

.. attribute:: Face.points

    *List* of points (x, y, z) as *tuple*.

.. method:: Face.is_edge_invisible(index)

    Returns ``True`` if edge *index* is invisible, index in [0, 1, 2, 3].

Text
----

.. class:: Text(Shape)

.. attribute:: Text.insert

    Location of text (x, y, z) as *tuple*.

.. attribute:: Text.text

    Text content as *string*.

.. attribute:: Text.height

    Text height as *float*

.. attribute:: Text.rotation

    Rotation angle in degrees as *float*. (full circle = 360 degrees)

.. attribute:: Text.style

    Text style name as *string*

.. attribute:: Text.halign

    Horizontal alignment as *int*.

.. attribute:: Text.valign

    Vertical alignment as *int*.

.. attribute:: Text.alignpoint

    Second alignment point as tuple or *None*.

Attrib
------

.. class:: Attrib(Text)

    A text entity, in usual cases attached to a block reference entity
    :class:`Insert`, inherits from :class:`Text`.

.. attribute:: Attrib.tag

    The attribute tag as *string*.

Attdef
------

Same as :class:`Attrib`, but located in a block definition entity
:class:`Block`.

Insert
------

.. class:: Insert(Shape)

.. attribute:: Insert.name

    Name of block definition as *string*.

.. attribute:: Insert.insert

    Location of block reference (x, y, z) as *tuple*.

.. attribute:: Insert.rotation

    Rotation angle in degrees as *float*. (full circle = 360 degrees)

.. attribute:: Insert.scale

    (x, y, z) block scaling as *tuple*, default is (1.0, 1.0, 1.0)

.. attribute:: Insert.attribs

    *List* of :class:`Attrib` entities attached to the :class:`Insert` entity.

.. method:: Insert.find_attrib(tag):

    Get :class:`Attrib` entity by *tag*, returns *None* if not found.

Polyline
--------

.. class:: Polyline(Shape)

    Multiple 2D- or 3D vertices connected by lines. The DXF entity *POLYLINE*
    is also used to define *Polyfaces* and *Polymeshes*, dxfgrabber defines
    separated classes for this entities see: :class:`Polyface` and
    :class:`Polymesh`.

.. attribute:: is_closed

    ``True`` if polyline is closed.

.. method:: Polyline.__getitem__(index)

    Returns vertex *index* as :class:`Vertex` entity. support for
    standard operator ``vertex = polyline[index]``. Raises *IndexError*

.. method:: Polyline.__len__()

    Returns count of vertices.

.. method:: Polyline.__iter__()

    Iterate of all vertices, as :class:`Vertex` entity.

.. method:: Polyline.points()

    Returns a generator over all vertex locations as (x, y, z)-tuple.

Vertex
------

.. class:: Vertex(Shape)

.. attribute:: Vertex.location

    Location as (x, y, z)-tuple.

.. attribute:: Vertex.bulge

    The bulge is the tangent of one fourth the included angle for an arc
    segment, made negative if the arc goes clockwise from the start point to
    the endpoint. A bulge of 0 indicates a straight segment, and a bulge of 1
    is a semicircle. If you have questions ask *Autodesk*.

.. attribute:: Vertex.tangent

    Curve fitting tangent in degrees as *float* or *None*. (full circle = 360
    degrees)

Polyface
--------

.. class:: Polyface(Shape)

    Dxftype is *POLYFACE*, which is a *POLYLINE* DXF entity.

.. attribute:: Polyface.vertices

    List of all :class:`Polyface` vertices a Vertex object.

.. method:: Polyface.__getitem__(index)

    Returns face *index* as :class:`SubFace` object. support for standard operator
    :code:`face = polyface[index]`. Raises *IndexError*

.. method:: Polyface.__len__()

    Returns count of faces.

.. method:: Polyface.__iter__()

    Iterate of all faces, as :class:`SubFace` objects.

SubFace
^^^^^^^

.. class:: SubFace

    A SubFace describes a single face of a :class:`Polyface`.

.. attribute:: SubFace.face_record

    Face record vertex, the basic DXF structure of faces, where you can get the DXF attributes of the face
    like color or linetype: :code:`subface.face_record.color`

.. method:: SubFace.__len__()

    Returns count of vertices 3 or 4.

.. method:: SubFace.__getitem__(pos):

    Returns vertex at index *pos* as :class:`Vertex` object

.. method:: SubFace.__iter__():

    Returns a list of the face vertices as (x, y, z)-tuples.

.. method:: SubFace.indices():

    Returns a list of vertex indices, get vertex by index from :code:`Polyface.vertices[index]`.

.. method:: SubFace.is_edge_visible(pos):

    Returns *True* if face edge *pos* is visible else *False*.


Polymesh
--------

.. class:: Polymesh(Shape)

    Dxftype is *POLYMESH*, which is a *POLYLINE* DXF entity.

    A *Polymesh* is a grid of m x n vertices, where every vertex has its own
    3D location.

.. attribute:: Polymesh.mcount

    Count of vertices in m direction as *int*.

.. attribute:: Polymesh.ncount

    Count of vertices in n direction as *int*.

.. attribute:: Polymesh.is_mclosed

    ``True`` if *Polymesh* is closed in m direction.

.. attribute:: Polymesh.is_nclosed

    ``True`` if *Polymesh* is closed in n direction.

.. method:: Polymesh.get_vertex(pos)

    Returns the :class:`Vertex` at *pos*, where *pos* is a *tuple* (m, n). First
    vertex is (0, 0).

.. method:: Polymesh.get_location(pos)

    Returns the location (x, y, z) as *tuple* at *pos*, where *pos* is a
    *tuple* (m, n). First vertex is (0, 0).

LWPolyline
----------

.. class:: LWPolyline(Shape)

    *LWPolyline* is a lightweight only 2D Polyline.

.. attribute:: LWPolyline.points

    *List* of 2D polyline points (x, y) as *tuple*.

.. attribute:: LWPolyline.is_closed

    ``True`` if the polyline is closed.

.. method:: LWPolyline.__len__()

    Returns the count of polyline points.

.. method:: LWPolyline.__getitem__(index)

    Returns polyline point (x, y) as *tuple* at position *index*, *slicing* is
    supported. Raises *IndexError*

.. method:: LWPolyline.__iter__()

    Iterate over all polyline points (x, y) as *tuple*.

Ellipse
-------

.. class:: Ellipse(Shape)

.. attribute:: Ellipse.center

    Location of ellipse center point (x, y[, z]) as *tuple*

.. attribute:: Ellipse.majoraxis

    End point of major axis (x, y[, z]) as *tuple*

.. attribute:: Ellipse.ratio

    Ratio of minor axis to major axis as *float*.

.. attribute:: Ellipse.startparam

    Start parameter (this value is 0.0 for a full ellipse).

.. attribute:: Ellipse.endparam

    End parameter (this value is 2pi for a full ellipse)

Ray
----

.. class:: Ray(Shape)

.. attribute:: start

    Location of the ray start point (x, y, z) as *tuple*

 .. attribute:: unitvector

    Ray direction as unit vector (x, y, z) as *tuple*

XLine
-----

.. class:: XLine(Ray)

    Same as :class:`Ray`, except a XLine (construction line) has no beginning
    and no end.

Spline
------

.. class:: Spline(Shape)

.. attribute:: Spline.flags

    Binary coded flags, constants stored in :mod:`dxfgrabber.const`.

=============== =====
Spline.flags    value
=============== =====
SPLINE_CLOSED   1
SPLINE_PERIODIC 2
SPLINE_RATIONAL 4
SPLINE_PLANAR   8
SPLINE_LINEAR   16 (a linear spline is also a planar spline)
=============== =====

.. attribute:: Spline.degree

    Degree of the spline curve as *int*

.. attribute:: Spline.starttangent

    Start tangent as (x, y, z) as *tuple* or *None*

.. attribute:: Spline.endtangent

    End tangent as (x, y, z) as *tuple* or *None*

.. attribute:: Spline.controlpoints

    *List* of control points (x, y, z) as *tuple*

.. attribute:: Spline.fitpoints

    *List* of fit points (x, y, z) as *tuple*

.. attribute:: Spline.knots

    *List* of knot values as *float*

.. attribute:: Spline.weights

    *List* of weight values as *float*

.. attribute:: Spline.normalvector

    Normal vector if spline is planar else *None*.

.. attribute:: Spline.is_closed

.. attribute:: Spline.is_periodic

.. attribute:: Spline.is_rational

.. attribute:: Spline.is_planar

.. attribute:: Spline.is_linear

Helix
-----

   3D spiral; Helix is also a :class:`Spline`.

.. class:: Helix(Spline)

.. attribute:: Helix.helix_version

    Tuple (main version, maintainance version)

.. attribute:: Helix.axis_base_point

    Helix axis base point as (x, y, z) as *tuple*.

.. attribute:: Helix.start_point

    Helix start point as (x, y, z) as *tuple*.

.. attribute:: Helix.axis_vector

    Helix axis vector as (x, y, z) as *tuple*.

.. attribute:: Helix.radius

.. attribute:: Helix.turns

    Count of turns.

.. attribute:: Helix.turn_height

    Height of one turn.

.. attribute:: Helix.handedness

    0 = left; 1 = right;

.. attribute:: Helix.constrain

    0 = Constrain turn height; 1 = Constrain turns; 2 = Constrain height

MText
-----


.. class:: MText(Shape)

    Multi line text entity.

.. attribute:: MText.insert

    Location of text (x, y, z) as *tuple*.

.. attribute:: MText.rawtext

    Whole text content as one *string*.

.. attribute:: MText.height

    Text height as *float*

.. attribute:: MText.linespacing

    Text line spacing as *float*, valid from 0.25 to 4.00.

.. attribute:: MText.attachmentpoint

    Text attachment point as *int*.

    ===== ===============
    Value Description
    ===== ===============
    1     Top left
    2     Top center
    3     Top right
    4     Middle left
    5     Middle center
    6     Middle right
    7     Bottom left
    8     Bottom center
    9     Bottom right
    ===== ===============

.. attribute:: MText.style

    Text style name as *string*.

.. attribute:: MText.xdirection

    X-Axis direction vector as (x, y, z) as *tuple*. (unit vector)

.. method:: MText.lines()

    Returns a *list* of lines. It is the :attr:`MText.rawtext` splitted into
    lines by the ``\P`` character.


Sun
---

.. class:: Sun(Entity)

    Sun representation. SUN is not a graphical object and resides in the objects section :attr:`Drawing.objects`.

.. attribute:: Sun.version

.. attribute:: Sun.status

   Boolean value: on/off

.. attribute:: Sun.sun_color

   Light color as ACI color index 1 - 255; 256 = BYLAYER; *None* if unset

.. attribute:: Sun.intensity

.. attribute:: Sun.shadows

   Boolean value

.. attribute:: Sun.date

   A Python standard datetime.datetime object.

.. attribute:: Sun.daylight_savings_time

   Boolean value

.. attribute:: Sun.shadow_type

   0 = Ray traced shadows; 1 = Shadow maps

.. attribute:: Sun.shadow_map_size

.. attribute:: Sun.shadow_softness

Light
-----

.. class:: Light(Shape)

   Defines a light source.

.. attribute:: Light.version

.. attribute:: Light.name

.. attribute:: Light.light_type

   distant = 1; point = 2; spot = 3

.. attribute:: Light.status

   Boolean value: on/off?

.. attribute:: Light.light_color

   Light color as ACI color index 1 - 255; 256 = BYLAYER; *None* if unset

.. attribute:: Light.true_color

   Light color as 24-bit RGB color 0x00RRGGBB, *None* if unset

.. attribute:: Light.plot_glyph

   Boolean value

.. attribute:: Light.intensity

.. attribute:: Light.position

   3D position of the light source as (x, y, z) tuple.

.. attribute:: Light.target

   3D target location of the light, determines the light direction as (x, y, z) tuple.

.. attribute:: Light.attenuation_type

   0 = None; 1 = Inverse Linear; 2 = Inverse Square

.. attribute:: Light.use_attenuation_limits

   Boolean value

.. attribute:: Light.attenuation_start_limit

.. attribute:: Light.attenuation_end_limit

.. attribute:: Light.hotspot_angle

.. attribute:: Light.fall_off_angle

.. attribute:: Light.cast_shadows

   Boolean value

.. attribute:: Light.shadow_type

   0 = Ray traced shadows; 1 = Shadow maps

.. attribute:: Light.shadow_map_size

.. attribute:: Light.shadow_softness

Mesh
----

.. class:: Mesh(Shape)

   3D mesh entity similar to the :class:`Polyface` entity.

.. attribute:: Mesh.version

.. attribute:: Mesh.blend_crease

   Boolean value (on/off)

.. attribute:: Mesh.subdivision_levels

.. attribute:: Mesh.vertices

   List of 3D vertices (x, y, z).

.. attribute:: Mesh.faces

   List of mesh faces as tuples of vertex indices (v1, v2, v3, ...). Indices are 0-based and can
   be used with the mesh.vertex list::

      first_face = mesh.faces[0]
      first_vertex = mesh.vertices[first_face[0]]

.. attribute:: Mesh.edges

   List of mesh edges as 2-tuple of vertex indices (v1, v2). Indices are 0-based and can
   be used with the mesh.vertex list::

      first_edge = mesh.edges[0]
      first_vertex = mesh.vertices[first_edge[0]]

.. attribute:: Mesh.edge_crease_list

   List of float values, one for each edge.

.. method:: Mesh.get_face(index)

   Returns a tuple of 3D points :code:`((x1, y1, z1), (x2, y2, z2), ...)` for face at position *index*.

.. method:: Mesh.get_edge(index)

   Returns a 2-tuple of 3D points :code:`((x1, y1, z1), (x2, y2, z2))` for edge at position *index*.

Body
----

.. class:: Body(Shape)

    ACIS based 3D solid geometry.

.. attribute:: Body.acis

    SAT (Standard ACIS Text) data as list of strings. AutoCAD stores the ACIS data since DXF version AC1027 (R21013) as
    SAB (Standard ACIS Binary) data in the undocumented (2014-05-06) section ACDSDATA and :attr:`~Body.acis` is a binary
    string.

.. attribute:: Body.is_sat

   Is *True* if data is stored as SAT, no guarantee for presence of data, but :attr:`~Body.acis` is a list of strings
   for sure.

.. attribute:: Body.is_sab

   Is *True* if data is stored as SAB and :attr:`~Body.acis` is a binary string.


Region
------

.. class:: Region(Body)

    ACIS based 2D enclosed areas.


3DSolid
-------

.. class:: 3DSolid(Body)

    ACIS based 3D solid geometry.


Surface
-------

.. class:: Surface(Body)

    ACIS based 3D freeform surfaces.


PlaneSurface
------------

.. class:: PlaneSurface(Surface)

    ACIS based 3D plane surfaces.


Howtos
======

Open a DXF file
---------------

Open files from file system::

    dwg = readfile("myfile.dxf")

To read file from a stream use: :func:`read`

Query Header Variables
----------------------

The HEADER section of a DXF file contains the settings of variables associated with the drawing.

Example::

    dxfversion = dwg.header['$ACADVER']

For available HEADER variables and their meaning see: `DXF Reference`_

Query Entities
--------------

All entities of the DXF drawing, independent from *modelspace* or *paperspace*, resides in the :attr:`Drawing.entities`
attribute and is an :class:`EntitySection` object. Iterate over all entities with the ``in`` operator::

    all_lines = [entity for entity in dwg.entities if entity.dxftype == 'LINE']
    all_entities_at_layer_0 = [entity for entity in dwg.entities if entity.layer == '0']

Query Blocks
------------

Block references are just DXF entities called INSERT.

Get all block references for block ``TestBlock``::

    references = [entity for entity in dwg.entities if entity.dxftype == 'INSERT' and entity.name == 'TestBlock']


See available attributes for the :class:`Insert` entity.

To examine the Block content, get the block definition from the blocks section::

    test_block = dwg.blocks['TestBlock']

and use the ``in`` operator (Iterator protocol)::

    circles_in_block = [entity for entity in test_block if entity.dxftype == 'CIRCLE']

Layers
------

Layers are nothing special, they are just another attribute of the DXF entity, *dxfgrabber* stores the layer as a
simple *string*. The DXF entitiy can inherit some attributes from the layer: *color, linetype*

To get the real value of an attribute value == *BYLAYER*, get the layer definition::

    layer = dwg.layers[dxf_entity.layer]
    color = layer.color if dxf_entity.color == dxfgrabber.BYLAYER else dxf_entity.color
    linetype = layer.linetype if dxf_entity.linetype is None else dxf_entity.linetype

Layers can be :attr:`~Layer.locked` (if ``True`` else *unlocked*), :attr:`~Layer.on` (if ``True`` else *off*) or
:attr:`~Layer.frozen` (if ``True`` else *thawed*).

Layouts (Modelspace or Paperspace)
----------------------------------

*dxfgrabber* just supports the :attr:`~Shape.paperspace` attribute, it is not possible to examine in which layout a
paperspace object resides (DXF12 has only one paperspace).

Get all *modelspace* entities::

    modelspace_entities = [entity for entity in dwg.entities if not entity.paperspace]

shortcuts since 0.5.1::

    modelspace_entities = list(dwg.modelspace())
    paperspace_entities = list(dwg.paperspace())

.. _Autodesk: http://usa.autodesk.com/adsk/servlet/item?siteID=123112&id=12272454&linkID=10809853
.. _DXF Reference: http://docs.autodesk.com/ACD/2014/ENU/index.html?url=files/GUID-235B22E0-A567-4CF6-92D3-38A2306D73F3.htm,topicNumber=d30e652301
