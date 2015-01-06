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

        # Renaming model from 'Accumulated_projection_xray_dose' to 'AccumXRayDose'
        db.rename_table(u'remapp_accumulated_projection_xray_dose', u'remapp_accumxraydose')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='accumulated_projection_xray_dose').update(model='accumxraydose')

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
