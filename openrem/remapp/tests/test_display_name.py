# This Python file uses the following encoding: utf-8
# test_import_dx_rdsr.py

import os
import dicom
from django.test import TestCase
from remapp.extractors.rdsr import _rdsr2db
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings, UniqueEquipmentNames, \
    MergeOnDeviceObserverUIDSettings


class UseDeviceObserverUID(TestCase):
    """Class to test the use of match_on_device_observer_uid setting"""
    def test_import_match_false(self):
        """
        Import DX RDSRs, same Device Observer UIDs, different Department. Should create different Display Names
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/DX-RDSR-Canon_CXDI.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        dataset = dicom.read_file(dicom_path)
        dataset.decode()
        _rdsr2db(dataset)

        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        display_name = study.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name
        self.assertEqual(display_name, u'OpenREM CANONDaRt')

        self.assertEqual(MergeOnDeviceObserverUIDSettings.get_solo().match_on_device_observer_uid, False)

        dataset_2 = dataset
        dataset_2.InstitutionalDepartmentName = "New Name"
        dataset_2.StationName = "StnName2"
        dataset_2.SOPInstanceUID = "1.2.3.4"
        dataset_2.StudyInstanceUID = "1.2.3.4"
        _rdsr2db(dataset_2)

        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 2)

        study_2 = GeneralStudyModuleAttr.objects.order_by('id')[1]
        display_name_2 = study_2.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name
        self.assertEqual(display_name_2, u'OpenREM StnName2')

    def test_import_match_true(self):
        """
        Import DX RDSRs, same Device Observer UIDs, different Department. Should use same Display Name
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/DX-RDSR-Canon_CXDI.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        dataset = dicom.read_file(dicom_path)
        dataset.decode()
        _rdsr2db(dataset)

        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        display_name = study.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name
        self.assertEqual(display_name, u'OpenREM CANONDaRt')

        device_uid_settings = MergeOnDeviceObserverUIDSettings.get_solo()
        device_uid_settings.match_on_device_observer_uid = True
        device_uid_settings.save()
        self.assertEqual(MergeOnDeviceObserverUIDSettings.get_solo().match_on_device_observer_uid, True)

        dataset_2 = dataset
        dataset_2.InstitutionalDepartmentName = "New Name"
        dataset_2.StationName = "StnName2"
        dataset_2.SOPInstanceUID = "1.2.3.4"
        dataset_2.StudyInstanceUID = "1.2.3.4"
        _rdsr2db(dataset_2)

        self.assertEqual(GeneralStudyModuleAttr.objects.count(), 2)

        study_2 = GeneralStudyModuleAttr.objects.order_by('id')[1]
        display_name_2 = study_2.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name
        self.assertEqual(display_name_2, u'OpenREM CANONDaRt')


