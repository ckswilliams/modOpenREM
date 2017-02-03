# This Python file uses the following encoding: utf-8
# test_test_import_esr_ge.py

import os, datetime
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTRDSR(TestCase):
    def test_import_ct_esr_ge(self):
        """
        Imports known GE Enhanced Structured Reports, and tests all the values
        imported against those expected.
        """
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        ge_optima = "test_files/CT-ESR-GE_Optima.dcm"
        ge_vct = "test_files/CT-ESR-GE_VCT.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        ge_optima_path = os.path.join(root_tests, ge_optima)
        ge_vct_path = os.path.join(root_tests, ge_vct)

        rdsr(ge_optima_path)
        rdsr(ge_vct_path)
        studies = GeneralStudyModuleAttr.objects.all()

        # Test that two studies have been imported
        self.assertEqual(studies.count(), 2)

        # Test that study level data is recorded correctly
        self.assertEqual(studies[0].accession_number, '0012345.12345678')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_name, 'An Optima Hospital')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer, 'GE Medical Systems')
        self.assertEqual(studies[1].accession_number, '001234512345678')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().institution_name, 'A VCT Hospital')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().manufacturer, 'GE Medical Systems')

        # Test that patient level data is recorded correctly
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_name, 'Patient^Optima')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_id, '00001234')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_birth_date, datetime.date(1957, 03, 12))
        self.assertAlmostEqual(studies[0].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(49.4))
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_name, 'Patient^DiscoVCT')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_id, '008F/g234')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_birth_date, datetime.date(1923, 05, 9))
        self.assertEqual(studies[1].patientstudymoduleattr_set.get().patient_age, '89Y')
        self.assertAlmostEqual(studies[1].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(89.8))

        # Test that exposure summary data is recorded correctly
        self.assertEqual(studies[0].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         total_number_of_irradiation_events, 6)
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         ct_dose_length_product_total, Decimal(415.82))
        self.assertEqual(studies[1].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         total_number_of_irradiation_events, 27)
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         ct_dose_length_product_total, Decimal(2002.39))

        # Test that event level dat is recorded correctly
        self.assertAlmostEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.all()[5].mean_ctdivol, Decimal(5.3))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.all()[26].mean_ctdivol, Decimal(32.83))


class ImportNonDoseSR(TestCase):
    def test_import_esr_non_dose(self):
        """
        Imports known GE Enhanced Structured Reports, and tests all the values
        imported against those expected.
        """

        PatientIDSettings.objects.create()

        enhanced_sr = "test_files/ESR_non-dose.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        esr_path = os.path.join(root_tests, enhanced_sr)

        rdsr(esr_path)
        studies = GeneralStudyModuleAttr.objects.all()

        # Test that no studies have been imported
        self.assertEqual(studies.count(), 0)
