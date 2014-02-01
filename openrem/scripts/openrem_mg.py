#!/usr/local/bin/python
# scripts/openrem_mg

"""Script to launch the mam module to import information from mammography images 

    :param filename: relative or absolute path to mammography DICOM image file.
    :type filename: str.

    Tested with:
        * GE Senographe DS software versions ADS_43.10.1 and ADS_53.10.10 only.

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

from remapp.extractors import mam

if len(sys.argv) != 2:
    sys.exit('Error: Supply exactly one argument - the DICOM mammography image file')

sys.exit(mam(sys.argv[1]))
