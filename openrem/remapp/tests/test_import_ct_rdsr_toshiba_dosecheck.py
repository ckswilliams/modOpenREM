# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_siemens.py

"""
..  module:: test_import_rdsr_toshiba_dosecheck
    :synopsis: Test module focusing on proper extraction of dose check data

..  moduleauthor:: Ed McDonagh
"""

import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings


class ImportToshibaWithDoseCheck(TestCase):
    """Test module focusing on proper extraction of dose check data

    """
    def test_dose_check_import(self):
        """Imports a known RDSR and checks the dose check details

        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/CT-RDSR-Toshiba_DoseCheck.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        series1 = study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0]
        series2 = study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[1]

        series1_dose_check = series1.ctdosecheckdetails_set.get()
        series2_dose_check = series2.ctdosecheckdetails_set.get()
        series1_dose_check_alert_person = series1_dose_check.tid1020_alert.get()
        series2_dose_check_alert_person = series2_dose_check.tid1020_alert.get()

        self.assertTrue(series1_dose_check.dlp_alert_value_configured)
        self.assertTrue(series1_dose_check.ctdivol_alert_value_configured)
        self.assertAlmostEqual(series1_dose_check.dlp_alert_value, Decimal(100.0))
        self.assertAlmostEqual(series1_dose_check.ctdivol_alert_value, Decimal(10.0))
        self.assertAlmostEqual(series1_dose_check.accumulated_dlp_forward_estimate, Decimal(251.2))
        self.assertEqual(series1_dose_check_alert_person.person_name, "Luuk")
        self.assertFalse(series1_dose_check.dlp_notification_value_configured)
        self.assertFalse(series1_dose_check.ctdivol_notification_value_configured)

        self.assertTrue(series2_dose_check.dlp_alert_value_configured)
        self.assertTrue(series2_dose_check.ctdivol_alert_value_configured)
        self.assertAlmostEqual(series2_dose_check.dlp_alert_value, Decimal(100.0))
        self.assertAlmostEqual(series2_dose_check.ctdivol_alert_value, Decimal(10.0))
        self.assertAlmostEqual(series2_dose_check.accumulated_dlp_forward_estimate, Decimal(502.4))
        self.assertAlmostEqual(series2_dose_check.accumulated_ctdivol_forward_estimate, Decimal(10.60))
        self.assertEqual(series2_dose_check_alert_person.person_name, "Luuk")
        self.assertFalse(series2_dose_check.dlp_notification_value_configured)
        self.assertFalse(series2_dose_check.ctdivol_notification_value_configured)
