.. dxfgrabber documentation master file, created by
   sphinx-quickstart on Mon Aug 13 09:33:38 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dxfgrabber |version| documentation
==================================

last updated |today|.

*dxfgrabber* is a Python library to grab information from DXF drawings - all DXF versions supported.

Python compatibility: *dxfgrabber* can be used with CPython 2.7, CPython 3.2+ and PyPy.

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

    like :func:`readfile`, but reads the DXF data from a stream. `stream`
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

    =========== =========================
    DXF         AutoCAD Version
    =========== =========================
    ``AC1009``  AutoCAD R12
    ``AC1015``  AutoCAD R2000
    ``AC1018``  AutoCAD R2004
    ``AC1021``  AutoCAD R2007
    ``AC1024``  AutoCAD R2010 up to R2013
    =========== =========================

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

    Contains all layer definitions in a object of type :class:`LayerTable`.

.. attribute:: Drawing.blocks

    Contains all block definitions in a *dict* like object of type :class:`BlocksSection`.

.. attribute:: Drawing.entities

    Contains all drawing entities in a *list* like object of type :class:`EntitySection`.

Layer Table
-----------

.. class:: LayerTable

    Contains all layer definitions as objects of type :class:`Layer`.

.. method:: LayerTable.get(name)

    Return layer *name* as object of type :class:`Layer`. Raises *IndexError*

.. method:: LayerTable.layernames(name)

    Returns a sorted list of all layer names.

.. method:: LayerTable.__iter__()

    Support for iterator protocol

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

.. attribute:: Layer.on

    type is *bool*


Blocks Section
--------------

.. class:: BlocksSection

    Contains all block definitions as objects of type :class:`Block`.

.. method:: BlocksSection.__len__()

    Returns count of blocks, support for standard :func:`len()` function.

.. method:: BlocksSection.__iter__()

    Support for iterator protocol, iterates over blocks not block names!

.. method:: BlocksSection.__contains__(self, name)

   Returns ``True`` if a block *name* exists, support for standard ``in``
   operator.

.. method:: BlocksSection.__getitem__(name)

   Returns block *name*, support for standard operator
   ``block = blocks[name]``. Raises *KeyError*

.. method:: BlocksSection.get(name[, default=None])

   Returns block *name* if exists or *default*.

Entity Section
--------------

.. class:: EntitySection

    Contains all drawing entities.

.. method:: EntitySection.__len__()

    Returns count of entities, support for standard :func:`len()` function.

.. method:: EntitySection.__iter__()

    Support for iterator protocol, iterates over all entities.

.. method:: EntitySection.__getitem__(index)

   Returns entity a location *index*, *slicing* is possible, support for
   standard operator ``entity = entities[index]``. Raises *IndexError*

example for accessing entities::

    dwg = dxfgrabber.readfile('test.dxf')
    all_layer_0_entities = [entity for entity in dwg.entities if entity.layer == '0']


Entity Types
============

Base Class Shape
----------------

.. class:: Shape

    Base class for all drawing entities.

.. attribute:: Shape.dxftype

    DXF entity name, like ``CIRCLE`` or ``LINE``

.. attribute:: Shape.layer

    Layer name as *string*

.. attribute:: Shape.linetype

    Linetype as *string* or *None*, *None* means linetype by layer.

.. attribute:: Shape.ltscale

    Linetype scale as *float*

.. attribute:: Shape.invisible

    ``True`` if entity is invisible.

.. attribute:: Shape.color

    Entity color as *int*, where 256 means color by layer and 0 means color by
    block.

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

    Returns a generator over all vertex locations (x, y, z) as *tuple*.

Vertex
------

.. class:: Vertex(Shape)

.. attribute:: Vertex.location

    Location (x, y, z) as *tuple*.

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

.. method:: Polyface.__getitem__(index)

    Returns face *index* as *SubFace*. support for standard operator
    ``face = polyface[index]``. Raises *IndexError*

.. method:: Polyface.__len__()

    Returns count of faces.

.. method:: Polyface.__iter__()

    Iterate of all faces, as *SubFaces*.

SubFace
^^^^^^^

A SubFace is a *list* of :class:`Vertex`, as part of a :class:`Polyface`, the
location of a vertex of a SubFace is: ``subface[index].location``

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


.. _Autodesk: http://usa.autodesk.com/adsk/servlet/item?siteID=123112&id=12272454&linkID=10809853
