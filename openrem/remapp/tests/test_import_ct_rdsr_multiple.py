# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_siemens.py

import os
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings


class ImportMultipleRDSRs(TestCase):  # pylint: disable=unused-variable
    """Tests for multiple RDSR imports of the same study at different stages

    """

    def test_import_ct_rdsr_mulitple(self):
        """Imports three RDSRs in turn, each for the same study, one generated after each exposure, each cumulative

        :return: None
        """
        PatientIDSettings.objects.create()

        dicom_file_1 = "test_files/CT-RDSR-Siemens-Multi-1.dcm"
        dicom_file_2 = "test_files/CT-RDSR-Siemens-Multi-2.dcm"
        dicom_file_3 = "test_files/CT-RDSR-Siemens-Multi-3.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path_1 = os.path.join(root_tests, dicom_file_1)
        dicom_path_2 = os.path.join(root_tests, dicom_file_2)
        dicom_path_3 = os.path.join(root_tests, dicom_file_3)

        rdsr(dicom_path_1)
        study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()

        # Test that there is one study, and it has one event
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
        self.assertEqual(num_events, 1)

        rdsr(dicom_path_2)
        study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()

        # Test that there is one study, and it has two events
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
        self.assertEqual(num_events, 2)

        rdsr(dicom_path_3)
        study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()

        # Test that there is one study, and it has three events
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
        self.assertEqual(num_events, 3)

        rdsr(dicom_path_1)
        study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()

        # Test that there is one study, and it still has three events
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
        self.assertEqual(num_events, 3)

