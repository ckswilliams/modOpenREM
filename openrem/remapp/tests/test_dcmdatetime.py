# This Python file uses the following encoding: utf-8
# test_dcmdatetime.py
"""
..  module:: test_dcmdatetime
    :synopsis: Unit test for the dcmdatetime functions

..  moduleauthor:: Ed McDonagh
"""


from __future__ import unicode_literals
import datetime
from django.test import TestCase
from dicom.dataset import Dataset
from remapp.tools.dcmdatetime import get_date, get_time, get_date_time, make_date, make_time, make_date_time,\
    make_dcm_date, make_dcm_date_range


class DCMDateTimeConversionTests(TestCase):
    def test_get_date_exists(self):
        """
        get_date should return the datetime object
        """
        ds = Dataset()
        ds.StudyDate = "20180131"
        date_object = get_date("StudyDate", ds)
        ref_date_object = datetime.datetime(2018, 1, 31, 0, 0)  # Date returned I think is actually a datetime

        self.assertIsInstance(date_object, datetime.date)
        self.assertEqual(date_object, ref_date_object)

    def test_get_date_does_not_exist(self):
        """
        get_date shouldn't return anything
        """
        ds = Dataset()
        date_object = get_date("StudyDate", ds)

        self.assertIsNone(date_object)

    def test_get_date_bad_value(self):
        """
        get_date should return None
        """
        ds = Dataset()
        ds.AccessionNumber = "1234567890"
        ds.StudyID = "asdf"
        date_object1 = get_date("AccessionNumber", ds)
        date_object2 = get_date("StudyID", ds)

        self.assertIsNone(date_object1)
        self.assertIsNone(date_object2)

    def test_get_time_exists(self):
        """
        get_time should return the datetime object
        """
        ds = Dataset()
        ds.StudyTime = "130426.214"
        ds.SeriesTime = "130426"
        time_object_decimal = get_time("StudyTime", ds)
        time_object_seconds = get_time("SeriesTime", ds)
        ref_time_decimal = datetime.datetime(1900, 1, 1, 13, 4, 26, 214000)
        ref_time_seconds = datetime.datetime(1900, 1, 1, 13, 4, 26)

        self.assertIsInstance(time_object_decimal, datetime.datetime)
        self.assertIsInstance(time_object_seconds, datetime.datetime)
        self.assertEqual(time_object_decimal, ref_time_decimal)
        self.assertEqual(time_object_seconds, ref_time_seconds)


