# This Python file uses the following encoding: utf-8
# test_test_import_mg_rdsr_hologic.py

import datetime
import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportCTRDSR(TestCase):
    def test_import_mg_rdsr_hologic(self):
        """
        Imports a known Hologic Radiation Dose Structured Report, and tests all the values
        imported against those expected.
        """
        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        hologic_2d = "test_files/MG-RDSR-Hologic_2D.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        hologic_2d_path = os.path.join(root_tests, hologic_2d)

        rdsr(hologic_2d_path)
        studies = GeneralStudyModuleAttr.objects.order_by('id')

        # Test that one study has been imported
        self.assertEqual(studies.count(), 1)

        # Test that study level data is recorded correctly
        self.assertEqual(studies[0].study_date, datetime.date(2015, 03, 22))
        self.assertEqual(studies[0].study_time, datetime.time(12, 47, 45))
        self.assertEqual(studies[0].accession_number, 'AJSKDL1234')
        self.assertEqual(studies[0].study_description, 'Bilateral Mammography')
        self.assertEqual(studies[0].study_instance_uid, '1.3.6.1.4.1.5962.99.1.84038123.1638714927.1486142755307.43.0')
        self.assertEqual(studies[0].study_id, '01')
        self.assertEqual(studies[0].modality_type, 'MG')    #Appears as SR in dcmdump?

        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_name, 'OpenREM')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institution_address, 'Milan')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer, 'HOLOGIC, Inc.')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().station_name, 'Dimensions')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().institutional_department_name, 'Mammography')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().manufacturer_model_name, 'Selenia Dimensions')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().device_serial_number, '765467656')
        self.assertEqual(studies[0].generalequipmentmoduleattr_set.get().software_versions, 'AWS:1.8.3.63')

        # Test that patient level data is recorded correctly
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_name, 'Lyons^Samantha')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_id, '00112233')
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_birth_date, datetime.date(1954, 03, 22))
        self.assertEqual(studies[0].patientmoduleattr_set.get().patient_sex, 'F')
        self.assertEqual(studies[0].patientstudymoduleattr_set.get().patient_age, '061Y')
        self.assertAlmostEqual(studies[0].patientstudymoduleattr_set.get().patient_age_decimal, Decimal(61))

        # Test that projectionxrayradiationdose
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().procedure_reported.code_meaning, 'Mammography')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().has_intent.code_meaning, 'Diagnostic Intent')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().scope_of_accumulation.code_meaning, 'Study')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().xray_detector_data_available.code_meaning, 'Yes')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().xray_source_data_available.code_meaning, 'Yes')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().xray_mechanical_data_available.code_meaning, 'Yes')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().source_of_dose_information.code_meaning, 'Computed From Image Attributes')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().observercontext_set.get().
            observer_type.code_meaning, 'Device')

        # Test that exposure summary data is recorded correctly
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.order_by('id').count(), 2)
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.order_by('id')[0].accumulated_average_glandular_dose, Decimal(1.30))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.order_by('id')[0].laterality.code_meaning, "Left breast")
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.order_by('id')[1].accumulated_average_glandular_dose, Decimal(1.28))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.order_by('id')[1].laterality.code_meaning, "Right breast")


        # Test that event level data is recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(1.3))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].entrance_exposure_at_rp, Decimal(3.65))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].half_value_layer, Decimal(0.535))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].acquisition_plane.code_meaning, 'Single Plane')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradiation_event_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].date_time_started, datetime.datetime(2015, 03, 22, 12, 47, 45))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].image_view.code_meaning, 'cranio-caudal')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].target_region.code_meaning, 'Breast')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].reference_point_definition.code_meaning, 'Entrance exposure to a 4.2 cm breast thickness')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].laterality.code_meaning, 'Left')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].laterality.code_meaning, 'Right')

        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().average_glandular_dose, Decimal(1.28))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].entrance_exposure_at_rp, Decimal(3.60))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].half_value_layer, Decimal(0.535))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].acquisition_plane.code_meaning, 'Single Plane')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradiation_event_type.code_meaning, 'Stationary Acquisition')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].date_time_started, datetime.datetime(2015, 03, 22, 12, 50, 15))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].image_view.code_meaning, 'cranio-caudal')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].target_region.code_meaning, 'Breast')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].reference_point_definition.code_meaning, 'Entrance exposure to a 4.2 cm breast thickness')
        #self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
        #    )[1].xray_grid.code_meaning, 'Grid in')

        # Test that xray source data is recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(28.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().kvp_set.get().kvp, Decimal(28.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().exposure_time, Decimal(854.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().exposure_time, Decimal(840.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(100.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().average_xray_tube_current, Decimal(100.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.3))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().focal_spot_size, Decimal(0.3))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().anode_target_material.code_meaning, 'Tungsten or Tungsten compound')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().anode_target_material.code_meaning, 'Tungsten or Tungsten compound')



        # Test that X-ray filter data is recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_minimum, Decimal(0.05))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_minimum, Decimal(0.05))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_maximum, Decimal(0.05))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_maximum, Decimal(0.05))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_type.code_meaning, 'Strip filter')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_type.code_meaning, 'Strip filter')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning, 'Rhodium or Rhodium compound')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning, 'Rhodium or Rhodium compound')


            # Test that exposure data is recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(90200.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraysourcedata_set.get().exposure_set.get().exposure, Decimal(88800.00))

        # Test that mechanical data is recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraymechanicaldata_set.get().positioner_primary_angle, Decimal(0.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraymechanicaldata_set.get().positioner_primary_angle, Decimal(0.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraymechanicaldata_set.get().compression_thickness, Decimal(43.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraymechanicaldata_set.get().compression_thickness, Decimal(43.00))
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraymechanicaldata_set.get().crdr_mechanical_configuration.code_meaning, 'Upright Stand Mount')
        self.assertEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraymechanicaldata_set.get().crdr_mechanical_configuration.code_meaning, 'Upright Stand Mount')

        # Test that dose related distance measurements are recorded correctly
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[0].irradeventxraymechanicaldata_set.get().
                doserelateddistancemeasurements_set.get().distance_source_to_detector, Decimal(700.00))
        self.assertAlmostEqual(studies[0].projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'
            )[1].irradeventxraymechanicaldata_set.get().
                doserelateddistancemeasurements_set.get().distance_source_to_detector, Decimal(700.00))
