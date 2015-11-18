#!/usr/local/bin/python
# scripts/openrem_qr

"""Script to launch the DICOM Store SCP service

    :param id: ID of the store SCP config in the database, obtained from the web interface
    :type id: str

"""

import sys
from openrem.remapp.netdicom.qrscu import qrscu_script

sys.exit(qrscu_script(sys.argv))
