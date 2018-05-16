# This Python file uses the following encoding: utf-8
# test_import_mam.py

import datetime
import logging
import os
from decimal import Decimal

from django.test import TestCase
from testfixtures import LogCapture

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
        self.assertEqual(study.patientmoduleattr_set.get().patient_id, None)
        self.assertEqual(study.patientmoduleattr_set.get().patient_birth_date, None)

        # Test that study level data is recorded correctly
        self.assertEqual(study.study_date, datetime.date(2013, 04, 12))
        self.assertEqual(study.study_time, datetime.time(12, 35, 46))
        self.assertEqual(study.accession_number, u'AAAA9876')
        self.assertEqual(study.modality_type, u'MG')

        institution_name_string = u"Institution name is {0}".format(
            study.generalequipmentmoduleattr_set.get().institution_name)
        self.assertEqual(institution_name_string, u"Institution name is 中心医院")
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, u'GE MEDICAL SYSTEMS')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_address, u'Москва')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().station_name, u'SENODS01')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer_model_name, u'Senograph DS ADS_43.10.1')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().device_serial_number, u'843b85b7')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().software_versions, u'Ads Application Package VERSION ADS_43.10.1')

        # Test that patient study level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, u'001D')
        self.assertEqual(study.patientmoduleattr_set.get().patient_sex, u'O')

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).acquisition_protocol, u'ROUTINE')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).percent_fibroglandular_tissue, Decimal(31))

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
            ).irradeventxraysourcedata_set.get().anode_target_material.code_meaning, u'Rhodium or Rhodium compound')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning,
            u'Rhodium or Rhodium compound')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.30))  # in mm
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().collimated_field_area, (Decimal(229)*Decimal(191))/Decimal(1000000))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(0.01373)*Decimal(100))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(51800))

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraymechanicaldata_set.get().compression_force, Decimal(50))  # not in std, recorded as presented
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraymechanicaldata_set.get().compression_thickness, Decimal(53))  # mm
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraymechanicaldata_set.get().magnification_factor, Decimal(1))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraymechanicaldata_set.get().column_angulation, Decimal(0))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(1.373))  # AGD in mGy
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).entrance_exposure_at_rp, Decimal(5.071))  # in mGy

        # Test that dose related distance measurements are recorded correctly
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all(
            )[0].irradeventxraymechanicaldata_set.get().
                doserelateddistancemeasurements_set.get().distance_source_to_detector, Decimal(660))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all(
            )[0].irradeventxraymechanicaldata_set.get().
                doserelateddistancemeasurements_set.get().distance_source_to_entrance_surface, Decimal(607))

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

        # Test that patient identifiable data is stored in hash
        self.assertEqual(study.patientmoduleattr_set.get().patient_name,
                         'fe66aceb4eb0ccbd76306a485e162cc3cad8c9312b25b002ad784f72575ae500')
        self.assertEqual(study.patientmoduleattr_set.get().patient_id,
                         '1635c8525afbae58c37bede3c9440844e9143727cc7c160bed665ec378d8a262')
        self.assertEqual(study.accession_number, '8f541d3a1bdab5e197e3acb3b51419b162809c926ee7f45044aca9aef9d6e22d')


class ImportDuplicatesMG(TestCase):
    """Test the following:

    * Import of second image of same study, different time
    * Rejection of third image of same study, same time
    * Rejection of third image, this time because SOPInstanceUID is recognised

    """

    def test_duplicate_event(self):

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        mg_im1_for_proc = os.path.join("test_files", "MG-Im-GE_Seno_1_ForProcessing.dcm")
        mg_im1_for_pres = os.path.join("test_files", "MG-Im-GE_Seno_1_ForPresentation.dcm")
        mg_im2_for_pres = os.path.join("test_files", "MG-Im-GE_Seno_2_ForPresentation.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        mam(os.path.join(root_tests, mg_im1_for_pres))

        # Check study has been imported, with one event
        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 1)
        number_events = GeneralStudyModuleAttr.objects.order_by('pk')[0].projectionxrayradiationdose_set.get(
            ).irradeventxraydata_set.all().count()
        self.assertEqual(number_events, 1)

        with LogCapture(level=logging.DEBUG) as log1:
            # Import second object, same time etc
            mam(os.path.join(root_tests, mg_im1_for_proc))

            # Check still one study, one event
            self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 1)
            number_events = GeneralStudyModuleAttr.objects.order_by('pk')[0].projectionxrayradiationdose_set.get(
                ).irradeventxraydata_set.all().count()
            self.assertEqual(number_events, 1)

            # Check log message
            log1.check_present(('remapp.extractors.mam', 'DEBUG',
                               u'A previous MG object with this study UID (1.3.6.1.4.1.5962.99.1.1270844358.1571783457'
                               u'.1525984267206.3.0) and time (2013-04-12T13:22:23) has been imported. Stopping'),)

        # Import third object, different event
        mam(os.path.join(root_tests, mg_im2_for_pres))

        # Check one study, two events
        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 1)
        number_events = GeneralStudyModuleAttr.objects.order_by('pk')[0].projectionxrayradiationdose_set.get(
        ).irradeventxraydata_set.all().count()
        self.assertEqual(number_events, 2)

        with LogCapture(level=logging.DEBUG) as log2:
            # Import second object again - should be stopped on event UID this time
            mam(os.path.join(root_tests, mg_im1_for_proc))

            # Check one study, two events
            self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 1)
            number_events = GeneralStudyModuleAttr.objects.order_by('pk')[0].projectionxrayradiationdose_set.get(
            ).irradeventxraydata_set.all().count()
            self.assertEqual(number_events, 2)

            # Check log message
            log2.check_present(
                ('remapp.extractors.mam',
                 'DEBUG',
                 u'MG instance UID 1.3.6.1.4.1.5962.99.1.1270844358.1571783457.1525984267206.2.0 of study UID '
                 u'1.3.6.1.4.1.5962.99.1.1270844358.1571783457.1525984267206.3.0 previously processed, stopping.'),
            )
