# This Python file uses the following encoding: utf-8
# test_import_ct_rdsr_siemens.py

import datetime
import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings, NotPatientIndicatorsID, NotPatientIndicatorsName


class ImportCTRDSR(TestCase):
    def setUp(self):
        """Adds the not-patient patterns to match against - set to be the same as in release 0.7.4"""
        NotPatientIndicatorsID(not_patient_id=u'*qa*').save()
        NotPatientIndicatorsID(not_patient_id=u'*phy*').save()
        NotPatientIndicatorsID(not_patient_id=u'*test*').save()
        NotPatientIndicatorsName(not_patient_name=u'*phys*').save()
        NotPatientIndicatorsName(not_patient_name=u'*test*').save()
        NotPatientIndicatorsName(not_patient_name=u'*qa*').save()


    def test_import_ct_rdsr_siemens(self):
        """
        Imports a known RDSR file derived from a Siemens Definition Flash single source RDSR, and tests all the values
        imported against those expected.
        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/CT-RDSR-Siemens_Flash-TAP-SS.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        # Test that patient identifiable data is not stored
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, None)
        self.assertEqual(study.patientmoduleattr_set.get().not_patient_indicator, None)

        # Test that study level data is recorded correctly
        self.assertEqual(study.study_date, datetime.date(1997, 1, 1))
        self.assertEqual(study.study_time, datetime.time(00, 00, 00))
        self.assertEqual(study.accession_number, 'ACC12345601')
        self.assertEqual(study.study_description, 'Thorax^TAP (Adult)')
        self.assertEqual(study.modality_type, 'CT')
        self.assertEqual(study.referring_physician_name, u'Müller')

        self.assertEqual(study.generalequipmentmoduleattr_set.get().institution_name, 'Hospital Number One Trust')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer, 'SIEMENS')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().manufacturer_model_name, 'SOMATOM Definition Flash')
        self.assertEqual(study.generalequipmentmoduleattr_set.get().station_name, 'CTAWP00001')

        # Test that patient study level data is recorded correctly
        self.assertEqual(study.patientstudymoduleattr_set.get().patient_age, '067Y')
        self.assertAlmostEqual(study.patientstudymoduleattr_set.get().patient_age_decimal, Decimal(67.6))

        # Test that irradiation time data is stored correctly
        self.assertEqual(study.ctradiationdose_set.get().start_of_xray_irradiation,
            datetime.datetime(1997, 1, 1, 0, 6, 31, 737000))
        self.assertEqual(study.ctradiationdose_set.get().end_of_xray_irradiation,
            datetime.datetime(1997, 1, 1, 0, 9, 47, 950000))
        self.assertEqual(study.ctradiationdose_set.get().procedure_reported.code_meaning,
            'Computed Tomography X-Ray')
        self.assertEqual(study.ctradiationdose_set.get().has_intent.code_meaning,
            'Diagnostic Intent')
        self.assertEqual(study.ctradiationdose_set.get().source_of_dose_information.code_meaning, 'Automated Data Collection')

        # Test that device observer data is stored correctly
        self.assertEqual(study.ctradiationdose_set.get().observercontext_set.get().
            device_observer_serial_number, '00001')
        self.assertEqual(study.ctradiationdose_set.get().observercontext_set.get().
            device_observer_name, 'CTAWP00001')
        self.assertEqual(study.ctradiationdose_set.get().observercontext_set.get().
            device_observer_manufacturer, 'SIEMENS')
        self.assertEqual(study.ctradiationdose_set.get().observercontext_set.get().
            device_observer_model_name, 'SOMATOM Definition Flash')
        self.assertEqual(study.ctradiationdose_set.get().observercontext_set.get().
            device_observer_physical_location_during_observation, 'Hospital Number One Trust')
        self.assertEqual(study.ctradiationdose_set.get().observercontext_set.get().
            observer_type.code_meaning, 'Device')
        self.assertEqual(study.ctradiationdose_set.get().scope_of_accumulation.code_meaning, 'Study')

        # Test that exposure data is recorded correctly
        self.assertEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
            total_number_of_irradiation_events, 4)
        self.assertAlmostEqual(study.ctradiationdose_set.get().ctaccumulateddosedata_set.get().
            ct_dose_length_product_total, Decimal(724.52))

        # Test that CT event data is recorded correctly
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].exposure_time, Decimal(8.37))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_single_collimation_width, Decimal(0.6))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_total_collimation_width, Decimal(3.6))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].acquisition_protocol, u'test\xc3\xa6\xc3\xb8\xc3\xa5')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].comment,
                'Internal technical scan parameters: Organ Characteristic = Abdomen, Body Size = Adult, Body Region = Body, X-ray Modulation Type = OFF')
        self.assertEqual(study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].target_region.code_meaning, 'Entire body')
        self.assertEqual(study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].exposure_time, Decimal(0.5))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].nominal_single_collimation_width, Decimal(10))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].nominal_total_collimation_width, Decimal(10))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].acquisition_protocol, 'PreMonitoring')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].comment,
                'Internal technical scan parameters: Organ Characteristic = Abdomen, Body Size = Adult, Body Region = Body, X-ray Modulation Type = OFF')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].exposure_time, Decimal(1.5))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].nominal_single_collimation_width, Decimal(10))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].nominal_total_collimation_width, Decimal(10))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].acquisition_protocol, 'Monitoring')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].comment,
                'Internal technical scan parameters: Organ Characteristic = Abdomen, Body Size = Adult, Body Region = Body, X-ray Modulation Type = OFF')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].exposure_time, Decimal(16.01))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].nominal_single_collimation_width, Decimal(0.6))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].nominal_total_collimation_width, Decimal(38.4))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].pitch_factor, Decimal(0.6))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].acquisition_protocol, 'TAP')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].comment,
                'Internal technical scan parameters: Organ Characteristic = Abdomen, Body Size = Adult, Body Region = Body, X-ray Modulation Type = XYZ_EC')

        self.assertEqual(
            study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[1].
                ct_acquisition_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(
            study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[2].
                ct_acquisition_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(
            study.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[3].
                ct_acquisition_type.code_meaning, 'Spiral Acquisition')

        # Test that CT xraysource data is recorded correctly
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(35))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(35))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(40))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(39))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                exposure_time_per_rotation, Decimal(0.5))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(40))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(39))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                exposure_time_per_rotation, Decimal(0.5))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(560))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(176))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                exposure_time_per_rotation, Decimal(0.5))

        # Test that scanning length data is recorded correctly
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].scanninglength_set.get().scanning_length, Decimal(821))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].scanninglength_set.get().scanning_length, Decimal(10))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].scanninglength_set.get().scanning_length, Decimal(10))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].scanninglength_set.get().scanning_length, Decimal(737))

        # Test that CT Dose data is recorded correctly
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].mean_ctdivol, Decimal(0.14))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].dlp, Decimal(11.51))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].procedure_context.code_meaning, 'CT without contrast')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].mean_ctdivol, Decimal(1.2))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].dlp, Decimal(1.2))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].procedure_context.code_meaning, 'CT without contrast')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].mean_ctdivol, Decimal(3.61))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].dlp, Decimal(3.61))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].procedure_context.code_meaning, 'Diagnostic radiography with contrast media')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].mean_ctdivol, Decimal(9.91))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].dlp, Decimal(708.2))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].procedure_context.code_meaning, 'Diagnostic radiography with contrast media')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].number_of_xray_sources, Decimal(1))
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')

        # Test that 'device participant' data is recorded correctly
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].deviceparticipant_set.get().
                         device_manufacturer, 'SIEMENS')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].deviceparticipant_set.get().
                         device_model_name, 'SOMATOM Definition Flash')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].deviceparticipant_set.get().
                         device_serial_number, '73491')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].deviceparticipant_set.get().
                         device_manufacturer, 'SIEMENS')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].deviceparticipant_set.get().
                         device_model_name, 'SOMATOM Definition Flash')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].deviceparticipant_set.get().
                         device_serial_number, '73491')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].deviceparticipant_set.get().
                         device_manufacturer, 'SIEMENS')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].deviceparticipant_set.get().
                         device_model_name, 'SOMATOM Definition Flash')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[2].deviceparticipant_set.get().
                         device_serial_number, '73491')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].deviceparticipant_set.get().
                         device_manufacturer, 'SIEMENS')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].deviceparticipant_set.get().
                         device_model_name, 'SOMATOM Definition Flash')
        self.assertEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[3].deviceparticipant_set.get().
                         device_serial_number, '73491')

    def test_import_ct_rdsr_siemens_dual_source(self):
        """
        Imports a known RDSR file derived from a Siemens Definition Flash dual source RDSR, and tests all the values
        imported against those expected.
        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/CT-RDSR-Siemens_Flash-QA-DS.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        study = GeneralStudyModuleAttr.objects.order_by('id')[0]

        # Test that patient identifiable data is not stored
        self.assertEqual(study.patientmoduleattr_set.get().patient_name, None)
        # Test that not-patient indicators are identified
        self.assertEqual(study.patientmoduleattr_set.get().not_patient_indicator, u'IDs: *qa* | Names: ')

        # Test that study level data is recorded correctly
        self.assertEqual(study.study_date, datetime.date(2013, 6, 11))
        self.assertEqual(study.study_time, datetime.time(14, 4, 19, 468000))
        self.assertEqual(study.accession_number, '74624646290')
        self.assertEqual(study.study_description, 'Specials^PhysicsTesting (Adult)')
        self.assertEqual(study.modality_type, 'CT')
        self.assertEqual(study.referring_physician_name, u'Müller | Smith')

        # Test that dual energy axial event data is recorded correctly
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].exposure_time, Decimal(0.5))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_single_collimation_width, Decimal(0.6))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_total_collimation_width, Decimal(19.2))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].acquisition_protocol, 'DE_laser align')
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].number_of_xray_sources, Decimal(2))
        self.assertEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].comment,
                'Internal technical scan parameters: Organ Characteristic = Abdomen, Body Size = Adult, Body Region = '
                'Body, X-ray Modulation Type = OFF, Sn Filter (Tube B) = yes')

        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[0].
                kvp, Decimal(100))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[1].
                kvp, Decimal(140))

        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[0].
                maximum_xray_tube_current, Decimal(400))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[1].
                maximum_xray_tube_current, Decimal(310))

        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[0].
                xray_tube_current, Decimal(399))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[1].
                xray_tube_current, Decimal(308))

        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[0].
                exposure_time_per_rotation, Decimal(0.5))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[1].
                exposure_time_per_rotation, Decimal(0.5))

        # Test Dual source series, just exposure time per rotation
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[0].
                exposure_time_per_rotation, Decimal(0.238))
        self.assertAlmostEqual(study.ctradiationdose_set.get().
                ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.order_by(
            'identification_of_the_xray_source')[1].
                exposure_time_per_rotation, Decimal(0.151))

