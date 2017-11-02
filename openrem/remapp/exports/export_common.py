# This Python file uses the following encoding: utf-8
#    OpenREM - Radiation Exposure Monitoring tools for the physicist
#    Copyright (C) 2017  The Royal Marsden NHS Foundation Trust
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
..  module:: export_common.
    :synopsis: Module to deduplicate some of the export code

..  moduleauthor:: Ed McDonagh

"""

def text_and_date_formats(book, sheet, pid=False, name=None, patid=None):
    """
    Function to write out the headings common to each sheet and modality and format the date, time, patient ID and
    accession number columns.
    :param book: xlsx book to work on
    :param sheet: xlsx sheet to work on
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: book
    """

    from django.conf import settings

    textformat = book.add_format({'num_format': '@'})
    dateformat = book.add_format({'num_format': settings.XLSX_DATE})
    timeformat = book.add_format({'num_format': settings.XLSX_TIME})

    date_column = 7
    patid_column = 0
    if pid and patid:
        date_column += 1
    if pid and name:
        date_column += 1
        patid_column += 1
    sheet.set_column(date_column, date_column, 10, dateformat)  # allow date to be displayed.
    sheet.set_column(date_column + 1, date_column + 1, None, timeformat)  # allow time to be displayed.
    if pid and (name or patid):
        sheet.set_column(date_column + 2, date_column + 2, 10, dateformat)  # Birth date column
    if pid and patid:
        sheet.set_column(patid_column, patid_column, None, textformat)  # make sure leading zeros are not dropped
    sheet.set_column(date_column - 2, date_column - 2, None, textformat)

    return book

def common_headers(pid=False, name=None, patid=None):
    """
    Function to generate list of header text common to several exports
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: list of strings
    """
    pidheadings = []
    if pid and name:
        pidheadings += [u'Patient name']
    if pid and patid:
        pidheadings += [u'Patient ID']
    commonheaders = pidheadings + [
        u'Institution',
        u'Manufacturer',
        u'Model name',
        u'Station name',
        u'Display name',
        u'Accession number',
        u'Operator',
        u'Study date',
        u'Study Time',
    ]
    if pid and (name or patid):
        commonheaders += [
            u'Date of birth',
        ]
    commonheaders += [
        u'Age',
        u'Sex',
        u'Height',
        u'Mass (kg)',
        u'Test patient?',
        u'Study description',
        u'Requested procedure',
        u'No. events',
    ]

    return commonheaders