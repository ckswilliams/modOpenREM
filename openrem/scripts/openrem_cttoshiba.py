#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
# scripts/openrem_rdsr_toshiba_ct_from_dose_images

"""Script to launch the ct_toshiba module to import information from
   Toshiba CT dose images and additional information from image tags.

    :param folder_name: absolute path to Toshiba CT study DICOM files.
    :type filename: str.

    Tested with:
        * Toshiba Aquilion CXL software version V4.40ER011
        * Toshiba Aquilion CX  software version V4.51ER014
        * Toshiba Aquilion CXL software version V4.86ER008

"""

import sys
from glob import glob
from openrem.remapp.extractors.ct_toshiba import ct_toshiba

if len(sys.argv) < 2:
    sys.exit('Error: supply at least one argument - the folder containing the DICOM objects')

for arg in sys.argv[1:]:
    for folder_name in glob(arg):
        ct_toshiba(folder_name)

sys.exit()
