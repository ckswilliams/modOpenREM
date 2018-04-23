#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
# scripts/openrem_qr

"""Script to launch the DICOM Store SCP service

"""

import sys
from openrem.remapp.netdicom.qrscu import qrscu_script

sys.exit(qrscu_script())
