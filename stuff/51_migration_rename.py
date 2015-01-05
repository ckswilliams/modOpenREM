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
