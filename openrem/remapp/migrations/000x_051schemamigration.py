# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


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

        #
        # Changing ForeignKey fields in models who's names haven't changed
        #
        # Changing field 'Kvp.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_kvp', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))

        # Changing field 'Calibration.dose_measurement_device'
        db.alter_column(u'remapp_calibration', 'dose_measurement_device_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True))

        # Changing field 'Calibration.accumulated_xray_dose'
        db.alter_column(u'remapp_calibration', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose']))

        # Changing field 'Exposure.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_exposure', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))

        #
        # Changing ForeignKey fields in models who's names have changed
        #
        # Changing field 'AccumXrayDose.projection_xray_radiation_dose' and 'AccumXRayDose.acquisition_plane'
        db.alter_column(u'remapp_accumxraydose', 'projection_xray_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose']))
        db.alter_column(u'remapp_accumxraydose', 'acquisition_plane_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # Changing field 'CtIrradiationEventData.ct_radiation_dose', 'target_region', 'ct_acquisition_type',
        # 'procedure_context', 'ctdiw_phantom_type' and 'measurement_method'
        db.alter_column(u'remapp_ctirradiationeventdata', 'ct_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose']))
        db.alter_column(u'remapp_ctirradiationeventdata', 'target_region_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_region', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctirradiationeventdata', 'ct_acquisition_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_type', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctirradiationeventdata', 'procedure_context_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_context', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctirradiationeventdata', 'ctdiw_phantom_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_phantom', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctirradiationeventdata', 'measurement_method_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_method', null=True, to=orm['remapp.ContextID']))

        # Changing field 'IrradEventXRayDetectorData.irradiation_event_xray_data'
        db.alter_column(u'remapp_irradeventxraydetectordata', 'irradiation_event_xray_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData']))

        # 'IrradEventXRayData.projection_xray_radiation_dose', 'acquisition_plane', 'label_type', 'irradiation_event_type',
        # 'anatomical_structure', 'laterality', 'image_view', 'target_region' and 'reference_point_definition'
        db.alter_column(u'remapp_irradeventxraydata', 'projection_xray_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose']))
        db.alter_column(u'remapp_irradeventxraydata', 'acquisition_plane_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_plane', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'label_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_labeltype', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'irradiation_event_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_eventtype', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'anatomical_structure_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_anatomy', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'laterality_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_laterality', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'image_view_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_view', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'target_region_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_region', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraydata', 'reference_point_definition_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_rpdefinition', null=True, to=orm['remapp.ContextID']))

        # 'CtDoseCheckDetails.ct_irradiation_event_data'
        db.alter_column(u'remapp_ctdosecheckdetails', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData']))

        # 'PatientModuleAttr.general_study_module_attributes'
        db.alter_column(u'remapp_patientmoduleattr', 'general_study_module_attributes_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr']))

        # 'ScanningLength.ct_irradiation_event_data'
        db.alter_column(u'remapp_scanninglength', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData']))

        # 'CtXRaySourceParameters.ct_irradiation_event_data'
        db.alter_column(u'remapp_ctxraysourceparameters', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData']))

        # 'AccumMammographyXRayDose.accumulated_xray_dose' and 'laterality'
        db.alter_column(u'remapp_accummammographyxraydose', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose']))
        db.alter_column(u'remapp_accummammographyxraydose', 'laterality_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'AccumIntegratedProjRadiogDose.accumulated_xray_dose' and 'reference_point_definition_code'
        db.alter_column(u'remapp_accumintegratedprojradiogdose', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose']))
        db.alter_column(u'remapp_accumintegratedprojradiogdose', 'reference_point_definition_code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'CtAccumulatedDoseData.ct_radiation_dose', 'reference_authority_code' and 'measurement_method'
        db.alter_column(u'remapp_ctaccumulateddosedata', 'ct_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose']))
        db.alter_column(u'remapp_ctaccumulateddosedata', 'reference_authority_code_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10012_authority', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctaccumulateddosedata', 'measurement_method_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10012_method', null=True, to=orm['remapp.ContextID']))

        # 'DoseRelatedDistanceMeasurements.irradiation_event_xray_mechanical_data'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'irradiation_event_xray_mechanical_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayMechanicalData']))

        # 'AccumCassetteBsdProjRadiogDose.accumulated_xray_dose' and 'detector_type'
        db.alter_column(u'remapp_accumcassettebsdprojradiogdose', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose']))
        db.alter_column(u'remapp_accumcassettebsdprojradiogdose', 'detector_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'GeneralEquipmentModuleAttr.general_study_module_attributes'
        db.alter_column(u'remapp_generalequipmentmoduleattr', 'general_study_module_attributes_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr']))

        # 'XrayFilters.irradiation_event_xray_source_data', 'xray_filter_type' and 'xray_filter_material'
        db.alter_column(u'remapp_xrayfilters', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))
        db.alter_column(u'remapp_xrayfilters', 'xray_filter_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='xrayfilters_type', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_xrayfilters', 'xray_filter_material_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='xrayfilters_material', null=True, to=orm['remapp.ContextID']))

        # 'PatientStudyModuleAttr.general_study_module_attributes'
        db.alter_column(u'remapp_patientstudymoduleattr', 'general_study_module_attributes_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr']))

        # 'IrradEventXRayMechanicalData.irradiation_event_xray_data' and 'crdr_mechanical_configuration'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'irradiation_event_xray_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData']))
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'crdr_mechanical_configuration_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'ObserverContext.projection_xray_radiation_dose', 'ct_radiation_dose', 'observer_type' and 'device_role_in_procedure'
        db.alter_column(u'remapp_observercontext', 'projection_xray_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose'], null=True, blank=True))
        db.alter_column(u'remapp_observercontext', 'ct_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'], null=True, blank=True)),
        db.alter_column(u'remapp_observercontext', 'observer_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_observertype', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_observercontext', 'device_role_in_procedure_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_role', null=True, to=orm['remapp.ContextID']))

        # 'PersonParticipant.projection_xray_radiation_dose', 'ct_radiation_dose', 'irradiation_event_xray_data',
        # 'ct_accumulated_dose_data', 'ct_irradiation_event_data', 'ct_dose_check_details_alert' and 'ct_dose_check_details_notification'
        db.alter_column(u'remapp_personparticipant', 'projection_xray_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose'], null=True, blank=True))
        db.alter_column(u'remapp_personparticipant', 'ct_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'], null=True, blank=True))
        db.alter_column(u'remapp_personparticipant', 'irradiation_event_xray_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData'], null=True, blank=True))
        db.alter_column(u'remapp_personparticipant', 'ct_accumulated_dose_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtAccumulatedDoseData'], null=True, blank=True))
        db.alter_column(u'remapp_personparticipant', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'], null=True, blank=True))
        db.alter_column(u'remapp_personparticipant', 'ct_dose_check_details_alert_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_alert', null=True, to=orm['remapp.CtDoseCheckDetails']))
        db.alter_column(u'remapp_personparticipant', 'ct_dose_check_details_notification_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_notification', null=True, to=orm['remapp.CtDoseCheckDetails']))

        # 'ProjectionXRayRadiationDose.general_study_module_attributes', 'procedure_reported', 'has_intent'.
        # 'scope_of_accumulation', 'xray_detector_data_available', 'xray_source_data_available',
        # 'xray_mechanical_data_available' and 'source_of_dose_information'
        db.alter_column(u'remapp_projectionxrayradiationdose', 'general_study_module_attributes_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'procedure_reported_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_procedure', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'has_intent_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_intent', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'scope_of_accumulation_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_scope', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'xray_detector_data_available_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_detector', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'xray_source_data_available_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_source', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'xray_mechanical_data_available_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_mech', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_projectionxrayradiationdose', 'source_of_dose_information_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_infosource', null=True, to=orm['remapp.ContextID']))

        # 'XrayTubeCurrent.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_xraytubecurrent', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))

        # 'CtRadiationDose.general_study_module_attributes', 'procedure_reported', 'has_intent', 'scope_of_accumulation'
        # and 'source_of_dose_information'
        db.alter_column(u'remapp_ctradiationdose', 'general_study_module_attributes_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr']))
        db.alter_column(u'remapp_ctradiationdose', 'procedure_reported_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_procedure', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctradiationdose', 'has_intent_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_intent', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctradiationdose', 'scope_of_accumulation_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_scope', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_ctradiationdose', 'source_of_dose_information_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_source', null=True, to=orm['remapp.ContextID']))

        # 'AccumProjXRayDose.accumulated_xray_dose' and 'reference_point_definition_code'
        db.alter_column(u'remapp_accumprojxraydose', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose']))
        db.alter_column(u'remapp_accumprojxraydose', 'reference_point_definition_code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'PulseWidth.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_pulsewidth', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))

        # 'IrradEventXRaySourceData.irradiation_event_xray_data', 'reference_point_definition_code', 'fluoro_mode' and 'anode_target_material'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'irradiation_event_xray_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData']))
        db.alter_column(u'remapp_irradeventxraysourcedata', 'reference_point_definition_code_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_rpdefinition', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraysourcedata', 'fluoro_mode_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_fluoromode', null=True, to=orm['remapp.ContextID']))
        db.alter_column(u'remapp_irradeventxraysourcedata', 'anode_target_material_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_anodetarget', null=True, to=orm['remapp.ContextID']))

        # 'XrayGrid.irradiation_event_xray_source_data' and 'xray_grid'
        db.alter_column(u'remapp_xraygrid', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))
        db.alter_column(u'remapp_xraygrid', 'xray_grid_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'ImageViewModifier.irradiation_event_xray_data' and 'image_view_modifier'
        db.alter_column(u'remapp_imageviewmodifier', 'irradiation_event_xray_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData']))
        db.alter_column(u'remapp_imageviewmodifier', 'image_view_modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        # 'DeviceParticipant.accumulated_xray_dose', 'irradiation_event_xray_detector_data',
        # 'irradiation_event_xray_source_data, 'ct_accumulated_dose_data', 'ct_irradiation_event_data' and
        # 'device_role_in_procedure'
        db.alter_column(u'remapp_deviceparticipant', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose'], null=True, blank=True))
        db.alter_column(u'remapp_deviceparticipant', 'irradiation_event_xray_detector_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayDetectorData'], null=True, blank=True))
        db.alter_column(u'remapp_deviceparticipant', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData'], null=True, blank=True))
        db.alter_column(u'remapp_deviceparticipant', 'ct_accumulated_dose_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtAccumulatedDoseData'], null=True, blank=True))
        db.alter_column(u'remapp_deviceparticipant', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'], null=True, blank=True))
        db.alter_column(u'remapp_deviceparticipant', 'device_role_in_procedure_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True))

        #######################################
        #
        #  Remaining database changes for 0.5.1
        #
        #######################################

        # Adding model 'CtReconstructionAlgorithm'
        db.create_table(u'remapp_ctreconstructionalgorithm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'])),
            ('reconstruction_algorithm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['CtReconstructionAlgorithm'])

        # Adding model 'SizeSpecificDoseEstimation'
        db.create_table(u'remapp_sizespecificdoseestimation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'])),
            ('measurement_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
            ('measured_lateral_dimension', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('measured_ap_dimension', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('derived_effective_diameter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['SizeSpecificDoseEstimation'])

        # Adding model 'SourceOfCTDoseInformation'
        db.create_table(u'remapp_sourceofctdoseinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'])),
            ('source_of_dose_information', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['SourceOfCTDoseInformation'])

        # Adding field 'CtIrradiationEventData.irradiation_event_label'
        db.add_column(u'remapp_ctirradiationeventdata', 'irradiation_event_label',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CtIrradiationEventData.label_type'
        db.add_column(u'remapp_ctirradiationeventdata', 'label_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_labeltype', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)


        # Changing field 'CtIrradiationEventData.exposure_time'
        db.alter_column(u'remapp_ctirradiationeventdata', 'exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.ctdifreeair_calculation_factor'
        db.alter_column(u'remapp_ctirradiationeventdata', 'ctdifreeair_calculation_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.mean_ctdivol'
        db.alter_column(u'remapp_ctirradiationeventdata', 'mean_ctdivol', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.effective_dose'
        db.alter_column(u'remapp_ctirradiationeventdata', 'effective_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.number_of_xray_sources'
        db.alter_column(u'remapp_ctirradiationeventdata', 'number_of_xray_sources', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=0))

        # Changing field 'CtIrradiationEventData.mean_ctdifreeair'
        db.alter_column(u'remapp_ctirradiationeventdata', 'mean_ctdifreeair', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.dlp'
        db.alter_column(u'remapp_ctirradiationeventdata', 'dlp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.effective_dose_conversion_factor'
        db.alter_column(u'remapp_ctirradiationeventdata', 'effective_dose_conversion_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.nominal_single_collimation_width'
        db.alter_column(u'remapp_ctirradiationeventdata', 'nominal_single_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.pitch_factor'
        db.alter_column(u'remapp_ctirradiationeventdata', 'pitch_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtIrradiationEventData.nominal_total_collimation_width'
        db.alter_column(u'remapp_ctirradiationeventdata', 'nominal_total_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayDetectorData.deviation_index'
        db.alter_column(u'remapp_irradeventxraydetectordata', 'deviation_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayDetectorData.sensitivity'
        db.alter_column(u'remapp_irradeventxraydetectordata', 'sensitivity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayDetectorData.relative_xray_exposure'
        db.alter_column(u'remapp_irradeventxraydetectordata', 'relative_xray_exposure', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayDetectorData.exposure_index'
        db.alter_column(u'remapp_irradeventxraydetectordata', 'exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayDetectorData.target_exposure_index'
        db.alter_column(u'remapp_irradeventxraydetectordata', 'target_exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'IrradEventXRayData.projection_eponymous_name_cid'
        db.add_column(u'remapp_irradeventxraydata', 'projection_eponymous_name_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_pojectioneponymous', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'IrradEventXRayData.patient_table_relationship_cid'
        db.add_column(u'remapp_irradeventxraydata', 'patient_table_relationship_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_pttablerel', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'IrradEventXRayData.patient_orientation_cid'
        db.add_column(u'remapp_irradeventxraydata', 'patient_orientation_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_ptorientation', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'IrradEventXRayData.patient_orientation_modifier_cid'
        db.add_column(u'remapp_irradeventxraydata', 'patient_orientation_modifier_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_ptorientationmod', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'IrradEventXRayData.patient_equivalent_thickness'
        db.add_column(u'remapp_irradeventxraydata', 'patient_equivalent_thickness',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRayData.breast_composition_cid'
        db.add_column(u'remapp_irradeventxraydata', 'breast_composition_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_breastcomposition', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)


        # Changing field 'IrradEventXRayData.entrance_exposure_at_rp'
        db.alter_column(u'remapp_irradeventxraydata', 'entrance_exposure_at_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayData.patient_table_relationship'
        db.alter_column(u'remapp_irradeventxraydata', 'patient_table_relationship', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'IrradEventXRayData.percent_fibroglandular_tissue'
        db.alter_column(u'remapp_irradeventxraydata', 'percent_fibroglandular_tissue', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayData.patient_orientation_modifier'
        db.alter_column(u'remapp_irradeventxraydata', 'patient_orientation_modifier', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'IrradEventXRayData.half_value_layer'
        db.alter_column(u'remapp_irradeventxraydata', 'half_value_layer', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayData.patient_orientation'
        db.alter_column(u'remapp_irradeventxraydata', 'patient_orientation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'IrradEventXRayData.projection_eponymous_name'
        db.alter_column(u'remapp_irradeventxraydata', 'projection_eponymous_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'IrradEventXRayData.dose_area_product'
        db.alter_column(u'remapp_irradeventxraydata', 'dose_area_product', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10))

        # Changing field 'IrradEventXRayData.breast_composition'
        db.alter_column(u'remapp_irradeventxraydata', 'breast_composition', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'CtDoseCheckDetails.accumulated_dlp_forward_estimate'
        db.alter_column(u'remapp_ctdosecheckdetails', 'accumulated_dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtDoseCheckDetails.accumulated_ctdivol_forward_estimate'
        db.alter_column(u'remapp_ctdosecheckdetails', 'accumulated_ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtDoseCheckDetails.ctdivol_alert_value'
        db.alter_column(u'remapp_ctdosecheckdetails', 'ctdivol_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtDoseCheckDetails.dlp_alert_value'
        db.alter_column(u'remapp_ctdosecheckdetails', 'dlp_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtDoseCheckDetails.notification_reason_for_proceeding'
        db.alter_column(u'remapp_ctdosecheckdetails', 'notification_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'CtDoseCheckDetails.alert_reason_for_proceeding'
        db.alter_column(u'remapp_ctdosecheckdetails', 'alert_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Kvp.kvp'
        db.alter_column(u'remapp_kvp', 'kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Exports.modality'
        db.alter_column(u'remapp_exports', 'modality', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'CtXRaySourceParameters.maximum_xray_tube_current'
        db.alter_column(u'remapp_ctxraysourceparameters', 'maximum_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtXRaySourceParameters.exposure_time_per_rotation'
        db.alter_column(u'remapp_ctxraysourceparameters', 'exposure_time_per_rotation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtXRaySourceParameters.xray_filter_aluminum_equivalent'
        db.alter_column(u'remapp_ctxraysourceparameters', 'xray_filter_aluminum_equivalent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtXRaySourceParameters.xray_tube_current'
        db.alter_column(u'remapp_ctxraysourceparameters', 'xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtXRaySourceParameters.kvp'
        db.alter_column(u'remapp_ctxraysourceparameters', 'kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'CtAccumulatedDoseData.patient_model'
        db.alter_column(u'remapp_ctaccumulateddosedata', 'patient_model', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'CtAccumulatedDoseData.reference_authority_text'
        db.alter_column(u'remapp_ctaccumulateddosedata', 'reference_authority_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'CtAccumulatedDoseData.effective_dose_phantom_type'
        db.alter_column(u'remapp_ctaccumulateddosedata', 'effective_dose_phantom_type', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'CtAccumulatedDoseData.dosimeter_type'
        db.alter_column(u'remapp_ctaccumulateddosedata', 'dosimeter_type', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'CtAccumulatedDoseData.total_number_of_irradiation_events'
        db.alter_column(u'remapp_ctaccumulateddosedata', 'total_number_of_irradiation_events', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=0))
        # Adding field 'DoseRelatedDistanceMeasurements.table_longitudinal_end_position'
        db.add_column(u'remapp_doserelateddistancemeasurements', 'table_longitudinal_end_position',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'DoseRelatedDistanceMeasurements.table_lateral_end_position'
        db.add_column(u'remapp_doserelateddistancemeasurements', 'table_lateral_end_position',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'DoseRelatedDistanceMeasurements.table_height_end_position'
        db.add_column(u'remapp_doserelateddistancemeasurements', 'table_height_end_position',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)


        # Changing field 'DoseRelatedDistanceMeasurements.table_longitudinal_position'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'table_longitudinal_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.table_lateral_position'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'table_lateral_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.distance_source_to_detector'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'distance_source_to_detector', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.radiological_thickness'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'radiological_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.distance_source_to_table_plane'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'distance_source_to_table_plane', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.distance_source_to_entrance_surface'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'distance_source_to_entrance_surface', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.distance_source_to_reference_point'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'distance_source_to_reference_point', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.distance_source_to_isocenter'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'distance_source_to_isocenter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'DoseRelatedDistanceMeasurements.table_height_position'
        db.alter_column(u'remapp_doserelateddistancemeasurements', 'table_height_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'PersonParticipant.person_role_in_procedure_cid'
        db.add_column(u'remapp_personparticipant', 'person_role_in_procedure_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_roleproc', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'PersonParticipant.person_role_in_organization_cid'
        db.add_column(u'remapp_personparticipant', 'person_role_in_organization_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_roleorg', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)


        # Changing field 'XrayFilters.xray_filter_thickness_minimum'
        db.alter_column(u'remapp_xrayfilters', 'xray_filter_thickness_minimum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'XrayFilters.xray_filter_thickness_maximum'
        db.alter_column(u'remapp_xrayfilters', 'xray_filter_thickness_maximum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.positioner_primary_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'positioner_primary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.positioner_primary_end_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'positioner_primary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.compression_thickness'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'compression_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.table_horizontal_rotation_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'table_horizontal_rotation_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.positioner_secondary_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'positioner_secondary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.table_cradle_tilt_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'table_cradle_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.positioner_secondary_end_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'positioner_secondary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.compression_force'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'compression_force', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.table_head_tilt_angle'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'table_head_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.column_angulation'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'column_angulation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRayMechanicalData.magnification_factor'
        db.alter_column(u'remapp_irradeventxraymechanicaldata', 'magnification_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'ObserverContext.person_observer_name'
        db.add_column(u'remapp_observercontext', 'person_observer_name',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ObserverContext.person_observer_organization_name'
        db.add_column(u'remapp_observercontext', 'person_observer_organization_name',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ObserverContext.person_observer_role_in_organization'
        db.add_column(u'remapp_observercontext', 'person_observer_role_in_organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_ptroleorg', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'ObserverContext.person_observer_role_in_procedure'
        db.add_column(u'remapp_observercontext', 'person_observer_role_in_procedure',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_ptroleproc', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)


        # Changing field 'GeneralStudyModuleAttr.modality_type'
        db.alter_column(u'remapp_generalstudymoduleattr', 'modality_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'XrayTubeCurrent.xray_tube_current'
        db.alter_column(u'remapp_xraytubecurrent', 'xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Calibration.calibration_factor'
        db.alter_column(u'remapp_calibration', 'calibration_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Calibration.calibration_uncertainty'
        db.alter_column(u'remapp_calibration', 'calibration_uncertainty', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'CtRadiationDose.uid_type'
        db.add_column(u'remapp_ctradiationdose', 'uid_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1011_uid', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)


        # Changing field 'AccumProjXRayDose.total_acquisition_time'
        db.alter_column(u'remapp_accumprojxraydose', 'total_acquisition_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'PulseWidth.pulse_width'
        db.alter_column(u'remapp_pulsewidth', 'pulse_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'IrradEventXRaySourceData.derivation_cid'
        db.add_column(u'remapp_irradeventxraysourcedata', 'derivation_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_derivation', null=True, to=orm['remapp.ContextID']),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.collimated_field_height'
        db.add_column(u'remapp_irradeventxraysourcedata', 'collimated_field_height',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.collimated_field_width'
        db.add_column(u'remapp_irradeventxraysourcedata', 'collimated_field_width',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_absorbing_material'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_absorbing_material',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_spacing_material'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_spacing_material',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_thickness'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_thickness',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_pitch'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_pitch',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_aspect_ratio'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_aspect_ratio',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_period'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_period',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'IrradEventXRaySourceData.grid_focal_distance'
        db.add_column(u'remapp_irradeventxraysourcedata', 'grid_focal_distance',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)


        # Changing field 'IrradEventXRaySourceData.average_glandular_dose'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRaySourceData.average_xray_tube_current'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'average_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRaySourceData.derivation'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'derivation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'IrradEventXRaySourceData.collimated_field_area'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'collimated_field_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRaySourceData.pulse_rate'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'pulse_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRaySourceData.number_of_pulses'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'number_of_pulses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2))

        # Changing field 'IrradEventXRaySourceData.irradiation_duration'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'irradiation_duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'IrradEventXRaySourceData.focal_spot_size'
        db.alter_column(u'remapp_irradeventxraysourcedata', 'focal_spot_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.top_z_location_of_reconstructable_volume'
        db.alter_column(u'remapp_scanninglength', 'top_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.exposed_range'
        db.alter_column(u'remapp_scanninglength', 'exposed_range', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.scanning_length'
        db.alter_column(u'remapp_scanninglength', 'scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.top_z_location_of_scanning_length'
        db.alter_column(u'remapp_scanninglength', 'top_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.length_of_reconstructable_volume'
        db.alter_column(u'remapp_scanninglength', 'length_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.bottom_z_location_of_reconstructable_volume'
        db.alter_column(u'remapp_scanninglength', 'bottom_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'ScanningLength.bottom_z_location_of_scanning_length'
        db.alter_column(u'remapp_scanninglength', 'bottom_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))



    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'remapp.accumcassettebsdprojradiogdose': {
            'Meta': {'object_name': 'AccumCassetteBsdProjRadiogDose'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.AccumXRayDose']"}),
            'detector_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_number_of_radiographic_frames': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.accumintegratedprojradiogdose': {
            'Meta': {'object_name': 'AccumIntegratedProjRadiogDose'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.AccumXRayDose']"}),
            'dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_point_definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_point_definition_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            'total_number_of_radiographic_frames': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.accummammographyxraydose': {
            'Meta': {'object_name': 'AccumMammographyXRayDose'},
            'accumulated_average_glandular_dose': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.AccumXRayDose']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laterality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.accumprojxraydose': {
            'Meta': {'object_name': 'AccumProjXRayDose'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.AccumXRayDose']"}),
            'acquisition_dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'acquisition_dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'fluoro_dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'fluoro_dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_point_definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_point_definition_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            'total_acquisition_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'total_fluoro_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'total_number_of_radiographic_frames': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.accumxraydose': {
            'Meta': {'object_name': 'AccumXRayDose'},
            'acquisition_plane': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ProjectionXRayRadiationDose']"})
        },
        u'remapp.calibration': {
            'Meta': {'object_name': 'Calibration'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.AccumXRayDose']"}),
            'calibration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'calibration_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'calibration_responsible_party': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'calibration_uncertainty': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'dose_measurement_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'remapp.contextid': {
            'Meta': {'ordering': "['code_value']", 'object_name': 'ContextID'},
            'cid_table': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'code_meaning': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code_value': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'remapp.ctaccumulateddosedata': {
            'Meta': {'object_name': 'CtAccumulatedDoseData'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ct_dose_length_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ct_effective_dose_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtRadiationDose']"}),
            'dosimeter_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effective_dose_phantom_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_method': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10012_method'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'patient_model': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_authority_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10012_authority'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'reference_authority_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'total_number_of_irradiation_events': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.ctdosecheckdetails': {
            'Meta': {'object_name': 'CtDoseCheckDetails'},
            'accumulated_ctdivol_forward_estimate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'accumulated_dlp_forward_estimate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'alert_reason_for_proceeding': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']"}),
            'ctdivol_alert_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ctdivol_alert_value_configured': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ctdivol_forward_estimate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'ctdivol_notification_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'ctdivol_notification_value_configured': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'dlp_alert_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'dlp_alert_value_configured': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'dlp_forward_estimate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'dlp_notification_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'dlp_notification_value_configured': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_reason_for_proceeding': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'remapp.ctirradiationeventdata': {
            'Meta': {'object_name': 'CtIrradiationEventData'},
            'acquisition_protocol': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ct_acquisition_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_type'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtRadiationDose']"}),
            'ctdifreeair_calculation_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ctdiw_phantom_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_phantom'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'date_time_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dlp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'effective_dose': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'effective_dose_conversion_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'exposure_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_label': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'irradiation_event_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_labeltype'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'mean_ctdifreeair': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'mean_ctdivol': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'measurement_method': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_method'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'nominal_single_collimation_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'nominal_total_collimation_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'number_of_xray_sources': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'pitch_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'procedure_context': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_context'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'series_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_region'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'xray_modulation_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'remapp.ctradiationdose': {
            'Meta': {'object_name': 'CtRadiationDose'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_of_xray_irradiation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.GeneralStudyModuleAttr']"}),
            'has_intent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_intent'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedure_reported': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_procedure'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'scope_of_accumulation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_scope'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'source_of_dose_information': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_source'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'start_of_xray_irradiation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uid_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1011_uid'", 'null': 'True', 'to': u"orm['remapp.ContextID']"})
        },
        u'remapp.ctreconstructionalgorithm': {
            'Meta': {'object_name': 'CtReconstructionAlgorithm'},
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reconstruction_algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.ctxraysourceparameters': {
            'Meta': {'object_name': 'CtXRaySourceParameters'},
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']"}),
            'exposure_time_per_rotation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification_of_the_xray_source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'kvp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'maximum_xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_filter_aluminum_equivalent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.deviceparticipant': {
            'Meta': {'object_name': 'DeviceParticipant'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.AccumXRayDose']", 'null': 'True', 'blank': 'True'}),
            'ct_accumulated_dose_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtAccumulatedDoseData']", 'null': 'True', 'blank': 'True'}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']", 'null': 'True', 'blank': 'True'}),
            'device_manufacturer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_model_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_role_in_procedure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            'device_serial_number': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_detector_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayDetectorData']", 'null': 'True', 'blank': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.doserelateddistancemeasurements': {
            'Meta': {'object_name': 'DoseRelatedDistanceMeasurements'},
            'distance_source_to_detector': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_entrance_surface': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_isocenter': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_reference_point': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_table_plane': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_mechanical_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayMechanicalData']"}),
            'radiological_thickness': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_height_end_position': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_height_position': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_lateral_end_position': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_lateral_position': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_longitudinal_end_position': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_longitudinal_position': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.exports': {
            'Meta': {'object_name': 'Exports'},
            'export_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'export_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modality': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'num_records': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processtime': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '30', 'decimal_places': '10', 'blank': 'True'}),
            'progress': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.TextField', [], {})
        },
        u'remapp.exposure': {
            'Meta': {'object_name': 'Exposure'},
            'exposure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']"})
        },
        u'remapp.generalequipmentmoduleattr': {
            'Meta': {'object_name': 'GeneralEquipmentModuleAttr'},
            'date_of_last_calibration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'device_serial_number': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gantry_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.GeneralStudyModuleAttr']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'institution_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'institutional_department_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'manufacturer_model_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'software_versions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'spatial_resolution': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'station_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'time_of_last_calibration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'remapp.generalstudymoduleattr': {
            'Meta': {'object_name': 'GeneralStudyModuleAttr'},
            'accession_number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modality_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'name_of_physician_reading_study': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'operator_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performing_physician_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'physician_of_record': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'procedure_code_meaning': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'procedure_code_value': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'referring_physician_identification': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'referring_physician_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'requested_procedure_code_meaning': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'requested_procedure_code_value': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'study_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'study_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'study_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'study_instance_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'study_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'remapp.imageviewmodifier': {
            'Meta': {'object_name': 'ImageViewModifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_view_modifier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayData']"})
        },
        u'remapp.irradeventxraydata': {
            'Meta': {'object_name': 'IrradEventXRayData'},
            'acquisition_plane': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_plane'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'acquisition_protocol': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'anatomical_structure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_anatomy'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'breast_composition': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'breast_composition_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_breastcomposition'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_time_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dose_area_product': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'entrance_exposure_at_rp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'half_value_layer': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_view': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_view'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'irradiation_event_label': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'irradiation_event_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_eventtype'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'irradiation_event_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_labeltype'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'laterality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_laterality'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'patient_equivalent_thickness': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'patient_orientation': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'patient_orientation_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_ptorientation'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'patient_orientation_modifier': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'patient_orientation_modifier_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_ptorientationmod'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'patient_table_relationship': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'patient_table_relationship_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_pttablerel'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'percent_fibroglandular_tissue': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'projection_eponymous_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'projection_eponymous_name_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_pojectioneponymous'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ProjectionXRayRadiationDose']"}),
            'reference_point_definition': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_rpdefinition'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'target_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_region'", 'null': 'True', 'to': u"orm['remapp.ContextID']"})
        },
        u'remapp.irradeventxraydetectordata': {
            'Meta': {'object_name': 'IrradEventXRayDetectorData'},
            'deviation_index': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'exposure_index': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayData']"}),
            'relative_exposure_unit': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'relative_xray_exposure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'sensitivity': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'target_exposure_index': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.irradeventxraymechanicaldata': {
            'Meta': {'object_name': 'IrradEventXRayMechanicalData'},
            'column_angulation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'compression_force': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'compression_thickness': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'crdr_mechanical_configuration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayData']"}),
            'magnification_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_primary_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_primary_end_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_secondary_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_secondary_end_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_cradle_tilt_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_head_tilt_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_horizontal_rotation_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.irradeventxraysourcedata': {
            'Meta': {'object_name': 'IrradEventXRaySourceData'},
            'anode_target_material': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_anodetarget'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'average_glandular_dose': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'average_xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'collimated_field_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'collimated_field_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'collimated_field_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'derivation': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'derivation_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_derivation'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'dose_rp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'exposure_control_mode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'exposure_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'fluoro_mode': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_fluoromode'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'focal_spot_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'grid_absorbing_material': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grid_aspect_ratio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grid_focal_distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '6', 'blank': 'True'}),
            'grid_period': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '6', 'blank': 'True'}),
            'grid_pitch': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '6', 'blank': 'True'}),
            'grid_spacing_material': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grid_thickness': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '6', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ii_field_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'irradiation_duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayData']"}),
            'number_of_pulses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'pulse_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'reference_point_definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_point_definition_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_rpdefinition'", 'null': 'True', 'to': u"orm['remapp.ContextID']"})
        },
        u'remapp.kvp': {
            'Meta': {'object_name': 'Kvp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']"}),
            'kvp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.observercontext': {
            'Meta': {'object_name': 'ObserverContext'},
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtRadiationDose']", 'null': 'True', 'blank': 'True'}),
            'device_observer_manufacturer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_model_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_physical_location_during_observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_serial_number': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_role_in_procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_role'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observer_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_observertype'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'person_observer_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_observer_organization_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_observer_role_in_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_ptroleorg'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'person_observer_role_in_procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_ptroleproc'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ProjectionXRayRadiationDose']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.patientmoduleattr': {
            'Meta': {'object_name': 'PatientModuleAttr'},
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.GeneralStudyModuleAttr']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'not_patient_indicator': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_patient_ids': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'patient_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'remapp.patientstudymoduleattr': {
            'Meta': {'object_name': 'PatientStudyModuleAttr'},
            'admitting_diagnosis_code_sequence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'admitting_diagnosis_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.GeneralStudyModuleAttr']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient_age': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'patient_age_decimal': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '3', 'blank': 'True'}),
            'patient_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'patient_weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.personparticipant': {
            'Meta': {'object_name': 'PersonParticipant'},
            'ct_accumulated_dose_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtAccumulatedDoseData']", 'null': 'True', 'blank': 'True'}),
            'ct_dose_check_details_alert': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_alert'", 'null': 'True', 'to': u"orm['remapp.CtDoseCheckDetails']"}),
            'ct_dose_check_details_notification': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_notification'", 'null': 'True', 'to': u"orm['remapp.CtDoseCheckDetails']"}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']", 'null': 'True', 'blank': 'True'}),
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtRadiationDose']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRayData']", 'null': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_id_issuer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_role_in_organization': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_role_in_organization_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_roleorg'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'person_role_in_procedure': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'person_role_in_procedure_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_roleproc'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ProjectionXRayRadiationDose']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.projectionxrayradiationdose': {
            'Meta': {'object_name': 'ProjectionXRayRadiationDose'},
            'acquisition_device_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.GeneralStudyModuleAttr']"}),
            'has_intent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_intent'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedure_reported': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_procedure'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'scope_of_accumulation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_scope'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'source_of_dose_information': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_infosource'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'xray_detector_data_available': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_detector'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'xray_mechanical_data_available': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_mech'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'xray_source_data_available': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_source'", 'null': 'True', 'to': u"orm['remapp.ContextID']"})
        },
        u'remapp.pulsewidth': {
            'Meta': {'object_name': 'PulseWidth'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']"}),
            'pulse_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.scanninglength': {
            'Meta': {'object_name': 'ScanningLength'},
            'bottom_z_location_of_reconstructable_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'bottom_z_location_of_scanning_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']"}),
            'exposed_range': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'frame_of_reference_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_of_reconstructable_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'scanning_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'top_z_location_of_reconstructable_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'top_z_location_of_scanning_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.sizespecificdoseestimation': {
            'Meta': {'object_name': 'SizeSpecificDoseEstimation'},
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtIrradiationEventData']"}),
            'derived_effective_diameter': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measured_ap_dimension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'measured_lateral_dimension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'measurement_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.sizeupload': {
            'Meta': {'object_name': 'SizeUpload'},
            'height_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'import_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'logfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'num_records': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processtime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'progress': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sizefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'weight_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'remapp.sourceofctdoseinformation': {
            'Meta': {'object_name': 'SourceOfCTDoseInformation'},
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.CtRadiationDose']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_of_dose_information': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.xrayfilters': {
            'Meta': {'object_name': 'XrayFilters'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']"}),
            'xray_filter_material': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'xrayfilters_material'", 'null': 'True', 'to': u"orm['remapp.ContextID']"}),
            'xray_filter_thickness_maximum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_filter_thickness_minimum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_filter_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'xrayfilters_type'", 'null': 'True', 'to': u"orm['remapp.ContextID']"})
        },
        u'remapp.xraygrid': {
            'Meta': {'object_name': 'XrayGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']"}),
            'xray_grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.ContextID']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.xraytubecurrent': {
            'Meta': {'object_name': 'XrayTubeCurrent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.IrradEventXRaySourceData']"}),
            'xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        }
    }

    complete_apps = ['contenttypes', 'remapp']