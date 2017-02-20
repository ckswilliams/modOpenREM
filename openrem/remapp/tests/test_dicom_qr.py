# This Python file uses the following encoding: utf-8
# test_dicom_qr.py

import os
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings


class DicomQR(TestCase):
    def test_response_sorting_ct_philips_with_desc(self):
        """
        Imports a known RDSR file derived from a Siemens Definition Flash and tests that patient IDs are stored when
        requested.
        """
        pass
