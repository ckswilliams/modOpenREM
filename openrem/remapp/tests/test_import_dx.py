# This Python file uses the following encoding: utf-8
# test_get_values.py

from __future__ import unicode_literals
import os, datetime
from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.test import TestCase
from dicom.dataelem import RawDataElement
from dicom.dataset import Dataset
from dicom.tag import Tag
from remapp.extractors.dx import _xray_filters_prep
from remapp.models import GeneralStudyModuleAttr, ProjectionXRayRadiationDose, IrradEventXRayData, \
    IrradEventXRaySourceData


class DXFilterTests(TestCase):
    def test_multiple_filter_kodak_dr7500(self):
        """
        Test the material extraction process when the materials are comma separated
        """

        rawelemmin = RawDataElement(Tag(0x187052), 'DS', 9, '0.09,1.18', 0, False, True)
        rawelemmax = RawDataElement(Tag(0x187054), 'DS', 9, '0.11,1.22', 0, False, True)
        rawdict = {0x187052: rawelemmin, 0x187054: rawelemmax}
        ds = Dataset(rawdict)

        ds.FilterMaterial = "niobium,europium"

        g = GeneralStudyModuleAttr.objects.create()
        g.save()
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
        proj.save()
        event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
        event.save()
        source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
        source.save()

        _xray_filters_prep(ds, source)

        self.assertEqual(source.xrayfilters_set.all().count(), 2,
                         "Testing Kodak old style, two filters should have been stored, {0} were".format(
                             source.xrayfilters_set.all().count()
                         ))
        self.assertEqual(source.xrayfilters_set.all()[0].xray_filter_material.code_meaning,
                         "Niobium or Niobium compound")
        self.assertEqual(source.xrayfilters_set.all()[1].xray_filter_material.code_meaning,
                         "Europium or Europium compound")


    def test_multiple_filter_kodak_drxevolution(self):
        """
        Test the material extraction process when the materials are in a MultiValue format
        """
        ds = Dataset()
        ds.FilterMaterial = "aluminum\\copper"
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

        self.assertEqual(source.xrayfilters_set.all().count(), 2, 'Wrong number of filters recorded')
        self.assertEqual(source.xrayfilters_set.all()[0].xray_filter_material.code_meaning,
                         "Aluminum or Aluminum compound")
        self.assertEqual(source.xrayfilters_set.all()[1].xray_filter_material.code_meaning,
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

        self.assertEqual(source.xrayfilters_set.all().count(), 1)
        self.assertEqual(source.xrayfilters_set.all()[0].xray_filter_material.code_meaning,
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

        dx_ge_xr220_1 ="test_files/DX-Im-GE_XR220-1.dcm"
        dx_ge_xr220_2 = "test_files/DX-Im-GE_XR220-2.dcm"
        dx_ge_xr220_3 = "test_files/DX-Im-GE_XR220-3.dcm"
        dx_carestream_dr7500_1 = "test_files/DX-Im-Carestream_DR7500-1.dcm"
        dx_carestream_dr7500_2 = "test_files/DX-Im-Carestream_DR7500-2.dcm"

        root_tests = os.path.dirname(os.path.abspath(__file__))
        dx_ge_xr220_1_path = os.path.join(root_tests, dx_ge_xr220_1)
        dx_ge_xr220_2_path = os.path.join(root_tests, dx_ge_xr220_2)
        dx_ge_xr220_3_path = os.path.join(root_tests, dx_ge_xr220_3)
        dx_carestream_dr7500_1_path = os.path.join(root_tests, dx_carestream_dr7500_1)
        dx_carestream_dr7500_2_path = os.path.join(root_tests, dx_carestream_dr7500_2)

        dx(dx_ge_xr220_1_path)
        dx(dx_ge_xr220_2_path)
        dx(dx_ge_xr220_3_path)
        dx(dx_carestream_dr7500_1_path)
        dx(dx_carestream_dr7500_2_path)

    def test_dr7500_and_xr220(self):
        studies = GeneralStudyModuleAttr.objects.all()

        # Test that five studies have been imported
        self.assertEqual(studies.count(), 2)

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



        # Test that patient level data is recorded correctly
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_name, 'XR220^Samantha')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_name, 'PHYSICS^TABLE AEC')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_id, '00098765')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_id, 'PHY12320140620YU')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_birth_date, datetime.date(1957, 11, 12))
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_birth_date, datetime.date(2014, 6, 20))
        self.assertAlmostEqual(studies[0].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(56.9))

        #Test that irradiation event data is stored correctl
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            acquisition_protocol, 'ABD_1_VIEW')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            acquisition_protocol, 'ABD_1_VIEW')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
            acquisition_protocol, 'ABD_1_VIEW')
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            dose_area_product, Decimal(0.41 / 100000))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            dose_area_product, Decimal(0.82 / 100000))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
            dose_area_product, Decimal(2.05 / 100000))

        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            acquisition_protocol, 'AEC')
        self.assertEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            acquisition_protocol, 'AEC')
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            dose_area_product, Decimal(11.013 / 100000))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            dose_area_product, Decimal(10.157 / 100000))

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(6))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(11))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(27))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(189))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.6))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.6))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
            irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.6))

        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(19))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(18))




        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(189))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(192))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(190))

        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(500))
        self.assertAlmostEqual(studies[1].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(500))


        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(1040))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(2040))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(5040))

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[0].
                               irradeventxraydetectordata_set.get().exposure_index, Decimal(51.745061))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[1].
                               irradeventxraydetectordata_set.get().exposure_index, Decimal(108.843060))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.all()[2].
                               irradeventxraydetectordata_set.get().exposure_index, Decimal(286.828227))
        #exposure_index



    def test_filter_thickness_order(self):
        from remapp.models import XrayFilters

        all_filters = XrayFilters.objects.all()
        for exposure in all_filters:
            self.assertGreaterEqual(exposure.xray_filter_thickness_maximum, exposure.xray_filter_thickness_minimum)
