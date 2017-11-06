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
    :param book: xlsxwriter book to work on
    :param sheet: xlsxwriter sheet to work on
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
    sheet.set_column(date_column - 2, date_column - 2, None, textformat) # Accession number as text

    return book


def common_headers(pid=False, name=None, patid=None):
    """
    Function to generate list of header text common to several exports
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: list of strings
    """
    pid_headings = []
    if pid and name:
        pid_headings += [u'Patient name']
    if pid and patid:
        pid_headings += [u'Patient ID']
    headers = pid_headings + [
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
        headers += [
            u'Date of birth',
        ]
    headers += [
        u'Age',
        u'Sex',
        u'Height',
        u'Mass (kg)',
        u'Test patient?',
        u'Study description',
        u'Requested procedure',
        u'No. events',
    ]

    return headers


def sheet_name(protocol_name):
    """
    Creates Excel safe version of protocol name for sheet tab text
    :param protocol_name: string, protocol name
    :return: string, Excel safe sheet name for tab text
    """
    tab_text = protocol_name.lower().replace(u" ", u"_")
    translation_table = {ord(u'['): ord(u'('), ord(u']'): ord(u')'), ord(u':'): ord(u';'), ord(u'*'): ord(u'#'),
                         ord(u'?'): ord(u';'), ord(u'/'): ord(u'|'), ord(u'\\'): ord(u'|')}
    tab_text = tab_text.translate(translation_table)  # remove illegal characters
    tab_text = tab_text[:31]
    return tab_text


def generate_sheets(studies, book, protocol_headers, modality=None, pid=False, name=None, patid=None):
    """
    Function to generate the sheets in the xlsx book based on the protocol names
    :param studies: filtered queryset of exams
    :param book: xlsxwriter book to work on
    :param protocol_headers: list of headers to insert on each sheet
    :param modality: study modality to determine database location of acquisition_protocol
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: book
    """
    sheet_list = {}
    protocols_list = []
    for exams in studies:
        if modality in u"DX":
            events = exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')
        elif modality in u"CT":
            events =  exams.ctradiationdose_set.get().ctirradiationeventdata_set.all()
        for s in events:
            if s.acquisition_protocol:
                safe_protocol = s.acquisition_protocol
            else:
                safe_protocol = u'Unknown'
            if safe_protocol not in protocols_list:
                protocols_list.append(safe_protocol)
    protocols_list.sort()

    for protocol in protocols_list:
        tab_text = sheet_name(protocol)
        if tab_text not in sheet_list:
            sheet_list[tab_text] = {
                'sheet': book.add_worksheet(tab_text),
                'count': 0,
                'protocolname': [protocol]}
            sheet_list[tab_text]['sheet'].write_row(0, 0, protocol_headers)
            book = text_and_date_formats(book, sheet_list[tab_text]['sheet'], pid=pid, name=name, patid=patid)
        else:
            if protocol not in sheet_list[tab_text]['protocolname']:
                sheet_list[tab_text]['protocolname'].append(protocol)

    return book, sheet_list
