# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_siemens.py

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

        # Test that irradiation length data is recorded before changes for ref #447
        irrad_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.all()
        self.assertEqual(irrad_events.count(), 4)
        self.assertAlmostEqual(irrad_events[0].scanninglength_set.get().scanning_length, 821)
        self.assertAlmostEqual(irrad_events[1].scanninglength_set.get().scanning_length, 10)
        self.assertAlmostEqual(irrad_events[2].scanninglength_set.get().scanning_length, 10)
        self.assertAlmostEqual(irrad_events[3].scanninglength_set.get().scanning_length, 737)
