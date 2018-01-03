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
from remapp.tools.dcmdatetime import get_date, get_time, get_date_time, make_dcm_date, make_dcm_date_range


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
        ds.StudyTime = "130426.214000-0600"
        ds.SeriesTime = "130426"
        time_object_decimal = get_time("StudyTime", ds)
        time_object_seconds = get_time("SeriesTime", ds)
        ref_time_decimal = datetime.datetime(1900, 1, 1, 13, 4, 26, 214000)  # Again object is datetime rather than time
        # Optional offset from UTC is currently ignored. Not sure how much TZ aware dates are used
        ref_time_seconds = datetime.datetime(1900, 1, 1, 13, 4, 26)

        self.assertIsInstance(time_object_decimal, datetime.datetime)
        self.assertIsInstance(time_object_seconds, datetime.datetime)
        self.assertEqual(time_object_decimal, ref_time_decimal)
        self.assertEqual(time_object_seconds, ref_time_seconds)

    def test_get_time_does_not_exist(self):
        """
        get_time shouldn't return anything
        """
        ds = Dataset()
        time_object = get_time("StudyTime", ds)

        self.assertIsNone(time_object)

    def test_get_time_bad_value(self):
        """
        get_time should return None
        """
        ds = Dataset()
        ds.AccessionNumber = "1234567890"
        ds.StudyID = "asdf"
        date_object1 = get_time("AccessionNumber", ds)
        date_object2 = get_date("StudyID", ds)

        self.assertIsNone(date_object1)
        self.assertIsNone(date_object2)

    def test_get_date_time_exists(self):
        """
        get_date_time should return the datetime object
        :return:
        """
        ds = Dataset()
        ds.AcquisitionDateTime = "20180629172304.023000+0515"
        ds.FrameAcquisitionDateTime = "20180629172304.023000"
        ds.FrameReferenceDateTime = "20180629"
        ds.StartAcquisitionDateTime = "20180629172304"
        time_date_object_tz = get_date_time("AcquisitionDateTime", ds)
        time_date_object_millisecond = get_date_time("FrameAcquisitionDateTime", ds)
        time_date_object_date_only = get_date_time("FrameReferenceDateTime", ds)
        time_date_object_date_time = get_date_time("StartAcquisitionDateTime", ds)
        ref_date_time_millisecond_object = datetime.datetime(2018, 6, 29, 17, 23, 4, 23000)
        # Optional offset from UTC is currently ignored. Not sure how much TZ aware dates are used
        ref_date_object = datetime.datetime(2018, 6, 29)
        ref_date_time_object = datetime.datetime(2018, 6, 29, 17, 23, 4)

        self.assertIsInstance(time_date_object_tz, datetime.datetime)
        self.assertIsInstance(time_date_object_millisecond, datetime.datetime)
        self.assertIsInstance(time_date_object_date_only, datetime.datetime)
        self.assertIsInstance(time_date_object_date_time, datetime.datetime)
        self.assertEqual(time_date_object_tz, ref_date_time_millisecond_object)
        self.assertEqual(time_date_object_millisecond, ref_date_time_millisecond_object)
        self.assertEqual(time_date_object_date_only, ref_date_object)
        self.assertEqual(time_date_object_date_time, ref_date_time_object)

    def test_get_date_time_does_not_exist(self):
        """
        get_date_time shouldn't return anything
        :return:
        """
        ds = Dataset()
        date_time_object = get_date_time("AcquisitionDateTime", ds)

        self.assertIsNone(date_time_object)

    def test_get_date_time_bad_value(self):
        """
        get_date_time should return None
        :return:
        """
        ds = Dataset()
        ds.AccessionNumber = "1234567890"
        ds.StudyID = "asdf"
        date_time_object1 = get_date_time("AccessionNumber", ds)
        date_time_object2 = get_date_time("StudyID", ds)

        self.assertIsNone(date_time_object1)
        self.assertIsNone(date_time_object2)

    def test_make_dcm_date_range(self):
        """
        Should return valid DICOM date range to use in query-retrieve operations
        :return:
        """
        older_date = "2012-03-14"
        newer_date = "2014-05-23"
        invalid_date_1 = "20130412"
        invalid_date_2 = "2015-23-12"
        invalid_date_3 = "Tuesday"

        standard = make_dcm_date_range(older_date, newer_date)
        reversed_standard = make_dcm_date_range(newer_date, older_date)
        single = make_dcm_date_range(older_date)
        equal = make_dcm_date_range(newer_date, newer_date)
        date1_bad = make_dcm_date_range(invalid_date_1, newer_date)
        date2_bad = make_dcm_date_range(older_date, invalid_date_2)
        both_bad = make_dcm_date_range(invalid_date_1, invalid_date_2)
        single_bad = make_dcm_date(invalid_date_3)

        date_today = make_dcm_date(datetime.date.today())

        self.assertEqual(standard, "20120314-20140523")
        self.assertEqual(reversed_standard, "20120314-20140523")
        self.assertEqual(single, "20120314")
        self.assertEqual(equal, "20140523")
        self.assertEqual(date1_bad, "19000101-20140523")
        self.assertEqual(date2_bad, "20120314-{0}".format(date_today))
        self.assertIsNone(both_bad)
        self.assertIsNone(single_bad)


