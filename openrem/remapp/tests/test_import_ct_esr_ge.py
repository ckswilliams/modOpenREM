# This Python file uses the following encoding: utf-8
# test_test_import_esr_ge.py

import os, datetime
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTRDSR(TestCase):
    def test_import_ct_esr_ge(self):
        """
        Imports known GE Enhanced Structured Reports, and tests all the values
        imported against those expected.
        """
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        ge_optima = "test_files/CT-ESR-GE_Optima.dcm"
        ge_vct = "test_files/CT-ESR-GE_VCT.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        ge_optima_path = os.path.join(root_tests, ge_optima)
        ge_vct_path = os.path.join(root_tests, ge_vct)

        rdsr(ge_optima_path)
        rdsr(ge_vct_path)
        studies = GeneralStudyModuleAttr.objects.order_by('id')

        # Test that two studies have been imported
        self.assertEqual(studies.count(), 2)

        # Test that study level data is recorded correctly
        self.assertEqual(studies[0].accession_number, '0012345.12345678')
        self.assertEqual(studies[0].study_date, datetime.date(2006, 8, 23))
        self.assertEqual(studies[0].study_time, datetime.time(11, 40, 14))
        self.assertEqual(studies[0].study_description, 'Colonography')
        self.assertEqual(studies[0].performing_physician_name, 'Doctor^Doctor')
        self.assertEqual(studies[0].name_of_physician_reading_study, 'Radiologist^Doctor')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_name, 'An Optima Hospital')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer, 'GE Medical Systems')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer_model_name, 'Optima CT660')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().station_name, 'geoptima')

        self.assertEqual(studies[1].accession_number, '001234512345678')
        self.assertEqual(studies[1].study_date, datetime.date(2013, 2, 28))
        self.assertEqual(studies[1].study_time, datetime.time(11, 37, 31))
        self.assertEqual(studies[1].study_description, 'FACIAL BONES')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().institution_name, 'A VCT Hospital')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().manufacturer, 'GE Medical Systems')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().manufacturer_model_name, 'LightSpeed VCT')
        self.assertEqual(studies[1].generalequipmentmoduleattr_set.get().station_name, 'VCTScanner')

        # Test that patient level data is recorded correctly
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_name, 'Patient^Optima')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_id, '00001234')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_birth_date, datetime.date(1957, 03, 12))
        self.assertAlmostEqual(studies[0].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(49.4))
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_name, 'Patient^DiscoVCT')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_id, '008F/g234')
        self.assertEqual(studies[1].patientmoduleattr_set.get().patient_birth_date, datetime.date(1923, 05, 9))
        self.assertEqual(studies[1].patientstudymoduleattr_set.get().patient_age, '89Y')
        self.assertAlmostEqual(studies[1].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(89.8))

        # Test that irradiation time data is stored correctly
        self.assertEqual(studies[0].ctradiationdose_set.get().start_of_xray_irradiation,
                         datetime.datetime(2006, 8, 23, 11, 40, 14))
        self.assertEqual(studies[0].ctradiationdose_set.get().end_of_xray_irradiation,
                         datetime.datetime(2006, 8, 23, 11, 48, 40))
        self.assertEqual(studies[1].ctradiationdose_set.get().start_of_xray_irradiation,
                         datetime.datetime(2013, 2, 28, 11, 37, 31))
        self.assertEqual(studies[1].ctradiationdose_set.get().end_of_xray_irradiation,
                         datetime.datetime(2013, 2, 28, 11, 52, 07))

        # Test that device observer data is stored correctly
        self.assertEqual(studies[0].ctradiationdose_set.get().observercontext_set.get().
                         device_observer_name, 'geoptima')
        self.assertEqual(studies[0].ctradiationdose_set.get().observercontext_set.get().
                         device_observer_manufacturer, 'GE Medical Systems')
        self.assertEqual(studies[0].ctradiationdose_set.get().observercontext_set.get().
                         device_observer_model_name, 'Optima CT660')
        self.assertEqual(studies[0].ctradiationdose_set.get().observercontext_set.get().
                         observer_type.code_meaning, 'Device')

        self.assertEqual(studies[1].ctradiationdose_set.get().observercontext_set.get().
                         device_observer_name, 'vct')
        self.assertEqual(studies[1].ctradiationdose_set.get().observercontext_set.get().
                         device_observer_manufacturer, 'GE Medical Systems')
        self.assertEqual(studies[1].ctradiationdose_set.get().observercontext_set.get().
                         device_observer_model_name, 'LightSpeed VCT')
        self.assertEqual(studies[1].ctradiationdose_set.get().observercontext_set.get().
                         observer_type.code_meaning, 'Device')

        # Test that exposure summary data is recorded correctly
        self.assertEqual(studies[0].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         total_number_of_irradiation_events, 6)
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         ct_dose_length_product_total, Decimal(415.82))
        self.assertEqual(studies[1].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         total_number_of_irradiation_events, 27)
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().ctaccumulateddosedata_set.get().
                         ct_dose_length_product_total, Decimal(2002.39))

        # Test that CT dose data is recorded correctly
        self.assertAlmostEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[2].mean_ctdivol, Decimal(3.23))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].dlp, Decimal(155.97))
        self.assertAlmostEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].mean_ctdivol, Decimal(5.3))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].dlp, Decimal(259.85))

        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].mean_ctdivol, Decimal(8.74))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].dlp, Decimal(429.19))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[6].mean_ctdivol, Decimal(4.93))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[6].dlp, Decimal(246.69))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[11].mean_ctdivol, Decimal(6.23))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[11].dlp, Decimal(3.12))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[12].mean_ctdivol, Decimal(22.26))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[12].dlp, Decimal(890.26))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[22].mean_ctdivol, Decimal(176.12))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[22].dlp, Decimal(352.24))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[23].mean_ctdivol, Decimal(29.31))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[23].dlp, Decimal(14.66))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[24].mean_ctdivol, Decimal(29.31))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[24].dlp, Decimal(14.66))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[25].mean_ctdivol, Decimal(31.66))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[25].dlp, Decimal(15.83))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[26].mean_ctdivol, Decimal(32.83))
        self.assertAlmostEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[26].dlp, Decimal(16.41))

        self.assertEqual(
           studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].target_region.code_meaning, 'Abdomen')
        self.assertEqual(
           studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[1].target_region.code_meaning, 'Abdomen')
        self.assertEqual(
           studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[2].target_region.code_meaning, 'Abdomen')
        self.assertEqual(
           studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[3].target_region.code_meaning, 'Abdomen')
        self.assertEqual(
           studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[4].target_region.code_meaning, 'Abdomen')
        self.assertEqual(
           studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].target_region.code_meaning, 'Abdomen')

        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[1].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[2].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[3].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[4].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[6].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[7].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[8].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[9].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[10].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[11].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[12].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[13].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[14].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[15].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[16].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[17].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[18].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[19].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[20].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[21].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[22].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[23].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[24].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[25].target_region.code_meaning, 'Unknown')
        self.assertEqual(
           studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[26].target_region.code_meaning, 'Unknown')

        self.assertEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[1].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[2].
                ct_acquisition_type.code_meaning, 'Spiral Acquisition')
        self.assertEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[3].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[4].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[0].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].
                ct_acquisition_type.code_meaning, 'Spiral Acquisition')

        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[0].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[1].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[2].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[3].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[4].
                ct_acquisition_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[5].
                ct_acquisition_type.code_meaning, 'Spiral Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[6].
                ct_acquisition_type.code_meaning, 'Spiral Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[7].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[8].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[9].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[10].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[11].
                ct_acquisition_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[12].
                ct_acquisition_type.code_meaning, 'Sequenced Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[13].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[14].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[15].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[16].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[17].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[18].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[19].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[20].
                ct_acquisition_type.code_meaning, 'Constant Angle Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[21].
                ct_acquisition_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[22].
                ct_acquisition_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[23].
                ct_acquisition_type.code_meaning, 'Sequenced Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[24].
                ct_acquisition_type.code_meaning, 'Sequenced Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[25].
                ct_acquisition_type.code_meaning, 'Sequenced Acquisition')
        self.assertEqual(
            studies[1].ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id')[26].
                ct_acquisition_type.code_meaning, 'Sequenced Acquisition')


        # Test that scanning length data is recorded correctly
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].scanninglength_set.get().scanning_length, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].scanninglength_set.get().scanning_length, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].scanninglength_set.get().scanning_length, Decimal(418.75))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].scanninglength_set.get().scanning_length, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].scanninglength_set.get().scanning_length, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].scanninglength_set.get().scanning_length, Decimal(443.75))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].scanninglength_set.get().scanning_length, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].scanninglength_set.get().scanning_length, Decimal(468.12))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].scanninglength_set.get().scanning_length, Decimal(468.12))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].scanninglength_set.get().scanning_length, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].scanninglength_set.get().scanning_length, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].scanninglength_set.get().scanning_length, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].scanninglength_set.get().scanning_length, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].scanninglength_set.get().scanning_length, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].scanninglength_set.get().scanning_length, Decimal(397.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].scanninglength_set.get().scanning_length, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].scanninglength_set.get().scanning_length, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].scanninglength_set.get().scanning_length, Decimal(18.75))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].scanninglength_set.get().scanning_length, Decimal(0))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].scanninglength_set.get().scanning_length, Decimal(0))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].scanninglength_set.get().scanning_length, Decimal(0))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].scanninglength_set.get().scanning_length, Decimal(0))

        # Test that CT event data is recorded correctly
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].exposure_time, Decimal(5.6))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].exposure_time, Decimal(5.6))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].exposure_time, Decimal(5.27))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].exposure_time, Decimal(5.6))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].exposure_time, Decimal(5.6))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].exposure_time, Decimal(7.47))

        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].nominal_single_collimation_width, Decimal(0.62))

        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_total_collimation_width, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].nominal_total_collimation_width, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].nominal_total_collimation_width, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].nominal_total_collimation_width, Decimal(560))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].nominal_total_collimation_width, Decimal(5))

        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].number_of_xray_sources, Decimal(1))

        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].pitch_factor, Decimal(1.38))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].pitch_factor, Decimal(0.98))
        self.assertEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].exposure_time, Decimal(7))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].exposure_time, Decimal(12.67))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].exposure_time, Decimal(7.28))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].exposure_time, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].exposure_time, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].exposure_time, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].exposure_time, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].exposure_time, Decimal(0.7))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].exposure_time, Decimal(7))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].exposure_time, Decimal(4.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].exposure_time, Decimal(1.2))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].exposure_time, Decimal(10.01))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].exposure_time, Decimal(10))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].exposure_time, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].exposure_time, Decimal(9))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].exposure_time, Decimal(4))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].nominal_single_collimation_width, Decimal(1.25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].nominal_single_collimation_width, Decimal(0.62))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].nominal_single_collimation_width, Decimal(0.62))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].nominal_total_collimation_width, Decimal(2.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].nominal_total_collimation_width, Decimal(2.5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].nominal_total_collimation_width, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].nominal_total_collimation_width, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].nominal_total_collimation_width, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].nominal_total_collimation_width, Decimal(500))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].nominal_total_collimation_width, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].nominal_total_collimation_width, Decimal(450))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].nominal_total_collimation_width, Decimal(20))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].nominal_total_collimation_width, Decimal(5))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].nominal_total_collimation_width, Decimal(5))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].number_of_xray_sources, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].number_of_xray_sources, Decimal(1))



        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].pitch_factor, Decimal(0.97))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].pitch_factor, Decimal(1.38))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].pitch_factor, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].pitch_factor, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].pitch_factor, Decimal(1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].pitch_factor, Decimal(0.1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].pitch_factor, Decimal(0.1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].pitch_factor, Decimal(0.1))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].pitch_factor, Decimal(0.1))
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].ctdiw_phantom_type.code_meaning, 'IEC Head Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].ctdiw_phantom_type.code_meaning, 'IEC Head Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')
        self.assertEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].ctdiw_phantom_type.code_meaning, 'IEC Body Dosimetry Phantom')


        # Test that CT xraysource data is recorded correctly
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctxraysourceparameters_set.get().
                kvp, Decimal(120))

        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(10))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(20))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(85))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(10))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(20))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(560))

        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(10))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(20))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(85))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(10))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(20))
        self.assertAlmostEqual(studies[0].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(100))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].ctxraysourceparameters_set.get().
                kvp, Decimal(120))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].ctxraysourceparameters_set.get().
                kvp, Decimal(120))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(50))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(30))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].ctxraysourceparameters_set.get().
                maximum_xray_tube_current, Decimal(70))

        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[0].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[1].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[2].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[3].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[4].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[5].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[6].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[7].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[8].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[9].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[10].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[11].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[12].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[13].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[14].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[15].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[16].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[17].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[18].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[19].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[20].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(80))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[21].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(40))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[22].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(200))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[23].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(25))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[24].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(50))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[25].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(30))
        self.assertAlmostEqual(studies[1].ctradiationdose_set.get().
            ctirradiationeventdata_set.order_by('id')[26].ctxraysourceparameters_set.get().
                xray_tube_current, Decimal(70))




class ImportNonDoseSR(TestCase):
    def test_import_esr_non_dose(self):
        """
        Imports Enhanced Structured Reports that isn't a radiadation dose structured report, and tests nothing is
        imported.
        """

        PatientIDSettings.objects.create()

        enhanced_sr = "test_files/ESR_non-dose.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        esr_path = os.path.join(root_tests, enhanced_sr)

        from testfixtures import LogCapture
        with LogCapture() as l:
            rdsr(esr_path)
            studies = GeneralStudyModuleAttr.objects.all()

            # Test that no studies have been imported
            self.assertEqual(studies.count(), 0)
        # Test that log file was written to
        l.check(
            ('remapp.extractors.rdsr', 'WARNING',
             'rdsr.py not attempting to extract from {0}, not a radiation dose structured report'.format(esr_path)))


