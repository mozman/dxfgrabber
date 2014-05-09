# Author:  mozman -- <mozman@gmx.at>
# Purpose: test option "assure_3d_coords", which guarantees (x, y, z) tuples for ALL coordinates
# Created: 04.05.2014
# Copyright (C) 2014, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

import unittest
import os

import dxfgrabber


filename = os.path.join(os.path.dirname(__file__), "assure_3d_coords.dxf")
DWG = dxfgrabber.readfile(filename, {"assure_3d_coords": True})

pcoords = [(1., 1., 0.), (-3., 2., 0.), (7., -1., 0.), (10., 10., 0.)]


class TestAssure3dCoords(unittest.TestCase):
    def test_line(self):
        line = [e for e in DWG.entities if e.dxftype == 'LINE'][0]
        self.assertEqual((1., 1., 0.), line.start)
        self.assertEqual((2., 2., 0.), line.end)

    def test_circle(self):
        circle = [e for e in DWG.entities if e.dxftype == 'CIRCLE'][0]
        self.assertEqual((12., 24., 0.), circle.center)

    def test_lwpolyline(self):
        # LWPOLYLINE can not return 3d coordinates (x, y, start_width, end_width, bulge)
        lwpolyline = [e for e in DWG.entities if e.dxftype == 'LWPOLYLINE'][0]
        self.assertEqual(pcoords, lwpolyline.points)

    def test_polyline2d(self):
        polyline = [e for e in DWG.entities if e.dxftype == 'POLYLINE'][0]
        self.assertEqual(pcoords, list(polyline.points))


if __name__ == '__main__':
    unittest.main()
