# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_siemens.py

"""
..  module:: test_import_rdsr_toshiba_multivaluesd
    :synopsis: Test module for safe handling of illegal multi-value in SD value

..  moduleauthor:: Ed McDonagh
"""

import os
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings


class ImportToshibaWithVariableHelicalPitch(TestCase):
    """Test module for safe handling of illegal multi-value in SD value

    """
    def test_dose_check_import(self):
        """Imports a Toshiba RDSR with variable helical pitch with illegal string in DS field

        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/CT-RDSR-Toshiba_MultiValSD.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]
        self.assertEqual(study.series_instance_uid, "1.3.6.1.4.1.5962.99.1.1042634278.1704769588.1538640959014.8.0")
