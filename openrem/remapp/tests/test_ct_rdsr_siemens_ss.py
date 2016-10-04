# test_get_values.py

import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTRDSR(TestCase):
    def test_import_ct_rdsr_siemens(self):
        """
        Imports a known RDSR file derived from a Siemens Definition Flash single source RDSR, and tests all the values
        imported against those expected.
        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/CT-RDSR-Siemens_Flash-TAP-SS.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.all()[0]

        # Test that patient identifiable data is not stored
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, None)

        # Test that study level data is recorded correctly
        self.assertEqual(study.accession_number, 'ACC12345601')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_name, 'Hospital Number One Trust')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, 'SIEMENS')

        # Test that patient study level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, '067Y')
        self.assertAlmostEqual(study.patientstudymoduleattr_set.get().patient_age_decimal, Decimal(67.6))

        # Test that exposure data is recorded correctly
        self.assertEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         total_number_of_irradiation_events, 4)
        self.assertAlmostEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         ct_dose_length_product_total, Decimal(724.52))


