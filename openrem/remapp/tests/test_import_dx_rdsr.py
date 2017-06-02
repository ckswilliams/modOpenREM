# This Python file uses the following encoding: utf-8
# test_import_dx_rdsr.py

import os
import datetime
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportDXRDSR(TestCase):
    def test_import_dx_rdsr_canon(self):

        """
        Imports a known RDSR file derived from a canon, and tests all the values
        imported against those expected.
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/DX-RDSR-Canon_CXDI.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        #Test that patient identifiable information is not stored
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, None)
        self.assertEqual(study.patientmoduleattr_set.get().patient_id, None)
        self.assertEqual(study.patientmoduleattr_set.get().patient_birth_date, None)

        # Test that study level data is recorded correctly
        self.assertEqual(study.accession_number, u'3599305798462538')
        self.assertEqual(study.study_date, datetime.date(2016, 8, 18))
        self.assertEqual(study.study_time, datetime.time(19, 25, 1, 650000))
        self.assertEqual(study.modality_type, u'DX')
        self.assertEqual(study.study_description, u'CR THORAX')
        self.assertEqual(study.performing_physician_name, u'Smith^Billy')
        self.assertEqual(study.operator_name, u'Stauss^Brook')

        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_name, u'OpenREM')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, u'Canon Inc.')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer_model_name, u'CXDI Control Software NE')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().station_name, u'CANONDaRt')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().device_serial_number, u'cabd8dc7c6d6dab5db7')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().software_versions, u'2.12.0.20')

        # Test that patient level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, u'058Y')
        self.assertAlmostEqual(study.patientstudymoduleattr_set.get().patient_age_decimal, Decimal(58.3))

        # Test that projectionxrayradiationdose data is stored correctly
        self.assertEqual(study.projectionxrayradiationdose_set.get().procedure_reported.code_meaning, u'Projection X-Ray')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.get().
            observer_type.code_meaning, u'Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.get().
            device_observer_name, u'PC')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.get().
            device_observer_manufacturer, u'Canon Inc.')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.get().
            device_observer_model_name, u'CXDI Control Software NE')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.get().
            device_observer_serial_number, u'cabd8dc7c6d6dab5db7')
        self.assertEqual(study.projectionxrayradiationdose_set.get().
            scope_of_accumulation.code_meaning, u'Performed Procedure Step')
        self.assertEqual(study.projectionxrayradiationdose_set.get().source_of_dose_information.
            code_meaning, 'Automated Data Collection')
        self.assertEqual(study.projectionxrayradiationdose_set.get().has_intent.code_meaning, 'Diagnostic Intent')


        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get().
            dose_area_product, Decimal(0.0000107))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).acquisition_plane.code_meaning, 'Single Plane')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).date_time_started, datetime.datetime(2016, 8, 18, 19, 26, 17, 43000))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradiation_event_type.code_meaning, u'Stationary Acquisition')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).acquisition_protocol, u'THORAX AP 90kv-0,9mAs')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).target_region.code_meaning, u'Chest')

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get().
            accumprojxraydose_set.get().acquisition_dose_area_product_total, Decimal(0.0000107))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get().
            accumprojxraydose_set.get().total_acquisition_time, Decimal(0.005))
        self.assertEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get().
            accumprojxraydose_set.get().reference_point_definition, u'Unknown')


        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().number_of_pulses, Decimal(1))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(90))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current, Decimal(160))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(800))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().exposure_time, Decimal(5))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).irradeventxraysourcedata_set.get().focal_spot_size, Decimal(10))

    def test_import_dx_rdsr_carestream(self):

        """
        Imports a known RDSR file derived from a carestream, and tests all the values
        imported against those expected.
        """

        PatientIDSettings.objects.create()

        dicom_file = "test_files/DX-RDSR-Carestream_DRXEvolution.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        #Test that patient identifiable information is not stored
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, None)
        self.assertEqual(study.patientmoduleattr_set.get().patient_id, None)
        self.assertEqual(study.patientmoduleattr_set.get().patient_birth_date, None)

        # Test that study level data is recorded correctly
        self.assertEqual(study.accession_number, u'7698466579781854')
        self.assertEqual(study.study_date, datetime.date(2016, 3, 9))
        self.assertEqual(study.study_time, datetime.time(17, 28, 33, 689000))
        self.assertEqual(study.modality_type, u'DX')
        self.assertEqual(study.study_description, u'CR LEG')
        self.assertEqual(study.referring_physician_name, u'Mathis^Judy')
        self.assertEqual(study.performing_physician_name, u'Nelson^Colin')
        self.assertEqual(study.operator_name, u'Clark^Laurence')

        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_name, u'OpenREM')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_address, u'London')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, u'CARESTREAM')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer_model_name, u'DRX-Evolution')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().station_name, u'CAREDRXEVO')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().device_serial_number, u'7664565786545')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().software_versions, u'5.7.412.2035')

       # Test that patient level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, u'029Y')
        self.assertAlmostEqual(study.patientstudymoduleattr_set.get().patient_age_decimal, Decimal(29.5))
        self.assertEqual(study.patientmoduleattr_set.get().patient_sex, u'F')

        # Test that projectionxrayradiationdose data is stored correctly
        self.assertEqual(study.projectionxrayradiationdose_set.get().procedure_reported.code_meaning, u'Projection X-Ray')
        #One of these 'observer_type's should be 'person' but it only works if they are noth set as 'device'...
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[0].
            observer_type.code_meaning, u'Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[1].
            observer_type.code_meaning, u'Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[0].
            device_observer_name, u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[0].
            device_observer_manufacturer, u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[0].
            device_observer_model_name, u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[0].
            device_observer_serial_number, u'7664565786545')
        self.assertEqual(study.projectionxrayradiationdose_set.get().observercontext_set.order_by('id')[0].
            device_role_in_procedure.code_meaning, u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().
            scope_of_accumulation.code_meaning, u'Performed Procedure Step')
        self.assertEqual(study.projectionxrayradiationdose_set.get().source_of_dose_information.
            code_meaning, u'Manual Entry')

        self.assertEqual(study.projectionxrayradiationdose_set.get().has_intent.code_meaning, u'Diagnostic Intent')
        self.assertEqual(study.projectionxrayradiationdose_set.get().xray_detector_data_available.code_meaning, u'Yes')
        self.assertEqual(study.projectionxrayradiationdose_set.get().xray_source_data_available.code_meaning, u'Yes')
        self.assertEqual(study.projectionxrayradiationdose_set.get().xray_mechanical_data_available.code_meaning, u'Yes')

        #Check that accumulated xray dose data is recorded correctly
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get().
                        accumintegratedprojradiogdose_set.get().dose_rp_total, Decimal(0.00029927175492))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get().
                        accumintegratedprojradiogdose_set.get().total_number_of_radiographic_frames, Decimal(5))
        self.assertEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get().
                        accumintegratedprojradiogdose_set.get().reference_point_definition_code.code_meaning,
                            u'In Detector Plane')

        #Check that x-ray irradiation event data is stored correctly
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            acquisition_plane.code_meaning, u'Single Plane')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            date_time_started, datetime.datetime(2016,3,9,17,3,17,534000))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradiation_event_type.code_meaning, u'Stationary Acquisition')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            acquisition_protocol, u'Thigh Right')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            anatomical_structure.code_meaning, u'Hip joint')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            target_region.code_meaning, u'Hip joint')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            dose_area_product, Decimal(0.00000082000002))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            reference_point_definition.code_meaning, u'In Detector Plane')

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().exposure_index, Decimal(662.18))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(226.22))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(4.66))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().dose_rp, Decimal(0.00005694444407))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().number_of_pulses, Decimal(1))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(48))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current, Decimal(250))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(18))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(4500))

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_role_in_procedure.code_meaning,
                u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_name,
                u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_manufacturer,
                u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_model_name,
                u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[0].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_serial_number,
                u'7664565786545')

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            acquisition_plane.code_meaning, u'Single Plane')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            date_time_started, datetime.datetime(2016,3,9,17,3,12,87000))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradiation_event_type.code_meaning, u'Stationary Acquisition')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            acquisition_protocol, u'Thigh Right')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            anatomical_structure.code_meaning, u'Femur')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            target_region.code_meaning, u'Femur')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            dose_area_product, Decimal(0.00000093000002))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            reference_point_definition.code_meaning, u'In Detector Plane')

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().exposure_index, Decimal(583.08))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(226.22))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(4.11))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().dose_rp, Decimal(0.00005812500021))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().number_of_pulses, Decimal(1))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(48))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current, Decimal(250))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(18))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(4500))

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_role_in_procedure.code_meaning,
                u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_name,
                u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_manufacturer,
                u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_model_name,
                u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[1].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_serial_number,
                u'7664565786545')

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            acquisition_plane.code_meaning, u'Single Plane')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            date_time_started, datetime.datetime(2016,3,9,17,3,55,725000))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradiation_event_type.code_meaning, u'Stationary Acquisition')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            acquisition_protocol, u'Thigh Right')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            anatomical_structure.code_meaning, u'Femur')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            target_region.code_meaning, u'Femur')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            image_view.code_meaning, u'antero-posterior')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            dose_area_product, Decimal(0.00000057))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            reference_point_definition.code_meaning, u'In Detector Plane')

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraydetectordata_set.get().exposure_index, Decimal(663.54))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(226.22))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(4.67))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().dose_rp, Decimal(0.000064772728))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().number_of_pulses, Decimal(1))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(48))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current, Decimal(250))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(20))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[2].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(5000))

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_role_in_procedure.code_meaning,
                u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_name,
                u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_manufacturer,
                u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_model_name,
                u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_serial_number,
                u'7664565786545')

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            acquisition_plane.code_meaning, u'Single Plane')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            date_time_started, datetime.datetime(2016,3,9,17,3,35,590000))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradiation_event_type.code_meaning, u'Stationary Acquisition')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            acquisition_protocol, u'Thigh Right')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            anatomical_structure.code_meaning, u'Femur')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            target_region.code_meaning, u'Femur')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            image_view.code_meaning, u'antero-posterior')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            dose_area_product, Decimal(0.00000116999998))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            reference_point_definition.code_meaning, u'In Detector Plane')

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraydetectordata_set.get().exposure_index, Decimal(684.78))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(226.22))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(4.81))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().dose_rp, Decimal(0.00006256684428))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().number_of_pulses, Decimal(1))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(49))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current, Decimal(250))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(18))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(4500))

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_role_in_procedure.code_meaning,
                u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_name,
                u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_manufacturer,
                u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_model_name,
                u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_serial_number,
                u'7664565786545')

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_role_in_procedure.code_meaning,
                u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_name,
                u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_manufacturer,
                u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_model_name,
                u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[3].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_serial_number,
                u'7664565786545')

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            acquisition_plane.code_meaning, u'Single Plane')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            date_time_started, datetime.datetime(2016,3,9,17,3,41,533000))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradiation_event_type.code_meaning, u'Stationary Acquisition')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            acquisition_protocol, u'Thigh Right')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            anatomical_structure.code_meaning, u'Femur')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            target_region.code_meaning, u'Femur')
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            dose_area_product, Decimal(0.00000231999993))
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            reference_point_definition.code_meaning, u'In Detector Plane')

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraydetectordata_set.get().exposure_index, Decimal(683.48))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraydetectordata_set.get().target_exposure_index, Decimal(226.22))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraydetectordata_set.get().deviation_index, Decimal(4.80))

        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().dose_rp, Decimal(0.0000568627438))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().number_of_pulses, Decimal(1))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(48))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current, Decimal(250))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().exposure_time, Decimal(18))
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(4500))

        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_role_in_procedure.code_meaning,
                u'Irradiating Device')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_name,
                u'CAREDXEVO')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_manufacturer,
                u'CARESTREAM')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_model_name,
                u'DRX-Evolution')
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')[4].
            irradeventxraysourcedata_set.get().deviceparticipant_set.get().device_serial_number,
                u'7664565786545')