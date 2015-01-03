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


    def backwards(self, orm):
        # Renaming model from 'CtDoseCheckDetails' to 'Ct_dose_check_details'
        db.rename_table(u'remapp_ctdosecheckdetails', u'remapp_ct_dose_check_details')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='remapp', model='ctdosecheckdetails').update(model='ct_dose_check_details')