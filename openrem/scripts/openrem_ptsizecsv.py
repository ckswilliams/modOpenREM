#!/usr/local/bin/python
# scripts/openrem_ptsizecsv

"""Script to launch the rdsr to import information from DICOM Radiation SR objects 

    :param filename: relative or absolute path to Radiation Dose Structured Report.
    :type filename: str.

    Tested with:
        * CT: Siemens, Philips and GE RDSR, GE Enhanced SR.
        * Fluoro: Siemens Artis Zee RDSR
"""

import sys,os

# This section places the openrem folder onto the python path
# so that openrem.settings can be found.

sitepaths = []
openrempathset=0
therealready = os.path.join('site-packages','openrem')

for paths in sys.path:
    if paths.endswith('site-packages'):
        sitepaths.append(paths)
    if paths.endswith(therealready):
        openrempathset = 1

if sitepaths and not openrempathset:
    for paths in sitepaths:
        sys.path.insert(1,os.path.join(paths,'openrem'))

from remapp.extractors import ptsizecsv2db

sys.exit(ptsizecsv2db.csv2db(sys.argv))
