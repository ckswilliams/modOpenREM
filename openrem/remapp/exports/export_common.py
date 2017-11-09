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
        if modality in [u"DX", u"RF"]:
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


def get_common_data(modality, exams, pid=None, name=None, patid=None):
    """Get the data common to several exports

    :param modality: Modality for the number of irradiation events database location
    :param exams: exam to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: the common data for that exam
    """
    from django.core.exceptions import ObjectDoesNotExist

    if pid and (name or patid):
        try:
            patient_birth_date = exams.patientmoduleattr_set.get().patient_birth_date
            if name:
                patient_name = exams.patientmoduleattr_set.get().patient_name
            if patid:
                patient_id = exams.patientmoduleattr_set.get().patient_id
        except ObjectDoesNotExist:
            patient_birth_date = None
            patient_name = None
            patient_id = None

    try:
        institution_name = exams.generalequipmentmoduleattr_set.get().institution_name
        manufacturer = exams.generalequipmentmoduleattr_set.get().manufacturer
        manufacturer_model_name = exams.generalequipmentmoduleattr_set.get().manufacturer_model_name
        station_name = exams.generalequipmentmoduleattr_set.get().station_name
        display_name = exams.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name
    except ObjectDoesNotExist:
        institution_name = None
        manufacturer = None
        manufacturer_model_name = None
        station_name = None
        display_name = None

    try:
        patient_sex = exams.patientmoduleattr_set.get().patient_sex
    except ObjectDoesNotExist:
        patient_sex = None

    try:
        patient_age_decimal = exams.patientstudymoduleattr_set.get().patient_age_decimal
        patient_size = exams.patientstudymoduleattr_set.get().patient_size
        patient_weight = exams.patientstudymoduleattr_set.get().patient_weight
    except ObjectDoesNotExist:
        patient_age_decimal = None
        patient_size = None
        patient_weight = None

    try:
        not_patient_indicator = exams.patientmoduleattr_set.get().not_patient_indicator
    except ObjectDoesNotExist:
        not_patient_indicator = None

    if modality in u"CT":
        try:
            exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get()
        except ObjectDoesNotExist:
            total_number_of_irradiation_events = None
            ct_dose_length_product_total = None
        else:
            try:
                total_number_of_irradiation_events = int(
                    exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get().total_number_of_irradiation_events)
            except TypeError:
                total_number_of_irradiation_events = None
            ct_dose_length_product_total = exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get(
                ).ct_dose_length_product_total
    elif modality in u"DX":
        try:
            total_number_of_radiographic_frames = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                ).accumintegratedprojradiogdose_set.get().total_number_of_radiographic_frames
            dap_total = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                ).accumintegratedprojradiogdose_set.get().dose_area_product_total
            if dap_total:
                cgycm2 = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                    ).accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
            else:
                cgycm2 = None
        except ObjectDoesNotExist:
            total_number_of_radiographic_frames = None
            cgycm2 = None
    elif modality in u"RF":
        try:
            event_count = exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
        except ObjectDoesNotExist:
            event_count = None

    examdata = []
    if pid and name:
        examdata += [patient_name]
    if pid and patid:
        examdata += [patient_id]
    examdata += [
        institution_name,
        manufacturer,
        manufacturer_model_name,
        station_name,
        display_name,
        exams.accession_number,
        exams.operator_name,
        exams.study_date,
        exams.study_time,
    ]
    if pid and (name or patid):
        examdata += [
            patient_birth_date,
        ]
    examdata += [
        patient_age_decimal,
        patient_sex,
        patient_size,
        patient_weight,
        not_patient_indicator,
        exams.study_description,
        exams.requested_procedure_code_meaning,
    ]
    if modality in u"CT":
        examdata += [
            total_number_of_irradiation_events,
            ct_dose_length_product_total,
        ]
    elif modality in u"DX":
        examdata += [
            total_number_of_radiographic_frames,
            cgycm2,
        ]
    elif modality in u"RF":
        examdata += [
            event_count,
        ]

    return examdata
