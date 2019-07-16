#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
# scripts/openrem_qr

"""Script to launch the DICOM Store SCP service

"""

import sys
import os
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from remapp.netdicom.qrscu import qrscu_script

sys.exit(qrscu_script())
