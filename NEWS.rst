
News
====

Version 0.8.1 - 2016-08-17

  * BUGFIX: restored VERTEX bulge values
  * NEW: excepts 'inf.0' and '-inf.0' float values created by QGIS (AutoCAD does not read this none standard values)

Version 0.8.0 - 2016-04-24

  * internal refactoring - removed extra layer for DXF R12 and DXF R13 implementation
  * removed parts implemented in Cython
  * new version is ~30% faster than the old pure Python version but ~15% slower than the version with C-extension
  * some pep8 refactorings, renamed attributes like startparam to start_param

Version 0.7.5 - 2015-11-29

  * Python only version runs with CPython (2.7, 3.4, 3.5), pypy-5.0.0 and pypy3-2.4.0
  * accepts block definitions without explicit base point, defaults to (0, 0, 0)
  * NEW: reads DXF versions older than AC1009 (DXF R12), as far I know, I need more old files for testing
  * KNOWN BUG: Win7 and Python 2.7.10 - can't build Cython extension with MingW32, use Python 2.7.9 instead
  * KNOWN BUG: Win7 and Python 3.5.0 - can't build Cython extension with MingW32 but work with VC2015

Version 0.7.4 - 2014-05-23

  * NEW: added support for R12 2d splines (by POLYLINE); POLYLINE.mode == "spline2d"
  * NEW: TEXT.plain_text(), removes format codes like ``&&u`` and transforms ``%%d`` to ``°``
  * BUGFIX: unicode/str error in Cython extension for Python 2.7
  * BUGFIX: every LWPolyline in DXF version > AC1009 had default thickness of 0.0
  * BUGFIX: Polyline.width had incorrect values

Version 0.7.3 - 2014-05-16

  * NEW: ``options = {"assure_3d_coords": True}``, guarantees (x, y, z) tuples for ALL coordinates, this option is by default
    ``False``
  * NEW: extended TrueColor() class, see docs
  * NEW: dxfgrabber.aci_to_true_color(index) returns the DXF default true color value for AutoCAD Color Index *index*
    as TrueColor()
  * NEW: added is_backwards, is_upside_down, width, oblique, font, bigfont attributes to TEXT, ATTRIB, ATTDEF entities
  * NEW: added plain_text() method to TEXT, ATTRIB and ATTDEF to get text content without formatting codes like '%%u'
  * NEW: added font, bigfont, rect_width, horizontal_width and vertical_height attributes to MTEXT
  * NEW: added resolve_text_styles(text_styles) method to TEXT, ATTRIB, ATTDEF, MTEXT entities
  * NEW: new import option "resolve_text_styles" and it is *True* by default
  * NEW: added extrusion direction to all entities
  * NEW: added row_count, col_count, row_spacing, col_spacing attributes to INSERT.
  * NEW: MText.plain_text(split=False) tries to remove format codes, returns a single string or a list of strings
  * NEW: added n_smooth_density, m_smooth_density, smooth_type to Polymesh
  * NEW: added smooth_type to Polyface
  * CHANGE: LWPolyline again: LWPolyline.points list of (x, y) or (x, y, z) depends on "assure_3d_coords",
    LWPolyline.width list of (start-width, end-width), .bulge list of floats, removed LWPolyline.get_rstrip_points() and
    added .const_width attribute (if != 0, ignore .width list).
  * CHANGE: Polyline method points() is now a field (list) and added lists for width and bulge for consistent APIs of
    LWPolyline and Polyline.
  * BUGFIX: wrong DXF subclass for Arc.extrusion (error in DXF Standard)

Version 0.7.2 - 2014-05-09

  * NEW: grabs SAB data of BODY, 3DSOLID, ... entities for DXF version AC1027 (R2013) and later
  * NEW: support for dxf attributes: true_color (AC1018), transparency (AC1018), shadow_mode (AC1021)
    in prior DXF versions this attributes are set to None.
  * NEW: using Cython for some speed optimizations, but Cython is not a installation requirement; control the Cython
    extension by environment variable DXFGRABBER_CYTHON = ON|OFF, by default the Cython extension is activated.
  * CHANGED: LWPolyline.points are always 5-tuples (x, y, start_width, end_width, bulge)

Version 0.7.1 - 2014-05-02

  * BUGFIX: now really accept floats as int (thanks to ProE)

Version 0.7.0 - 2014-05-01

  * NEW: support for MESH entity
  * NEW: support for LIGHT entity
  * NEW: support for SUN entity
  * NEW: support for HELIX entity
  * NEW: support for BODY entity, you get the ACIS code
  * NEW: support for 3DSOLID entity, you get the ACIS code
  * NEW: support for REGION entity, you get the ACIS code
  * NEW: support for SURFACE entity, you get the ACIS code
  * NEW: support for undocumented PLANESURFACE entity, you get the ACIS code
  * BUGFIX: accept floats as int (thanks to ProE)

Version 0.6.1 - 2014-04-25

  * BUGFIX: support for undocumented VERTEX subclass 'AcDbFaceRecord' without preceding 'AcDbVertex'
  * extended the Polyface entity, see new docs

Version 0.6.0 - 2014-01-09

  * skip comment tags (999)
  * dxfversion defaults to 'AC1009', if no header variable $ACADVER exists
  * can open minimalistic DXF12 files (without HEADER, TABLES and BLOCKS section)
  * added support for STYLE table
  * added support for LTYPE table

Version 0.5.2 - 2013-05-20

  * bugfix: fixed \*nix newline problem in readfile_as_asc()

Version 0.5.1 - 2013-05-20

  * updated docs - added a *Howto* section
  * added attribute frozen to class Layer()
  * index operator for: Drawing.layers[layername]
  * added modelspace() and paperspace() iterators to class Drawing()
  * supported Python versions: CPython 2.7, CPython 3.3, pypy - no explicit testing with CPython 3.2

Version 0.5.0 - 2013-05-04

  * beta status
  * solved problems with 'utf-8' and codepage ANSI_936 encoded dxf files

Version 0.4.0 - 2012-08-12

  * beta status

Version 0.1.0 - 2012-07-21

  * Initial setup
