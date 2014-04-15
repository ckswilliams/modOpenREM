#!/usr/local/bin/python
# scripts/openrem_ctphilips

"""Script to launch the ct_philips module to import information from Philips CT 

    :param filename: relative or absolute path to Philips CT dose report DICOM image file.
    :type filename: str.

    Tested with:
        * Philips Gemini TF PET-CT v2.3.0
        * Brilliance BigBore v3.5.4.17001.
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

from remapp.extractors import ct_philips

if len(sys.argv) < 2:
    sys.exit('Error: Supply at least one argument - the Philips dose report image')

for sr in sys.argv[1:]:
    ct_philips(sr)

sys.exit()
