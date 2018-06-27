# This Python file uses the following encoding: utf-8
# test_import_rf_rdsr_philips.py

import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings

# pylint: disable=unused-variable

class ImportRFRDSRPhilips(TestCase):
    """Tests for importing the Philips Allura RDSR

    """

    def test_private_collimation_data(self):
        """Tests that the collimated field information has been successfully obtained

        :return: None
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/RF-RDSR-Philips_Allura.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        projection_dose = study.projectionxrayradiationdose_set.get()
        first_source_data = projection_dose.irradeventxraydata_set.order_by('pk')[0].irradeventxraysourcedata_set.get()

        first_field_height = Decimal((164.5+164.5)*1.194)
        first_field_width = Decimal((131.+131.)*1.194)
        first_field_area = (first_field_height * first_field_width) / 1000000

        self.assertAlmostEqual(first_source_data.collimated_field_height, first_field_height)
        self.assertAlmostEqual(first_source_data.collimated_field_width, first_field_width)
        self.assertAlmostEqual(first_source_data.collimated_field_area, first_field_area)
