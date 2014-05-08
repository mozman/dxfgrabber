#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 21.07.2012
# License: MIT License

import os
from setuptools import setup
from setuptools import Extension

VERSION = "0.7.2"
AUTHOR_NAME = 'Manfred Moitzi'
AUTHOR_EMAIL = 'mozman@gmx.at'

try:
    from Cython.Distutils import build_ext
    ext_modules = [
        Extension("dxfgrabber.cytags", ["dxfgrabber/cytags.pyx", ]),
        Extension("dxfgrabber.cydxfentity", ["dxfgrabber/cydxfentity.pyx", ])
    ]
    commands = {'build_ext': build_ext}
except ImportError:
    print("Install Cython to get the speed optimized version of dxfgrabber.")
    ext_modules = []
    commands = {}


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname


setup(name='dxfgrabber',
      version=VERSION,
      description='A Python library to grab information from DXF drawings - all DXF versions supported.',
      author=AUTHOR_NAME,
      url='http://bitbucket.org/mozman/dxfgrabber',
      download_url='http://bitbucket.org/mozman/dxfgrabber/downloads',
      author_email=AUTHOR_EMAIL,
      packages=['dxfgrabber'],
      provides=['dxfgrabber'],
      keywords=['DXF', 'CAD'],
      cmdclass=commands,
      ext_modules=ext_modules,
      long_description=read('README.txt') + read('NEWS.txt'),
      platforms="OS Independent",
      license="MIT License",
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Libraries :: Python Modules", ]
)
