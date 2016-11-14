# This Python file uses the following encoding: utf-8
# test_export_mammo_csv.py

import hashlib
import os
from decimal import Decimal
from django.contrib.auth.models import AnonymousUser, User, Group
from django.test import TestCase, RequestFactory
from remapp.extractors import mam
from remapp.exports.exportcsv import exportMG2excel
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings, Exports
from remapp.tools.hash_id import hash_id
from remapp.exports.exportviews import mgcsv1

class ExportMammoCSV(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        eg = Group(name="exportgroup")
        eg.save()
        eg.user_set.add(self.user)
        eg.save()

        PatientIDSettings.objects.create()

        dicom_file = "test_files/MG-Im-GE-SenDS-scaled.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)

        filter_set = ""
        pid = False
        name = False
        patient_id = False

        exportMG2excel(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)


    def test_export_no_ascii(self):
        """

        """

        task = Exports.objects.all()[0]
        file_sha256 = '6a7f762a4cb67068f9150489f76eae89dbc21ca4748e1d9427c5d750df97754a'

        self.assertTrue(os.path.isfile(task.filename.path))
        self.assertEqual(hashlib.sha256(open(task.filename.path, 'rb').read()).hexdigest(), file_sha256)

    def test_all_values(self):
        import pandas as pd
        import numpy as np
        task = Exports.objects.all()[0]
        csvdf = pd.read_csv(task.filename.path)

        cols = ['Institution name', 'Manufacturer', 'Station name', 'Display name', 'Accession number', 'Study UID',
                'Study date', 'Study time', 'Patient age', 'Patient sex', 'Number of events', 'Study description',
                'View', 'Laterality', 'Acquisition', 'Thickness', 'Radiological thickness', 'Force', 'Mag', 'Area',
                'Mode', 'Target', 'Filter', 'Focal spot size', 'kVp', 'mA', 'ms', 'uAs', 'ESD', 'AGD',
                '% Fibroglandular tissue', 'Exposure mode description']
        exportline = ['中心医院', 'GE MEDICAL SYSTEMS', 'SENODS01', '中心医院 SENODS01', 'AAAA9876',
                      '1.3.6.1.4.1.5962.99.1.693088767.1633245212.1473866904063.3.0', '2013-04-12',
                      '2013-04-12 12:41:47', '0.000', 'O', '1', '', 'cranio-caudal', 'Left', 'ROUTINE', '53.00000000',
                      '45.00000000', '50.00000000', '1.00000000', '0.04373900', 'AUTOMATIC',
                      'Rhodium or Rhodium compound', 'Rhodium or Rhodium compound', '0.30000000', '29.00000000',
                      '61.00000000', '834.00', '51800.00', '5.07100000', '1.37300000', '31.00000000',
                      'AOP standard RECTANGLE 1662 mm 10 mm 180 mm 240 mm EXP DOSE 87504 nGy PRE-EXP DOSE 5655 nGy PRE-EXP THICK 45 mm PRE-EXP COMPO 29 % PRE-EXP KV 28 PRE-EXP TRACK Rh PRE-EXP FILTER Rh PADDLE 1 FLATFIELD no']
        refdf = pd.DataFrame([exportline], columns=cols, index=range(1))

        self.assertEqual(list(csvdf.columns), cols)
        for col in cols:
            if pd.isnull(csvdf[col][0]):  # deals with missing data
                self.assertEqual('', refdf[col][0])
            elif type(csvdf[col][0]) is str:  # compare all the string values
                self.assertEqual(csvdf[col][0], refdf[col][0])
            else:  # assume all other values are numbers
                self.assertAlmostEqual(csvdf[col][0], float(refdf[col][0]))