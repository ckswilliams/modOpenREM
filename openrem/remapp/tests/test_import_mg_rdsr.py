# This Python file uses the following encoding: utf-8
# test_test_import_mg_rdsr_hologic.py

import datetime
import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTRDSR(TestCase):
    def test_import_mg_rdsr_hologic(self):
        """
        Imports a known Hologic Radiation Dose Structured Report, and tests all the values
        imported against those expected.
        """
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        hologic_2d = "test_files/MG-RDSR-Hologic_2D.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        hologic_2d_path = os.path.join(root_tests, hologic_2d)

        rdsr(hologic_2d_path)
        studies = GeneralStudyModuleAttr.objects.all()

        # Test that one study has been imported
        self.assertEqual(studies.count(), 1)

        # Test that study level data is recorded correctly
        self.assertEqual(studies[0].accession_number, 'AJSKDL1234')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_name, 'OpenREM')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer, 'HOLOGIC, Inc.')

        # Test that patient level data is recorded correctly
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_name, 'Lyons^Samantha')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_id, '00112233')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_birth_date, datetime.date(1954, 03, 22))
        self.assertEqual(studies[0].patientstudymoduleattr_set.get().patient_age, '061Y')
        self.assertAlmostEqual(studies[0].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(61))

        # Test that exposure summary data is recorded correctly
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.all().count(), 2)
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.all()[0].accumulated_average_glandular_dose, Decimal(1.30))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.all()[0].laterality.code_meaning, "Left breast")
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.all()[1].accumulated_average_glandular_dose, Decimal(1.28))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.all()[1].laterality.code_meaning, "Right breast")

        # Test that event level dat is recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all(
            )[0].irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(1.3))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all(
            )[0].entrance_exposure_at_rp, Decimal(3.65))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all(
            )[1].irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(1.28))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all(
            )[1].entrance_exposure_at_rp, Decimal(3.60))
