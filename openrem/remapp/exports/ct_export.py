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
..  module:: ct_export.
    :synopsis: Module to export database data to multi-sheet Microsoft XLSX files and single-sheet csv files

..  moduleauthor:: Ed McDonagh

"""
import logging

from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from remapp.exports.export_common import get_common_data, common_headers, create_xlsx, create_csv, write_export, \
    create_summary_sheet, abort_if_zero_studies

logger = logging.getLogger(__name__)


@shared_task
def ctxlsx(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered CT database data to multi-sheet Microsoft XSLX files

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :return: Saves xlsx file into Media directory for user to download
    """

    import datetime
    from django.db.models import Max
    from remapp.exports.export_common import text_and_date_formats, generate_sheets, sheet_name
    from remapp.models import Exports
    from remapp.interface.mod_filters import ct_acq_filter
    import uuid

    tsk = Exports.objects.create()

    tsk.task_id = ctxlsx.request.id
    if tsk.task_id is None:  # Required when testing without celery
        tsk.task_id = u'NotCelery-{0}'.format(uuid.uuid4())
    tsk.modality = u"CT"
    tsk.export_type = u"XLSX export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = u'Query filters imported, task started'
    tsk.status = u'CURRENT'
    tsk.includes_pid = bool(pid and (name or patid))
    tsk.export_user_id = user
    tsk.save()

    tmpxlsx, book = create_xlsx(tsk)
    if not tmpxlsx:
        exit()

    # Get the data!
    e = ct_acq_filter(filterdict, pid=pid).qs

    tsk.num_records = e.count()
    if abort_if_zero_studies(tsk.num_records, tsk):
        return

    # Add summary sheet and all data sheet
    summarysheet = book.add_worksheet(u"Summary")
    wsalldata = book.add_worksheet(u'All data')

    book = text_and_date_formats(book, wsalldata, pid=pid, name=name, patid=patid)

    # Some prep
    commonheaders = common_headers(pid=pid, name=name, patid=patid)
    commonheaders += [
        u'DLP total (mGy.cm)',
        ]
    protocolheaders = commonheaders + [
        u'Protocol',
        u'Type',
        u'Exposure time',
        u'Scanning length',
        u'Slice thickness',
        u'Total collimation',
        u'Pitch',
        u'No. sources',
        u'CTDIvol',
        u'Phantom',
        u'DLP',
        u'S1 name',
        u'S1 kVp',
        u'S1 max mA',
        u'S1 mA',
        u'S1 Exposure time/rotation',
        u'S2 name',
        u'S2 kVp',
        u'S2 max mA',
        u'S2 mA',
        u'S2 Exposure time/rotation',
        u'mA Modulation type',
        u'Dose check details',
        u'Comments',
        ]

    # Generate list of protocols in queryset and create worksheets for each
    tsk.progress = u'Generating list of protocols in the dataset...'
    tsk.save()

    book, sheet_list = generate_sheets(e, book, protocolheaders, modality=u"CT", pid=pid, name=name, patid=patid)

    max_events_dict = e.aggregate(Max('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events'))
    max_events = max_events_dict['ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events__max']

    alldataheaders = list(commonheaders)

    tsk.progress = u'Generating headers for the all data sheet...'
    tsk.save()

    if not max_events:
        max_events = 1
    alldataheaders += _generate_all_data_headers_ct(max_events)

    wsalldata.write_row('A1', alldataheaders)
    numcolumns = len(alldataheaders) - 1
    numrows = e.count()
    wsalldata.autofilter(0, 0, numrows, numcolumns)

    for row, exams in enumerate(e):

        tsk.progress = u'Writing study {0} of {1} to All data sheet and individual protocol sheets'.format(
            row + 1, numrows)
        tsk.save()

        try:
            common_exam_data = get_common_data(u"CT", exams, pid, name, patid)
            all_exam_data = list(common_exam_data)

            for s in exams.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id'):
                # Get series data
                series_data = _ct_get_series_data(s)
                # Add series to all data
                all_exam_data += series_data
                # Add series data to series tab
                protocol = s.acquisition_protocol
                if not protocol:
                    protocol = u'Unknown'
                tabtext = sheet_name(protocol)
                sheet_list[tabtext]['count'] += 1
                sheet_list[tabtext]['sheet'].write_row(sheet_list[tabtext]['count'], 0, common_exam_data + series_data)

            wsalldata.write_row(row + 1, 0, all_exam_data)
        except ObjectDoesNotExist:
            error_message = u"DoesNotExist error whilst exporting study {0} of {1},  study UID {2}, accession number" \
                            u" {3} - maybe database entry was deleted as part of importing later version of same" \
                            u" study?".format(row + 1, numrows, exams.study_instance_uid, exams.accession_number)
            logger.error(error_message)
            wsalldata.write(row + 1, 0, error_message)

    create_summary_sheet(tsk, e, book, summarysheet, sheet_list)

    book.close()
    tsk.progress = u'XLSX book written.'
    tsk.save()

    xlsxfilename = u"ctexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    write_export(tsk, xlsxfilename, tmpxlsx, datestamp)


@shared_task
def ct_csv(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered CT database data to a single-sheet CSV file.

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :return: Saves csv file into Media directory for user to download
    """

    import datetime
    from django.db.models import Max
    from remapp.models import Exports
    from remapp.interface.mod_filters import ct_acq_filter

    tsk = Exports.objects.create()

    tsk.task_id = ct_csv.request.id
    tsk.modality = u"CT"
    tsk.export_type = u"CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = u'Query filters imported, task started'
    tsk.status = u'CURRENT'
    tsk.includes_pid = bool(pid and (name or patid))
    tsk.export_user_id = user
    tsk.save()

    tmpfile, writer = create_csv(tsk)
    if not tmpfile:
        exit()

    # Get the data!
    e = ct_acq_filter(filterdict, pid=pid).qs

    tsk.num_records = e.count()
    if abort_if_zero_studies(tsk.num_records, tsk):
        return

    tsk.progress = u'{0} studies in query.'.format(tsk.num_records)
    tsk.save()

    headings = common_headers(pid=pid, name=name, patid=patid)
    headings += [
        u'DLP total (mGy.cm)',
        ]

    max_events_dict = e.aggregate(Max('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events'))
    max_events = max_events_dict['ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events__max']
    if not max_events:
        max_events = 1
    headings += _generate_all_data_headers_ct(max_events)
    writer.writerow(headings)

    tsk.progress = u'CSV header row written.'
    tsk.save()

    for i, exams in enumerate(e):
        tsk.progress = u"{0} of {1}".format(i+1, tsk.num_records)
        tsk.save()
        try:
            exam_data = get_common_data(u"CT", exams, pid, name, patid)
            for s in exams.ctradiationdose_set.get().ctirradiationeventdata_set.order_by('id'):
                # Get series data
                exam_data += _ct_get_series_data(s)
            # Clear out any commas
            for index, item in enumerate(exam_data):
                if item is None:
                    exam_data[index] = ''
                if isinstance(item, basestring) and u',' in item:
                    exam_data[index] = item.replace(u',', u';')
            writer.writerow([unicode(data_string).encode("utf-8") for data_string in exam_data])
        except ObjectDoesNotExist:
            error_message = u"DoesNotExist error whilst exporting study {0} of {1},  study UID {2}, accession number" \
                            u" {3} - maybe database entry was deleted as part of importing later version of same" \
                            u" study?".format(i + 1, tsk.num_records, exams.study_instance_uid, exams.accession_number)
            logger.error(error_message)
            writer.writerow([error_message, ])

    tsk.progress = u'All study data written.'
    tsk.save()

    csvfilename = u"ctexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    write_export(tsk, csvfilename, tmpfile, datestamp)


def _generate_all_data_headers_ct(max_events):
    """Generate the headers for CT that repeat once for each series of the exaqm with the most series in

    :param max_events: maximum number of times to repeat headers
    :return: list of headers
    """

    repeating_series_headers = []
    for h in range(max_events):
        repeating_series_headers += [
            u'E' + str(h+1) + u' Protocol',
            u'E' + str(h+1) + u' Type',
            u'E' + str(h+1) + u' Exposure time',
            u'E' + str(h+1) + u' Scanning length',
            u'E' + str(h+1) + u' Slice thickness',
            u'E' + str(h+1) + u' Total collimation',
            u'E' + str(h+1) + u' Pitch',
            u'E' + str(h+1) + u' No. sources',
            u'E' + str(h+1) + u' CTDIvol',
            u'E' + str(h+1) + u' Phantom',
            u'E' + str(h+1) + u' DLP',
            u'E' + str(h+1) + u' S1 name',
            u'E' + str(h+1) + u' S1 kVp',
            u'E' + str(h+1) + u' S1 max mA',
            u'E' + str(h+1) + u' S1 mA',
            u'E' + str(h+1) + u' S1 Exposure time/rotation',
            u'E' + str(h+1) + u' S2 name',
            u'E' + str(h+1) + u' S2 kVp',
            u'E' + str(h+1) + u' S2 max mA',
            u'E' + str(h+1) + u' S2 mA',
            u'E' + str(h+1) + u' S2 Exposure time/rotation',
            u'E' + str(h+1) + u' mA Modulation type',
            u'E' + str(h+1) + u' Dose check details',
            u'E' + str(h+1) + u' Comments',
            ]

    return repeating_series_headers


def _ct_get_series_data(s):
    from collections import OrderedDict

    try:
        if s.ctdiw_phantom_type.code_value == u'113691':
            phantom = u'32 cm'
        elif s.ctdiw_phantom_type.code_value == u'113690':
            phantom = u'16 cm'
        else:
            phantom = s.ctdiw_phantom_type.code_meaning
    except AttributeError:
        phantom = None

    try:
        ct_acquisition_type = s.ct_acquisition_type.code_meaning
    except AttributeError:
        ct_acquisition_type = ""

    seriesdata = [
        s.acquisition_protocol,
        ct_acquisition_type,
        s.exposure_time,
        s.scanninglength_set.get().scanning_length,
        s.nominal_single_collimation_width,
        s.nominal_total_collimation_width,
        s.pitch_factor,
        s.number_of_xray_sources,
        s.mean_ctdivol,
        phantom,
        s.dlp,
        ]
    source_parameters = OrderedDict()
    source_parameters[0] = {'id': None, 'kvp': None, 'max_current': None, 'current': None, 'time': None}
    source_parameters[1] = {'id': None, 'kvp': None, 'max_current': None, 'current': None, 'time': None}
    try:
        for index, source in enumerate(s.ctxraysourceparameters_set.all()):
            source_parameters[index]['id'] = source.identification_of_the_xray_source
            source_parameters[index]['kvp'] = source.kvp
            source_parameters[index]['max_current'] = source.maximum_xray_tube_current
            source_parameters[index]['current'] = source.xray_tube_current
            source_parameters[index]['time'] = source.exposure_time_per_rotation
    except (ObjectDoesNotExist, KeyError):
        logger.debug("Export: ctxraysourceparameters_set does not exist")
    for source in source_parameters:
        seriesdata += [
            source_parameters[source]['id'],
            source_parameters[source]['kvp'],
            source_parameters[source]['max_current'],
            source_parameters[source]['current'],
            source_parameters[source]['time'],
        ]
    try:
        dose_check = s.ctdosecheckdetails_set.get()
        dose_check_string = []
        if dose_check.dlp_alert_value_configured or dose_check.ctdivol_alert_value_configured:
            dose_check_string += [u"Dose Check Alerts: "]
            if dose_check.dlp_alert_value_configured:
                dose_check_string += [
                    u"DLP alert is configured at {0:.2f} mGy.cm with ".format(dose_check.dlp_alert_value)]
                if dose_check.accumulated_dlp_forward_estimate:
                    dose_check_string += [u"an accumulated forward estimate of {0:.2f} mGy.cm. ".format(
                        dose_check.accumulated_dlp_forward_estimate)]
                else:
                    dose_check_string += [u"no accumulated forward estimate recorded. "]
            if dose_check.ctdivol_alert_value_configured:
                dose_check_string += [
                    u"CTDIvol alert is configured at {0:.2f} mGy with ".format(dose_check.ctdivol_alert_value)]
                if dose_check.accumulated_ctdivol_forward_estimate:
                    dose_check_string += [u"an accumulated forward estimate of {0:.2f} mGy. ".format(
                        dose_check.accumulated_ctdivol_forward_estimate)]
                else:
                    dose_check_string += [u"no accumulated forward estimate recorded. "]
            if dose_check.alert_reason_for_proceeding:
                dose_check_string += [u"Reason for proceeding: {0}. ".format(dose_check.alert_reason_for_proceeding)]
            try:
                dose_check_person_alert = dose_check.tid1020_alert.get()
                if dose_check_person_alert.person_name:
                    dose_check_string += [
                        u"Person authorizing irradiation: {0}. ".format(dose_check_person_alert.person_name)]
            except ObjectDoesNotExist:
                pass
        if dose_check.dlp_notification_value_configured or dose_check.ctdivol_notification_value_configured:
            dose_check_string += [u"Dose Check Notifications: "]
            if dose_check.dlp_notification_value_configured:
                dose_check_string += [
                    u"DLP notification is configured at {0:.2f} mGy.cm with ".format(dose_check.dlp_notification_value)]
                if dose_check.dlp_forward_estimate:
                    dose_check_string += [
                        u"an accumulated forward estimate of {0:.2f} mGy.cm. ".format(dose_check.dlp_forward_estimate)]
                else:
                    dose_check_string += [u"no accumulated forward estimate recorded. "]
            if dose_check.ctdivol_notification_value_configured:
                dose_check_string += [u"CTDIvol notification is configured at {0:.2f} mGy with ".format(
                    dose_check.ctdivol_notification_value)]
                if dose_check.ctdivol_forward_estimate:
                    dose_check_string += [
                        u"a forward estimate of {0:.2f} mGy. ".format(dose_check.ctdivol_forward_estimate)]
                else:
                    dose_check_string += [u"no forward estimate recorded. "]
            if dose_check.notification_reason_for_proceeding:
                dose_check_string += [
                    u"Reason for proceeding: {0}. ".format(dose_check.notification_reason_for_proceeding)]
            try:
                dose_check_person_notification = dose_check.tid1020_notification.get()
                if dose_check_person_notification.person_name:
                    dose_check_string += [
                        u"Person authorizing irradiation: {0}. ".format(dose_check_person_notification.person_name)]
            except ObjectDoesNotExist:
                pass
        dose_check_string = ''.join(dose_check_string)
    except ObjectDoesNotExist:
        dose_check_string = ""
    seriesdata += [
        s.xray_modulation_type,
        dose_check_string,
        s.comment,
        ]
    return seriesdata