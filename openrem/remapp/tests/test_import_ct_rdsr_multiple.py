# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_siemens.py

import os
from collections import Counter
from django.test import TestCase
from testfixtures import LogCapture
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
        with LogCapture() as log:

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
            sop_instance_uid_list1 = Counter(study.objectuidsprocessed_set.values_list('sop_instance_uid', flat=True))

            # Test that there is one study, and it has one event
            self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
            self.assertEqual(num_events, 1)
            self.assertEqual(sop_instance_uid_list1, Counter(
                [u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.11.0']))

            rdsr(dicom_path_2)
            study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
            num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()
            sop_instance_uid_list2 = Counter(study.objectuidsprocessed_set.values_list('sop_instance_uid', flat=True))
            uid_list2 = Counter([u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.11.0',
                                 u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.6.0'])

            # Test that there is one study, and it has two events
            self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
            self.assertEqual(num_events, 2)
            self.assertEqual(sop_instance_uid_list2, uid_list2)

            rdsr(dicom_path_3)
            study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
            num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()
            sop_instance_uid_list3 = Counter(study.objectuidsprocessed_set.values_list('sop_instance_uid', flat=True))
            uid_list3 = Counter([u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.11.0',
                                 u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.9.0',
                                 u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.6.0'])

            # Test that there is one study, and it has three events
            self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
            self.assertEqual(num_events, 3)
            self.assertEqual(sop_instance_uid_list3, uid_list3)

            rdsr(dicom_path_1)
            study = GeneralStudyModuleAttr.objects.order_by('pk')[0]
            num_events = study.ctradiationdose_set.get().ctirradiationeventdata_set.count()
            sop_instance_uid_list4 = Counter(study.objectuidsprocessed_set.values_list('sop_instance_uid', flat=True))
            study_uid = u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.3.0'
            new_sop_instance_uid = u'1.3.6.1.4.1.5962.99.1.792239193.1702185591.1516915727449.11.0'

            # Test that there is one study, and it still has three events
            self.assertEqual(GeneralStudyModuleAttr.objects.count(), 1)
            self.assertEqual(num_events, 3)
            self.assertEqual(sop_instance_uid_list4, uid_list3)
            # Test that the attempt to import a duplicate is stopped at the instance UID check
            log.check_present(('remapp.extractors.rdsr', 'DEBUG',
                               u"Import match on Study Instance UID {0} and object SOP Instance UID {1}. "
                               u"Will not import.".format(study_uid, new_sop_instance_uid)))


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
