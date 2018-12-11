# This Python file uses the following encoding: utf-8
# test_import_rf_rdsr_philips.py

import os
from decimal import Decimal

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
        first_field_area = (first_field_height * first_field_width) / 1000000

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

