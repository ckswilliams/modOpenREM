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
