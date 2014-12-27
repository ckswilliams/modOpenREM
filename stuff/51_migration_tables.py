# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Ct_dose_check_details'
        db.delete_table(u'remapp_ct_dose_check_details')

        # Deleting model 'Ct_radiation_dose'
        db.delete_table(u'remapp_ct_radiation_dose')

        # Deleting model 'Accumulated_projection_xray_dose'
        db.delete_table(u'remapp_accumulated_projection_xray_dose')

        # Deleting model 'Patient_study_module_attributes'
        db.delete_table(u'remapp_patient_study_module_attributes')

        # Deleting model 'Size_upload'
        db.delete_table(u'remapp_size_upload')

        # Deleting model 'General_equipment_module_attributes'
        db.delete_table(u'remapp_general_equipment_module_attributes')

        # Deleting model 'Accumulated_cassette_based_projection_radiography_dose'
        db.delete_table(u'remapp_accumulated_cassette_based_projection_radiography_dose')

        # Deleting model 'Pulse_width'
        db.delete_table(u'remapp_pulse_width')

        # Deleting model 'Person_participant'
        db.delete_table(u'remapp_person_participant')

        # Deleting model 'Projection_xray_radiation_dose'
        db.delete_table(u'remapp_projection_xray_radiation_dose')

        # Deleting model 'Irradiation_event_xray_source_data'
        db.delete_table(u'remapp_irradiation_event_xray_source_data')

        # Deleting model 'Ct_accumulated_dose_data'
        db.delete_table(u'remapp_ct_accumulated_dose_data')

        # Deleting model 'Device_participant'
        db.delete_table(u'remapp_device_participant')

        # Deleting model 'Image_view_modifier'
        db.delete_table(u'remapp_image_view_modifier')

        # Deleting model 'Scanning_length'
        db.delete_table(u'remapp_scanning_length')

        # Deleting model 'Accumulated_xray_dose'
        db.delete_table(u'remapp_accumulated_xray_dose')

        # Deleting model 'Irradiation_event_xray_mechanical_data'
        db.delete_table(u'remapp_irradiation_event_xray_mechanical_data')

        # Deleting model 'Xray_tube_current'
        db.delete_table(u'remapp_xray_tube_current')

        # Deleting model 'Xray_filters'
        db.delete_table(u'remapp_xray_filters')

        # Deleting model 'Xray_grid'
        db.delete_table(u'remapp_xray_grid')

        # Deleting model 'Content_item_descriptions'
        db.delete_table(u'remapp_content_item_descriptions')

        # Deleting model 'Accumulated_mammography_xray_dose'
        db.delete_table(u'remapp_accumulated_mammography_xray_dose')

        # Deleting model 'Observer_context'
        db.delete_table(u'remapp_observer_context')

        # Deleting model 'Accumulated_integrated_projection_radiography_dose'
        db.delete_table(u'remapp_accumulated_integrated_projection_radiography_dose')

        # Deleting model 'Ct_xray_source_parameters'
        db.delete_table(u'remapp_ct_xray_source_parameters')

        # Deleting model 'General_study_module_attributes'
        db.delete_table(u'remapp_general_study_module_attributes')

        # Deleting model 'Dose_related_distance_measurements'
        db.delete_table(u'remapp_dose_related_distance_measurements')

        # Deleting model 'Irradiation_event_xray_detector_data'
        db.delete_table(u'remapp_irradiation_event_xray_detector_data')

        # Deleting model 'Ct_irradiation_event_data'
        db.delete_table(u'remapp_ct_irradiation_event_data')

        # Deleting model 'Irradiation_event_xray_data'
        db.delete_table(u'remapp_irradiation_event_xray_data')

        # Deleting model 'Patient_module_attributes'
        db.delete_table(u'remapp_patient_module_attributes')

        # Adding model 'AccumXRayDose'
        db.create_table(u'remapp_accumxraydose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose'])),
            ('acquisition_plane', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['AccumXRayDose'])

        # Adding model 'CtIrradiationEventData'
        db.create_table(u'remapp_ctirradiationeventdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'])),
            ('acquisition_protocol', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('target_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_region', null=True, to=orm['remapp.ContextID'])),
            ('ct_acquisition_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_type', null=True, to=orm['remapp.ContextID'])),
            ('procedure_context', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_context', null=True, to=orm['remapp.ContextID'])),
            ('irradiation_event_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('irradiation_event_label', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('label_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_labeltype', null=True, to=orm['remapp.ContextID'])),
            ('exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('nominal_single_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('nominal_total_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('pitch_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('number_of_xray_sources', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=0, blank=True)),
            ('mean_ctdivol', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ctdiw_phantom_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_phantom', null=True, to=orm['remapp.ContextID'])),
            ('ctdifreeair_calculation_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('mean_ctdifreeair', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('dlp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('effective_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('measurement_method', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_method', null=True, to=orm['remapp.ContextID'])),
            ('effective_dose_conversion_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('xray_modulation_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_time_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('series_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['CtIrradiationEventData'])

        # Adding model 'IrradEventXRayDetectorData'
        db.create_table(u'remapp_irradeventxraydetectordata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData'])),
            ('exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('target_exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('deviation_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('relative_xray_exposure', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('relative_exposure_unit', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('sensitivity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['IrradEventXRayDetectorData'])

        # Adding model 'IrradEventXRayData'
        db.create_table(u'remapp_irradeventxraydata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose'])),
            ('acquisition_plane', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_plane', null=True, to=orm['remapp.ContextID'])),
            ('irradiation_event_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('irradiation_event_label', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('label_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_labeltype', null=True, to=orm['remapp.ContextID'])),
            ('date_time_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('irradiation_event_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_eventtype', null=True, to=orm['remapp.ContextID'])),
            ('acquisition_protocol', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('anatomical_structure', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_anatomy', null=True, to=orm['remapp.ContextID'])),
            ('laterality', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_laterality', null=True, to=orm['remapp.ContextID'])),
            ('image_view', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_view', null=True, to=orm['remapp.ContextID'])),
            ('projection_eponymous_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('patient_table_relationship', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('patient_orientation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('patient_orientation_modifier', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('projection_eponymous_name_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_pojectioneponymous', null=True, to=orm['remapp.ContextID'])),
            ('patient_table_relationship_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_pttablerel', null=True, to=orm['remapp.ContextID'])),
            ('patient_orientation_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_ptorientation', null=True, to=orm['remapp.ContextID'])),
            ('patient_orientation_modifier_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_ptorientationmod', null=True, to=orm['remapp.ContextID'])),
            ('target_region', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_region', null=True, to=orm['remapp.ContextID'])),
            ('dose_area_product', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('half_value_layer', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('patient_equivalent_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('entrance_exposure_at_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_rpdefinition', null=True, to=orm['remapp.ContextID'])),
            ('breast_composition', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('breast_composition_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_breastcomposition', null=True, to=orm['remapp.ContextID'])),
            ('percent_fibroglandular_tissue', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['IrradEventXRayData'])

        # Adding model 'CtDoseCheckDetails'
        db.create_table(u'remapp_ctdosecheckdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'])),
            ('dlp_alert_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ctdivol_alert_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('dlp_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ctdivol_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('accumulated_dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('accumulated_ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('alert_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dlp_notification_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ctdivol_notification_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('dlp_notification_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('ctdivol_notification_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('notification_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['CtDoseCheckDetails'])

        # Adding model 'PatientModuleAttr'
        db.create_table(u'remapp_patientmoduleattr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr'])),
            ('patient_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('patient_sex', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('other_patient_ids', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('not_patient_indicator', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['PatientModuleAttr'])

        # Adding model 'ContextID'
        db.create_table(u'remapp_contextid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_value', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('code_meaning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cid_table', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['ContextID'])

        # Adding model 'CtXRaySourceParameters'
        db.create_table(u'remapp_ctxraysourceparameters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'])),
            ('identification_of_the_xray_source', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('maximum_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('exposure_time_per_rotation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('xray_filter_aluminum_equivalent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['CtXRaySourceParameters'])

        # Adding model 'AccumMammographyXRayDose'
        db.create_table(u'remapp_accummammographyxraydose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose'])),
            ('accumulated_average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('laterality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['AccumMammographyXRayDose'])

        # Adding model 'AccumIntegratedProjRadiogDose'
        db.create_table(u'remapp_accumintegratedprojradiogdose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose'])),
            ('dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('total_number_of_radiographic_frames', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0, blank=True)),
            ('reference_point_definition_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['AccumIntegratedProjRadiogDose'])

        # Adding model 'CtAccumulatedDoseData'
        db.create_table(u'remapp_ctaccumulateddosedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'])),
            ('total_number_of_irradiation_events', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=0, blank=True)),
            ('ct_dose_length_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ct_effective_dose_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('reference_authority_code', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10012_authority', null=True, to=orm['remapp.ContextID'])),
            ('reference_authority_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('measurement_method', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10012_method', null=True, to=orm['remapp.ContextID'])),
            ('patient_model', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('effective_dose_phantom_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dosimeter_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['CtAccumulatedDoseData'])

        # Adding model 'DoseRelatedDistanceMeasurements'
        db.create_table(u'remapp_doserelateddistancemeasurements', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_mechanical_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayMechanicalData'])),
            ('distance_source_to_isocenter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_reference_point', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_detector', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_longitudinal_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_lateral_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_height_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_table_plane', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_longitudinal_end_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_lateral_end_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_height_end_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_entrance_surface', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('radiological_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['DoseRelatedDistanceMeasurements'])

        # Adding model 'AccumCassetteBsdProjRadiogDose'
        db.create_table(u'remapp_accumcassettebsdprojradiogdose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose'])),
            ('detector_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
            ('total_number_of_radiographic_frames', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['AccumCassetteBsdProjRadiogDose'])

        # Adding model 'GeneralEquipmentModuleAttr'
        db.create_table(u'remapp_generalequipmentmoduleattr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr'])),
            ('manufacturer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('institution_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('institution_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('station_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('institutional_department_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('manufacturer_model_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_serial_number', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('software_versions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('gantry_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('spatial_resolution', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('date_of_last_calibration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time_of_last_calibration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['GeneralEquipmentModuleAttr'])

        # Adding model 'XrayFilters'
        db.create_table(u'remapp_xrayfilters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData'])),
            ('xray_filter_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='xrayfilters_type', null=True, to=orm['remapp.ContextID'])),
            ('xray_filter_material', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='xrayfilters_material', null=True, to=orm['remapp.ContextID'])),
            ('xray_filter_thickness_minimum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('xray_filter_thickness_maximum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['XrayFilters'])

        # Adding model 'PatientStudyModuleAttr'
        db.create_table(u'remapp_patientstudymoduleattr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr'])),
            ('admitting_diagnosis_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('admitting_diagnosis_code_sequence', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_age', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('patient_age_decimal', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=3, blank=True)),
            ('patient_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('patient_weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['PatientStudyModuleAttr'])

        # Adding model 'IrradEventXRayMechanicalData'
        db.create_table(u'remapp_irradeventxraymechanicaldata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData'])),
            ('crdr_mechanical_configuration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
            ('positioner_primary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('positioner_secondary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('positioner_primary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('positioner_secondary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('column_angulation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_head_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_horizontal_rotation_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_cradle_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('compression_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('compression_force', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('magnification_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['IrradEventXRayMechanicalData'])

        # Adding model 'ObserverContext'
        db.create_table(u'remapp_observercontext', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose'], null=True, blank=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'], null=True, blank=True)),
            ('observer_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_observertype', null=True, to=orm['remapp.ContextID'])),
            ('person_observer_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_observer_organization_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_observer_role_in_organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_ptroleorg', null=True, to=orm['remapp.ContextID'])),
            ('person_observer_role_in_procedure', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_ptroleproc', null=True, to=orm['remapp.ContextID'])),
            ('device_observer_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_manufacturer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_model_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_serial_number', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_physical_location_during_observation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_role_in_procedure', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_role', null=True, to=orm['remapp.ContextID'])),
        ))
        db.send_create_signal(u'remapp', ['ObserverContext'])

        # Adding model 'PersonParticipant'
        db.create_table(u'remapp_personparticipant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ProjectionXRayRadiationDose'], null=True, blank=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose'], null=True, blank=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData'], null=True, blank=True)),
            ('ct_accumulated_dose_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtAccumulatedDoseData'], null=True, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'], null=True, blank=True)),
            ('ct_dose_check_details_alert', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_alert', null=True, to=orm['remapp.CtDoseCheckDetails'])),
            ('ct_dose_check_details_notification', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_notification', null=True, to=orm['remapp.CtDoseCheckDetails'])),
            ('person_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_role_in_procedure', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('person_role_in_procedure_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_roleproc', null=True, to=orm['remapp.ContextID'])),
            ('person_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_id_issuer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('organization_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_role_in_organization', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_role_in_organization_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_roleorg', null=True, to=orm['remapp.ContextID'])),
        ))
        db.send_create_signal(u'remapp', ['PersonParticipant'])

        # Adding model 'ProjectionXRayRadiationDose'
        db.create_table(u'remapp_projectionxrayradiationdose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr'])),
            ('procedure_reported', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_procedure', null=True, to=orm['remapp.ContextID'])),
            ('has_intent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_intent', null=True, to=orm['remapp.ContextID'])),
            ('acquisition_device_type', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('scope_of_accumulation', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_scope', null=True, to=orm['remapp.ContextID'])),
            ('xray_detector_data_available', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_detector', null=True, to=orm['remapp.ContextID'])),
            ('xray_source_data_available', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_source', null=True, to=orm['remapp.ContextID'])),
            ('xray_mechanical_data_available', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_mech', null=True, to=orm['remapp.ContextID'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_of_dose_information', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10001_infosource', null=True, to=orm['remapp.ContextID'])),
        ))
        db.send_create_signal(u'remapp', ['ProjectionXRayRadiationDose'])

        # Adding model 'GeneralStudyModuleAttr'
        db.create_table(u'remapp_generalstudymoduleattr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('study_instance_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('study_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('study_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('referring_physician_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('referring_physician_identification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('study_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('accession_number', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('study_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('physician_of_record', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name_of_physician_reading_study', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('performing_physician_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('operator_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modality_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('procedure_code_value', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('procedure_code_meaning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('requested_procedure_code_value', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('requested_procedure_code_meaning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['GeneralStudyModuleAttr'])

        # Adding model 'XrayTubeCurrent'
        db.create_table(u'remapp_xraytubecurrent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData'])),
            ('xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['XrayTubeCurrent'])

        # Adding model 'SizeUpload'
        db.create_table(u'remapp_sizeupload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sizefile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('height_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('weight_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('task_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('progress', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('num_records', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('logfile', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('import_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('processtime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['SizeUpload'])

        # Adding model 'CtRadiationDose'
        db.create_table(u'remapp_ctradiationdose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.GeneralStudyModuleAttr'])),
            ('procedure_reported', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_procedure', null=True, to=orm['remapp.ContextID'])),
            ('has_intent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_intent', null=True, to=orm['remapp.ContextID'])),
            ('start_of_xray_irradiation', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_of_xray_irradiation', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('scope_of_accumulation', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_scope', null=True, to=orm['remapp.ContextID'])),
            ('uid_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1011_uid', null=True, to=orm['remapp.ContextID'])),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_of_dose_information', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10011_source', null=True, to=orm['remapp.ContextID'])),
        ))
        db.send_create_signal(u'remapp', ['CtRadiationDose'])

        # Adding model 'PulseWidth'
        db.create_table(u'remapp_pulsewidth', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData'])),
            ('pulse_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['PulseWidth'])

        # Adding model 'IrradEventXRaySourceData'
        db.create_table(u'remapp_irradeventxraysourcedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData'])),
            ('dose_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reference_point_definition_code', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_rpdefinition', null=True, to=orm['remapp.ContextID'])),
            ('average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('fluoro_mode', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_fluoromode', null=True, to=orm['remapp.ContextID'])),
            ('pulse_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('number_of_pulses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('derivation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('derivation_cid', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_derivation', null=True, to=orm['remapp.ContextID'])),
            ('irradiation_duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('average_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('focal_spot_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('anode_target_material', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_anodetarget', null=True, to=orm['remapp.ContextID'])),
            ('collimated_field_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('collimated_field_height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('collimated_field_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ii_field_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exposure_control_mode', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('grid_absorbing_material', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('grid_spacing_material', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('grid_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('grid_pitch', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('grid_aspect_ratio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('grid_period', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('grid_focal_distance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['IrradEventXRaySourceData'])

        # Adding model 'ScanningLength'
        db.create_table(u'remapp_scanninglength', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'])),
            ('scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('length_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('exposed_range', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('top_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('bottom_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('top_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('bottom_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('frame_of_reference_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['ScanningLength'])

        # Adding model 'AccumProjectionXRayDose'
        db.create_table(u'remapp_accumprojectionxraydose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose'])),
            ('fluoro_dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('fluoro_dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('total_fluoro_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('acquisition_dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('acquisition_dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('total_acquisition_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('total_number_of_radiographic_frames', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reference_point_definition_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['AccumProjectionXRayDose'])

        # Adding model 'XrayGrid'
        db.create_table(u'remapp_xraygrid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData'])),
            ('xray_grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['XrayGrid'])

        # Adding model 'ImageViewModifier'
        db.create_table(u'remapp_imageviewmodifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayData'])),
            ('image_view_modifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['ImageViewModifier'])

        # Adding model 'DeviceParticipant'
        db.create_table(u'remapp_deviceparticipant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose'], null=True, blank=True)),
            ('irradiation_event_xray_detector_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRayDetectorData'], null=True, blank=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData'], null=True, blank=True)),
            ('ct_accumulated_dose_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtAccumulatedDoseData'], null=True, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData'], null=True, blank=True)),
            ('device_role_in_procedure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True, blank=True)),
            ('device_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_manufacturer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_model_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_serial_number', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['DeviceParticipant'])


        # Changing field 'Kvp.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_kvp', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))

        # Changing field 'CtReconstructionAlgorithm.reconstruction_algorithm'
        db.alter_column(u'remapp_ctreconstructionalgorithm', 'reconstruction_algorithm_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True))

        # Changing field 'CtReconstructionAlgorithm.ct_irradiation_event_data'
        db.alter_column(u'remapp_ctreconstructionalgorithm', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData']))

        # Changing field 'Calibration.dose_measurement_device'
        db.alter_column(u'remapp_calibration', 'dose_measurement_device_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True))

        # Changing field 'Calibration.accumulated_xray_dose'
        db.alter_column(u'remapp_calibration', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.AccumXRayDose']))

        # Changing field 'Exposure.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_exposure', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.IrradEventXRaySourceData']))

        # Changing field 'SizeSpecificDoseEstimation.measurement_method'
        db.alter_column(u'remapp_sizespecificdoseestimation', 'measurement_method_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True))

        # Changing field 'SizeSpecificDoseEstimation.ct_irradiation_event_data'
        db.alter_column(u'remapp_sizespecificdoseestimation', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtIrradiationEventData']))

        # Changing field 'SourceOfCTDoseInformation.ct_radiation_dose'
        db.alter_column(u'remapp_sourceofctdoseinformation', 'ct_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.CtRadiationDose']))

        # Changing field 'SourceOfCTDoseInformation.source_of_dose_information'
        db.alter_column(u'remapp_sourceofctdoseinformation', 'source_of_dose_information_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.ContextID'], null=True))

    def backwards(self, orm):
        # Adding model 'Ct_dose_check_details'
        db.create_table(u'remapp_ct_dose_check_details', (
            ('accumulated_dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('dlp_notification_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('dlp_notification_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('accumulated_ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ctdivol_notification_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ctdivol_alert_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ctdivol_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('dlp_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'])),
            ('ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            ('dlp_alert_value_configured', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('alert_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ctdivol_notification_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Ct_dose_check_details'])

        # Adding model 'Ct_radiation_dose'
        db.create_table(u'remapp_ct_radiation_dose', (
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('has_intent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10011_intent', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.General_study_module_attributes'])),
            ('end_of_xray_irradiation', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('start_of_xray_irradiation', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_of_dose_information', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10011_source', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('procedure_reported', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10011_procedure', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('scope_of_accumulation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10011_scope', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('uid_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1011_uid', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Ct_radiation_dose'])

        # Adding model 'Accumulated_projection_xray_dose'
        db.create_table(u'remapp_accumulated_projection_xray_dose', (
            ('fluoro_dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('total_fluoro_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Accumulated_xray_dose'])),
            ('total_number_of_radiographic_frames', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0, blank=True)),
            ('fluoro_dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('acquisition_dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('total_acquisition_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('reference_point_definition_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            ('acquisition_dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Accumulated_projection_xray_dose'])

        # Adding model 'Patient_study_module_attributes'
        db.create_table(u'remapp_patient_study_module_attributes', (
            ('admitting_diagnosis_code_sequence', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('patient_age', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('admitting_diagnosis_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_age_decimal', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=3, blank=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.General_study_module_attributes'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Patient_study_module_attributes'])

        # Adding model 'Size_upload'
        db.create_table(u'remapp_size_upload', (
            ('status', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('height_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('processtime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('id_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logfile', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('num_records', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('weight_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('import_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sizefile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('progress', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Size_upload'])

        # Adding model 'General_equipment_module_attributes'
        db.create_table(u'remapp_general_equipment_module_attributes', (
            ('time_of_last_calibration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('institution_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('gantry_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.General_study_module_attributes'])),
            ('station_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_last_calibration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('software_versions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_serial_number', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('institution_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('institutional_department_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('manufacturer_model_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('spatial_resolution', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['General_equipment_module_attributes'])

        # Adding model 'Accumulated_cassette_based_projection_radiography_dose'
        db.create_table(u'remapp_accumulated_cassette_based_projection_radiography_dose', (
            ('total_number_of_radiographic_frames', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0, blank=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Accumulated_xray_dose'])),
            ('detector_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'remapp', ['Accumulated_cassette_based_projection_radiography_dose'])

        # Adding model 'Pulse_width'
        db.create_table(u'remapp_pulse_width', (
            ('pulse_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data'])),
        ))
        db.send_create_signal(u'remapp', ['Pulse_width'])

        # Adding model 'Person_participant'
        db.create_table(u'remapp_person_participant', (
            ('person_role_in_procedure_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1020_roleproc', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('person_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_id_issuer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_dose_check_details_notification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1020_notification', null=True, to=orm['remapp.Ct_dose_check_details'], blank=True)),
            ('person_role_in_organization_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1020_roleorg', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('person_role_in_procedure', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'], null=True, blank=True)),
            ('organization_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_dose_check_details_alert', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1020_alert', null=True, to=orm['remapp.Ct_dose_check_details'], blank=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_radiation_dose'], null=True, blank=True)),
            ('person_role_in_organization', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_data'], null=True, blank=True)),
            ('person_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_accumulated_dose_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_accumulated_dose_data'], null=True, blank=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Projection_xray_radiation_dose'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'remapp', ['Person_participant'])

        # Adding model 'Projection_xray_radiation_dose'
        db.create_table(u'remapp_projection_xray_radiation_dose', (
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('has_intent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_intent', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('acquisition_device_type', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.General_study_module_attributes'])),
            ('xray_detector_data_available', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_detector', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_of_dose_information', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_infosource', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('xray_mechanical_data_available', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_mech', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('scope_of_accumulation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_scope', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('xray_source_data_available', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_source', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('procedure_reported', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10001_procedure', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Projection_xray_radiation_dose'])

        # Adding model 'Irradiation_event_xray_source_data'
        db.create_table(u'remapp_irradiation_event_xray_source_data', (
            ('exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('collimated_field_height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('number_of_pulses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('exposure_control_mode', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('grid_pitch', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('grid_period', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('anode_target_material', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003b_anodetarget', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grid_focal_distance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('derivation_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003b_derivation', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('collimated_field_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('collimated_field_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('dose_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('grid_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True)),
            ('reference_point_definition_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003b_rpdefinition', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('average_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('grid_spacing_material', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('irradiation_duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('grid_aspect_ratio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('derivation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('grid_absorbing_material', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ii_field_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pulse_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_data'])),
            ('reference_point_definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fluoro_mode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003b_fluoromode', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('focal_spot_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Irradiation_event_xray_source_data'])

        # Adding model 'Ct_accumulated_dose_data'
        db.create_table(u'remapp_ct_accumulated_dose_data', (
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_model', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_radiation_dose'])),
            ('reference_authority_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10012_authority', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('dosimeter_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('effective_dose_phantom_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_dose_length_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('reference_authority_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('measurement_method', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10012_method', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('ct_effective_dose_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('total_number_of_irradiation_events', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=0, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Ct_accumulated_dose_data'])

        # Adding model 'Device_participant'
        db.create_table(u'remapp_device_participant', (
            ('device_observer_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'], null=True, blank=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Accumulated_xray_dose'], null=True, blank=True)),
            ('device_model_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_manufacturer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_role_in_procedure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_serial_number', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_accumulated_dose_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_accumulated_dose_data'], null=True, blank=True)),
            ('irradiation_event_xray_detector_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_detector_data'], null=True, blank=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Device_participant'])

        # Adding model 'Image_view_modifier'
        db.create_table(u'remapp_image_view_modifier', (
            ('image_view_modifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_data'])),
        ))
        db.send_create_signal(u'remapp', ['Image_view_modifier'])

        # Adding model 'Scanning_length'
        db.create_table(u'remapp_scanning_length', (
            ('top_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('frame_of_reference_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('length_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exposed_range', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'])),
            ('top_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('bottom_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('bottom_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Scanning_length'])

        # Adding model 'Accumulated_xray_dose'
        db.create_table(u'remapp_accumulated_xray_dose', (
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Projection_xray_radiation_dose'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('acquisition_plane', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Accumulated_xray_dose'])

        # Adding model 'Irradiation_event_xray_mechanical_data'
        db.create_table(u'remapp_irradiation_event_xray_mechanical_data', (
            ('positioner_primary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_cradle_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_horizontal_rotation_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('compression_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_head_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('column_angulation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('compression_force', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('crdr_mechanical_configuration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            ('positioner_secondary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('positioner_secondary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_data'])),
            ('positioner_primary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('magnification_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Irradiation_event_xray_mechanical_data'])

        # Adding model 'Xray_tube_current'
        db.create_table(u'remapp_xray_tube_current', (
            ('xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data'])),
        ))
        db.send_create_signal(u'remapp', ['Xray_tube_current'])

        # Adding model 'Xray_filters'
        db.create_table(u'remapp_xray_filters', (
            ('xray_filter_material', self.gf('django.db.models.fields.related.ForeignKey')(related_name='xrayfilters_material', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('xray_filter_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='xrayfilters_type', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('xray_filter_thickness_minimum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('xray_filter_thickness_maximum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data'])),
        ))
        db.send_create_signal(u'remapp', ['Xray_filters'])

        # Adding model 'Xray_grid'
        db.create_table(u'remapp_xray_grid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('xray_grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            ('irradiation_event_xray_source_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data'])),
        ))
        db.send_create_signal(u'remapp', ['Xray_grid'])

        # Adding model 'Content_item_descriptions'
        db.create_table(u'remapp_content_item_descriptions', (
            ('cid_table', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('code_meaning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_value', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'remapp', ['Content_item_descriptions'])

        # Adding model 'Accumulated_mammography_xray_dose'
        db.create_table(u'remapp_accumulated_mammography_xray_dose', (
            ('laterality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Accumulated_xray_dose'])),
            ('accumulated_average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'remapp', ['Accumulated_mammography_xray_dose'])

        # Adding model 'Observer_context'
        db.create_table(u'remapp_observer_context', (
            ('observer_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1002_observertype', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('device_observer_model_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_observer_role_in_procedure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1002_ptroleproc', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('device_role_in_procedure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1002_role', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('device_observer_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_observer_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('device_observer_manufacturer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_radiation_dose'], null=True, blank=True)),
            ('device_observer_physical_location_during_observation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person_observer_role_in_organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid1002_ptroleorg', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('device_observer_serial_number', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Projection_xray_radiation_dose'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person_observer_organization_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Observer_context'])

        # Adding model 'Accumulated_integrated_projection_radiography_dose'
        db.create_table(u'remapp_accumulated_integrated_projection_radiography_dose', (
            ('accumulated_xray_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Accumulated_xray_dose'])),
            ('total_number_of_radiographic_frames', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0, blank=True)),
            ('dose_area_product_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reference_point_definition_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            ('dose_rp_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'remapp', ['Accumulated_integrated_projection_radiography_dose'])

        # Adding model 'Ct_xray_source_parameters'
        db.create_table(u'remapp_ct_xray_source_parameters', (
            ('xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('maximum_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('exposure_time_per_rotation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('identification_of_the_xray_source', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('xray_filter_aluminum_equivalent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'])),
        ))
        db.send_create_signal(u'remapp', ['Ct_xray_source_parameters'])

        # Adding model 'General_study_module_attributes'
        db.create_table(u'remapp_general_study_module_attributes', (
            ('requested_procedure_code_value', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('study_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('physician_of_record', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('referring_physician_identification', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('referring_physician_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name_of_physician_reading_study', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('procedure_code_meaning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accession_number', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('study_instance_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('study_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('study_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('modality_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('operator_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('requested_procedure_code_meaning', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('procedure_code_value', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('study_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('performing_physician_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['General_study_module_attributes'])

        # Adding model 'Dose_related_distance_measurements'
        db.create_table(u'remapp_dose_related_distance_measurements', (
            ('table_longitudinal_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_longitudinal_end_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('irradiation_event_xray_mechanical_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_mechanical_data'])),
            ('radiological_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_detector', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_isocenter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_table_plane', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_lateral_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_lateral_end_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('distance_source_to_entrance_surface', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('distance_source_to_reference_point', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_height_end_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('table_height_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Dose_related_distance_measurements'])

        # Adding model 'Irradiation_event_xray_detector_data'
        db.create_table(u'remapp_irradiation_event_xray_detector_data', (
            ('relative_exposure_unit', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('target_exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('irradiation_event_xray_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_data'])),
            ('deviation_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('sensitivity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relative_xray_exposure', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Irradiation_event_xray_detector_data'])

        # Adding model 'Ct_irradiation_event_data'
        db.create_table(u'remapp_ct_irradiation_event_data', (
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('target_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10013_region', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('ctdifreeair_calculation_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('mean_ctdivol', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('acquisition_protocol', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('effective_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10013_labeltype', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('series_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('xray_modulation_type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('number_of_xray_sources', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=0, blank=True)),
            ('measurement_method', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10013_method', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('mean_ctdifreeair', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('dlp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('irradiation_event_label', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('effective_dose_conversion_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('procedure_context', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10013_context', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('ct_acquisition_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10013_type', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_radiation_dose'])),
            ('nominal_single_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('pitch_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('ctdiw_phantom_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10013_phantom', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('nominal_total_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('date_time_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('irradiation_event_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Ct_irradiation_event_data'])

        # Adding model 'Irradiation_event_xray_data'
        db.create_table(u'remapp_irradiation_event_xray_data', (
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('acquisition_plane', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_plane', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('entrance_exposure_at_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('patient_equivalent_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('breast_composition_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_breastcomposition', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_labeltype', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('patient_table_relationship', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('reference_point_definition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_rpdefinition', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('image_view', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_view', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('projection_eponymous_name_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_pojectioneponymous', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('patient_orientation_modifier', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('half_value_layer', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('patient_table_relationship_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_pttablerel', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('laterality', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_laterality', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('patient_orientation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('projection_eponymous_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('irradiation_event_label', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_orientation_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_ptorientation', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('anatomical_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_anatomy', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('acquisition_protocol', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('projection_xray_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Projection_xray_radiation_dose'])),
            ('target_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_region', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('dose_area_product', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('irradiation_event_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_eventtype', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('percent_fibroglandular_tissue', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('patient_orientation_modifier_cid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tid10003_ptorientationmod', null=True, to=orm['remapp.Content_item_descriptions'], blank=True)),
            ('breast_composition', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('date_time_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('irradiation_event_uid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Irradiation_event_xray_data'])

        # Adding model 'Patient_module_attributes'
        db.create_table(u'remapp_patient_module_attributes', (
            ('patient_sex', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('other_patient_ids', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('not_patient_indicator', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_study_module_attributes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.General_study_module_attributes'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient_birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('patient_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['Patient_module_attributes'])

        # Deleting model 'AccumXRayDose'
        db.delete_table(u'remapp_accumxraydose')

        # Deleting model 'CtIrradiationEventData'
        db.delete_table(u'remapp_ctirradiationeventdata')

        # Deleting model 'IrradEventXRayDetectorData'
        db.delete_table(u'remapp_irradeventxraydetectordata')

        # Deleting model 'IrradEventXRayData'
        db.delete_table(u'remapp_irradeventxraydata')

        # Deleting model 'CtDoseCheckDetails'
        db.delete_table(u'remapp_ctdosecheckdetails')

        # Deleting model 'PatientModuleAttr'
        db.delete_table(u'remapp_patientmoduleattr')

        # Deleting model 'ContextID'
        db.delete_table(u'remapp_contextid')

        # Deleting model 'CtXRaySourceParameters'
        db.delete_table(u'remapp_ctxraysourceparameters')

        # Deleting model 'AccumMammographyXRayDose'
        db.delete_table(u'remapp_accummammographyxraydose')

        # Deleting model 'AccumIntegratedProjRadiogDose'
        db.delete_table(u'remapp_accumintegratedprojradiogdose')

        # Deleting model 'CtAccumulatedDoseData'
        db.delete_table(u'remapp_ctaccumulateddosedata')

        # Deleting model 'DoseRelatedDistanceMeasurements'
        db.delete_table(u'remapp_doserelateddistancemeasurements')

        # Deleting model 'AccumCassetteBsdProjRadiogDose'
        db.delete_table(u'remapp_accumcassettebsdprojradiogdose')

        # Deleting model 'GeneralEquipmentModuleAttr'
        db.delete_table(u'remapp_generalequipmentmoduleattr')

        # Deleting model 'XrayFilters'
        db.delete_table(u'remapp_xrayfilters')

        # Deleting model 'PatientStudyModuleAttr'
        db.delete_table(u'remapp_patientstudymoduleattr')

        # Deleting model 'IrradEventXRayMechanicalData'
        db.delete_table(u'remapp_irradeventxraymechanicaldata')

        # Deleting model 'ObserverContext'
        db.delete_table(u'remapp_observercontext')

        # Deleting model 'PersonParticipant'
        db.delete_table(u'remapp_personparticipant')

        # Deleting model 'ProjectionXRayRadiationDose'
        db.delete_table(u'remapp_projectionxrayradiationdose')

        # Deleting model 'GeneralStudyModuleAttr'
        db.delete_table(u'remapp_generalstudymoduleattr')

        # Deleting model 'XrayTubeCurrent'
        db.delete_table(u'remapp_xraytubecurrent')

        # Deleting model 'SizeUpload'
        db.delete_table(u'remapp_sizeupload')

        # Deleting model 'CtRadiationDose'
        db.delete_table(u'remapp_ctradiationdose')

        # Deleting model 'PulseWidth'
        db.delete_table(u'remapp_pulsewidth')

        # Deleting model 'IrradEventXRaySourceData'
        db.delete_table(u'remapp_irradeventxraysourcedata')

        # Deleting model 'ScanningLength'
        db.delete_table(u'remapp_scanninglength')

        # Deleting model 'AccumProjectionXRayDose'
        db.delete_table(u'remapp_accumprojectionxraydose')

        # Deleting model 'XrayGrid'
        db.delete_table(u'remapp_xraygrid')

        # Deleting model 'ImageViewModifier'
        db.delete_table(u'remapp_imageviewmodifier')

        # Deleting model 'DeviceParticipant'
        db.delete_table(u'remapp_deviceparticipant')


        # Changing field 'Kvp.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_kvp', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data']))

        # Changing field 'CtReconstructionAlgorithm.reconstruction_algorithm'
        db.alter_column(u'remapp_ctreconstructionalgorithm', 'reconstruction_algorithm_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True))

        # Changing field 'CtReconstructionAlgorithm.ct_irradiation_event_data'
        db.alter_column(u'remapp_ctreconstructionalgorithm', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data']))

        # Changing field 'Calibration.dose_measurement_device'
        db.alter_column(u'remapp_calibration', 'dose_measurement_device_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True))

        # Changing field 'Calibration.accumulated_xray_dose'
        db.alter_column(u'remapp_calibration', 'accumulated_xray_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Accumulated_xray_dose']))

        # Changing field 'Exposure.irradiation_event_xray_source_data'
        db.alter_column(u'remapp_exposure', 'irradiation_event_xray_source_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Irradiation_event_xray_source_data']))

        # Changing field 'SizeSpecificDoseEstimation.measurement_method'
        db.alter_column(u'remapp_sizespecificdoseestimation', 'measurement_method_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True))

        # Changing field 'SizeSpecificDoseEstimation.ct_irradiation_event_data'
        db.alter_column(u'remapp_sizespecificdoseestimation', 'ct_irradiation_event_data_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data']))

        # Changing field 'SourceOfCTDoseInformation.ct_radiation_dose'
        db.alter_column(u'remapp_sourceofctdoseinformation', 'ct_radiation_dose_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_radiation_dose']))

        # Changing field 'SourceOfCTDoseInformation.source_of_dose_information'
        db.alter_column(u'remapp_sourceofctdoseinformation', 'source_of_dose_information_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True))

    models = {
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
        u'remapp.accumprojectionxraydose': {
            'Meta': {'object_name': 'AccumProjectionXRayDose'},
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

    complete_apps = ['remapp']