#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
# scripts/openrem_store

"""Script to launch the DICOM Store SCP service

    :param id: ID of the store SCP config in the database, obtained from the web interface
    :type id: str

"""

import sys
from openrem.remapp.netdicom import storescp

if len(sys.argv) != 2:
    sys.exit(u'Error: Supply at one argument - the ID of the SCP configuration from the web interface')

try:
    print "Starting OpenREM Store SCP. Kill with control-c"
    storescp.web_store(store_pk=sys.argv[1])
except KeyboardInterrupt:
    storescp._interrupt(store_pk=sys.argv[1])
except:
    sys.exit(0)
