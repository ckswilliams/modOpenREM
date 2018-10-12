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
..  module:: exportcsv.
    :synopsis: Module to export database data to single-sheet CSV files.

..  moduleauthor:: Ed McDonagh

"""

import logging

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from remapp.exports.export_common import common_headers,  text_and_date_formats, generate_sheets, create_summary_sheet,\
    get_common_data, get_anode_target_material, get_xray_filter_info, create_csv, create_xlsx, write_export, \
    sheet_name, abort_if_zero_studies

logger = logging.getLogger(__name__)


def _series_headers(max_events):
    """Return a list of series headers

    :param max_events: number of series
    :return: headers as a list of strings
    """
    series_headers = []
    for series_number in range(max_events):
        series_headers += [
            u'E' + str(series_number+1) + u' View',
            u'E' + str(series_number+1) + u' Laterality',
            u'E' + str(series_number+1) + u' Acquisition',
            u'E' + str(series_number+1) + u' Thickness',
            u'E' + str(series_number+1) + u' Radiological thickness',
            u'E' + str(series_number+1) + u' Force',
            u'E' + str(series_number+1) + u' Mag',
            u'E' + str(series_number+1) + u' Area',
            u'E' + str(series_number+1) + u' Mode',
            u'E' + str(series_number+1) + u' Target',
            u'E' + str(series_number+1) + u' Filter',
            u'E' + str(series_number+1) + u' Filter thickness',
            u'E' + str(series_number+1) + u' Focal spot size',
            u'E' + str(series_number+1) + u' kVp',
            u'E' + str(series_number+1) + u' mA',
            u'E' + str(series_number+1) + u' ms',
            u'E' + str(series_number+1) + u' uAs',
            u'E' + str(series_number+1) + u' ESD',
            u'E' + str(series_number+1) + u' AGD',
            u'E' + str(series_number+1) + u' % Fibroglandular tissue',
            u'E' + str(series_number+1) + u' Exposure mode description'
        ]
    return series_headers


def _mg_get_series_data(event):
    """Return the series level data

    :param event: event level object
    :return: series data as list of strings
    """
    try:
        mechanical_data = event.irradeventxraymechanicaldata_set.get()
        compression_thickness = mechanical_data.compression_thickness
        compression_force = mechanical_data.compression_force
        magnification_factor = mechanical_data.magnification_factor
    except ObjectDoesNotExist:
        compression_thickness = None
        compression_force = None
        magnification_factor = None

    try:
        radiological_thickness = event.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(
            ).radiological_thickness
    except ObjectDoesNotExist:
        radiological_thickness = None

    try:
        source_data = event.irradeventxraysourcedata_set.get()
        collimated_field_area = source_data.collimated_field_area
        exposure_control_mode = source_data.exposure_control_mode
        anode_target_material = get_anode_target_material(source_data)
        focal_spot_size = source_data.focal_spot_size
        average_xray_tube_current = source_data.average_xray_tube_current
        exposure_time = source_data.exposure_time
        average_glandular_dose = source_data.average_glandular_dose
        try:
            filters, filter_thicknesses = get_xray_filter_info(source_data)
        except ObjectDoesNotExist:
            filters = None
            filter_thicknesses = None
        try:
            kvp = source_data.kvp_set.get().kvp
        except ObjectDoesNotExist:
            kvp = None
        try:
            exposure = source_data.exposure_set.get().exposure
        except ObjectDoesNotExist:
            exposure = None
    except ObjectDoesNotExist:
        collimated_field_area = None
        exposure_control_mode = None
        anode_target_material = None
        focal_spot_size = None
        average_xray_tube_current = None
        exposure_time = None
        average_glandular_dose = None
        filters = None
        filter_thicknesses = None
        kvp = None
        exposure = None

    if event.image_view:
        view = event.image_view.code_meaning
    else:
        view = None
    if event.laterality:
        laterality = event.laterality.code_meaning
    else:
        laterality = None

    series_data = [
        view,
        laterality,
        event.acquisition_protocol,
        compression_thickness,
        radiological_thickness,
        compression_force,
        magnification_factor,
        collimated_field_area,
        exposure_control_mode,
        anode_target_material,
        filters,
        filter_thicknesses,
        focal_spot_size,
        kvp,
        average_xray_tube_current,
        exposure_time,
        exposure,
        event.entrance_exposure_at_rp,
        average_glandular_dose,
        event.percent_fibroglandular_tissue,
        event.comment,
    ]
    return series_data


@shared_task
def exportMG2excel(filterdict, pid=False, name=None, patid=None, user=None, xlsx=False):
    """Export filtered mammography database data to a single-sheet CSV file or a multi sheet xlsx file.

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :param xlsx: Whether to export a single sheet csv or a multi sheet xlsx
    :return: Saves csv file into Media directory for user to download
    """

    import datetime
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import MGSummaryListFilter, MGFilterPlusPid
    import uuid

    tsk = Exports.objects.create()
    tsk.task_id = exportMG2excel.request.id
    if tsk.task_id is None:  # Required when testing without celery
        tsk.task_id = u'NotCelery-{0}'.format(uuid.uuid4())
    tsk.modality = u"MG"
    if xlsx:
        tsk.export_type = u"XLSX export"
    else:
        tsk.export_type = u"CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = u'Query filters imported, task started'
    tsk.status = u'CURRENT'
    tsk.includes_pid = bool(pid and (name or patid))
    tsk.export_user_id = user
    tsk.save()

    if xlsx:
        tmpfile, book = create_xlsx(tsk)
        if not tmpfile:
            exit()
    else:
        tmpfile, writer = create_csv(tsk)
        if not tmpfile:
            exit()

    # Resetting the ordering key to avoid duplicates
    if isinstance(filterdict, dict):
        if u'o' in filterdict and filterdict[u'o'] == '-projectionxrayradiationdose__accumxraydose__' \
                                                      'accummammographyxraydose__accumulated_average_glandular_dose':
            logger.info("Replacing AGD ordering with study date to avoid duplication")
            filterdict['o'] = '-study_date'

    # Get the data!
    if pid:
        df_filtered_qs = MGFilterPlusPid(
            filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact=u'MG'))
    else:
        df_filtered_qs = MGSummaryListFilter(
            filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact=u'MG'))
    studies = df_filtered_qs.qs

    tsk.progress = u'Required study filter complete.'
    tsk.save()

    tsk.num_records = studies.count()
    if abort_if_zero_studies(tsk.num_records, tsk):
        return

    if xlsx:
        # Add summary sheet and all data sheet
        summarysheet = book.add_worksheet("Summary")
        wsalldata = book.add_worksheet('All data')
        book = text_and_date_formats(book, wsalldata, pid=pid, name=name, patid=patid)

    headings = common_headers(modality=u"MG", pid=pid, name=name, patid=patid)
    all_data_headings = list(headings)
    headings += [
        u'View',
        u'Laterality',
        u'Acquisition',
        u'Thickness',
        u'Radiological thickness',
        u'Force',
        u'Mag',
        u'Area',
        u'Mode',
        u'Target',
        u'Filter',
        u'Filter thickness',
        u'Focal spot size',
        u'kVp',
        u'mA',
        u'ms',
        u'uAs',
        u'ESD',
        u'AGD',
        u'% Fibroglandular tissue',
        u'Exposure mode description'
        ]

    if not xlsx:
        writer.writerow(headings)
    else:
        # Generate list of protocols in queryset and create worksheets for each
        tsk.progress = u'Generating list of protocols in the dataset...'
        tsk.save()

        tsk.progress = u'Creating an Excel safe version of protocol names and creating a worksheet for each...'
        tsk.save()

        book, sheet_list = generate_sheets(studies, book, headings, modality=u"MG", pid=pid, name=name, patid=patid)

    max_events = 0
    for study_index, exam in enumerate(studies):
        tsk.progress = u"{0} of {1}".format(study_index + 1, tsk.num_records)
        tsk.save()

        try:
            common_exam_data = get_common_data(u"MG", exam, pid=pid, name=name, patid=patid)
            all_exam_data = list(common_exam_data)

            this_study_max_events = 0
            for series in exam.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):
                this_study_max_events += 1
                if this_study_max_events > max_events:
                    max_events = this_study_max_events
                series_data = _mg_get_series_data(series)
                if not xlsx:
                    series_data = list(common_exam_data) + series_data
                    for index, item in enumerate(series_data):
                        if item is None:
                            series_data[index] = ''
                        if isinstance(item, basestring) and u',' in item:
                            series_data[index] = item.replace(u',', u';')
                    writer.writerow([unicode(data_string).encode("utf-8") for data_string in series_data])
                else:
                    all_exam_data += series_data  # For all data
                    protocol = series.acquisition_protocol
                    if not protocol:
                        protocol = u'Unknown'
                    tabtext = sheet_name(protocol)
                    sheet_list[tabtext]['count'] += 1
                    try:
                        sheet_list[tabtext]['sheet'].write_row(sheet_list[tabtext]['count'], 0,
                                                               common_exam_data + series_data)
                    except TypeError:
                        logger.error("Common is |{0}| series is |{1}|".format(common_exam_data, series_data))
                        exit()
            if xlsx:
                wsalldata.write_row(study_index + 1, 0, all_exam_data)
        except ObjectDoesNotExist:
            error_message = u"DoesNotExist error whilst exporting study {0} of {1},  study UID {2}, accession number" \
                            u" {3} - maybe database entry was deleted as part of importing later version of same" \
                            u" study?".format(
                                study_index + 1, tsk.num_records, exam.study_instance_uid, exam.accession_number)
            logger.error(error_message)
            if xlsx:
                wsalldata.write(study_index + 1, 0, error_message)
            else:
                writer.writerow([error_message, ])

    if xlsx:
        all_data_headings += _series_headers(max_events)
        wsalldata.write_row('A1', all_data_headings)
        numrows = studies.count()
        wsalldata.autofilter(0, 0, numrows, len(all_data_headings) - 1)
        create_summary_sheet(tsk, studies, book, summarysheet, sheet_list)

    tsk.progress = u'All study data written.'
    tsk.save()

    filetype_suffix = u"csv"
    if xlsx:
        book.close()
        filetype_suffix = u"xlsx"

    export_filename = u"mgexport{0}.{1}".format(datestamp.strftime("%Y%m%d-%H%M%S%f"), filetype_suffix)

    write_export(tsk, export_filename, tmpfile, datestamp)
