#!/usr/bin/env python
#coding:utf-8
# Purpose: 
# Created: 21.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from dxfwrite import DXFEngine as dxf

def make_line_data():
    dwg = dxf.drawing('lines.dxf')
    dwg.add(dxf.line((0,0), (1,0)))
    dwg.add(dxf.line((1,0), (1,1)))
    dwg.add(dxf.line((1,1), (0,1)))
    dwg.add(dxf.line((0,1), (0,0)))
    dwg.save()

def make_circle_data():
    dwg = dxf.drawing('circles.dxf')
    dwg.add(dxf.circle(5, (0, 0), layer='mozman'))
    dwg.add(dxf.circle(3, (3, 3), layer='mozman'))
    dwg.save()

def make_polyline_data():
    dwg = dxf.drawing('polyline.dxf')
    dwg.add(dxf.polyline([(0,0), (1,0), (1,1), (0,1)], layer='mozman', color=7))
    dwg.save()

def main():
    make_line_data()
    make_circle_data()
    make_polyline_data()

if __name__ == '__main__':
    main()
