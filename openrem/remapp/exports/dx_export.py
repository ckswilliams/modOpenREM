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
..  module:: dx_export.
    :synopsis: Module to export radiographic data to single-sheet CSV files and to multi-sheet XLSX files.

..  moduleauthor:: David Platten and Ed McDonagh

"""
from __future__ import division

import csv
import logging
from xlsxwriter.workbook import Workbook
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from remapp.exports.export_common import text_and_date_formats, common_headers, generate_sheets, sheet_name, \
    get_common_data, get_xray_filter_info

logger = logging.getLogger(__name__)


def _series_headers(max_events):
    """Return the series headers common to both DX exports

    :param max_events: number of series
    :return: headers as a list of strings
    """
    series_headers = []
    for series_number in range(max_events):
        series_headers += [
            u'E' + str(series_number+1) + u' Protocol',
            u'E' + str(series_number+1) + u' Anatomy',
            u'E' + str(series_number+1) + u' Image view',
            u'E' + str(series_number+1) + u' Exposure control mode',
            u'E' + str(series_number+1) + u' kVp',
            u'E' + str(series_number+1) + u' mAs',
            u'E' + str(series_number+1) + u' mA',
            u'E' + str(series_number+1) + u' Exposure time (ms)',
            u'E' + str(series_number+1) + u' Filters',
            u'E' + str(series_number+1) + u' Filter thicknesses (mm)',
            u'E' + str(series_number+1) + u' Exposure index',
            u'E' + str(series_number+1) + u' Relative x-ray exposure',
            u'E' + str(series_number+1) + u' DAP (cGy.cm^2)',
            u'E' + str(series_number+1) + u' Entrance Exposure at RP (mGy)',
            u'E' + str(series_number+1) + u' SDD Detector Dist',
            u'E' + str(series_number+1) + u' SPD Patient Dist',
            u'E' + str(series_number+1) + u' SIsoD Isocentre Dist',
            u'E' + str(series_number+1) + u' Table Height',
            u'E' + str(series_number+1) + u' Comment',
            ]
    return series_headers

def _dx_get_series_data(s):
    """Return the series level data

    :param s: series
    :return: series data
    """
    try:
        exposure_control_mode = s.irradeventxraysourcedata_set.get().exposure_control_mode
        average_xray_tube_current = s.irradeventxraysourcedata_set.get().average_xray_tube_current
        exposure_time = s.irradeventxraysourcedata_set.get().exposure_time
        try:
            kvp = s.irradeventxraysourcedata_set.get().kvp_set.get().kvp
        except ObjectDoesNotExist:
            kvp = None
        try:
            uas = s.irradeventxraysourcedata_set.get().exposure_set.get().exposure
            if uas:
                mas = s.irradeventxraysourcedata_set.get().exposure_set.get().convert_uAs_to_mAs()
            else:
                mas = None
        except ObjectDoesNotExist:
            mas = None
        filters, filter_thicknesses = get_xray_filter_info(s.irradeventxraysourcedata_set.get())
    except ObjectDoesNotExist:
        exposure_control_mode = None
        average_xray_tube_current = None
        exposure_time = None
        kvp = None
        mas = None
        filters = None
        filter_thicknesses = None

    try:
        exposure_index = s.irradeventxraydetectordata_set.get().exposure_index
        relative_xray_exposure = s.irradeventxraydetectordata_set.get().relative_xray_exposure
    except ObjectDoesNotExist:
        exposure_index = None
        relative_xray_exposure = None

    cgycm2 = s.convert_gym2_to_cgycm2()
    entrance_exposure_at_rp = s.entrance_exposure_at_rp

    try:
        distance_source_to_detector = s.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().distance_source_to_detector
        distance_source_to_entrance_surface = s.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().distance_source_to_entrance_surface
        distance_source_to_isocenter = s.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().distance_source_to_isocenter
        table_height_position = s.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().table_height_position
    except ObjectDoesNotExist:
        distance_source_to_detector = None
        distance_source_to_entrance_surface = None
        distance_source_to_isocenter = None
        table_height_position = None

    series_data = [
        s.acquisition_protocol,
        str(s.anatomical_structure),
    ]
    try:
        series_data += [s.image_view.code_meaning,]
    except AttributeError:
        series_data += [None, ]
    series_data += [
        exposure_control_mode,
        kvp,
        mas,
        average_xray_tube_current,
        exposure_time,
        filters,
        filter_thicknesses,
        exposure_index,
        relative_xray_exposure,
        cgycm2,
        entrance_exposure_at_rp,
        distance_source_to_detector,
        distance_source_to_entrance_surface,
        distance_source_to_isocenter,
        table_height_position,
        s.comment,
    ]
    return series_data


@shared_task
def exportDX2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered DX database data to a single-sheet CSV file.

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :return: Saves csv file into Media directory for user to download
    """

    import datetime
    import sys
    from tempfile import TemporaryFile
    from django.core.files import File
    from remapp.models import Exports
    from remapp.interface.mod_filters import dx_acq_filter

    tsk = Exports.objects.create()

    tsk.task_id = exportDX2excel.request.id
    tsk.modality = u"DX"
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
        writer = csv.writer(tmpfile, dialect=csv.excel)

        tsk.progress = u'CSV file created'
        tsk.save()
    except IOError as e:
        logger.error("Unexpected error creating temporary file - please contact an administrator: {0}".format(e))
        exit()

    # Get the data!

    e = dx_acq_filter(filterdict, pid=pid).qs

    tsk.progress = u'Required study filter complete.'
    tsk.save()
        
    numresults = e.count()

    tsk.progress = u'{0} studies in query.'.format(numresults)
    tsk.num_records = numresults
    tsk.save()

    headers = common_headers(pid=pid, name=name, patid=patid)
    headers += [
        u'DAP total (cGy.cm^2)',
    ]

    from django.db.models import Max
    max_events_dict = e.aggregate(Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                                      'total_number_of_radiographic_frames'))
    max_events = max_events_dict['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                                 'total_number_of_radiographic_frames__max']
    if not max_events:
        max_events = 1

    headers += _series_headers(max_events)

    writer.writerow([unicode(header).encode("utf-8") for header in headers])

    tsk.progress = u'CSV header row written.'
    tsk.save()

    for row, exams in enumerate(e):
        exam_data = get_common_data(u"DX", exams, pid=pid, name=name, patid=patid)
        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):
            # Get series data
            series_data = _dx_get_series_data(s)
            # Add series to all data
            exam_data += series_data
        # Clear out any commas
        for index, item in enumerate(exam_data):
            if item is None:
                exam_data[index] = ''
            if isinstance(item, basestring) and u',' in item:
                exam_data[index] = item.replace(u',', u';')
        writer.writerow([unicode(data_string).encode("utf-8") for data_string in exam_data])
        tsk.progress = u"{0} of {1}".format(row + 1, numresults)
        tsk.save()
    tsk.progress = u'All study data written.'
    tsk.save()

    csvfilename = u"dxexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(csvfilename, File(tmpfile))
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

@shared_task
def dxxlsx(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered DX and CR database data to multi-sheet Microsoft XSLX files.

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :return: Saves xlsx file into Media directory for user to download
    """

    import datetime
    import sys
    from tempfile import TemporaryFile
    from django.core.files import File
    from django.db.models import Count
    from remapp.models import Exports
    from remapp.interface.mod_filters import dx_acq_filter
    import uuid

    tsk = Exports.objects.create()

    tsk.task_id = dxxlsx.request.id
    if tsk.task_id is None:  # Required when testing without celery
        tsk.task_id = u'NotCelery-{0}'.format(uuid.uuid4())
    tsk.modality = u"DX"
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
        book = Workbook(tmpxlsx, {'strings_to_numbers': False})
        tsk.progress = u'Workbook created'
        tsk.save()
    except IOError as e:
        logger.error("Unexpected error creating temporary file - please contact an administrator: {0}".format(e))
        exit()

    e = dx_acq_filter(filterdict, pid=pid).qs

    tsk.progress = u'Required study filter complete.'
    tsk.num_records = e.count()
    tsk.save()

    # Add summary sheet and all data sheet
    summarysheet = book.add_worksheet("Summary")
    wsalldata = book.add_worksheet('All data')

    book = text_and_date_formats(book, wsalldata, pid=pid, name=name, patid=patid)

    # Some prep
    commonheaders = common_headers(pid=pid, name=name, patid=patid)
    commonheaders += [
        u'DAP total (cGy.cm^2)',
        ]
    protocolheaders = commonheaders + [
        u'Protocol',
        u'Anatomy',
        u'Image view',
        u'Exposure control mode',
        u'kVp',
        u'mAs',
        u'mA',
        u'Exposure time (ms)',
        u'Filters',
        u'Filter thicknesses (mm)',
        u'Exposure index',
        u'Relative x-ray exposure',
        u'DAP (cGy.cm^2)',
        u'Entrance exposure at RP',
        u'SDD Detector Dist',
        u'SPD Patient Dist',
        u'SIsoD Isocentre Dist',
        u'Table Height',
        u'Comment'
        ]

    # Generate list of protocols in queryset and create worksheets for each
    tsk.progress = u'Generating list of protocols in the dataset...'
    tsk.save()

    tsk.progress = u'Creating an Excel safe version of protocol names and creating a worksheet for each...'
    tsk.save()

    book, sheet_list = generate_sheets(e, book, protocolheaders, modality=u"DX", pid=pid, name=name, patid=patid)

    ##################
    # All data sheet

    from django.db.models import Max
    max_events_dict = e.aggregate(Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                                      'total_number_of_radiographic_frames'))
    max_events = max_events_dict['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                                 'total_number_of_radiographic_frames__max']
    if not max_events:
        max_events = 1

    alldataheaders = list(commonheaders)

    tsk.progress = u'Generating headers for the all data sheet...'
    tsk.save()

    alldataheaders += _series_headers(max_events)
    wsalldata.write_row('A1', alldataheaders)
    numrows = e.count()
    wsalldata.autofilter(0, 0, numrows, len(alldataheaders) - 1)

    for row, exams in enumerate(e):

        tsk.progress = u'Writing study {0} of {1} to All data sheet and individual protocol sheets'.format(
            row + 1, numrows)
        tsk.save()

        common_exam_data = get_common_data(u"DX", exams, pid=pid, name=name, patid=patid)
        all_exam_data = list(common_exam_data)

        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):
            # Get series data
            series_data = _dx_get_series_data(s)
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

    import pkg_resources  # part of setuptools

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''

    version = vers
    titleformat = book.add_format()
    titleformat.set_font_size=(22)
    titleformat.set_font_color=('#FF0000')
    titleformat.set_bold()
    toplinestring = u'XLSX Export from OpenREM version {0} on {1}'.format(version, str(datetime.datetime.now()))
    linetwostring = u'OpenREM is copyright 2017 The Royal Marsden NHS Foundation Trust, and available under the GPL. ' \
                    u'See http://openrem.org'
    summarysheet.write(0,0, toplinestring, titleformat)
    summarysheet.write(1,0, linetwostring)

    # Number of exams
    summarysheet.write(3,0, u"Total number of exams")
    summarysheet.write(3,1,e.count())

    # Generate list of Study Descriptions
    summarysheet.write(5,0, u"Study Description")
    summarysheet.write(5,1, u"Frequency")
    study_descriptions = e.values("study_description").annotate(n=Count("pk"))
    for row, item in enumerate(study_descriptions.order_by('n').reverse()):
        summarysheet.write(row+6,0,item['study_description'])
        summarysheet.write(row+6,1,item['n'])
    summarysheet.set_column('A:A', 25)

    # Generate list of Requested Procedures
    summarysheet.write(5,3, u"Requested Procedure")
    summarysheet.write(5,4, u"Frequency")
    requested_procedure = e.values("requested_procedure_code_meaning").annotate(n=Count("pk"))
    for row, item in enumerate(requested_procedure.order_by('n').reverse()):
        summarysheet.write(row+6,3,item['requested_procedure_code_meaning'])
        summarysheet.write(row+6,4,item['n'])
    summarysheet.set_column('D:D', 25)

    # Generate list of Series Protocols
    summarysheet.write(5,6, u"Series Protocol")
    summarysheet.write(5,7, u"Frequency")
    sortedprotocols = sorted(sheet_list.iteritems(), key=lambda (k,v): v['count'], reverse=True)
    for row, item in enumerate(sortedprotocols):
        summarysheet.write(row+6,6,u', '.join(item[1]['protocolname'])) # Join as can't write a list to a single cell.
        summarysheet.write(row+6,7,item[1]['count'])
    summarysheet.set_column('G:G', 15)


    book.close()
    tsk.progress = u'XLSX book written.'
    tsk.save()

    xlsxfilename = u"dxexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(xlsxfilename,File(tmpxlsx))
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
