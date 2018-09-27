#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
# scripts/openrem_dx

"""Script to launch the mam module to import information from radiographic images

    :param filename: relative or absolute path to radiographic DICOM image file.
    :type filename: str.

    Example::

        openrem_dx.py dximage.dcm

"""

import sys
from glob import glob
from openrem.remapp.extractors.dx import dx

if len(sys.argv) < 2:
    sys.exit(u'Error: Supply at least one argument - the DICOM radiography image file')

for arg in sys.argv[1:]:
    for filename in glob(arg):
        dx(filename)

sys.exit()
