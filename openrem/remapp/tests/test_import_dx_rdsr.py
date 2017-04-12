# This Python file uses the following encoding: utf-8
# test_import_mam.py

import os
import datetime
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import mam
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportDXRDSR(TestCase):
    def test_import_dx_rdsr_canon(self):
        """
        Imports a known mammography image file derived from a GE Senographe DS image, and tests the values
        imported against those expected.
        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/MG-Im-GE-SenDS-scaled.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)
        study = GeneralStudyModuleAttr.objects.all()[0]

