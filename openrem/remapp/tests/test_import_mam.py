# This Python file uses the following encoding: utf-8
# test_get_values.py

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
        # self.assertEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
        #                  total_number_of_irradiation_events, 4)
        # self.assertAlmostEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
        #                  ct_dose_length_product_total, Decimal(724.52))

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
