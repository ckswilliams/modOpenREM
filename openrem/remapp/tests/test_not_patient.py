# This Python file uses the following encoding: utf-8

from __future__ import unicode_literals
from dicom.dataset import Dataset
from django.test import TestCase
from remapp.models import NotPatientIndicatorsID, NotPatientIndicatorsName
from remapp.tools.not_patient_indicators import get_not_pt

class NotPatientIndicatorTests(TestCase):
    """
    Test class for the indicators that a study might not be for a real patient
    """
    def setUp(self):
        NotPatientIndicatorsID(not_patient_id=u'qa*').save()
        NotPatientIndicatorsID(not_patient_id=u'PHY*').save()
        NotPatientIndicatorsName(not_patient_name=u'*TEST*').save()
        NotPatientIndicatorsName(not_patient_name=u'QA*').save()
        NotPatientIndicatorsName(not_patient_name=u'PHYSICS*').save()

    def test_real_patient(self):
        ds = Dataset()
        ds.PatientName = u'Smith^Dolliquay'
        ds.PatientID = u'278247623467'

        self.assertEqual(get_not_pt(ds), None)

    def test_qa_id(self):
        ds = Dataset()
        ds.PatientName = u'Smith^Dolliquay'
        ds.PatientID = u'QA12345'

        self.assertEqual(get_not_pt(ds), u'IDs: qa* | Names: ')

    def test_physics_name(self):
        ds = Dataset()
        ds.PatientName = u'Physics^LBDAlignment'
        ds.PatientID = u'12345'

        self.assertEqual(get_not_pt(ds), u'IDs:  | Names: PHYSICS*')

    def test_names(self):
        ds = Dataset()
        ds.PatientName = u'Physics^LBDAlignmentTest'
        ds.PatientID = u'12345'

        self.assertEqual(get_not_pt(ds), u'IDs:  | Names: *TEST* PHYSICS*')

    def test_names_and_id(self):
        ds = Dataset()
        ds.PatientName = u'Physics^LBDAlignmentTest'
        ds.PatientID = u'PHY12345'

        self.assertEqual(get_not_pt(ds), u'IDs: PHY* | Names: *TEST* PHYSICS*')
