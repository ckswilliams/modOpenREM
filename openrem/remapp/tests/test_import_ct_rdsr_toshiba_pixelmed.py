# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_toshiba_pixelmed.py

import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTRDSR(TestCase):
    def test_import_ct_rdsr_siemens(self):
        """
        Imports a known RDSR generated by PixelMed from a Toshiba Aquilion CT study, and tests all the values
        imported against those expected.
        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/CT-RDSR-ToshibaPixelMed.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.all()[0]

        # Test that study level data is recorded correctly
        self.assertEqual(study.accession_number, '4935683')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_name, 'Oxbridge County Hospital')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, 'TOSHIBA')

        # Test that patient study level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, '042Y')
        self.assertAlmostEqual(study.patientstudymoduleattr_set.get().patient_age_decimal, Decimal(42.9))

        # Test that exposure data is recorded correctly
        self.assertEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         total_number_of_irradiation_events, 3)
        self.assertAlmostEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         ct_dose_length_product_total, Decimal(349.7))


