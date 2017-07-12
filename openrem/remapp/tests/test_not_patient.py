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
        """Adds the not-patient patterns to match against in each test"""
        NotPatientIndicatorsID(not_patient_id=u'qa*').save()
        NotPatientIndicatorsID(not_patient_id=u'PHY*').save()
        NotPatientIndicatorsName(not_patient_name=u'*TEST*').save()
        NotPatientIndicatorsName(not_patient_name=u'QA*').save()
        NotPatientIndicatorsName(not_patient_name=u'PHYSICS*').save()

    def test_real_patient(self):
        """Tests that nothing is returned if we think it is a real patient"""
        ds = Dataset()
        ds.PatientName = u'Smith^Dolliquay'
        ds.PatientID = u'278247623467'

        self.assertEqual(get_not_pt(ds), None)

    def test_qa_id(self):
        """Tests the qa* pattern in the ID field, with different case"""
        ds = Dataset()
        ds.PatientName = u'Smith^Dolliquay'
        ds.PatientID = u'QA12345'

        self.assertEqual(get_not_pt(ds), u'IDs: qa* | Names: ')

    def test_physics_name(self):
        """Tests the PHYSICS* name pattern, different case"""
        ds = Dataset()
        ds.PatientName = u'Physics^LBDAlignment'
        ds.PatientID = u'12345'

        self.assertEqual(get_not_pt(ds), u'IDs:  | Names: physics*')

    def test_names(self):
        """Tests multiple name patterns matching simultaneously"""
        ds = Dataset()
        ds.PatientName = u'Physics^LBDAlignmentTest'
        ds.PatientID = u'12345'

        self.assertEqual(get_not_pt(ds), u'IDs:  | Names: *test* physics*')

    def test_names_and_id(self):
        """Tests both name and ID patterns matching together"""
        ds = Dataset()
        ds.PatientName = u'Physics^LBDAlignmentTest'
        ds.PatientID = u'PHY12345'

        self.assertEqual(get_not_pt(ds), u'IDs: phy* | Names: *test* physics*')
