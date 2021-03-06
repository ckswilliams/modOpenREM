# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


# TODO: Run through all ForeignKey fields in models and change them in both directions


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Renaming model from 'Ct_dose_check_details' to 'CtDoseCheckDetails'
        db.rename_table(u'remapp_ct_dose_check_details', u'remapp_ctdosecheckdetails')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ct_dose_check_details').update(model='ctdosecheckdetails')

        # Renaming model from 'Ct_radiation_dose' to 'CtRadiationDose'
        db.rename_table(u'remapp_ct_radiation_dose', u'remapp_ctradiationdose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ct_radiation_dose').update(model='ctradiationdose')

        # Renaming model from 'Accumulated_projection_xray_dose' to 'AccumProjXRayDose'
        db.rename_table(u'remapp_accumulated_projection_xray_dose', u'remapp_accumprojxraydose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumulated_projection_xray_dose').update(model='accumprojxraydose')

        # Renaming model from 'Patient_study_module_attributes' to 'PatientStudyModuleAttr'
        db.rename_table(u'remapp_patient_study_module_attributes', u'remapp_patientstudymoduleattr')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='patient_study_module_attributes').update(model='patientstudymoduleattr')

        # Renaming model from 'Size_upload' to 'SizeUpload'
        db.rename_table(u'remapp_size_upload', u'remapp_sizeupload')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='size_upload').update(model='sizeupload')

        # Renaming model from 'General_equipment_module_attributes' to 'GeneralEquipmentModuleAttr'
        db.rename_table(u'remapp_general_equipment_module_attributes', u'remapp_generalequipmentmoduleattr')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='general_equipment_module_attributes').update(
                model='generalequipmentmoduleattr')

        # Renaming model from 'Accumulated_cassette_based_projection_radiography_dose' to
        # 'AccumCassetteBsdProjRadiogDose'
        db.rename_table(u'remapp_accumulated_cassette_based_projection_radiography_dose',
                        u'remapp_accumcassettebsdprojradiogdose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumulated_cassette_based_projection_radiography_dose'
            ).update(model='accumcassettebsdprojradiogdose')

        # Renaming model from 'Pulse_width' to 'PulseWidth'
        db.rename_table(u'remapp_pulse_width', u'remapp_pulsewidth')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='pulse_width').update(model='pulsewidth')

        # Renaming model from 'Person_participant' to 'PersonParticipant'
        db.rename_table(u'remapp_person_participant', u'remapp_personparticipant')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='person_participant').update(model='personparticipant')

        # Renaming model from 'Projection_xray_radiation_dose' to 'ProjectionXRayRadiationDose'
        db.rename_table(u'remapp_projection_xray_radiation_dose', u'remapp_projectionxrayradiationdose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='projection_xray_radiation_dose').update(model='projectionxrayradiationdose')

        # Renaming model from 'Irradiation_event_xray_source_data' to 'IrradEventXRaySourceData'
        db.rename_table(u'remapp_irradiation_event_xray_source_data', u'remapp_irradeventxraysourcedata')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradiation_event_xray_source_data').update(model='irradeventxraysourcedata')

        # Renaming model from 'Ct_accumulated_dose_data' to 'CtAccumulatedDoseData'
        db.rename_table(u'remapp_ct_accumulated_dose_data', u'remapp_ctaccumulateddosedata')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ct_accumulated_dose_data').update(model='ctaccumulateddosedata')

        # Renaming model from 'Device_participant' to 'DeviceParticipant'
        db.rename_table(u'remapp_device_participant', u'remapp_deviceparticipant')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='device_participant').update(model='deviceparticipant')

        # Renaming model from 'Image_view_modifier' to 'ImageViewModifier'
        db.rename_table(u'remapp_image_view_modifier', u'remapp_imageviewmodifier')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='image_view_modifier').update(model='imageviewmodifier')

        # Renaming model from 'Scanning_length' to 'ScanningLength'
        db.rename_table(u'remapp_scanning_length', u'remapp_scanninglength')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='scanning_length').update(model='scanninglength')

        # Renaming model from 'Accumulated_xray_dose' to 'AccumXRayDose'
        db.rename_table(u'remapp_accumulated_xray_dose', u'remapp_accumxraydose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumulated_xray_dose').update(model='accumxraydose')

        # Renaming model from 'Irradiation_event_xray_mechanical_data' to 'IrradEventXRayMechanicalData'
        db.rename_table(u'remapp_irradiation_event_xray_mechanical_data', u'remapp_irradeventxraymechanicaldata')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradiation_event_xray_mechanical_data'
            ).update(model='irradeventxraymechanicaldata')

        # Renaming model from 'Xray_tube_current' to 'XrayTubeCurrent'
        db.rename_table(u'remapp_xray_tube_current', u'remapp_xraytubecurrent')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='xray_tube_current').update(model='xraytubecurrent')

        # Renaming model from 'Xray_filters' to 'XrayFilters'
        db.rename_table(u'remapp_xray_filters', u'remapp_xrayfilters')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='xray_filters').update(model='xrayfilters')

        # Renaming model from 'Xray_grid' to 'XrayGrid'
        db.rename_table(u'remapp_xray_grid', u'remapp_xraygrid')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='xray_grid').update(model='xraygrid')

        # Renaming model from 'Content_item_descriptions' to 'ContextID'
        db.rename_table(u'remapp_content_item_descriptions', u'remapp_contextid')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='content_item_descriptions').update(model='contextid')

        # Renaming model from 'Accumulated_mammography_xray_dose' to 'AccumMammographyXRayDose'
        db.rename_table(u'remapp_accumulated_mammography_xray_dose', u'remapp_accummammographyxraydose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumulated_mammography_xray_dose').update(model='accummammographyxraydose')

        # Renaming model from 'Observer_context' to 'ObserverContext'
        db.rename_table(u'remapp_observer_context', u'remapp_observercontext')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='observer_context').update(model='observercontext')

        # Renaming model from 'Accumulated_integrated_projection_radiography_dose' to 'AccumIntegratedProjRadiogDose'
        db.rename_table(
            u'remapp_accumulated_integrated_projection_radiography_dose', u'remapp_accumintegratedprojradiogdose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumulated_integrated_projection_radiography_dose'
            ).update(model='accumintegratedprojradiogdose')

        # Renaming model from 'Ct_xray_source_parameters' to 'CtXRaySourceParameters'
        db.rename_table(u'remapp_ct_xray_source_parameters', u'remapp_ctxraysourceparameters')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ct_xray_source_parameters').update(model='ctxraysourceparameters')

        # Renaming model from 'General_study_module_attributes' to 'GeneralStudyModuleAttr'
        db.rename_table(u'remapp_general_study_module_attributes', u'remapp_generalstudymoduleattr')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='general_study_module_attributes').update(model='generalstudymoduleattr')

        # Renaming model from 'Dose_related_distance_measurements' to 'DoseRelatedDistanceMeasurements'
        db.rename_table(u'remapp_dose_related_distance_measurements', u'remapp_doserelateddistancemeasurements')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='dose_related_distance_measurements'
            ).update(model='doserelateddistancemeasurements')

        # Renaming model from 'Irradiation_event_xray_detector_data' to 'IrradEventXRayDetectorData'
        db.rename_table(u'remapp_irradiation_event_xray_detector_data', u'remapp_irradeventxraydetectordata')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradiation_event_xray_detector_data'
            ).update(model='irradeventxraydetectordata')

        # Renaming model from 'Ct_irradiation_event_data' to 'CtIrradiationEventData'
        db.rename_table(u'remapp_ct_irradiation_event_data', u'remapp_ctirradiationeventdata')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ct_irradiation_event_data').update(model='ctirradiationeventdata')

        # Renaming model from 'Irradiation_event_xray_data' to 'IrradEventXRayData'
        db.rename_table(u'remapp_irradiation_event_xray_data', u'remapp_irradeventxraydata')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradiation_event_xray_data').update(model='irradeventxraydata')

        # Renaming model from 'Patient_module_attributes' to 'PatientModuleAttr'
        db.rename_table(u'remapp_patient_module_attributes', u'remapp_patientmoduleattr')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='patient_module_attributes').update(model='patientmoduleattr')


    def backwards(self, orm):
        # Renaming model from 'CtDoseCheckDetails' to 'Ct_dose_check_details'
        db.rename_table(u'remapp_ctdosecheckdetails', u'remapp_ct_dose_check_details')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ctdosecheckdetails').update(model='ct_dose_check_details')

        # Renaming model from 'CtRadiationDose' to 'Ct_radiation_dose'
        db.rename_table(u'remapp_ctradiationdose', u'remapp_ct_radiation_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ctradiationdose').update(model='ct_radiation_dose')

        # Renaming model from 'AccumXRayDose' to 'Accumulated_projection_xray_dose'
        db.rename_table(u'remapp_accumxraydose', u'remapp_accumulated_projection_xray_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumxraydose').update(model='accumulated_projection_xray_dose')

        # Renaming model from 'PatientStudyModuleAttr' to 'Patient_study_module_attributes'
        db.rename_table(u'remapp_patientstudymoduleattr', u'remapp_patient_study_module_attributes')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='patientstudymoduleattr').update(model='patient_study_module_attributes')

        # Renaming model from 'SizeUpload' to 'Size_upload'
        db.rename_table(u'remapp_sizeupload', u'remapp_size_upload')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='sizeupload').update(model='size_upload')

        # Renaming model from 'GeneralEquipmentModuleAttr' to 'General_equipment_module_attributes'
        db.rename_table(u'remapp_generalequipmentmoduleattr', u'remapp_general_equipment_module_attributes')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='generalequipmentmoduleattr').update(
                model='general_equipment_module_attributes')

        # Renaming model from 'AccumCassetteBsdProjRadiogDose' to
        # 'Accumulated_cassette_based_projection_radiography_dose'
        db.rename_table(u'remapp_accumcassettebsdprojradiogdose',
                        u'remapp_accumulated_cassette_based_projection_radiography_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumcassettebsdprojradiogdose'
            ).update(model='accumulated_cassette_based_projection_radiography_dose')

        # Renaming model from 'PulseWidth' to 'Pulse_width'
        db.rename_table(u'remapp_pulsewidth', u'remapp_pulse_width')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='pulsewidth').update(model='pulse_width')

        # Renaming model from 'PersonParticipant' to 'Person_participant'
        db.rename_table(u'remapp_personparticipant', u'remapp_person_participant')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='personparticipant').update(model='person_participant')

        # Renaming model from 'ProjectionXRayRadiationDose' to 'Projection_xray_radiation_dose'
        db.rename_table(u'remapp_projectionxrayradiationdose', u'remapp_projection_xray_radiation_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='projectionxrayradiationdose').update(model='projection_xray_radiation_dose')

        # Renaming model from 'IrradEventXRaySourceData' to 'Irradiation_event_xray_source_data'
        db.rename_table(u'remapp_irradeventxraysourcedata', u'remapp_irradiation_event_xray_source_data')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradeventxraysourcedata').update(model='irradiation_event_xray_source_data')

        # Renaming model from 'CtAccumulatedDoseData' to 'Ct_accumulated_dose_data'
        db.rename_table(u'remapp_ctaccumulateddosedata', u'remapp_ct_accumulated_dose_data')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ctaccumulateddosedata').update(model='ct_accumulated_dose_data')

        # Renaming model from 'DeviceParticipant' to 'Device_participant'
        db.rename_table(u'remapp_deviceparticipant', u'remapp_device_participant')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='deviceparticipant').update(model='device_participant')

        # Renaming model from 'ImageViewModifier' to 'Image_view_modifier'
        db.rename_table(u'remapp_imageviewmodifier', u'remapp_image_view_modifier')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='imageviewmodifier').update(model='image_view_modifier')

        # Renaming model from 'ScanningLength' to 'Scanning_length'
        db.rename_table(u'remapp_scanninglength', u'remapp_scanning_length')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='scanninglength').update(model='scanning_length')

        # Renaming model from 'AccumXRayDose' to 'Accumulated_xray_dose'
        db.rename_table(u'remapp_accumxraydose', u'remapp_accumulated_xray_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumxraydose').update(model='accumulated_xray_dose')

        # Renaming model from 'IrradEventXRayMechanicalData' to 'Irradiation_event_xray_mechanical_data'
        db.rename_table(u'remapp_irradeventxraymechanicaldata', u'remapp_irradiation_event_xray_mechanical_data')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradeventxraymechanicaldata'
            ).update(model='irradiation_event_xray_mechanical_data')

        # Renaming model from 'XrayTubeCurrent' to 'Xray_tube_current'
        db.rename_table(u'remapp_xraytubecurrent', u'remapp_xray_tube_current')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='xraytubecurrent').update(model='xray_tube_current')

        # Renaming model from 'XrayFilters' to 'Xray_filters'
        db.rename_table(u'remapp_xrayfilters', u'remapp_xray_filters')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='xrayfilters').update(model='xray_filters')

        # Renaming model from 'XrayGrid' to 'Xray_grid'
        db.rename_table(u'remapp_xraygrid', u'remapp_xray_grid')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='xraygrid').update(model='xray_grid')

        # Renaming model from 'ContextID' to 'Content_item_descriptions'
        db.rename_table(u'remapp_contextid', u'remapp_content_item_descriptions')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='contextid').update(model='content_item_descriptions')

        # Renaming model from 'AccumMammographyXRayDose' to 'Accumulated_mammography_xray_dose'
        db.rename_table(u'remapp_accummammographyxraydose', u'remapp_accumulated_mammography_xray_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accummammographyxraydose').update(model='accumulated_mammography_xray_dose')

        # Renaming model from 'ObserverContext' to 'Observer_context'
        db.rename_table(u'remapp_observercontext', u'remapp_observer_context')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='observercontext').update(model='observer_context')

        # Renaming model from 'AccumIntegratedProjRadiogDose' to 'Accumulated_integrated_projection_radiography_dose'
        db.rename_table(
            u'remapp_accumintegratedprojradiogdose', u'remapp_accumulated_integrated_projection_radiography_dose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumintegratedprojradiogdose'
            ).update(model='accumulated_integrated_projection_radiography_dose')

        # Renaming model from 'CtXRaySourceParameters' to 'Ct_xray_source_parameters'
        db.rename_table(u'remapp_ctxraysourceparameters', u'remapp_ct_xray_source_parameters')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ctxraysourceparameters').update(model='ct_xray_source_parameters')

        # Renaming model from 'GeneralStudyModuleAttr' to 'General_study_module_attributes'
        db.rename_table(u'remapp_generalstudymoduleattr', u'remapp_general_study_module_attributes')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='generalstudymoduleattr').update(model='general_study_module_attributes')

        # Renaming model from 'DoseRelatedDistanceMeasurements' to 'Dose_related_distance_measurements'
        db.rename_table(u'remapp_doserelateddistancemeasurements', u'remapp_dose_related_distance_measurements')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='doserelateddistancemeasurements'
            ).update(model='dose_related_distance_measurements')

        # Renaming model from 'IrradEventXRayDetectorData' to 'Irradiation_event_xray_detector_data'
        db.rename_table(u'remapp_irradeventxraydetectordata', u'remapp_irradiation_event_xray_detector_data')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradeventxraydetectordata'
            ).update(model='irradiation_event_xray_detector_data')

        # Renaming model from 'CtIrradiationEventData' to 'Ct_irradiation_event_data'
        db.rename_table(u'remapp_ctirradiationeventdata', u'remapp_ct_irradiation_event_data')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ctirradiationeventdata').update(model='ct_irradiation_event_data')

        # Renaming model from 'IrradEventXRayData' to 'Irradiation_event_xray_data'
        db.rename_table(u'remapp_irradeventxraydata', u'remapp_irradiation_event_xray_data')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='irradeventxraydata').update(model='irradiation_event_xray_data')

        # Renaming model from 'PatientModuleAttr' to 'Patient_module_attributes'
        db.rename_table(u'remapp_patientmoduleattr', u'remapp_patient_module_attributes')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='patientmoduleattr').update(model='patient_module_attributes')
