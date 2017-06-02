# This Python file uses the following encoding: utf-8
# test_test_import_esr_ge.py

import os, datetime
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import ct_philips
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTPhilipsSC(TestCase):
    """
    Class for testing Philips SC Dose Info series
    """
    def test_missing_time_stamps(self):
        """
        Imports known Philips Secondary Capture object. Initially just checks it is imported as the missing
        time stamps caused the import to fail before the issue #500 changes
        """
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        philips_sc = "test_files/CT-SC-Philips_Brilliance16P.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        philips_sc_path = os.path.join(root_tests, philips_sc)

        ct_philips(philips_sc_path)
        studies = GeneralStudyModuleAttr.objects.all()

        # Test that two studies have been imported
        self.assertEqual(studies.count(), 1)

