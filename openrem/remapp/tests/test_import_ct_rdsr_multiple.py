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


class ImportContinuedRDSRs(TestCase):
    """Tests for multiple RDSRs of the same study that are a continuation of each other

    """
    def test_import_ct_rdsr_continued(self):
        """Imports two RDSRs, the second is a continuation of the first with different events in.

        :return: None
        """
        PatientIDSettings.objects.create()

        dicom_file_1 = "test_files/CT-RDSR-Siemens-Continued-1.dcm"
        dicom_file_2 = "test_files/CT-RDSR-Siemens-Continued-2.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path_1 = os.path.join(root_tests, dicom_file_1)
        dicom_path_2 = os.path.join(root_tests, dicom_file_2)

        rdsr(dicom_path_1)
        study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()

        # Test that there is one study, and it has one event
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
        self.assertEqual(num_events, 2)

        rdsr(dicom_path_2)
        # Test the the new study has been imported separately
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 2)

        # Test that each study has two events in
        studies = GeneralStudyModuleAttr.objects.all().order_by('pk')
        for study in studies:
            num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()
            self.assertEqual(num_events, 2)

        latest_study_pk = GeneralStudyModuleAttr.objects.all().order_by('pk').last().pk
        rdsr(dicom_path_2)
        # Test that it doesn't import a second time...
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 2)
        self.assertEqual(GeneralStudyModuleAttr.objects.all().order_by('pk').last().pk, latest_study_pk)


class ImportDuplicateNonCTRDSRs(TestCase):
    """Tests for non-CT RDSRs

    """
    def test_import_duplicate_dx(self):
        """

        :return:
        """
        PatientIDSettings.objects.create()

        dicom_file_1 = "test_files/DX-RDSR-Canon_CXDI.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path_1 = os.path.join(root_tests, dicom_file_1)

        rdsr(dicom_path_1)
        # Test that there is one study, and it has one event
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)

        rdsr(dicom_path_1)
        # Test that there is one study, and it has one event
        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
