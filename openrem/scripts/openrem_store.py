#!/usr/local/bin/python
# scripts/openrem_store

"""Script to launch the DICOM Store SCP service

    :param id: ID of the store SCP config in the database, obtained from the web interface
    :type id: str

"""

import sys
from openrem.remapp.netdicom import storescp

if len(sys.argv) != 2:
    sys.exit('Error: Supply at one argument - the ID of the SCP configuration from the web interface')

sys.exit(storescp.web_store(store_pk=sys.argv))
