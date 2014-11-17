#!/usr/local/bin/python
# scripts/openrem_dx

"""Script to launch the mam module to import information from radiographic images 

    :param filename: relative or absolute path to radiographic DICOM image file.
    :type filename: str.

    Tested with:
        * Nothing yet...

"""

import sys
from glob import glob
from openrem.remapp.extractors import dx

if len(sys.argv) < 2:
    sys.exit('Error: Supply at least one argument - the DICOM radiography image file')

for arg in sys.argv[1:]:
    for filename in glob(arg):
        dx(filename)
    
sys.exit()
