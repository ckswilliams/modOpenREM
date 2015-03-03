# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CtReconstructionAlgorithm'
        db.create_table(u'remapp_ctreconstructionalgorithm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'])),
            ('reconstruction_algorithm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['CtReconstructionAlgorithm'])

        # Adding model 'SizeSpecificDoseEstimation'
        db.create_table(u'remapp_sizespecificdoseestimation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_irradiation_event_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_irradiation_event_data'])),
            ('measurement_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
            ('measured_lateral_dimension', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('measured_ap_dimension', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
            ('derived_effective_diameter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['SizeSpecificDoseEstimation'])

        # Adding model 'SourceOfCTDoseInformation'
        db.create_table(u'remapp_sourceofctdoseinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ct_radiation_dose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Ct_radiation_dose'])),
            ('source_of_dose_information', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['remapp.Content_item_descriptions'], null=True, blank=True)),
        ))
        db.send_create_signal(u'remapp', ['SourceOfCTDoseInformation'])


        # Changing field 'Ct_dose_check_details.accumulated_dlp_forward_estimate'
        db.alter_column(u'remapp_ct_dose_check_details', 'accumulated_dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_dose_check_details.accumulated_ctdivol_forward_estimate'
        db.alter_column(u'remapp_ct_dose_check_details', 'accumulated_ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_dose_check_details.ctdivol_alert_value'
        db.alter_column(u'remapp_ct_dose_check_details', 'ctdivol_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_dose_check_details.dlp_alert_value'
        db.alter_column(u'remapp_ct_dose_check_details', 'dlp_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_dose_check_details.notification_reason_for_proceeding'
        db.alter_column(u'remapp_ct_dose_check_details', 'notification_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Ct_dose_check_details.alert_reason_for_proceeding'
        db.alter_column(u'remapp_ct_dose_check_details', 'alert_reason_for_proceeding', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'Ct_radiation_dose.uid_type'
        db.add_column(u'remapp_ct_radiation_dose', 'uid_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1011_uid', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)


        # Changing field 'Accumulated_projection_xray_dose.total_acquisition_time'
        db.alter_column(u'remapp_accumulated_projection_xray_dose', 'total_acquisition_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Kvp.kvp'
        db.alter_column(u'remapp_kvp', 'kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Exports.modality'
        db.alter_column(u'remapp_exports', 'modality', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Pulse_width.pulse_width'
        db.alter_column(u'remapp_pulse_width', 'pulse_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'Person_participant.person_role_in_procedure_cid'
        db.add_column(u'remapp_person_participant', 'person_role_in_procedure_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_roleproc', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Person_participant.person_role_in_organization_cid'
        db.add_column(u'remapp_person_participant', 'person_role_in_organization_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1020_roleorg', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.derivation_cid'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'derivation_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003b_derivation', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.collimated_field_height'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'collimated_field_height',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.collimated_field_width'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'collimated_field_width',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_absorbing_material'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_absorbing_material',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_spacing_material'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_spacing_material',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_thickness'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_thickness',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_pitch'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_pitch',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_aspect_ratio'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_aspect_ratio',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_period'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_period',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_source_data.grid_focal_distance'
        db.add_column(u'remapp_irradiation_event_xray_source_data', 'grid_focal_distance',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=6, blank=True),
                      keep_default=False)


        # Changing field 'Irradiation_event_xray_source_data.average_glandular_dose'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_source_data.average_xray_tube_current'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'average_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_source_data.derivation'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'derivation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Irradiation_event_xray_source_data.collimated_field_area'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'collimated_field_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_source_data.pulse_rate'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'pulse_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_source_data.number_of_pulses'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'number_of_pulses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2))

        # Changing field 'Irradiation_event_xray_source_data.irradiation_duration'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'irradiation_duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_source_data.focal_spot_size'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'focal_spot_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_accumulated_dose_data.patient_model'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'patient_model', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Ct_accumulated_dose_data.reference_authority_text'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'reference_authority_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Ct_accumulated_dose_data.effective_dose_phantom_type'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'effective_dose_phantom_type', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Ct_accumulated_dose_data.dosimeter_type'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'dosimeter_type', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Ct_accumulated_dose_data.total_number_of_irradiation_events'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'total_number_of_irradiation_events', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=0))

        # Changing field 'Scanning_length.top_z_location_of_reconstructable_volume'
        db.alter_column(u'remapp_scanning_length', 'top_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Scanning_length.exposed_range'
        db.alter_column(u'remapp_scanning_length', 'exposed_range', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Scanning_length.scanning_length'
        db.alter_column(u'remapp_scanning_length', 'scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Scanning_length.top_z_location_of_scanning_length'
        db.alter_column(u'remapp_scanning_length', 'top_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Scanning_length.length_of_reconstructable_volume'
        db.alter_column(u'remapp_scanning_length', 'length_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Scanning_length.bottom_z_location_of_reconstructable_volume'
        db.alter_column(u'remapp_scanning_length', 'bottom_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Scanning_length.bottom_z_location_of_scanning_length'
        db.alter_column(u'remapp_scanning_length', 'bottom_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_primary_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_primary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_primary_end_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_primary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.compression_thickness'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'compression_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.table_horizontal_rotation_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'table_horizontal_rotation_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_secondary_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_secondary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.table_cradle_tilt_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'table_cradle_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_secondary_end_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_secondary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.compression_force'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'compression_force', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.table_head_tilt_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'table_head_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.column_angulation'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'column_angulation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_mechanical_data.magnification_factor'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'magnification_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Xray_tube_current.xray_tube_current'
        db.alter_column(u'remapp_xray_tube_current', 'xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Xray_filters.xray_filter_thickness_minimum'
        db.alter_column(u'remapp_xray_filters', 'xray_filter_thickness_minimum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Xray_filters.xray_filter_thickness_maximum'
        db.alter_column(u'remapp_xray_filters', 'xray_filter_thickness_maximum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'Observer_context.person_observer_name'
        db.add_column(u'remapp_observer_context', 'person_observer_name',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Observer_context.person_observer_organization_name'
        db.add_column(u'remapp_observer_context', 'person_observer_organization_name',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Observer_context.person_observer_role_in_organization'
        db.add_column(u'remapp_observer_context', 'person_observer_role_in_organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_ptroleorg', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Observer_context.person_observer_role_in_procedure'
        db.add_column(u'remapp_observer_context', 'person_observer_role_in_procedure',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid1002_ptroleproc', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)


        # Changing field 'Calibration.calibration_factor'
        db.alter_column(u'remapp_calibration', 'calibration_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Calibration.calibration_uncertainty'
        db.alter_column(u'remapp_calibration', 'calibration_uncertainty', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_xray_source_parameters.maximum_xray_tube_current'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'maximum_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_xray_source_parameters.exposure_time_per_rotation'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'exposure_time_per_rotation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_xray_source_parameters.xray_filter_aluminum_equivalent'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'xray_filter_aluminum_equivalent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_xray_source_parameters.xray_tube_current'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_xray_source_parameters.kvp'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'General_study_module_attributes.modality_type'
        db.alter_column(u'remapp_general_study_module_attributes', 'modality_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))
        # Adding field 'Dose_related_distance_measurements.table_longitudinal_end_position'
        db.add_column(u'remapp_dose_related_distance_measurements', 'table_longitudinal_end_position',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'Dose_related_distance_measurements.table_lateral_end_position'
        db.add_column(u'remapp_dose_related_distance_measurements', 'table_lateral_end_position',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'Dose_related_distance_measurements.table_height_end_position'
        db.add_column(u'remapp_dose_related_distance_measurements', 'table_height_end_position',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)


        # Changing field 'Dose_related_distance_measurements.table_longitudinal_position'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'table_longitudinal_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.table_lateral_position'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'table_lateral_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_detector'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_detector', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.radiological_thickness'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'radiological_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_table_plane'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_table_plane', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_entrance_surface'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_entrance_surface', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_reference_point'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_reference_point', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_isocenter'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_isocenter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Dose_related_distance_measurements.table_height_position'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'table_height_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_detector_data.deviation_index'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'deviation_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_detector_data.sensitivity'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'sensitivity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_detector_data.relative_xray_exposure'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'relative_xray_exposure', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_detector_data.exposure_index'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_detector_data.target_exposure_index'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'target_exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'Ct_irradiation_event_data.irradiation_event_label'
        db.add_column(u'remapp_ct_irradiation_event_data', 'irradiation_event_label',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Ct_irradiation_event_data.label_type'
        db.add_column(u'remapp_ct_irradiation_event_data', 'label_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10013_labeltype', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)


        # Changing field 'Ct_irradiation_event_data.exposure_time'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.ctdifreeair_calculation_factor'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'ctdifreeair_calculation_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.mean_ctdivol'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'mean_ctdivol', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.effective_dose'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'effective_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.number_of_xray_sources'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'number_of_xray_sources', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=0))

        # Changing field 'Ct_irradiation_event_data.mean_ctdifreeair'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'mean_ctdifreeair', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.dlp'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'dlp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.effective_dose_conversion_factor'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'effective_dose_conversion_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.nominal_single_collimation_width'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'nominal_single_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.pitch_factor'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'pitch_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Ct_irradiation_event_data.nominal_total_collimation_width'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'nominal_total_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))
        # Adding field 'Irradiation_event_xray_data.projection_eponymous_name_cid'
        db.add_column(u'remapp_irradiation_event_xray_data', 'projection_eponymous_name_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_pojectioneponymous', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_data.patient_table_relationship_cid'
        db.add_column(u'remapp_irradiation_event_xray_data', 'patient_table_relationship_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_pttablerel', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_data.patient_orientation_cid'
        db.add_column(u'remapp_irradiation_event_xray_data', 'patient_orientation_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_ptorientation', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_data.patient_orientation_modifier_cid'
        db.add_column(u'remapp_irradiation_event_xray_data', 'patient_orientation_modifier_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_ptorientationmod', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_data.patient_equivalent_thickness'
        db.add_column(u'remapp_irradiation_event_xray_data', 'patient_equivalent_thickness',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8, blank=True),
                      keep_default=False)

        # Adding field 'Irradiation_event_xray_data.breast_composition_cid'
        db.add_column(u'remapp_irradiation_event_xray_data', 'breast_composition_cid',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tid10003_breastcomposition', null=True, to=orm['remapp.Content_item_descriptions']),
                      keep_default=False)


        # Changing field 'Irradiation_event_xray_data.entrance_exposure_at_rp'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'entrance_exposure_at_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_data.patient_table_relationship'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'patient_table_relationship', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Irradiation_event_xray_data.percent_fibroglandular_tissue'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'percent_fibroglandular_tissue', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_data.patient_orientation_modifier'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'patient_orientation_modifier', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Irradiation_event_xray_data.half_value_layer'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'half_value_layer', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=8))

        # Changing field 'Irradiation_event_xray_data.patient_orientation'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'patient_orientation', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Irradiation_event_xray_data.projection_eponymous_name'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'projection_eponymous_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Irradiation_event_xray_data.dose_area_product'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'dose_area_product', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10))

        # Changing field 'Irradiation_event_xray_data.breast_composition'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'breast_composition', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

    def backwards(self, orm):
        # Deleting model 'CtReconstructionAlgorithm'
        db.delete_table(u'remapp_ctreconstructionalgorithm')

        # Deleting model 'SizeSpecificDoseEstimation'
        db.delete_table(u'remapp_sizespecificdoseestimation')

        # Deleting model 'SourceOfCTDoseInformation'
        db.delete_table(u'remapp_sourceofctdoseinformation')


        # Changing field 'Ct_dose_check_details.accumulated_dlp_forward_estimate'
        db.alter_column(u'remapp_ct_dose_check_details', 'accumulated_dlp_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_dose_check_details.accumulated_ctdivol_forward_estimate'
        db.alter_column(u'remapp_ct_dose_check_details', 'accumulated_ctdivol_forward_estimate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_dose_check_details.ctdivol_alert_value'
        db.alter_column(u'remapp_ct_dose_check_details', 'ctdivol_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_dose_check_details.dlp_alert_value'
        db.alter_column(u'remapp_ct_dose_check_details', 'dlp_alert_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_dose_check_details.notification_reason_for_proceeding'
        db.alter_column(u'remapp_ct_dose_check_details', 'notification_reason_for_proceeding', self.gf('django.db.models.fields.CharField')(default='', max_length=512))

        # Changing field 'Ct_dose_check_details.alert_reason_for_proceeding'
        db.alter_column(u'remapp_ct_dose_check_details', 'alert_reason_for_proceeding', self.gf('django.db.models.fields.CharField')(default='', max_length=512))
        # Deleting field 'Ct_radiation_dose.uid_type'
        db.delete_column(u'remapp_ct_radiation_dose', 'uid_type_id')


        # Changing field 'Accumulated_projection_xray_dose.total_acquisition_time'
        db.alter_column(u'remapp_accumulated_projection_xray_dose', 'total_acquisition_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Kvp.kvp'
        db.alter_column(u'remapp_kvp', 'kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Changing field 'Exports.modality'
        db.alter_column(u'remapp_exports', 'modality', self.gf('django.db.models.fields.CharField')(max_length=8, null=True))

        # Changing field 'Pulse_width.pulse_width'
        db.alter_column(u'remapp_pulse_width', 'pulse_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=3))
        # Deleting field 'Person_participant.person_role_in_procedure_cid'
        db.delete_column(u'remapp_person_participant', 'person_role_in_procedure_cid_id')

        # Deleting field 'Person_participant.person_role_in_organization_cid'
        db.delete_column(u'remapp_person_participant', 'person_role_in_organization_cid_id')

        # Deleting field 'Irradiation_event_xray_source_data.derivation_cid'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'derivation_cid_id')

        # Deleting field 'Irradiation_event_xray_source_data.collimated_field_height'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'collimated_field_height')

        # Deleting field 'Irradiation_event_xray_source_data.collimated_field_width'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'collimated_field_width')

        # Deleting field 'Irradiation_event_xray_source_data.grid_absorbing_material'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_absorbing_material')

        # Deleting field 'Irradiation_event_xray_source_data.grid_spacing_material'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_spacing_material')

        # Deleting field 'Irradiation_event_xray_source_data.grid_thickness'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_thickness')

        # Deleting field 'Irradiation_event_xray_source_data.grid_pitch'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_pitch')

        # Deleting field 'Irradiation_event_xray_source_data.grid_aspect_ratio'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_aspect_ratio')

        # Deleting field 'Irradiation_event_xray_source_data.grid_period'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_period')

        # Deleting field 'Irradiation_event_xray_source_data.grid_focal_distance'
        db.delete_column(u'remapp_irradiation_event_xray_source_data', 'grid_focal_distance')


        # Changing field 'Irradiation_event_xray_source_data.average_glandular_dose'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'average_glandular_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Irradiation_event_xray_source_data.average_xray_tube_current'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'average_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Irradiation_event_xray_source_data.derivation'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'derivation', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Irradiation_event_xray_source_data.collimated_field_area'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'collimated_field_area', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6))

        # Changing field 'Irradiation_event_xray_source_data.pulse_rate'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'pulse_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Irradiation_event_xray_source_data.number_of_pulses'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'number_of_pulses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0))

        # Changing field 'Irradiation_event_xray_source_data.irradiation_duration'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'irradiation_duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Irradiation_event_xray_source_data.focal_spot_size'
        db.alter_column(u'remapp_irradiation_event_xray_source_data', 'focal_spot_size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Ct_accumulated_dose_data.patient_model'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'patient_model', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

        # Changing field 'Ct_accumulated_dose_data.reference_authority_text'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'reference_authority_text', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

        # Changing field 'Ct_accumulated_dose_data.effective_dose_phantom_type'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'effective_dose_phantom_type', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

        # Changing field 'Ct_accumulated_dose_data.dosimeter_type'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'dosimeter_type', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

        # Changing field 'Ct_accumulated_dose_data.total_number_of_irradiation_events'
        db.alter_column(u'remapp_ct_accumulated_dose_data', 'total_number_of_irradiation_events', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0))

        # Changing field 'Scanning_length.top_z_location_of_reconstructable_volume'
        db.alter_column(u'remapp_scanning_length', 'top_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Scanning_length.exposed_range'
        db.alter_column(u'remapp_scanning_length', 'exposed_range', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Scanning_length.scanning_length'
        db.alter_column(u'remapp_scanning_length', 'scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Scanning_length.top_z_location_of_scanning_length'
        db.alter_column(u'remapp_scanning_length', 'top_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Scanning_length.length_of_reconstructable_volume'
        db.alter_column(u'remapp_scanning_length', 'length_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Scanning_length.bottom_z_location_of_reconstructable_volume'
        db.alter_column(u'remapp_scanning_length', 'bottom_z_location_of_reconstructable_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Scanning_length.bottom_z_location_of_scanning_length'
        db.alter_column(u'remapp_scanning_length', 'bottom_z_location_of_scanning_length', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_primary_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_primary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_primary_end_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_primary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.compression_thickness'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'compression_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.table_horizontal_rotation_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'table_horizontal_rotation_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_secondary_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_secondary_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.table_cradle_tilt_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'table_cradle_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.positioner_secondary_end_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'positioner_secondary_end_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.compression_force'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'compression_force', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Irradiation_event_xray_mechanical_data.table_head_tilt_angle'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'table_head_tilt_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.column_angulation'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'column_angulation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Irradiation_event_xray_mechanical_data.magnification_factor'
        db.alter_column(u'remapp_irradiation_event_xray_mechanical_data', 'magnification_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Xray_tube_current.xray_tube_current'
        db.alter_column(u'remapp_xray_tube_current', 'xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Xray_filters.xray_filter_thickness_minimum'
        db.alter_column(u'remapp_xray_filters', 'xray_filter_thickness_minimum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))

        # Changing field 'Xray_filters.xray_filter_thickness_maximum'
        db.alter_column(u'remapp_xray_filters', 'xray_filter_thickness_maximum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2))
        # Deleting field 'Observer_context.person_observer_name'
        db.delete_column(u'remapp_observer_context', 'person_observer_name')

        # Deleting field 'Observer_context.person_observer_organization_name'
        db.delete_column(u'remapp_observer_context', 'person_observer_organization_name')

        # Deleting field 'Observer_context.person_observer_role_in_organization'
        db.delete_column(u'remapp_observer_context', 'person_observer_role_in_organization_id')

        # Deleting field 'Observer_context.person_observer_role_in_procedure'
        db.delete_column(u'remapp_observer_context', 'person_observer_role_in_procedure_id')


        # Changing field 'Calibration.calibration_factor'
        db.alter_column(u'remapp_calibration', 'calibration_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5))

        # Changing field 'Calibration.calibration_uncertainty'
        db.alter_column(u'remapp_calibration', 'calibration_uncertainty', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5))

        # Changing field 'Ct_xray_source_parameters.maximum_xray_tube_current'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'maximum_xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Ct_xray_source_parameters.exposure_time_per_rotation'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'exposure_time_per_rotation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_xray_source_parameters.xray_filter_aluminum_equivalent'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'xray_filter_aluminum_equivalent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_xray_source_parameters.xray_tube_current'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'xray_tube_current', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Ct_xray_source_parameters.kvp'
        db.alter_column(u'remapp_ct_xray_source_parameters', 'kvp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'General_study_module_attributes.modality_type'
        db.alter_column(u'remapp_general_study_module_attributes', 'modality_type', self.gf('django.db.models.fields.CharField')(max_length=8, null=True))
        # Deleting field 'Dose_related_distance_measurements.table_longitudinal_end_position'
        db.delete_column(u'remapp_dose_related_distance_measurements', 'table_longitudinal_end_position')

        # Deleting field 'Dose_related_distance_measurements.table_lateral_end_position'
        db.delete_column(u'remapp_dose_related_distance_measurements', 'table_lateral_end_position')

        # Deleting field 'Dose_related_distance_measurements.table_height_end_position'
        db.delete_column(u'remapp_dose_related_distance_measurements', 'table_height_end_position')


        # Changing field 'Dose_related_distance_measurements.table_longitudinal_position'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'table_longitudinal_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.table_lateral_position'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'table_lateral_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_detector'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_detector', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.radiological_thickness'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'radiological_thickness', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_table_plane'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_table_plane', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_entrance_surface'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_entrance_surface', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_reference_point'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_reference_point', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.distance_source_to_isocenter'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'distance_source_to_isocenter', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Dose_related_distance_measurements.table_height_position'
        db.alter_column(u'remapp_dose_related_distance_measurements', 'table_height_position', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Irradiation_event_xray_detector_data.deviation_index'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'deviation_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Irradiation_event_xray_detector_data.sensitivity'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'sensitivity', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=6))

        # Changing field 'Irradiation_event_xray_detector_data.relative_xray_exposure'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'relative_xray_exposure', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=6))

        # Changing field 'Irradiation_event_xray_detector_data.exposure_index'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Irradiation_event_xray_detector_data.target_exposure_index'
        db.alter_column(u'remapp_irradiation_event_xray_detector_data', 'target_exposure_index', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))
        # Deleting field 'Ct_irradiation_event_data.irradiation_event_label'
        db.delete_column(u'remapp_ct_irradiation_event_data', 'irradiation_event_label')

        # Deleting field 'Ct_irradiation_event_data.label_type'
        db.delete_column(u'remapp_ct_irradiation_event_data', 'label_type_id')


        # Changing field 'Ct_irradiation_event_data.exposure_time'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'exposure_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.ctdifreeair_calculation_factor'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'ctdifreeair_calculation_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.mean_ctdivol'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'mean_ctdivol', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.effective_dose'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'effective_dose', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.number_of_xray_sources'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'number_of_xray_sources', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=0))

        # Changing field 'Ct_irradiation_event_data.mean_ctdifreeair'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'mean_ctdifreeair', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.dlp'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'dlp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.effective_dose_conversion_factor'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'effective_dose_conversion_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.nominal_single_collimation_width'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'nominal_single_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.pitch_factor'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'pitch_factor', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Ct_irradiation_event_data.nominal_total_collimation_width'
        db.alter_column(u'remapp_ct_irradiation_event_data', 'nominal_total_collimation_width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4))
        # Deleting field 'Irradiation_event_xray_data.projection_eponymous_name_cid'
        db.delete_column(u'remapp_irradiation_event_xray_data', 'projection_eponymous_name_cid_id')

        # Deleting field 'Irradiation_event_xray_data.patient_table_relationship_cid'
        db.delete_column(u'remapp_irradiation_event_xray_data', 'patient_table_relationship_cid_id')

        # Deleting field 'Irradiation_event_xray_data.patient_orientation_cid'
        db.delete_column(u'remapp_irradiation_event_xray_data', 'patient_orientation_cid_id')

        # Deleting field 'Irradiation_event_xray_data.patient_orientation_modifier_cid'
        db.delete_column(u'remapp_irradiation_event_xray_data', 'patient_orientation_modifier_cid_id')

        # Deleting field 'Irradiation_event_xray_data.patient_equivalent_thickness'
        db.delete_column(u'remapp_irradiation_event_xray_data', 'patient_equivalent_thickness')

        # Deleting field 'Irradiation_event_xray_data.breast_composition_cid'
        db.delete_column(u'remapp_irradiation_event_xray_data', 'breast_composition_cid_id')


        # Changing field 'Irradiation_event_xray_data.entrance_exposure_at_rp'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'entrance_exposure_at_rp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=4))

        # Changing field 'Irradiation_event_xray_data.patient_table_relationship'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'patient_table_relationship', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Irradiation_event_xray_data.percent_fibroglandular_tissue'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'percent_fibroglandular_tissue', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

        # Changing field 'Irradiation_event_xray_data.patient_orientation_modifier'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'patient_orientation_modifier', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Irradiation_event_xray_data.half_value_layer'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'half_value_layer', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5))

        # Changing field 'Irradiation_event_xray_data.patient_orientation'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'patient_orientation', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Irradiation_event_xray_data.projection_eponymous_name'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'projection_eponymous_name', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'Irradiation_event_xray_data.dose_area_product'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'dose_area_product', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=12))

        # Changing field 'Irradiation_event_xray_data.breast_composition'
        db.alter_column(u'remapp_irradiation_event_xray_data', 'breast_composition', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

    models = {
        u'remapp.accumulated_cassette_based_projection_radiography_dose': {
            'Meta': {'object_name': 'Accumulated_cassette_based_projection_radiography_dose'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Accumulated_xray_dose']"}),
            'detector_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_number_of_radiographic_frames': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.accumulated_integrated_projection_radiography_dose': {
            'Meta': {'object_name': 'Accumulated_integrated_projection_radiography_dose'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Accumulated_xray_dose']"}),
            'dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_point_definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_point_definition_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            'total_number_of_radiographic_frames': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.accumulated_mammography_xray_dose': {
            'Meta': {'object_name': 'Accumulated_mammography_xray_dose'},
            'accumulated_average_glandular_dose': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Accumulated_xray_dose']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laterality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.accumulated_projection_xray_dose': {
            'Meta': {'object_name': 'Accumulated_projection_xray_dose'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Accumulated_xray_dose']"}),
            'acquisition_dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'acquisition_dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'fluoro_dose_area_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'fluoro_dose_rp_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_point_definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_point_definition_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            'total_acquisition_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'total_fluoro_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'total_number_of_radiographic_frames': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.accumulated_xray_dose': {
            'Meta': {'object_name': 'Accumulated_xray_dose'},
            'acquisition_plane': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Projection_xray_radiation_dose']"})
        },
        u'remapp.calibration': {
            'Meta': {'object_name': 'Calibration'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Accumulated_xray_dose']"}),
            'calibration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'calibration_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'calibration_responsible_party': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'calibration_uncertainty': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'dose_measurement_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'remapp.content_item_descriptions': {
            'Meta': {'ordering': "['code_value']", 'object_name': 'Content_item_descriptions'},
            'cid_table': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'code_meaning': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code_value': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'remapp.ct_accumulated_dose_data': {
            'Meta': {'object_name': 'Ct_accumulated_dose_data'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ct_dose_length_product_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ct_effective_dose_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_radiation_dose']"}),
            'dosimeter_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effective_dose_phantom_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_method': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10012_method'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'patient_model': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_authority_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10012_authority'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'reference_authority_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'total_number_of_irradiation_events': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '0', 'blank': 'True'})
        },
        u'remapp.ct_dose_check_details': {
            'Meta': {'object_name': 'Ct_dose_check_details'},
            'accumulated_ctdivol_forward_estimate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'accumulated_dlp_forward_estimate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'alert_reason_for_proceeding': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']"}),
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
        u'remapp.ct_irradiation_event_data': {
            'Meta': {'object_name': 'Ct_irradiation_event_data'},
            'acquisition_protocol': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ct_acquisition_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_type'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_radiation_dose']"}),
            'ctdifreeair_calculation_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ctdiw_phantom_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_phantom'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'date_time_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dlp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'effective_dose': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'effective_dose_conversion_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'exposure_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_label': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'irradiation_event_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_labeltype'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'mean_ctdifreeair': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'mean_ctdivol': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'measurement_method': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_method'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'nominal_single_collimation_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'nominal_total_collimation_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'number_of_xray_sources': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '0', 'blank': 'True'}),
            'pitch_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'procedure_context': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_context'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'series_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'target_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10013_region'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'xray_modulation_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'remapp.ct_radiation_dose': {
            'Meta': {'object_name': 'Ct_radiation_dose'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_of_xray_irradiation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.General_study_module_attributes']"}),
            'has_intent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_intent'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedure_reported': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_procedure'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'scope_of_accumulation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_scope'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'source_of_dose_information': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10011_source'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'start_of_xray_irradiation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uid_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1011_uid'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"})
        },
        u'remapp.ct_xray_source_parameters': {
            'Meta': {'object_name': 'Ct_xray_source_parameters'},
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']"}),
            'exposure_time_per_rotation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification_of_the_xray_source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'kvp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'maximum_xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_filter_aluminum_equivalent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.ctreconstructionalgorithm': {
            'Meta': {'object_name': 'CtReconstructionAlgorithm'},
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reconstruction_algorithm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.device_participant': {
            'Meta': {'object_name': 'Device_participant'},
            'accumulated_xray_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Accumulated_xray_dose']", 'null': 'True', 'blank': 'True'}),
            'ct_accumulated_dose_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_accumulated_dose_data']", 'null': 'True', 'blank': 'True'}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']", 'null': 'True', 'blank': 'True'}),
            'device_manufacturer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_model_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_role_in_procedure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            'device_serial_number': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_detector_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_detector_data']", 'null': 'True', 'blank': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.dose_related_distance_measurements': {
            'Meta': {'object_name': 'Dose_related_distance_measurements'},
            'distance_source_to_detector': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_entrance_surface': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_isocenter': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_reference_point': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'distance_source_to_table_plane': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_mechanical_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_mechanical_data']"}),
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
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']"})
        },
        u'remapp.general_equipment_module_attributes': {
            'Meta': {'object_name': 'General_equipment_module_attributes'},
            'date_of_last_calibration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'device_serial_number': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gantry_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.General_study_module_attributes']"}),
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
        u'remapp.general_study_module_attributes': {
            'Meta': {'object_name': 'General_study_module_attributes'},
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
        u'remapp.image_view_modifier': {
            'Meta': {'object_name': 'Image_view_modifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_view_modifier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_data']"})
        },
        u'remapp.irradiation_event_xray_data': {
            'Meta': {'object_name': 'Irradiation_event_xray_data'},
            'acquisition_plane': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_plane'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'acquisition_protocol': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'anatomical_structure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_anatomy'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'breast_composition': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'breast_composition_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_breastcomposition'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_time_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dose_area_product': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'entrance_exposure_at_rp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'half_value_layer': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_view': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_view'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'irradiation_event_label': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'irradiation_event_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_eventtype'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'irradiation_event_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_labeltype'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'laterality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_laterality'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'patient_equivalent_thickness': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'patient_orientation': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'patient_orientation_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_ptorientation'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'patient_orientation_modifier': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'patient_orientation_modifier_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_ptorientationmod'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'patient_table_relationship': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'patient_table_relationship_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_pttablerel'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'percent_fibroglandular_tissue': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'projection_eponymous_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'projection_eponymous_name_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_pojectioneponymous'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Projection_xray_radiation_dose']"}),
            'reference_point_definition': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_rpdefinition'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'target_region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003_region'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"})
        },
        u'remapp.irradiation_event_xray_detector_data': {
            'Meta': {'object_name': 'Irradiation_event_xray_detector_data'},
            'deviation_index': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'exposure_index': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_data']"}),
            'relative_exposure_unit': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'relative_xray_exposure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'sensitivity': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'target_exposure_index': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.irradiation_event_xray_mechanical_data': {
            'Meta': {'object_name': 'Irradiation_event_xray_mechanical_data'},
            'column_angulation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'compression_force': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'compression_thickness': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'crdr_mechanical_configuration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_data']"}),
            'magnification_factor': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_primary_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_primary_end_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_secondary_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'positioner_secondary_end_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_cradle_tilt_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_head_tilt_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'table_horizontal_rotation_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.irradiation_event_xray_source_data': {
            'Meta': {'object_name': 'Irradiation_event_xray_source_data'},
            'anode_target_material': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_anodetarget'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'average_glandular_dose': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'average_xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'collimated_field_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'collimated_field_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'collimated_field_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'derivation': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'derivation_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_derivation'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'dose_rp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '12', 'blank': 'True'}),
            'exposure_control_mode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'exposure_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'fluoro_mode': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_fluoromode'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
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
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_data']"}),
            'number_of_pulses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'pulse_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'reference_point_definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_point_definition_code': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10003b_rpdefinition'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"})
        },
        u'remapp.kvp': {
            'Meta': {'object_name': 'Kvp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']"}),
            'kvp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.observer_context': {
            'Meta': {'object_name': 'Observer_context'},
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_radiation_dose']", 'null': 'True', 'blank': 'True'}),
            'device_observer_manufacturer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_model_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_physical_location_during_observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_serial_number': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_observer_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_role_in_procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_role'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observer_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_observertype'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'person_observer_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_observer_organization_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_observer_role_in_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_ptroleorg'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'person_observer_role_in_procedure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1002_ptroleproc'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Projection_xray_radiation_dose']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.patient_module_attributes': {
            'Meta': {'object_name': 'Patient_module_attributes'},
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.General_study_module_attributes']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'not_patient_indicator': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_patient_ids': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'patient_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient_sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'remapp.patient_study_module_attributes': {
            'Meta': {'object_name': 'Patient_study_module_attributes'},
            'admitting_diagnosis_code_sequence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'admitting_diagnosis_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.General_study_module_attributes']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient_age': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'patient_age_decimal': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '3', 'blank': 'True'}),
            'patient_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'patient_weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.person_participant': {
            'Meta': {'object_name': 'Person_participant'},
            'ct_accumulated_dose_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_accumulated_dose_data']", 'null': 'True', 'blank': 'True'}),
            'ct_dose_check_details_alert': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_alert'", 'null': 'True', 'to': u"orm['remapp.Ct_dose_check_details']"}),
            'ct_dose_check_details_notification': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_notification'", 'null': 'True', 'to': u"orm['remapp.Ct_dose_check_details']"}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']", 'null': 'True', 'blank': 'True'}),
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_radiation_dose']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_data']", 'null': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_id_issuer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_role_in_organization': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person_role_in_organization_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_roleorg'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'person_role_in_procedure': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'person_role_in_procedure_cid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid1020_roleproc'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'projection_xray_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Projection_xray_radiation_dose']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.projection_xray_radiation_dose': {
            'Meta': {'object_name': 'Projection_xray_radiation_dose'},
            'acquisition_device_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_study_module_attributes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.General_study_module_attributes']"}),
            'has_intent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_intent'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedure_reported': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_procedure'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'scope_of_accumulation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_scope'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'source_of_dose_information': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_infosource'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'xray_detector_data_available': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_detector'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'xray_mechanical_data_available': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_mech'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'xray_source_data_available': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tid10001_source'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"})
        },
        u'remapp.pulse_width': {
            'Meta': {'object_name': 'Pulse_width'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']"}),
            'pulse_width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.scanning_length': {
            'Meta': {'object_name': 'Scanning_length'},
            'bottom_z_location_of_reconstructable_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'bottom_z_location_of_scanning_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']"}),
            'exposed_range': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'frame_of_reference_uid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_of_reconstructable_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'scanning_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'top_z_location_of_reconstructable_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'top_z_location_of_scanning_length': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        },
        u'remapp.size_upload': {
            'Meta': {'object_name': 'Size_upload'},
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
        u'remapp.sizespecificdoseestimation': {
            'Meta': {'object_name': 'SizeSpecificDoseEstimation'},
            'ct_irradiation_event_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_irradiation_event_data']"}),
            'derived_effective_diameter': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measured_ap_dimension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'measured_lateral_dimension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'measurement_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.sourceofctdoseinformation': {
            'Meta': {'object_name': 'SourceOfCTDoseInformation'},
            'ct_radiation_dose': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Ct_radiation_dose']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_of_dose_information': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.xray_filters': {
            'Meta': {'object_name': 'Xray_filters'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']"}),
            'xray_filter_material': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'xrayfilters_material'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"}),
            'xray_filter_thickness_maximum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_filter_thickness_minimum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'}),
            'xray_filter_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'xrayfilters_type'", 'null': 'True', 'to': u"orm['remapp.Content_item_descriptions']"})
        },
        u'remapp.xray_grid': {
            'Meta': {'object_name': 'Xray_grid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']"}),
            'xray_grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Content_item_descriptions']", 'null': 'True', 'blank': 'True'})
        },
        u'remapp.xray_tube_current': {
            'Meta': {'object_name': 'Xray_tube_current'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irradiation_event_xray_source_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['remapp.Irradiation_event_xray_source_data']"}),
            'xray_tube_current': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8', 'blank': 'True'})
        }
    }

    complete_apps = ['remapp']