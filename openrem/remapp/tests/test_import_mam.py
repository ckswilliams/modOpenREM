# This Python file uses the following encoding: utf-8
# test_import_mam.py

import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import mam
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportMGImg(TestCase):
    def test_import_mg_img_ge(self):
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

        # Test that patient identifiable data is not stored
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, None)

        # Test that study level data is recorded correctly
        self.assertEqual(study.accession_number, 'AAAA9876')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_name, u'中心医院')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, 'GE MEDICAL SYSTEMS')

        # Test that patient study level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, '001D')
        self.assertAlmostEqual(study.patientstudymoduleattr_set.get().patient_age_decimal, Decimal(0.00))

        # Test that exposure data is recorded correctly
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().exposure_time, Decimal(834)) # in ms
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(61))  # in mA
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(51800))  # in μAs
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(29))  # in kV
        self.assertEqual('Reciprocating grid' in set(
            grid.xray_grid.code_meaning for grid in study.projectionxrayradiationdose_set.get(
            ).irradeventxraydata_set.get().irradeventxraysourcedata_set.get().xraygrid_set.all()), True)
        self.assertEqual('Focused grid' in set(
            grid.xray_grid.code_meaning for grid in study.projectionxrayradiationdose_set.get(
            ).irradeventxraydata_set.get().irradeventxraysourcedata_set.get().xraygrid_set.all()), True)
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().anode_target_material.code_meaning, 'Rhodium or Rhodium compound')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning,
            'Rhodium or Rhodium compound')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.30))  # in mm
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraymechanicaldata_set.get().compression_force, Decimal(50))  # not in std, recorded as presented
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraymechanicaldata_set.get().compression_thickness, Decimal(53))  # mm
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(1.373))  # AGD in mGy
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).entrance_exposure_at_rp, Decimal(5.071))  # in mGy

    def test_import_mg_img_ge_pid(self):
        """
        Imports a known mammography image file derived from a GE Senographe DS image, and tests the values
        imported against those expected.
        """
        import datetime
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        dicom_file = "test_files/MG-Im-GE-SenDS-scaled.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)
        study = GeneralStudyModuleAttr.objects.all()[0]

        # Test that patient identifiable data is stored in plain text
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, u'Mamografía^Bịnhnhân')
        self.assertEqual(study.patientmoduleattr_set.get().patient_id, u'ABCD1234')
        birth_date = datetime.date(2013, 4, 12)
        self.assertEqual(study.patientmoduleattr_set.get().patient_birth_date, birth_date)


    def test_import_mg_img_ge_pid_hashed(self):
        """
        Imports a known mammography image file derived from a GE Senographe DS image, and tests the values
        imported against those expected.
        """
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = True
        pid.id_stored = True
        pid.id_hashed = True
        pid.accession_hashed = True
        pid.save()

        dicom_file = "test_files/MG-Im-GE-SenDS-scaled.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)
        study = GeneralStudyModuleAttr.objects.all()[0]

        # Test that patient identifiable data is stored in plain text
        self.assertEqual(study.patientmoduleattr_set.get().patient_name,
                         'fe66aceb4eb0ccbd76306a485e162cc3cad8c9312b25b002ad784f72575ae500')
        self.assertEqual(study.patientmoduleattr_set.get().patient_id,
                         '1635c8525afbae58c37bede3c9440844e9143727cc7c160bed665ec378d8a262')
        self.assertEqual(study.accession_number, '8f541d3a1bdab5e197e3acb3b51419b162809c926ee7f45044aca9aef9d6e22d')