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
..  module:: xlsx.
    :synopsis: Module to export database data to multi-sheet Microsoft XLSX files.

..  moduleauthor:: Ed McDonagh

"""
import csv
import logging

from django.core.exceptions import ObjectDoesNotExist
from xlsxwriter.workbook import Workbook
from celery import shared_task
from remapp.exports.export_common import get_common_data, common_headers
from remapp.exports.exportcsv import logger

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

    import sys
    import datetime
    import pkg_resources  # part of setuptools
    from tempfile import TemporaryFile
    from django.core.files import File
    from django.db.models import Count, Max
    from remapp.exports.export_common import text_and_date_formats, common_headers, generate_sheets, sheet_name
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

    try:
        tmpxlsx = TemporaryFile()
        book = Workbook(tmpxlsx, {'strings_to_numbers':  False})
        tsk.progress = u'Workbook created'
        tsk.save()
    except IOError as e:
        logger.error("Unexpected error creating temporary file - please contact an administrator: {0}".format(e))
        exit()

    # Get the data!
    e = ct_acq_filter(filterdict, pid=pid).qs

    tsk.progress = u'Required study filter complete.'
    tsk.num_records = e.count()
    tsk.save()

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

    alldataheaders += _generate_all_data_headers_ct(max_events)

    wsalldata.write_row('A1', alldataheaders)
    numcolumns = len(alldataheaders) - 1
    numrows = e.count()
    wsalldata.autofilter(0, 0, numrows, numcolumns)

    for row, exams in enumerate(e):

        tsk.progress = u'Writing study {0} of {1} to All data sheet and individual protocol sheets'.format(
            row + 1, numrows)
        tsk.save()

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

    # Could at this point go through each sheet adding on the auto filter as we now know how many of each there are...
    
    # Populate summary sheet
    tsk.progress = u'Now populating the summary sheet...'
    tsk.save()

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = u''

    version = vers
    titleformat = book.add_format()
    titleformat.set_font_size=(22)
    titleformat.set_font_color=('#FF0000')
    titleformat.set_bold()
    toplinestring = u'XLSX Export from OpenREM version {0} on {1}'.format(version, str(datetime.datetime.now()))
    linetwostring = u'OpenREM is copyright 2016 The Royal Marsden NHS Foundation Trust, and available under the GPL. ' \
                    u'See http://openrem.org'
    summarysheet.write(0, 0, toplinestring, titleformat)
    summarysheet.write(1, 0, linetwostring)

    # Number of exams
    summarysheet.write(3, 0, u"Total number of exams")
    summarysheet.write(3, 1, e.count())

    # Generate list of Study Descriptions
    summarysheet.write(5, 0, u"Study Description")
    summarysheet.write(5, 1, u"Frequency")
    study_descriptions = e.values("study_description").annotate(n=Count("pk"))
    for row, item in enumerate(study_descriptions.order_by('n').reverse()):
        summarysheet.write(row+6, 0, item['study_description'])
        summarysheet.write(row+6, 1, item['n'])
    summarysheet.set_column('A:A', 25)

    # Generate list of Requested Procedures
    summarysheet.write(5, 3, u"Requested Procedure")
    summarysheet.write(5, 4, u"Frequency")
    requested_procedure = e.values("requested_procedure_code_meaning").annotate(n=Count("pk"))
    for row, item in enumerate(requested_procedure.order_by('n').reverse()):
        summarysheet.write(row+6, 3, item['requested_procedure_code_meaning'])
        summarysheet.write(row+6, 4, item['n'])
    summarysheet.set_column('D:D', 25)

    # Generate list of Series Protocols
    summarysheet.write(5, 6, u"Series Protocol")
    summarysheet.write(5, 7, u"Frequency")
    sortedprotocols = sorted(sheet_list.iteritems(), key=lambda (k, v): v['count'], reverse=True)
    for row, item in enumerate(sortedprotocols):
        summarysheet.write(row+6, 6, u', '.join(item[1]['protocolname'])) # Join as can't write a list to a single cell.
        summarysheet.write(row+6, 7, item[1]['count'])
    summarysheet.set_column('G:G', 15)


    book.close()
    tsk.progress = u'XLSX book written.'
    tsk.save()

    xlsxfilename = u"ctexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(xlsxfilename, File(tmpxlsx))
    except OSError as e:
        tsk.progress = u"Error saving export file - please contact an administrator. Error({0}): {1}".format(
            e.errno, e.strerror)
        tsk.status = u'ERROR'
        tsk.save()
        return
    except:
        tsk.progress = u"Unexpected error saving export file - please contact an administrator: {0}".format(
            sys.exc_info()[0])
        tsk.status = u'ERROR'
        tsk.save()
        return

    tsk.status = u'COMPLETE'
    tsk.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    tsk.save()


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

    import sys
    import datetime
    from tempfile import TemporaryFile
    from django.core.files import File
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

    try:
        tmpfile = TemporaryFile()
        writer = csv.writer(tmpfile)

        tsk.progress = u'CSV file created'
        tsk.save()
    except IOError as e:
        logger.error("Unexpected error creating temporary file - please contact an administrator: {0}".format(e))
        exit()

    # Get the data!
    e = ct_acq_filter(filterdict, pid=pid).qs

    tsk.progress = u'Required study filter complete.'
    tsk.save()

    numresults = e.count()

    tsk.progress = u'{0} studies in query.'.format(numresults)
    tsk.num_records = numresults
    tsk.save()

    headings = common_headers(pid=pid, name=name, patid=patid)
    headings += [
        u'DLP total (mGy.cm)',
        ]

    max_events_dict = e.aggregate(Max('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events'))
    max_events = max_events_dict['ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events__max']
    headings += _generate_all_data_headers_ct(max_events)
    writer.writerow(headings)

    tsk.progress = u'CSV header row written.'
    tsk.save()

    for i, exams in enumerate(e):
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
        tsk.progress = u"{0} of {1}".format(i+1, numresults)
        tsk.save()
    tsk.progress = u'All study data written.'
    tsk.save()

    csvfilename = u"ctexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(csvfilename,File(tmpfile))
    except OSError as e:
        tsk.progress = u"Error saving export file - please contact an administrator. Error({0}): {1}".format(e.errno, e.strerror)
        tsk.status = u'ERROR'
        tsk.save()
        return
    except:
        tsk.progress = u"Unexpected error saving export file - please contact an administrator: {0}".format(sys.exc_info()[0])
        tsk.status = u'ERROR'
        tsk.save()
        return

    tsk.status = u'COMPLETE'
    tsk.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    tsk.save()


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
            u'E' + str(h+1) + u' Comments',
            ]

    return repeating_series_headers


def _ct_get_series_data(s):
    from remapp.tools.get_values import return_for_export, string_to_float

    try:
        if s.ctdiw_phantom_type.code_value == u'113691':
            phantom = u'32 cm'
        elif s.ctdiw_phantom_type.code_value == u'113690':
            phantom = u'16 cm'
        else:
            phantom = s.ctdiw_phantom_type.code_meaning
    except AttributeError:
        phantom = None

    seriesdata = [
        str(s.acquisition_protocol),
        str(s.ct_acquisition_type),
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
    if s.number_of_xray_sources > 1:
        for source in s.ctxraysourceparameters_set.all():
            seriesdata += [
                str(source.identification_of_the_xray_source),
                source.kvp,
                source.maximum_xray_tube_current,
                source.xray_tube_current,
                source.exposure_time_per_rotation,
                ]
    else:
        try:
            try:
                s.ctxraysourceparameters_set.get()
            except ObjectDoesNotExist:
                identification_of_the_xray_source = None
                kvp = None
                maximum_xray_tube_current = None
                xray_tube_current = None
                exposure_time_per_rotation = None
            else:
                identification_of_the_xray_source = return_for_export(s.ctxraysourceparameters_set.get(),
                                                                      'identification_of_the_xray_source')
                kvp = string_to_float(return_for_export(s.ctxraysourceparameters_set.get(), 'kvp'))
                maximum_xray_tube_current = string_to_float(return_for_export(s.ctxraysourceparameters_set.get(),
                                                                        'maximum_xray_tube_current'))
                xray_tube_current = string_to_float(return_for_export(s.ctxraysourceparameters_set.get(),
                                                                'xray_tube_current'))
                exposure_time_per_rotation = string_to_float(return_for_export(s.ctxraysourceparameters_set.get(),
                                                                         'exposure_time_per_rotation'))

            seriesdata += [
                identification_of_the_xray_source,
                kvp,
                maximum_xray_tube_current,
                xray_tube_current,
                exposure_time_per_rotation,
                u'n/a',
                u'n/a',
                u'n/a',
                u'n/a',
                u'n/a',
                ]
        except:
            seriesdata += [u'n/a', u'n/a', u'n/a', u'n/a', u'n/a', u'n/a', u'n/a', u'n/a', u'n/a', u'n/a', ]
    seriesdata += [
        s.xray_modulation_type,
        str(s.comment),
        ]
    return seriesdata