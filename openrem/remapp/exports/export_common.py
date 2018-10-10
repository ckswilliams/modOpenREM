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

import logging
import sys
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


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


def common_headers(modality=None, pid=False, name=None, patid=None):
    """
    Function to generate list of header text common to several exports
    :param modality: export modality to customise some of the columns
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
        u'Study time',
    ]
    if pid and (name or patid):
        headers += [
            u'Date of birth',
        ]
    headers += [
        u'Age',
        u'Sex',
    ]
    mammo = bool(modality == u"MG")
    if not mammo:
        headers += [
            u'Height',
            u'Mass (kg)',
        ]
    headers += [
        u'Test patient?',
        u'Study description',
        u'Requested procedure',
        u'Study Comments',
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
        try:
            if modality in [u"DX", u"RF", u"MG"]:
                events = exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id')
            elif modality in u"CT":
                events = exams.ctradiationdose_set.get().ctirradiationeventdata_set.all()
            for s in events:
                if s.acquisition_protocol:
                    safe_protocol = s.acquisition_protocol
                else:
                    safe_protocol = u'Unknown'
                if safe_protocol not in protocols_list:
                    protocols_list.append(safe_protocol)
        except ObjectDoesNotExist:
            logger.error(u"Study missing during generation of sheet names; most likely due to study being deleted "
                         u"whilst export in progress to be replace by later version of RDSR.")
            continue
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

    patient_birth_date = None
    patient_name = None
    patient_id = None
    patient_sex = None
    not_patient_indicator = None
    try:
        patient_module = exams.patientmoduleattr_set.get()
        patient_sex = patient_module.patient_sex
        not_patient_indicator = patient_module.not_patient_indicator
        if pid and (name or patid):
            patient_birth_date = patient_module.patient_birth_date
            if name:
                patient_name = patient_module.patient_name
            if patid:
                patient_id = patient_module.patient_id
    except ObjectDoesNotExist:
        logger.debug("Export {0}; patientmoduleattr_set object does not exist. AccNum {1}, Date {2}".format(
            modality, exams.accession_number, exams.study_date))

    institution_name = None
    manufacturer = None
    manufacturer_model_name = None
    station_name = None
    display_name = None
    try:
        equipment_module = exams.generalequipmentmoduleattr_set.get()
        institution_name = equipment_module.institution_name
        manufacturer = equipment_module.manufacturer
        manufacturer_model_name = equipment_module.manufacturer_model_name
        station_name = equipment_module.station_name
        try:
            display_name = equipment_module.unique_equipment_name.display_name
        except AttributeError:
            logger.debug("Export {0}; unique_equipment_name object does not exist. AccNum {1}, Date {2}".format(
                modality, exams.accession_number, exams.study_date))
    except ObjectDoesNotExist:
        logger.debug("Export {0}; generalequipmentmoduleattr_set object does not exist. AccNum {1}, Date {2}".format(
            modality, exams.accession_number, exams.study_date))

    patient_age_decimal = None
    patient_size = None
    patient_weight = None
    try:
        patient_study_module = exams.patientstudymoduleattr_set.get()
        patient_age_decimal = patient_study_module.patient_age_decimal
        patient_size = patient_study_module.patient_size
        patient_weight = patient_study_module.patient_weight
    except ObjectDoesNotExist:
        logger.debug("Export {0}; patientstudymoduleattr_set object does not exist. AccNum {1}, Date {2}".format(
            modality, exams.accession_number, exams.study_date))

    event_count = None
    cgycm2 = None
    comment = None
    ct_dose_length_product_total = None
    if modality in u"CT":
        try:
            comment = exams.ctradiationdose_set.get().comment
            ct_accumulated = exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get()
            ct_dose_length_product_total = ct_accumulated.ct_dose_length_product_total
            try:
                event_count = int(ct_accumulated.total_number_of_irradiation_events)
            except TypeError:
                logger.debug("Export CT; couldn't get number of irradiation events. AccNum {0}, Date {1}".format(
                    exams.accession_number, exams.study_date))
        except ObjectDoesNotExist:
            logger.debug("Export CT; ctradiationdose_set object does not exist. AccNum {0}, Date {1}".format(
                exams.accession_number, exams.study_date))

    elif modality in u"DX":
        try:
            comment = exams.projectionxrayradiationdose_set.get().comment
            dx_accumulated = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                            ).accumintegratedprojradiogdose_set.get()
            event_count = dx_accumulated.total_number_of_radiographic_frames
            dap_total = dx_accumulated.dose_area_product_total
            if dap_total:
                cgycm2 = dx_accumulated.convert_gym2_to_cgycm2()
            else:
                cgycm2 = None
        except ObjectDoesNotExist:
            logger.debug("Export DX; projectionxrayradiationdose_set object does not exist."
                         " AccNum {0}, Date {1}".format(exams.accession_number, exams.study_date))
    elif modality in [u"RF", u"MG"]:
        try:
            event_count = exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count()
            comment = exams.projectionxrayradiationdose_set.get().comment
        except ObjectDoesNotExist:
            logger.debug("Export {0}; projectionxrayradiationdose_set object does not exist."
                         " AccNum {1}, Date {2}".format(modality, exams.accession_number, exams.study_date))

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
    ]
    if modality not in u"MG":
        examdata += [
            patient_size,
            patient_weight,
        ]
    examdata += [
        not_patient_indicator,
        exams.study_description,
        exams.requested_procedure_code_meaning,
        comment,
    ]
    if modality in u"CT":
        examdata += [
            event_count,
            ct_dose_length_product_total,
        ]
    elif modality in u"DX":
        examdata += [
            event_count,
            cgycm2,
        ]
    elif modality in [u"RF", u"MG"]:
        examdata += [
            event_count,
        ]

    return examdata


def get_pulse_data(source_data, modality=None):
    """Get the pulse level data, which could be a single value or average, or could be per pulse data. Return average.

    :param source_data: IrradEventXRaySourceData table
    :param modality: RF or DX to limit what we look for
    :return: dict of values
    """
    from django.core.exceptions import MultipleObjectsReturned
    from django.db.models import Avg
    from numbers import Number

    try:
        kvp = source_data.kvp_set.get().kvp
    except MultipleObjectsReturned:
        kvp = source_data.kvp_set.all().exclude(kvp__isnull=True).exclude(kvp__exact=0).aggregate(
            Avg('kvp'))['kvp__avg']
    except ObjectDoesNotExist:
        kvp = None

    if modality == "DX":
        try:
            exposure_set = source_data.exposure_set.get()
            uas = exposure_set.exposure
            if isinstance(uas, Number):
                mas = exposure_set.convert_uAs_to_mAs()
            else:
                mas = None
        except MultipleObjectsReturned:
            mas = source_data.exposure_set.all().exclude(exposure__isnull=True).exclude(exposure__exact=0).aggregate(
                Avg('exposure'))['exposure__avg']
            mas = mas / 1000.
        except ObjectDoesNotExist:
            mas = None
    else:
        mas = None

    if modality == "RF":
        try:
            xray_tube_current = source_data.xraytubecurrent_set.get().xray_tube_current
        except MultipleObjectsReturned:
            xray_tube_current = source_data.xraytubecurrent_set.all().exclude(
                xray_tube_current__isnull=True).exclude(
                xray_tube_current__exact=0).aggregate(
                Avg('xray_tube_current'))['xray_tube_current__avg']
        except ObjectDoesNotExist:
            xray_tube_current = None
    else:
        xray_tube_current = None

    if modality == "RF":
        try:
            pulse_width = source_data.pulsewidth_set.get().pulse_width
        except MultipleObjectsReturned:
            pulse_width = source_data.pulsewidth_set.all().exclude(
                pulse_width__isnull=True).exclude(
                pulse_width__exact=0).aggregate(
                Avg('pulse_width'))['pulse_width__avg']
        except ObjectDoesNotExist:
            pulse_width = None
    else:
        pulse_width = None

    return {'kvp': kvp, 'mas': mas, 'xray_tube_current': xray_tube_current, 'pulse_width': pulse_width}


def get_xray_filter_info(source):
    """Compile a string containing details of the filters, and a corresponding string of filter thicknesses

    :param source: exposure in question
    :return: two strings of filters and filter thicknesses
    """
    try:
        filters = u''
        filter_thicknesses = u''
        for current_filter in source.xrayfilters_set.all():
            if u'Aluminum' in str(current_filter.xray_filter_material):
                filters += u'Al'
            elif u'Copper' in str(current_filter.xray_filter_material):
                filters += u'Cu'
            elif u'Tantalum' in str(current_filter.xray_filter_material):
                filters += u'Ta'
            elif u'Molybdenum' in str(current_filter.xray_filter_material):
                filters += u'Mo'
            elif u'Rhodium' in str(current_filter.xray_filter_material):
                filters += u'Rh'
            elif u'Silver' in str(current_filter.xray_filter_material):
                filters += u'Ag'
            elif u'Niobium' in str(current_filter.xray_filter_material):
                filters += u'Nb'
            elif u'Europium' in str(current_filter.xray_filter_material):
                filters += u'Eu'
            elif u'Lead' in str(current_filter.xray_filter_material):
                filters += u'Pb'
            else:
                filters += str(current_filter.xray_filter_material)
            filters += u' | '
            thicknesses = [current_filter.xray_filter_thickness_minimum,
                           current_filter.xray_filter_thickness_maximum]
            if thicknesses[0] is not None and thicknesses[1] is not None:
                thick = sum(thicknesses) / len(thicknesses)
            elif thicknesses[0] is None and thicknesses[1] is None:
                thick = u''
            elif thicknesses[0] is not None:
                thick = thicknesses[0]
            elif thicknesses[1] is not None:
                thick = thicknesses[1]
            if thick:
                thick = round(thick, 4)
            filter_thicknesses += str(thick) + u' | '
        filters = filters[:-3]
        filter_thicknesses = filter_thicknesses[:-3]
    except ObjectDoesNotExist:
        filters = None
        filter_thicknesses = None
    return filters, filter_thicknesses


def get_anode_target_material(source):
    """Return abbreviated version of anode target material

    :param source: x-ray source data for the exposure
    :return: string containing target material abbreviation
    """
    if u"Molybdenum" in str(source.anode_target_material):
        anode = u"Mo"
    elif u"Rhodium" in str(source.anode_target_material):
        anode = u"Rh"
    elif u"Tungsten" in str(source.anode_target_material):
        anode = u"W"
    else:
        anode = str(source.anode_target_material)

    return anode


def create_xlsx(task):
    """Function to create the xlsx temporary file

    :param task: Export task object
    :return: workbook, temp file
    """
    from tempfile import TemporaryFile
    from xlsxwriter.workbook import Workbook

    try:
        temp_xlsx = TemporaryFile()
        book = Workbook(temp_xlsx, {'strings_to_numbers':  False})
    except (OSError, IOError) as e:
        print("Error saving xlsx temporary file ({0}): {1}".format(e.errno, e.strerror))
    except Exception:
        print("Unexpected error: {0}".format(sys.exc_info()[0]))
    else:
        task.progress = u'Workbook created'
        task.save()
        return temp_xlsx, book


def create_csv(task):
    """Function to create the xlsx temporary file

    :param task: Export task object
    :return: workbook, temp file
    """
    import csv
    from tempfile import TemporaryFile

    try:
        temp_csv = TemporaryFile()
        writer = csv.writer(temp_csv)
    except (OSError, IOError) as e:
        print("Error saving csv temporary file ({0}): {1}".format(e.errno, e.strerror))
    except Exception:
        print("Unexpected error: {0}".format(sys.exc_info()[0]))
    else:
        task.progress = u'CSV file created'
        task.save()
        return temp_csv, writer


def write_export(task, filename, temp_file, datestamp):
    """Function to write out the exported xlsx or csv file.

    :param task: Export task object
    :param filename: Filename to use
    :param temp_file: Temporary file
    :param datestamp: dat and time export function started
    :return: Nothing
    """
    import datetime
    from django.core.files import File

    try:
        task.filename.save(filename, File(temp_file))
    except (OSError, IOError) as e:
        print("Error saving export file ({0}): {1}".format(e.errno, e.strerror))
    except Exception:
        print("Unexpected error: {0}".format(sys.exc_info()[0]))

    task.status = u'COMPLETE'
    task.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    task.save()


def create_summary_sheet(task, studies, book, summary_sheet, sheet_list):
    """Create summary sheet for xlsx exports

    :param task: Export task object
    :param studies: study level object that has been exported
    :param book: xlsxwriter book to work on
    :param summary_sheet: worksheet object
    :param sheet_list: list of sheet names
    :return: nothing
    """
    import datetime
    import pkg_resources
    from django.db.models import Count

    # Populate summary sheet
    task.progress = u'Now populating the summary sheet...'
    task.save()

    vers = pkg_resources.require("openrem")[0].version
    version = vers
    titleformat = book.add_format()
    titleformat.set_font_size = 22
    titleformat.set_font_color = '#FF0000'
    titleformat.set_bold()
    toplinestring = u'XLSX Export from OpenREM version {0} on {1}'.format(version, str(datetime.datetime.now()))
    linetwostring = u'OpenREM is copyright 2018 The Royal Marsden NHS Foundation Trust, and available under the GPL. ' \
                    u'See http://openrem.org'
    summary_sheet.write(0, 0, toplinestring, titleformat)
    summary_sheet.write(1, 0, linetwostring)

    # Number of exams
    summary_sheet.write(3, 0, u"Total number of exams")
    summary_sheet.write(3, 1, studies.count())

    # Generate list of Study Descriptions
    summary_sheet.write(5, 0, u"Study Description")
    summary_sheet.write(5, 1, u"Frequency")
    study_descriptions = studies.values("study_description").annotate(n=Count("pk"))
    for row, item in enumerate(study_descriptions.order_by('n').reverse()):
        summary_sheet.write(row+6, 0, item['study_description'])
        summary_sheet.write(row+6, 1, item['n'])
    summary_sheet.set_column('A:A', 25)

    # Generate list of Requested Procedures
    summary_sheet.write(5, 3, u"Requested Procedure")
    summary_sheet.write(5, 4, u"Frequency")
    requested_procedure = studies.values("requested_procedure_code_meaning").annotate(n=Count("pk"))
    for row, item in enumerate(requested_procedure.order_by('n').reverse()):
        summary_sheet.write(row+6, 3, item['requested_procedure_code_meaning'])
        summary_sheet.write(row+6, 4, item['n'])
    summary_sheet.set_column('D:D', 25)

    # Generate list of Series Protocols
    summary_sheet.write(5, 6, u"Series Protocol")
    summary_sheet.write(5, 7, u"Frequency")
    sorted_protocols = sorted(sheet_list.iteritems(), key=lambda (k, v): v['count'], reverse=True)
    for row, item in enumerate(sorted_protocols):
        summary_sheet.write(row+6, 6, u', '.join(item[1]['protocolname'])) # Join as can't write a list to a single cell.
        summary_sheet.write(row+6, 7, item[1]['count'])
    summary_sheet.set_column('G:G', 15)


def abort_if_zero_studies(num_studies, tsk):
    """Function to update progress and status if filter is empty

    :param num_studies: study count in fiilter
    :param tsk: export task
    :return: bool - True if should abort
    """
    if not num_studies:
        tsk.status = u"ERROR"
        tsk.progress = u"Export aborted - zero studies in the filter!"
        tsk.save()
        return True
    else:
        tsk.progress = u'Required study filter complete.'
        tsk.save()
        return False
