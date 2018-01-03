# This Python file uses the following encoding: utf-8
#    OpenREM - Radiation Exposure Monitoring tools for the physicist
#    Copyright (C) 2012,2013  The Royal Marsden NHS Foundation Trust
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    Additional permission under section 7 of GPLv3:
#    You shall not make any use of the name of The Royal Marsden NHS
#    Foundation trust in connection with this Program in any press or
#    other public announcement without the prior written consent of
#    The Royal Marsden NHS Foundation Trust.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
..  module:: dcmdatetime.
    :synopsis: Module to create Python dates and times from DICOM dates and times and vice versa.

..  moduleauthor:: Ed McDonagh

"""


def get_date(tag, dataset):
    """Get DICOM date string and return Python date.

    :param tag:         DICOM keyword, no spaces or plural as per dictionary.
    :type tag:          str.
    :param dataset:     The DICOM dataset containing the tag.
    :type dataset:      dataset
    :returns:           Python date value
    """
    if tag in dataset:
        dicomdate = getattr(dataset, tag)
        return make_date(dicomdate)


def get_time(tag, dataset):
    """Get DICOM time string and return Python time.

    :param tag:         DICOM keyword, no spaces or plural as per dictionary.
    :type tag:          str.
    :param dataset:     The DICOM dataset containing the tag.
    :type dataset:      dataset
    :returns:           python time value
    """
    if tag in dataset:
        dicomtime = getattr(dataset, tag)
        return make_time(dicomtime)


def get_date_time(tag, dataset):
    """Get DICOM date time string and return Python date time.

    :param tag:         DICOM keyword, no spaces or plural as per dictionary.
    :type tag:          str.
    :param dataset:     The DICOM dataset containing the tag.
    :type dataset:      dataset
    :returns:           Python date time value
    """
    if tag in dataset:
        dicomdatetime = getattr(dataset, tag)
        return make_date_time(dicomdatetime)


def make_date(dicomdate):
    """Given a DICOM date, return a Python date.

    :param dicomdate:   DICOM style date.
    :type dicomdate:    str.
    :returns:           Python date value
    """
    import datetime
    try:
        return datetime.datetime.strptime(dicomdate, "%Y%m%d")
    except ValueError:
        return None


def make_time(dicomtime):
    """Given a DICOM time, return a Python time.

    :param dicomdate:   DICOM style time.
    :type dicomdate:    str.
    :returns:           Python time value
    """
    import datetime
    if '+' in dicomtime or '-' in dicomtime:
        import re
        dicomtime = re.split('\+|-', dicomtime)[0]
    try:
        if '.' in dicomtime:
            return datetime.datetime.strptime(dicomtime, "%H%M%S.%f")
        return datetime.datetime.strptime(dicomtime, "%H%M%S")
    except ValueError:
        return None


def make_date_time(dicomdatetime):
    """Given a DICOM date time, return a Python date time.

    :param dicomdate:   DICOM style date time.
    :type dicomdate:    str.
    :returns:           Python date time value
    """
    import datetime
    if not dicomdatetime:
        return None
    if '+' in dicomdatetime or '-' in dicomdatetime:
        import re
        dicomdatetime = re.split('\+|-', dicomdatetime)[0]
    try:
        if '.' in dicomdatetime:
            return datetime.datetime.strptime(dicomdatetime, "%Y%m%d%H%M%S.%f")
        elif len(dicomdatetime) <= 8:
            return datetime.datetime.strptime(dicomdatetime, "%Y%m%d")
        return datetime.datetime.strptime(dicomdatetime, "%Y%m%d%H%M%S")
    except ValueError:
        return None


def make_dcm_date(pythondate):
    """Given a Python date, return a DICOM date
    :param pythondate:  Date
    :type pythondate:   Python date object
    :returns:           DICOM date as string
    """
    import datetime
    if not isinstance(pythondate, datetime.date):
        return None

    try:
        return pythondate.strftime("%Y%m%d")
    except ValueError:
        return None


def make_dcm_date_range(date1=None, date2=None):
    """Given one or two dates of the form yyyy-mm-dd, return a DICOM date range
    :param: date1, date2:   One or two yyyy-mm-dd dates
    :type date1, date2:     String
    :returns:               DICOM date range as string
    """
    import datetime

    date_single = bool(date2 is None)
    date1_python = None
    date2_python = None

    if date1:
        try:
            date1_python = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
        except ValueError:
            date1_python = None
    if date2:
        try:
            date2_python = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
        except ValueError:
            date2_python = None

    if date1_python == date2_python:
        date_single = True

    if date_single and date1_python:
        return make_dcm_date(date1_python)

    if date1_python and date2_python:
        if date1_python < date2_python:
            date_from = make_dcm_date(date1_python)
            date_until = make_dcm_date(date2_python)
        elif date1_python > date2_python:
            date_until = make_dcm_date(date1_python)
            date_from = make_dcm_date(date2_python)
    elif date1_python and not date_single:
        date_from = make_dcm_date(date1_python)
        date_until = make_dcm_date(datetime.date.today())
    elif date2_python:
        date_from = '19000101'
        date_until = make_dcm_date(date2_python)
    else:
        return None

    return '{0}-{1}'.format(date_from, date_until)
