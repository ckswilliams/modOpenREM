#!/usr/local/bin/python
# scripts/openrem_rdsr

"""Script to launch the rdsr to import information from DICOM Radiation SR objects 

    :param filename: relative or absolute path to Radiation Dose Structured Report.
    :type filename: str.

    Tested with:
        * CT: Siemens, Philips and GE RDSR, GE Enhanced SR.
        * Fluoro: Siemens Artis Zee RDSR
"""

import sys,os

# This section attempts to place the openrem folder onto the python path
# so that openrem.settings can be found.
sitepaths = []
openrempathset=0
for paths in sys.path:
    if paths.endswith('site-packages'):
        sitepaths.append(paths)
    if paths.endswith('openrem'):
        openrempathset = 1
        
if sitepaths and not openrempathset:
    for paths in sitepaths:
        sys.path.insert(1,os.path.join(paths,'openrem'))

from remapp.extractors import rdsr

if len(sys.argv) != 2:
    sys.exit('Error: Supply exactly one argument - the radiation dose structured report')

sys.exit(rdsr(sys.argv[1]))
