#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test layers
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

import unittest

from dxfgrabber.tags import Tags
from dxfgrabber.layers import LayerTable


class DrawingProxy:
    def __init__(self, version):
        self.dxfversion = version


class TestDXF12Layer(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(DXF12LAYERS)
        self.layers = LayerTable(tags, DrawingProxy("AC1009"))

    def test_get_existing_layer(self):
        layer = self.layers.get("VIEW_PORT")
        self.assertEqual("VIEW_PORT", layer.name)

    def test_get_existing_layer_2(self):
        layer = self.layers["VIEW_PORT"]
        self.assertEqual("VIEW_PORT", layer.name)

    def test_contains(self):
        self.assertTrue("VIEW_PORT" in self.layers)
        self.assertTrue("0" in self.layers)
        self.assertTrue("DEFPOINTS" in self.layers)

    def test_get_color(self):
        layer = self.layers.get("VIEW_PORT")
        self.assertEqual(7, layer.color)

    def test_get_linetype(self):
        layer = self.layers.get("VIEW_PORT")
        self.assertEqual("CONTINUOUS", layer.linetype)

    def test_not_existing_layer(self):
        with self.assertRaises(KeyError):
            layer = self.layers.get("LAYER-DOES-NOT-EXIST")

    def test_layernames(self):
        self.assertEqual(3, len(self.layers.layernames()))

    def test_is_on(self):
        layer = self.layers.get("VIEW_PORT")
        self.assertTrue(layer.on)

    def test_is_locked(self):
        layer = self.layers.get("VIEW_PORT")
        self.assertFalse(layer.locked)

    def test_is_frozen(self):
        layer = self.layers.get("VIEW_PORT")
        self.assertFalse(layer.frozen)

class TestDXF13Layer(unittest.TestCase):
    def setUp(self):
        tags = Tags.fromtext(DXF13LAYERS)
        self.layers = LayerTable(tags, DrawingProxy("AC1024"))

    def test_get_existing_layer(self):
        layer = self.layers.get("View Port")
        self.assertEqual("View Port", layer.name)

    def test_get_existing_layer_2(self):
        layer = self.layers["View Port"]
        self.assertEqual("View Port", layer.name)

    def test_contains(self):
        self.assertTrue("View Port" in self.layers)
        self.assertTrue("0" in self.layers)
        self.assertTrue("Defpoints" in self.layers)

    def test_get_color(self):
        layer = self.layers.get("View Port")
        self.assertEqual(7, layer.color)

    def test_get_linetype(self):
        layer = self.layers.get("View Port")
        self.assertEqual("Continuous", layer.linetype)

    def test_not_existing_layer(self):
        with self.assertRaises(KeyError):
            layer = self.layers.get("LAYER-DOES-NOT-EXIST")

    def test_layernames(self):
        self.assertEqual(3, len(self.layers.layernames()))

    def test_is_on(self):
        layer = self.layers.get("View Port")
        self.assertTrue(layer.on)

    def test_is_locked(self):
        layer = self.layers.get("View Port")
        self.assertFalse(layer.locked)

    def test_is_frozen(self):
        layer = self.layers.get("View Port")
        self.assertFalse(layer.frozen)

DXF13LAYERS = """  0
TABLE
  2
LAYER
  5
2
102
{ACAD_XDICTIONARY
360
2A2
102
}
330
0
100
AcDbSymbolTable
 70
     3
  0
LAYER
  5
10
102
{ACAD_XDICTIONARY
360
E6
102
}
330
2
100
AcDbSymbolTableRecord
100
AcDbLayerTableRecord
  2
0
 70
     0
 62
     7
  6
Continuous
370
    -3
390
F
347
98
  0
LAYER
  5
1B4
330
2
100
AcDbSymbolTableRecord
100
AcDbLayerTableRecord
  2
View Port
 70
     0
 62
     7
  6
Continuous
290
     0
370
    -3
390
F
347
98
1001
AcAecLayerStandard
1000

1000
View Ports, set to Not Plot
  0
LAYER
  5
21D
330
2
100
AcDbSymbolTableRecord
100
AcDbLayerTableRecord
  2
Defpoints
 70
     0
 62
     7
  6
Continuous
290
     0
370
    -3
390
F
347
98
  0
ENDTAB
"""

DXF12LAYERS = """  0
TABLE
  2
LAYER
 70
     3
  0
LAYER
  2
0
 70
     0
 62
     7
  6
CONTINUOUS
  0
LAYER
  2
VIEW_PORT
 70
     0
 62
     7
  6
CONTINUOUS
  0
LAYER
  2
DEFPOINTS
 70
     0
 62
     7
  6
CONTINUOUS
  0
ENDTAB
"""
