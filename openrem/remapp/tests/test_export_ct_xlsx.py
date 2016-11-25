# This Python file uses the following encoding: utf-8
# test_export_ct_xlsx.py

import hashlib
import os
from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory
from remapp.extractors import rdsr
from remapp.exports.xlsx import ctxlsx
from remapp.models import PatientIDSettings, Exports


class ExportCTxlsx(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        eg = Group(name="exportgroup")
        eg.save()
        eg.user_set.add(self.user)
        eg.save()

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        ct_ge_ct660 = os.path.join("test_files", "CT-RDSR-GE_Optima.dcm")
        ct_ge_vct = os.path.join("test_files", "CT-RDSR-GE_VCT.dcm")
        ct_siemens_flash_ss = os.path.join("test_files", "CT-RDSR-Siemens_Flash-TAP-SS.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        rdsr(os.path.join(root_tests, ct_ge_ct660))
        rdsr(os.path.join(root_tests, ct_ge_vct))
        rdsr(os.path.join(root_tests, ct_siemens_flash_ss))

    def test_id_as_text(self):  # See https://bitbucket.org/openrem/openrem/issues/443
        filter_set = ""
        pid = True
        name = False
        patient_id = True

        ctxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        import pandas as pd
        task = Exports.objects.all()[0]
        all_data_sheet = pd.read_excel(task.filename.path, sheetname='All data')
        self.assertEqual(all_data_sheet['Patient ID'][1], '00001234')
