# This Python file uses the following encoding: utf-8
# test_export_dx_xlsx.py

import hashlib
import os
from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory
from remapp.extractors import dx
from remapp.exports.dx_export import dxxlsx
from remapp.models import PatientIDSettings, Exports


class ExportDXxlsx(TestCase):
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

        dx_ge_xr220_1 = os.path.join("test_files", "DX-Im-GE_XR220-1.dcm")
        dx_ge_xr220_2 = os.path.join("test_files", "DX-Im-GE_XR220-2.dcm")
        dx_ge_xr220_3 = os.path.join("test_files", "DX-Im-GE_XR220-3.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        dx(os.path.join(root_tests, dx_ge_xr220_1))
        dx(os.path.join(root_tests, dx_ge_xr220_2))
        dx(os.path.join(root_tests, dx_ge_xr220_3))

    def test_id_as_text(self):  # See https://bitbucket.org/openrem/openrem/issues/443
        filter_set = ""
        pid = True
        name = False
        patient_id = True

        dxxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        import pandas as pd
        task = Exports.objects.all()[0]
        all_data_sheet = pd.read_excel(task.filename.path, sheetname='All data')
        self.assertEqual(all_data_sheet['Patient ID'][1], '00001234')
        self.assertEqual(all_data_sheet['Accession number'][0], '001234512345678')
        self.assertEqual(all_data_sheet['Accession number'][1], '0012345.12345678')

        # cleanup
        # task.filename.delete()  # delete file so local testing doesn't get too messy!
        # task.delete()  # not necessary, by hey, why not?
