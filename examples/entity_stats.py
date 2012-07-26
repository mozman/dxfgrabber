#!/usr/bin/env python
#coding:utf-8
# Purpose: 
# Created: 23.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: GPLv3

__author__ = "mozman <mozman@gmx.at>"

import sys
import os
import time

sys.path.insert(0, os.path.abspath('..'))

import dxfgrabber
from collections import Counter

def print_layers(counter):
    print("used Layers: {}".format(len(counter)))
    for item in sorted(counter.items()):
        print("Layer: {} has {} entities".format(*item))

def main(filename):
    print("reading file: {}".format(filename))
    starttime = time.time()
    dxf = dxfgrabber.readfile(filename)
    endtime = time.time()
    print("time to read: {:.2f}s".format(endtime-starttime))
    print("entities: {:d}".format(len(dxf.entities)))
    print("defined Layers: {}".format(len(dxf.layers)))
    print_layers(Counter(entity.layer for entity in dxf.entities))

if __name__ == '__main__':
    main(sys.argv[1])
