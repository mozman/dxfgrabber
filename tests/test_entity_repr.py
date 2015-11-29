# Created: 17.08.15
# License: MIT License
from __future__ import unicode_literals
import traceback
import sys

__author__ = "phistrom <phillip+dxfgrabber@stromberg.me>"

import dxfgrabber
import os
from stress_test import all_files
import unittest
import tempfile


@unittest.skip  # runs too long
class TestEntityRepr(unittest.TestCase):
    """
    Tests to make sure all classes in the entities module do not raise an exception when converted to a human-readable
    string. This generates an approximately 38MB text file when using the CADKit sample DXFs.
    """
    def test_entity_repr(self):
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as outfile:
            print("Writing all entities as human-readable strings to %s" % outfile.name)
            for filename in all_files:
                print("Printing all entities in %s to %s" % (filename, outfile.name))
                self.print_all_entity_reprs(filename, outfile)
            print("Finished printing entities")
        os.remove(outfile.name)  # deletes the temporary file manually at the end so you can examine the output

    @staticmethod
    def print_all_entity_reprs(filename, output):
        dxf = dxfgrabber.readfile(filename)
        all_entities = [entity for entity in dxf.entities]
        for block in dxf.blocks:
            for entity in block:
                all_entities.append(entity)
        for e in all_entities:
            if sys.version_info[0] == 2:
                value = str(e).decode('utf-8') + "\t" + repr(e).decode('utf-8')
            else:
                value = str(e) + "\t" + repr(e)
            output.write(value.encode('utf-8'))
            output.write(os.linesep.encode())
