# This Python file uses the following encoding: utf-8
# test_export_mammo_csv.py

import os
from decimal import Decimal
from django.test import TestCase, RequestFactory
from remapp.extractors import mam
from remapp.exports.exportcsv import exportMG2excel
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings
from remapp.tools.hash_id import hash_id

class ExportMammoCSV(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_export_no_ascii(self):
        """

        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/MG-Im-GE-SenDS-scaled.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)
        studies = GeneralStudyModuleAttr.objects.all()

        request = self.factory.get('/openrem/exportmgcsv1/0/0/?')


