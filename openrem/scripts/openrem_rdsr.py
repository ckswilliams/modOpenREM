#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
# scripts/openrem_rdsr

"""Script to launch the rdsr to import information from DICOM Radiation SR objects 

    :param filename: relative or absolute path to Radiation Dose Structured Report.
    :type filename: str.

    Tested with:
        * CT: Siemens, Philips and GE RDSR, GE Enhanced SR.
        * Fluoro: Siemens Artis Zee RDSR
"""

import sys
import os
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from glob import glob
from remapp.extractors.rdsr import rdsr

if len(sys.argv) < 2:
    sys.exit(u'Error: Supply at least one argument - the radiation dose structured report')

for arg in sys.argv[1:]:
    for filename in glob(arg):
        rdsr(filename)

sys.exit()
