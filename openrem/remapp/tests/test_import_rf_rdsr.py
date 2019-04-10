# This Python file uses the following encoding: utf-8
# test_import_rf_rdsr_philips.py

from __future__ import division
from past.utils import old_div
import os
from decimal import Decimal
import datetime

from django.test import TestCase

from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings


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
        first_field_area = old_div((first_field_height * first_field_width), 1000000)

        self.assertAlmostEqual(first_source_data.collimated_field_height, first_field_height)
        self.assertAlmostEqual(first_source_data.collimated_field_width, first_field_width)
        self.assertAlmostEqual(first_source_data.collimated_field_area, first_field_area)


class ImportRFRDSRPhilipsAzurion(TestCase):
    """
    Test importing Azurion RDSR with empty calibration data and incorrect Acquisition Device Type

    *** Currently disabled as RDSR too big - import adds 15 seconds to tests! ***
    To enable, remove '_disable_' from the function name
    """

    def _disable_test_azurion_import(self):
        """
        Tests that the file was imported without error (empty calibrations)
        Tests that the accumulated fluoroscopy data is captured (incorrect Acquisition Device Type)
        :return: None
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/RF-RDSR-Philips_Azurion.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        fluoro_totals = study.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumprojxraydose_set.get()

        self.assertAlmostEqual(fluoro_totals.fluoro_dose_area_product_total, Decimal(0.00101567))


class DAPUnitsTest(TestCase):
    """
    Test handling of incorrect DAP units found in Toshiba/Canon RF Ultimax
    """

    def test_dgycm2(self):
        """
        Initial test of sequence as presented in Ultimax RDSR
        :return: None
        """
        from dicom.dataset import Dataset
        from dicom.sequence import Sequence
        from remapp.extractors.rdsr import _check_dap_units

        units_sequence = Dataset()
        units_sequence.CodeValue = u'dGy.cm2'
        units_sequence.CodingSchemeDesignator = u'UCUM'
        units_sequence.CodeMeaning = u'dGy.cm2'
        measured_values_sequence = Dataset()
        measured_values_sequence.NumericValue = 1.034
        measured_values_sequence.MeasurementUnitsCodeSequence = Sequence([units_sequence])

        dap = _check_dap_units(measured_values_sequence)
        self.assertAlmostEqual(dap, 0.00001034)

    def test_gym2(self):
        """
        Test case of correct sequence as presented in conformant RDSR
        :return: None
        """
        from dicom.dataset import Dataset
        from dicom.sequence import Sequence
        from remapp.extractors.rdsr import _check_dap_units

        units_sequence = Dataset()
        units_sequence.CodeValue = u'Gym2'
        units_sequence.CodingSchemeDesignator = u'UCUM'
        units_sequence.CodeMeaning = u'Gym2'
        measured_values_sequence = Dataset()
        measured_values_sequence.NumericValue = 1.6e-005
        measured_values_sequence.MeasurementUnitsCodeSequence = Sequence([units_sequence])

        dap = _check_dap_units(measured_values_sequence)
        self.assertAlmostEqual(dap, 0.000016)

    def test_no_units(self):
        """
        Test case of missing units sequence - not seen by the auther in the wild
        :return: None
        """
        from dicom.dataset import Dataset
        from remapp.extractors.rdsr import _check_dap_units

        measured_values_sequence = Dataset()
        measured_values_sequence.NumericValue = 1.6e-005

        dap = _check_dap_units(measured_values_sequence)
        self.assertAlmostEqual(dap, 0.000016)


class ImportRFRDSRSiemens(TestCase):
    """Tests for importing the Siemens Zee RDSR

    """

    def test_comment_xml_extraction(self):
        """Tests that the patient orientation and II size information has been successfully obtained

        :return: None
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/RF-RDSR-Siemens-Zee.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        event_data = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0]
        self.assertEqual(event_data.patient_table_relationship_cid.code_value, 'F-10470')
        self.assertEqual(event_data.patient_orientation_cid.code_value, 'F-10450')
        self.assertEqual(event_data.patient_orientation_modifier_cid.code_meaning, 'supine')
        source_data = event_data.irradeventxraysourcedata_set.get()
        self.assertEqual(source_data.ii_field_size, 220)


class ImportRFRDSRGESurgical(TestCase):
    """
    Tests for importing an RDSR from a GE Surgical C-Arm FPD system
    """

    def test_ge_c_arm_rdsr(self):
        """Tests for extracting from GE RDSRs, particularly the fields that have the wrong type
        or typographical errors.

        :return: None
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/RF-RDSR-GE.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        device_observer_uid = study.generalequipmentmoduleattr_set.get().unique_equipment_name.device_observer_uid
        self.assertEqual(device_observer_uid, u'1.3.6.1.4.1.45593.912345678.9876543123')

        accum_proj = study.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumprojxraydose_set.get()
        total_fluoro_dap = accum_proj.fluoro_dose_area_product_total
        total_fluoro_rp_dose = accum_proj.fluoro_dose_rp_total
        total_acq_dap = accum_proj.acquisition_dose_area_product_total
        total_acq_rp_dose = accum_proj.acquisition_dose_rp_total
        self.assertAlmostEqual(total_fluoro_dap, Decimal(0.00024126))
        self.assertAlmostEqual(total_fluoro_rp_dose, Decimal(0.01173170))
        self.assertEqual(total_acq_dap, Decimal(0))
        self.assertEqual(total_acq_rp_dose, Decimal(0))

        events = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('pk')
        event_4 = events[3]
        self.assertEqual(event_4.date_time_started, datetime.datetime(2019, 3, 16, 13, 27, 25))
        self.assertEqual(event_4.reference_point_definition.code_value, u'113861')
        self.assertEqual(event_4.irradiation_event_uid, u'1.3.6.1.4.1.5962.99.1.3577657414.286912992.1554060884038.8.0')
        self.assertAlmostEqual(event_4.dose_area_product, Decimal(0.00004334))
        event_4_source = event_4.irradeventxraysourcedata_set.get()
        self.assertAlmostEqual(event_4_source.dose_rp, Decimal(0.00210763))
        self.assertAlmostEqual(event_4_source.collimated_field_area, Decimal(0.04196800))
        self.assertAlmostEqual(event_4_source.average_xray_tube_current, Decimal(18.90340042))
