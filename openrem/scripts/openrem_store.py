#!/usr/local/bin/python
# scripts/openrem_store

"""Script to launch the OpenREM built-in DICOM C-Store SCP

    :param filename: relative or absolute path to radiographic DICOM image file.
    :type filename: str.

    Tested with:
        * Nothing yet...

"""

import sys
from openrem.remapp.netdicom.storescp import store

sys.exit(store(sys.argv))
