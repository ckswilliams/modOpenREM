# This Python file uses the following encoding: utf-8
# test_get_values.py

from __future__ import unicode_literals
import os
from collections import Counter
import datetime
from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.test import TestCase
from dicom.dataset import Dataset
from dicom.dataelem import DataElement
from dicom.multival import MultiValue
import logging
from testfixtures import LogCapture
from remapp.extractors.dx import _xray_filters_prep
from remapp.models import GeneralStudyModuleAttr, ProjectionXRayRadiationDose, IrradEventXRayData, \
    IrradEventXRaySourceData


class DXFilterTests(TestCase):
    def test_multiple_filter_kodak_drxevolution(self):
        """
        Test the material extraction process when the materials are in a MultiValue format
        """
        ds = Dataset()
        multi = MultiValue(str, ["ALUMINUM", "COPPER"])
        data_el = DataElement(0x187050, "CS", multi, already_converted=True)
        ds[0x187050] = data_el
        ds.FilterThicknessMinimum = "1.0\\0.1"
        ds.FilterThicknessMaximum = "1.0\\0.1"

        g = GeneralStudyModuleAttr.objects.create()
        g.save()
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
        proj.save()
        event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
        event.save()
        source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
        source.save()

        _xray_filters_prep(ds, source)

        self.assertEqual(source.xrayfilters_set.order_by('id').count(), 2, 'Wrong number of filters recorded')
        self.assertEqual(source.xrayfilters_set.order_by('id')[0].xray_filter_material.code_meaning,
                         "Aluminum or Aluminum compound")
        self.assertEqual(source.xrayfilters_set.order_by('id')[1].xray_filter_material.code_meaning,
                         "Copper or Copper compound")


    def test_single_filter(self):
        """
        Test the material extraction process when there is just one filter
        """
        ds = Dataset()
        ds.FilterMaterial = "lead"
        ds.FilterThicknessMinimum = "1.0"
        ds.FilterThicknessMaximum = "1.0"

        g = GeneralStudyModuleAttr.objects.create()
        g.save()
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
        proj.save()
        event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
        event.save()
        source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
        source.save()

        _xray_filters_prep(ds, source)

        self.assertEqual(source.xrayfilters_set.order_by('id').count(), 1)
        self.assertEqual(source.xrayfilters_set.order_by('id')[0].xray_filter_material.code_meaning,
                         "Lead or Lead compound")


class ImportCarestreamDR7500(TestCase):

    def setUp(self):
        from remapp.extractors import dx
        from remapp.models import PatientIDSettings

        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        eg = Group(name="exportgroup")
        eg.save()
        eg.user_set.add(self.user)
        eg.save()

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        dx_ge_xr220_1 = os.path.join("test_files", "DX-Im-GE_XR220-1.dcm")
        dx_ge_xr220_2 = os.path.join("test_files", "DX-Im-GE_XR220-2.dcm")
        dx_ge_xr220_3 = os.path.join("test_files", "DX-Im-GE_XR220-3.dcm")
        dx_carestream_dr7500_1 = os.path.join("test_files", "DX-Im-Carestream_DR7500-1.dcm")
        dx_carestream_dr7500_2 = os.path.join("test_files", "DX-Im-Carestream_DR7500-2.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        with LogCapture(level=logging.DEBUG) as self.log:
            dx(os.path.join(root_tests, dx_ge_xr220_1))
            dx(os.path.join(root_tests, dx_ge_xr220_2))
            dx(os.path.join(root_tests, dx_ge_xr220_3))
            dx(os.path.join(root_tests, dx_carestream_dr7500_1))
            dx(os.path.join(root_tests, dx_carestream_dr7500_2))
            dx(os.path.join(root_tests, dx_ge_xr220_2))

    def test_dr7500_and_xr220(self):

        studies = GeneralStudyModuleAttr.objects.order_by('id')

        # Test that two studies have been imported
        self.assertEqual(studies.count(), 2)

        # Test that the second attempt to import dx_ge_xr220_2 results in debug message
        self.log.check_present(('remapp.extractors.dx', 'DEBUG',
                                u'DX instance UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.26.0 of '
                                u'study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0 '
                                u'previously processed, stopping.'))

        # Test that study level data is recorded correctly
        self.assertEqual(studies[0].study_date, datetime.date(2014, 9, 30))
        self.assertEqual(studies[1].study_date, datetime.date(2014, 6, 20))
        self.assertEqual(studies[0].study_time, datetime.time(14, 10, 24))
        self.assertEqual(studies[1].study_time, datetime.time(10, 48, 5))
        self.assertEqual(studies[1].study_description, 'AEC')
        self.assertEqual(studies[1].operator_name, 'PHYSICS')

        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_name, 'Digital Mobile Hospital')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().institution_name, 'Carestream Clinic')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_address, 'Kvitfjell')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer, 'GE Healthcare')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().manufacturer, 'KODAK')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().station_name, '01234MOB54')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().station_name, 'KODAK7500')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer_model_name, 'Optima XR220')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().manufacturer_model_name, 'DR 7500')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().software_versions, 'dm_Platform_release_superbee-FW23.1-SB')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().software_versions, '4.0.3.B8.P6')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().device_serial_number, '00012345abc')

        # Test the SOP instance UIDs have been recorded correctly
        sop_instance_uid_list0 = Counter(studies[0].objectuidsprocessed_set.values_list('sop_instance_uid', flat=True))
        sop_instance_uid_list1 = Counter(studies[1].objectuidsprocessed_set.values_list('sop_instance_uid', flat=True))
        uid_list0 = Counter([u'1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.20.0',
                             u'1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.26.0',
                             u'1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.28.0'])
        uid_list1 = Counter([u'1.2.276.0.7230010.3.1.4.8323329.11838.1483692281.541544',
                             u'1.2.276.0.7230010.3.1.4.8323329.11853.1483692311.916929'])
        self.assertEqual(sop_instance_uid_list0, uid_list0)
        self.assertEqual(sop_instance_uid_list1, uid_list1)

        # Test that patient level data is recorded correctly
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_name, 'XR220^Samantha')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_name, 'PHYSICS^TABLE AEC')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_id, '00098765')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_id, 'PHY12320140620YU')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_birth_date, datetime.date(1957, 11, 12))
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_birth_date, datetime.date(2014, 6, 20))
        self.assertAlmostEqual(studies[0].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(56.9))

        # Test that irradiation event data is stored correctl
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            acquisition_protocol, 'ABD_1_VIEW')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            acquisition_protocol, 'ABD_1_VIEW')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            acquisition_protocol, 'ABD_1_VIEW')
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            dose_area_product, Decimal(0.41 / 100000))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            dose_area_product, Decimal(0.82 / 100000))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            dose_area_product, Decimal(2.05 / 100000))

        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            acquisition_protocol, 'AEC')
        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            acquisition_protocol, 'AEC')
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            dose_area_product, Decimal(11.013 / 100000))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            dose_area_product, Decimal(10.157 / 100000))

        # Check that dose related distance measurement data is stored correctly
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get().
                distance_source_to_detector, Decimal(11.5 * 100))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get().
                distance_source_to_detector, Decimal(11.5 * 100))

        # Test that irradiation event source data is stored correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(6))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(11))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(27))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(189))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.6))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.6))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.6))

        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(19))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(18))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(1.2))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(1.2))

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(189))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(192))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(190))

        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(500))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(500))

        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning,
                'Aluminum or Aluminum compound')
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_minimum, Decimal(0.94))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_maximum, Decimal(1.06))

        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xrayfilters_set.order_by('id')[0].xray_filter_material.code_meaning,
                'Aluminum or Aluminum compound')
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xrayfilters_set.order_by('id')[0].xray_filter_thickness_minimum,
                Decimal(0.94))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xrayfilters_set.order_by('id')[0].xray_filter_thickness_maximum,
                Decimal(1.06))

        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xrayfilters_set.order_by('id')[1].xray_filter_material.code_meaning,
                'Copper or Copper compound')
        self.assertAlmostEqual(
            studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xrayfilters_set.order_by('id')[1].xray_filter_thickness_minimum,
            Decimal(0.194))
        self.assertAlmostEqual(
            studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xrayfilters_set.order_by('id')[1].xray_filter_thickness_maximum,
            Decimal(0.206))


        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().grid_focal_distance, Decimal(1828.8))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().grid_focal_distance, Decimal(1828.8))



        #Test exposure data is stored correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(1040))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(2040))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(5040))

        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(10 * 1000))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(9 * 1000))


        #Test that irradiation event detector data is stored correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
                               irradeventxraydetectordata_set.get().exposure_index, Decimal(51.745061))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
                               irradeventxraydetectordata_set.get().exposure_index, Decimal(108.843060))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
                               irradeventxraydetectordata_set.get().exposure_index, Decimal(286.828227))

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(438.469173))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(438.469173))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(438.469173))

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(-9.3))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(-6.1))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(-1.8))

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().sensitivity, Decimal(97.213916))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().sensitivity, Decimal(97.213916))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraydetectordata_set.get().sensitivity, Decimal(97.213916))

        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().relative_xray_exposure, Decimal(1460))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().relative_xray_exposure, Decimal(1430))



    def test_filter_thickness_order(self):
        from remapp.models import XrayFilters

        all_filters = XrayFilters.objects.order_by('id')
        for exposure in all_filters:
            self.assertGreaterEqual(exposure.xray_filter_thickness_maximum, exposure.xray_filter_thickness_minimum)

    def test_multiple_filter_carestream_comma(self):
        """
        Testing the DR7500 file can be imported with illegal comma separated floats
        :return: None
        """

        study = GeneralStudyModuleAttr.objects.order_by('id')[1]

        source = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].irradeventxraysourcedata_set.get()

        self.assertEqual(source.xrayfilters_set.order_by('id').count(), 2,
                         "Testing Kodak old style, two filters should have been stored, {0} were".format(
                             source.xrayfilters_set.order_by('id').count()))
        self.assertEqual(source.xrayfilters_set.order_by('id')[0].xray_filter_material.code_meaning,
                         "Aluminum or Aluminum compound")
        self.assertAlmostEqual(source.xrayfilters_set.order_by('id')[0].xray_filter_thickness_minimum, Decimal(0.94))
        self.assertEqual(source.xrayfilters_set.order_by('id')[1].xray_filter_material.code_meaning,
                         "Copper or Copper compound")
        self.assertAlmostEqual(source.xrayfilters_set.order_by('id')[1].xray_filter_thickness_minimum, Decimal(0.194))


class ImportCarestreamDRXRevolution(TestCase):

    def setUp(self):
        """
        Imports a known radigraphic image file derived from a Carestream DRX Revolution image.
        """
        from remapp.extractors import dx
        from remapp.models import PatientIDSettings

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        dx_carestream_drx_revolution = os.path.join("test_files", "DX-Im-Carestream_DRX.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dx(os.path.join(root_tests, dx_carestream_drx_revolution))

    def test_requested_procedure_name(self):
        """
        Tests the imported value of requested procedure code meaning against what is expected.
        """
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        self.assertEqual(study.requested_procedure_code_meaning, u'XR CHEST')


class ImportDuplicateDX(TestCase):

    def setUp(self):
        """

        """
        from remapp.models import PatientIDSettings

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        from remapp.extractors import dx

        dx_ge_xr220_1 = os.path.join("test_files", "DX-Im-GE_XR220-1.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        dx(os.path.join(root_tests, dx_ge_xr220_1))
        study_one = GeneralStudyModuleAttr.objects.order_by('pk')[0]
        original_study_uid = study_one.study_instance_uid
        original_sop_instance_uid = study_one.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradiation_event_uid
        study_one.study_instance_uid = u'1.2.3.4.5.6.7.8'
        study_one.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradiation_event_uid = u'2.3.4.5.6.7.8.9'
        study_one.save()

        # Check there is one study in the database
        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 1)

        # Import the image again...
        dx(os.path.join(root_tests, dx_ge_xr220_1))

        # Check there are two studies now
        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 2)

        study_one.study_instance_uid = original_study_uid
        study_one.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
        ).irradiation_event_uid = original_sop_instance_uid
        study_one.save()

        # Now we are ready to test import with duplicate study UIDs.

    def test_duplicate_study_dx(self):
        """Imports second image, original two both have modality set.

        """
        from remapp.extractors import dx

        dx_ge_xr220_2 = os.path.join("test_files", "DX-Im-GE_XR220-2.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 2)

        study_1_pk = GeneralStudyModuleAttr.objects.order_by('pk').first().pk

        with LogCapture(level=logging.DEBUG) as log:
            dx(os.path.join(root_tests, dx_ge_xr220_2))

        log.check_present(('remapp.extractors.dx',
                           'WARNING',
                           u'Duplicate DX study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0 in '
                           u'database - could be a problem! There are 2 copies.'),
                          ('remapp.extractors.dx',
                           'DEBUG',
                           u'Duplicate DX study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0 - '
                           u'first instance (pk={0}) with modality type assigned (DX) selected to import new event '
                           u'into.'.format(study_1_pk))
                          )

        number_of_events_study_1 = GeneralStudyModuleAttr.objects.order_by('pk').first(
            ).projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        self.assertEqual(number_of_events_study_1, 2)
        number_of_events_study_2 = GeneralStudyModuleAttr.objects.order_by('pk')[
            1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        self.assertEqual(number_of_events_study_2, 1)

    def test_duplicate_study_dx_second_mod(self):
        """Imports second image, later existing has modality set.

        """
        from remapp.extractors import dx

        dx_ge_xr220_2 = os.path.join("test_files", "DX-Im-GE_XR220-2.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 2)

        # Set first study modality to None
        study_1 = GeneralStudyModuleAttr.objects.order_by('pk').first()
        study_1.modality_type = None
        study_1.save()

        study_2_pk = GeneralStudyModuleAttr.objects.order_by('pk')[1].pk

        with LogCapture(level=logging.DEBUG) as log:
            dx(os.path.join(root_tests, dx_ge_xr220_2))

        log.check_present(('remapp.extractors.dx',
                           'WARNING',
                           u'Duplicate DX study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0 in '
                           u'database - could be a problem! There are 2 copies.'),
                          ('remapp.extractors.dx',
                           'DEBUG',
                           u'Duplicate DX study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0 - '
                           u'first instance (pk={0}) with modality type assigned (DX) selected to import new event '
                           u'into.'.format(study_2_pk))
                          )

        number_of_events_study_1 = GeneralStudyModuleAttr.objects.order_by('pk').first(
            ).projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        self.assertEqual(number_of_events_study_1, 1)
        number_of_events_study_2 = GeneralStudyModuleAttr.objects.order_by('pk')[
            1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        self.assertEqual(number_of_events_study_2, 2)

    def test_duplicate_study_dx_no_mod(self):
        """Imports second image, original two don't have modality set.

        """
        from remapp.extractors import dx

        dx_ge_xr220_2 = os.path.join("test_files", "DX-Im-GE_XR220-2.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        self.assertEqual(GeneralStudyModuleAttr.objects.all().count(), 2)

        # Set modality type to None
        for study in GeneralStudyModuleAttr.objects.order_by('pk'):
            study.modality_type = None
            study.save()

        with LogCapture(level=logging.DEBUG) as log:
            dx(os.path.join(root_tests, dx_ge_xr220_2))

        log.check_present(('remapp.extractors.dx',
                           'WARNING',
                           u'Duplicate DX study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0 in '
                           u'database - could be a problem! There are 2 copies.'),
                          ('remapp.extractors.dx',
                           'WARNING',
                           u'Duplicate DX study UID 1.3.6.1.4.1.5962.99.1.2282339064.1266597797.1479751121656.24.0, '
                           u'none of which have modality_type assigned! Setting first instance to DX')
                          )

        number_of_events_study_1 = GeneralStudyModuleAttr.objects.order_by('pk').first(
            ).projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        self.assertEqual(number_of_events_study_1, 2)
        number_of_events_study_2 = GeneralStudyModuleAttr.objects.order_by('pk')[
            1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        self.assertEqual(number_of_events_study_2, 1)
