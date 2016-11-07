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

    def test_export_no_ascii(self):
        """

        """
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

        task = Exports.objects.all()[0]
        file_sha256 = '6a7f762a4cb67068f9150489f76eae89dbc21ca4748e1d9427c5d750df97754a'

        self.assertTrue(os.path.isfile(task.filename.path))
        self.assertEqual(hashlib.sha256(open(task.filename.path, 'rb').read()).hexdigest(), file_sha256)

        # studies = GeneralStudyModuleAttr.objects.all()

        # request = self.factory.get('/openrem/exportmgcsv1/0/0/?')
        # request.user = self.user
        # response = mgcsv1(request)
        # print "Response is {0}".format(response)

