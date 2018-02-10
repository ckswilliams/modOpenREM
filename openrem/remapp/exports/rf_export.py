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
..  module:: rf_export.
    :synopsis: Module to export RF data from database to single sheet csv and multisheet xlsx.

..  moduleauthor:: Ed McDonagh

"""

import logging
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from remapp.exports.export_common import text_and_date_formats, common_headers, generate_sheets, sheet_name, \
    get_common_data, get_xray_filter_info, create_xlsx, create_csv, write_export, create_summary_sheet, \
    get_pulse_data, abort_if_zero_studies
from remapp.tools.get_values import return_for_export

logger = logging.getLogger(__name__)


def _get_accumulated_data(accumXrayDose):
    """Extract all the summary level data

    :param accumXrayDose: Accumulated x-ray radiation dose object
    :return: dict of summary level data
    """
    accum = {}
    accum['plane'] = accumXrayDose.acquisition_plane.code_meaning
    try:
        accumulated_integrated_projection_dose = accumXrayDose.accumintegratedprojradiogdose_set.get()
        accum['dose_area_product_total'] = accumulated_integrated_projection_dose.dose_area_product_total
        accum['dose_rp_total'] = accumulated_integrated_projection_dose.dose_rp_total
        accum['reference_point_definition'] = accumulated_integrated_projection_dose.reference_point_definition_code
        if not accum['reference_point_definition']:
            accum['reference_point_definition'] = accumulated_integrated_projection_dose.reference_point_definition
    except ObjectDoesNotExist:
        accum['dose_area_product_total'] = None
        accum['dose_rp_total'] = None
        accum['reference_point_definition_code'] = None
    try:
        accumulated_projection_dose = accumXrayDose.accumprojxraydose_set.get()
        accum['fluoro_dose_area_product_total'] = accumulated_projection_dose.fluoro_dose_area_product_total
        accum['fluoro_dose_rp_total'] = accumulated_projection_dose.fluoro_dose_rp_total
        accum['total_fluoro_time'] = accumulated_projection_dose.total_fluoro_time
        accum['acquisition_dose_area_product_total'] = accumulated_projection_dose.acquisition_dose_area_product_total
        accum['acquisition_dose_rp_total'] = accumulated_projection_dose.acquisition_dose_rp_total
        accum['total_acquisition_time'] = accumulated_projection_dose.total_acquisition_time
    except ObjectDoesNotExist:
        accum['fluoro_dose_area_product_total'] = None
        accum['fluoro_dose_rp_total'] = None
        accum['total_fluoro_time'] = None
        accum['acquisition_dose_area_product_total'] = None
        accum['acquisition_dose_rp_total'] = None
        accum['total_acquisition_time'] = None

    try:
        accum['eventcount'] = int(accumXrayDose.projection_xray_radiation_dose.irradeventxraydata_set.filter(
            acquisition_plane__code_meaning__exact=accum['plane']).count())
    except ObjectDoesNotExist:
        accum['eventcount'] = None

    return accum


def _add_plane_summary_data(exam):
    """Add plane level accumulated data to examdata

    :param exams: exam to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: list of summary data at plane level
    """
    exam_data = []
    for plane in exam.projectionxrayradiationdose_set.get().accumxraydose_set.all():
        accum = _get_accumulated_data(plane)
        exam_data += [
            accum['dose_area_product_total'],
            accum['dose_rp_total'],
            accum['fluoro_dose_area_product_total'],
            accum['fluoro_dose_rp_total'],
            accum['total_fluoro_time'],
            accum['acquisition_dose_area_product_total'],
            accum['acquisition_dose_rp_total'],
            accum['total_acquisition_time'],
            accum['eventcount'],
        ]
        if 'Single' in accum['plane']:
            exam_data += [
                u'', u'', u'', u'', u'', u'', u'', u'', u''
            ]

    return exam_data


def _get_series_data(event, filter_data):
    """Return series level data for protocol sheets

    :param event: evnt in question
    :return: list of data
    """
    try:
        source_data = event.irradeventxraysourcedata_set.get()
        pulse_rate = source_data.pulse_rate
        ii_field_size = source_data.ii_field_size
        exposure_time = source_data.exposure_time
        dose_rp = source_data.dose_rp
        number_of_pulses = source_data.number_of_pulses
        irradiation_duration = source_data.irradiation_duration
        pulse_data = get_pulse_data(source_data=source_data, modality="RF")
        kVp = pulse_data['kvp']
        xray_tube_current = pulse_data['xray_tube_current']
        pulse_width = pulse_data['pulse_width']
    except ObjectDoesNotExist:
        pulse_rate = None
        ii_field_size = None
        exposure_time = None
        dose_rp = None
        number_of_pulses = None
        irradiation_duration = None
        kVp = None
        xray_tube_current = None
        pulse_width = None
    try:
        mechanical_data = event.irradeventxraymechanicaldata_set.get()
        pos_primary_angle = mechanical_data.positioner_primary_angle
        pos_secondary_angle = mechanical_data.positioner_secondary_angle
    except ObjectDoesNotExist:
        pos_primary_angle = None
        pos_secondary_angle = None

    series_data = [
        str(event.date_time_started),
        event.irradiation_event_type.code_meaning,
        event.acquisition_protocol,
        event.acquisition_plane.code_meaning,
        ii_field_size,
        filter_data['filter_material'],
        filter_data['filter_thick'],
        kVp,
        xray_tube_current,
        pulse_width,
        pulse_rate,
        number_of_pulses,
        exposure_time,
        irradiation_duration,
        str(event.convert_gym2_to_cgycm2()),
        dose_rp,
        pos_primary_angle,
        pos_secondary_angle,
    ]

    return series_data


def _all_data_headers(pid=False, name=None, patid=None):
    """Compile list of column headers

    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :return: list of headers for all_data sheet and csv sheet
    """
    all_data_headers = common_headers(pid=pid, name=name, patid=patid) + [
        u'A DAP total (Gy.m^2)',
        u'A Dose RP total (Gy)',
        u'A Fluoro DAP total (Gy.m^2)',
        u'A Fluoro dose RP total (Gy)',
        u'A Fluoro duration total (s)',
        u'A Acq. DAP total (Gy.m^2)',
        u'A Acq. dose RP total (Gy)',
        u'A Acq. duration total (s)',
        u'A Number of events',
        u'B DAP total (Gy.m^2)',
        u'B Dose RP total (Gy)',
        u'B Fluoro DAP total (Gy.m^2)',
        u'B Fluoro dose RP total (Gy)',
        u'B Fluoro duration total (s)',
        u'B Acq. DAP total (Gy.m^2)',
        u'B Acq. dose RP total (Gy)',
        u'B Acq. duration total (s)',
        u'B Number of events',
    ]
    return all_data_headers



@shared_task
def rfxlsx(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered RF database data to multi-sheet Microsoft XSLX files.

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :return: Saves xlsx file into Media directory for user to download
    """

    import datetime
    from django.db.models import Max, Min, Avg
    from remapp.models import GeneralStudyModuleAttr, IrradEventXRayData
    from remapp.models import Exports
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid
    import uuid

    tsk = Exports.objects.create()

    tsk.task_id = rfxlsx.request.id
    if tsk.task_id is None:  # Required when testing without celery
        tsk.task_id = u'NotCelery-{0}'.format(uuid.uuid4())
    tsk.modality = u"RF"
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

    # Get the data
    if pid:
        df_filtered_qs = RFFilterPlusPid(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'RF'))
    else:
        df_filtered_qs = RFSummaryListFilter(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'RF'))
    e = df_filtered_qs.qs

    tsk.num_records = e.count()
    if abort_if_zero_studies(tsk.num_records, tsk):
        return

    # Add summary sheet and all data sheet
    summarysheet = book.add_worksheet(u"Summary")
    wsalldata = book.add_worksheet(u'All data')

    book = text_and_date_formats(book, wsalldata, pid=pid, name=name, patid=patid)
    tsk.progress = u'Creating an Excel safe version of protocol names and creating a worksheet for each...'
    tsk.save()

    all_data_headers = _all_data_headers(pid=pid, name=name, patid=patid)

    sheet_headers = list(all_data_headers)
    protocolheaders = sheet_headers + [
        u'Time',
        u'Type',
        u'Protocol',
        u'Plane',
        u'Field size',
        u'Filter material',
        u'Mean filter thickness (mm)',
        u'kVp',
        u'mA',
        u'Pulse width (ms)',
        u'Pulse rate',
        u'Number of pulses',
        u'Exposure time (ms)',
        u'Exposure duration (s)',
        u'DAP (cGy.cm^2)',
        u'Ref point dose (Gy)',
        u'Primary angle',
        u'Secondary angle',
    ]

    book, sheetlist = generate_sheets(e, book, protocolheaders, modality=u"RF", pid=pid, name=name, patid=patid)

    ##################
    # All data sheet

    num_groups_max = 0
    for row, exams in enumerate(e):

        tsk.progress = u'Writing study {0} of {1}'.format(row + 1, e.count())
        tsk.save()

        try:
            examdata = get_common_data(u"RF", exams, pid=pid, name=name, patid=patid)
            examdata += _add_plane_summary_data(exams)
            common_exam_data = list(examdata)

            angle_range = 5.0  # plus or minus range considered to be the same position
            studyiuid = exams.study_instance_uid
            # TODO: Check if generation of inst could be more efficient, ie start with exams?
            inst = IrradEventXRayData.objects.filter(
                projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__exact=studyiuid)

            num_groups_this_exam = 0
            while inst:  # ie while there are events still left that haven't been matched into a group
                tsk.progress = u'Writing study {0} of {1}; {2} events remaining.'.format(
                    row + 1, e.count(), inst.count())
                tsk.save()
                num_groups_this_exam += 1
                plane = inst[0].acquisition_plane.code_meaning
                try:
                    mechanical_data = inst[0].irradeventxraymechanicaldata_set.get()
                    anglei = mechanical_data.positioner_primary_angle
                    angleii = mechanical_data.positioner_secondary_angle
                except ObjectDoesNotExist:
                    anglei = None
                    angleii = None
                try:
                    source_data = inst[0].irradeventxraysourcedata_set.get()
                    pulse_rate = source_data.pulse_rate
                    fieldsize = source_data.ii_field_size
                    try:
                        filter_material, filter_thick = get_xray_filter_info(source_data)
                    except ObjectDoesNotExist:
                        filter_material = None
                        filter_thick = None
                except ObjectDoesNotExist:
                    pulse_rate = None
                    fieldsize = None
                    filter_material = None
                    filter_thick = None

                protocol = inst[0].acquisition_protocol
                event_type = inst[0].irradiation_event_type.code_meaning

                similarexposures = inst
                if plane:
                    similarexposures = similarexposures.filter(
                        acquisition_plane__code_meaning__exact = plane)
                if protocol:
                    similarexposures = similarexposures.filter(
                        acquisition_protocol__exact = protocol)
                if fieldsize:
                    similarexposures = similarexposures.filter(
                        irradeventxraysourcedata__ii_field_size__exact = fieldsize)
                if pulse_rate:
                    similarexposures = similarexposures.filter(
                        irradeventxraysourcedata__pulse_rate__exact = pulse_rate)
                if filter_material:
                    for xray_filter in inst[0].irradeventxraysourcedata_set.get().xrayfilters_set.all():
                        similarexposures = similarexposures.filter(
                            irradeventxraysourcedata__xrayfilters__xray_filter_material__code_meaning__exact = xray_filter.xray_filter_material)
                        similarexposures = similarexposures.filter(
                            irradeventxraysourcedata__xrayfilters__xray_filter_thickness_maximum__exact = xray_filter.xray_filter_thickness_maximum)
                if anglei:
                    similarexposures = similarexposures.filter(
                        irradeventxraymechanicaldata__positioner_primary_angle__range=(float(anglei) - angle_range, float(anglei) + angle_range))
                if angleii:
                    similarexposures = similarexposures.filter(
                        irradeventxraymechanicaldata__positioner_secondary_angle__range=(float(angleii) - angle_range, float(angleii) + angle_range))
                if event_type:
                    similarexposures = similarexposures.filter(
                        irradiation_event_type__code_meaning__exact = event_type)

                # Remove exposures included in this group from inst
                exposures_to_exclude = [o.irradiation_event_uid for o in similarexposures]
                inst = inst.exclude(irradiation_event_uid__in = exposures_to_exclude)

                angle1 = similarexposures.all().aggregate(
                    Min('irradeventxraymechanicaldata__positioner_primary_angle'),
                    Max('irradeventxraymechanicaldata__positioner_primary_angle'),
                    Avg('irradeventxraymechanicaldata__positioner_primary_angle'))
                angle2 = similarexposures.all().aggregate(
                    Min('irradeventxraymechanicaldata__positioner_secondary_angle'),
                    Max('irradeventxraymechanicaldata__positioner_secondary_angle'),
                    Avg('irradeventxraymechanicaldata__positioner_secondary_angle'))
                dap = similarexposures.all().aggregate(
                    Min('dose_area_product'),
                    Max('dose_area_product'),
                    Avg('dose_area_product'))
                dose_rp = similarexposures.all().aggregate(
                    Min('irradeventxraysourcedata__dose_rp'),
                    Max('irradeventxraysourcedata__dose_rp'),
                    Avg('irradeventxraysourcedata__dose_rp'))
                kvp = similarexposures.all().aggregate(
                    Min('irradeventxraysourcedata__kvp__kvp'),
                    Max('irradeventxraysourcedata__kvp__kvp'),
                    Avg('irradeventxraysourcedata__kvp__kvp'))
                tube_current = similarexposures.all().aggregate(
                    Min('irradeventxraysourcedata__xraytubecurrent__xray_tube_current'),
                    Max('irradeventxraysourcedata__xraytubecurrent__xray_tube_current'),
                    Avg('irradeventxraysourcedata__xraytubecurrent__xray_tube_current'))
                exp_time = similarexposures.all().aggregate(
                    Min('irradeventxraysourcedata__exposure_time'),
                    Max('irradeventxraysourcedata__exposure_time'),
                    Avg('irradeventxraysourcedata__exposure_time'))
                pulse_width = similarexposures.all().aggregate(
                    Min('irradeventxraysourcedata__pulsewidth__pulse_width'),
                    Max('irradeventxraysourcedata__pulsewidth__pulse_width'),
                    Avg('irradeventxraysourcedata__pulsewidth__pulse_width'))

                examdata += [
                    event_type,
                    protocol,
                    similarexposures.count(),
                    plane,
                    pulse_rate,
                    fieldsize,
                    filter_material,
                    filter_thick,
                    kvp['irradeventxraysourcedata__kvp__kvp__min'],
                    kvp['irradeventxraysourcedata__kvp__kvp__max'],
                    kvp['irradeventxraysourcedata__kvp__kvp__avg'],
                    tube_current['irradeventxraysourcedata__xraytubecurrent__xray_tube_current__min'],
                    tube_current['irradeventxraysourcedata__xraytubecurrent__xray_tube_current__max'],
                    tube_current['irradeventxraysourcedata__xraytubecurrent__xray_tube_current__avg'],
                    pulse_width['irradeventxraysourcedata__pulsewidth__pulse_width__min'],
                    pulse_width['irradeventxraysourcedata__pulsewidth__pulse_width__max'],
                    pulse_width['irradeventxraysourcedata__pulsewidth__pulse_width__avg'],
                    exp_time['irradeventxraysourcedata__exposure_time__min'],
                    exp_time['irradeventxraysourcedata__exposure_time__max'],
                    exp_time['irradeventxraysourcedata__exposure_time__avg'],
                    dap['dose_area_product__min'],
                    dap['dose_area_product__max'],
                    dap['dose_area_product__avg'],
                    dose_rp['irradeventxraysourcedata__dose_rp__min'],
                    dose_rp['irradeventxraysourcedata__dose_rp__max'],
                    dose_rp['irradeventxraysourcedata__dose_rp__avg'],
                    angle1['irradeventxraymechanicaldata__positioner_primary_angle__min'],
                    angle1['irradeventxraymechanicaldata__positioner_primary_angle__max'],
                    angle1['irradeventxraymechanicaldata__positioner_primary_angle__avg'],
                    angle2['irradeventxraymechanicaldata__positioner_secondary_angle__min'],
                    angle2['irradeventxraymechanicaldata__positioner_secondary_angle__max'],
                    angle2['irradeventxraymechanicaldata__positioner_secondary_angle__avg'],
                ]

                if not protocol:
                    protocol = u'Unknown'
                tab_text = sheet_name(protocol)
                filter_data = {
                    'filter_material': filter_material,
                    'filter_thick': filter_thick,
                }
                for exposure in similarexposures:
                    series_data = _get_series_data(exposure, filter_data)
                    sheetlist[tab_text]['count'] += 1
                    sheetlist[tab_text]['sheet'].write_row(sheetlist[tab_text]['count'], 0, common_exam_data + series_data)

            if num_groups_this_exam > num_groups_max:
                num_groups_max = num_groups_this_exam

            wsalldata.write_row(row + 1, 0, examdata)
        except ObjectDoesNotExist:
            error_message = u"DoesNotExist error whilst exporting study {0} of {1},  study UID {2}, accession number" \
                            u" {3} - maybe database entry was deleted as part of importing later version of same" \
                            u" study?".format(
                                row + 1, tsk.num_records, exams.study_instance_uid, exams.accession_number)
            logger.error(error_message)
            wsalldata.write(row + 1, 0, error_message)

    tsk.progress = u'Generating headers for the all data sheet...'
    tsk.save()

    for h in range(num_groups_max):
        all_data_headers += [
            u'G' + str(h+1) + u' Type',
            u'G' + str(h+1) + u' Protocol',
            u'G' + str(h+1) + u' No. exposures',
            u'G' + str(h+1) + u' Plane',
            u'G' + str(h+1) + u' Pulse rate',
            u'G' + str(h+1) + u' Field size',
            u'G' + str(h+1) + u' Filter material',
            u'G' + str(h+1) + u' Mean filter thickness (mm)',
            u'G' + str(h+1) + u' kVp min',
            u'G' + str(h+1) + u' kVp max',
            u'G' + str(h+1) + u' kVp mean',
            u'G' + str(h+1) + u' mA min',
            u'G' + str(h+1) + u' mA max',
            u'G' + str(h+1) + u' mA mean',
            u'G' + str(h+1) + u' pulse width min (ms)',
            u'G' + str(h+1) + u' pulse width max (ms)',
            u'G' + str(h+1) + u' pulse width mean (ms)',
            u'G' + str(h+1) + u' Exp time min (ms)',
            u'G' + str(h+1) + u' Exp time max (ms)',
            u'G' + str(h+1) + u' Exp time mean (ms)',
            u'G' + str(h+1) + u' DAP min (Gy.m^2)',
            u'G' + str(h+1) + u' DAP max (Gy.m^2)',
            u'G' + str(h+1) + u' DAP mean (Gy.m^2)',
            u'G' + str(h+1) + u' Ref point dose min (Gy)',
            u'G' + str(h+1) + u' Ref point dose max (Gy)',
            u'G' + str(h+1) + u' Ref point dose mean (Gy)',
            u'G' + str(h+1) + u' Primary angle min',
            u'G' + str(h+1) + u' Primary angle max',
            u'G' + str(h+1) + u' Primary angle mean',
            u'G' + str(h+1) + u' Secondary angle min',
            u'G' + str(h+1) + u' Secondary angle max',
            u'G' + str(h+1) + u' Secondary angle mean',
            ]
    wsalldata.write_row('A1', all_data_headers)
    num_rows = e.count()
    wsalldata.autofilter(0, 0, num_rows, len(all_data_headers) - 1)

    create_summary_sheet(tsk, e, book, summarysheet, sheetlist)

    book.close()
    tsk.progress = u'XLSX book written.'
    tsk.save()

    xlsxfilename = u"rfexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    write_export(tsk, xlsxfilename, tmpxlsx, datestamp)


@shared_task
def exportFL2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered fluoro database data to a single-sheet CSV file.

    :param filterdict: Queryset of studies to export
    :param pid: does the user have patient identifiable data permission
    :param name: has patient name been selected for export
    :param patid: has patient ID been selected for export
    :param user: User that has started the export
    :return: Saves csv file into Media directory for user to download
    """

    import datetime
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid

    tsk = Exports.objects.create()

    tsk.task_id = exportFL2excel.request.id
    tsk.modality = u"RF"
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
    if pid:
        df_filtered_qs = RFFilterPlusPid(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='RF'))
    else:
        df_filtered_qs = RFSummaryListFilter(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='RF'))
    e = df_filtered_qs.qs

    tsk.num_records = e.count()
    if abort_if_zero_studies(tsk.num_records, tsk):
        return

    headings = _all_data_headers(pid=pid, name=name, patid=patid)
    writer.writerow(headings)
    for i, exams in enumerate(e):

        tsk.progress = u"{0} of {1}".format(i + 1, tsk.num_records)
        tsk.save()

        try:
            exam_data = get_common_data(u"RF", exams, pid=pid, name=name, patid=patid)

            for plane in exams.projectionxrayradiationdose_set.get().accumxraydose_set.all():
                accum = _get_accumulated_data(plane)
                exam_data += [
                    accum['dose_area_product_total'],
                    accum['dose_rp_total'],
                    accum['fluoro_dose_area_product_total'],
                    accum['fluoro_dose_rp_total'],
                    accum['total_fluoro_time'],
                    accum['acquisition_dose_area_product_total'],
                    accum['acquisition_dose_rp_total'],
                    accum['total_acquisition_time'],
                    accum['eventcount'],
                ]
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

    csvfilename = u"rfexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    write_export(tsk, csvfilename, tmpfile, datestamp)


@shared_task
def rfopenskin(studyid):
    u"""Export filtered RF database data to multi-sheet Microsoft XSLX files.

    :param studyid: RF study database ID.
    :type studyid: int

    u"""

    import datetime
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.tools.get_values import export_csv_prep

    tsk = Exports.objects.create()

    tsk.task_id = rfopenskin.request.id
    tsk.modality = u"RF"
    tsk.export_type = u"OpenSkin RF csv export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = u'Query filters imported, task started'
    tsk.status = u'CURRENT'
    tsk.save()

    tmpfile, writer = create_csv(tsk)
    if not tmpfile:
        exit()

    # Get the data
    study = GeneralStudyModuleAttr.objects.get(pk=studyid)
    numevents = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.count()
    tsk.num_records = numevents
    tsk.save()

    for i, event in enumerate(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()):
        try:
            study.patientmoduleattr_set.get()
        except ObjectDoesNotExist:
            patient_sex = u''
        else:
            patient_sex = study.patientmoduleattr_set.get().patient_sex

        try:
            event.irradeventxraysourcedata_set.get()
        except ObjectDoesNotExist:
            reference_point_definition = u''
            dose_rp = u''
            fluoro_mode = u''
            pulse_rate = u''
            number_of_pulses = u''
            exposure_time = u''
            focal_spot_size = u''
            irradiation_duration = u''
            average_xray_tube_current = u''
        else:
            reference_point_definition = event.irradeventxraysourcedata_set.get().reference_point_definition
            dose_rp = event.irradeventxraysourcedata_set.get().dose_rp
            fluoro_mode = event.irradeventxraysourcedata_set.get().fluoro_mode
            pulse_rate = event.irradeventxraysourcedata_set.get().pulse_rate
            number_of_pulses = event.irradeventxraysourcedata_set.get().number_of_pulses
            exposure_time = event.irradeventxraysourcedata_set.get().exposure_time
            focal_spot_size = event.irradeventxraysourcedata_set.get().focal_spot_size
            irradiation_duration = event.irradeventxraysourcedata_set.get().irradiation_duration
            average_xray_tube_current = event.irradeventxraysourcedata_set.get().average_xray_tube_current

        try:
            event.irradeventxraymechanicaldata_set.get()
        except ObjectDoesNotExist:
            positioner_primary_angle = u''
            positioner_secondary_angle = u''
            positioner_primary_end_angle = u''
            positioner_secondary_end_angle = u''
            column_angulation = u''
        else:
            positioner_primary_angle = event.irradeventxraymechanicaldata_set.get().positioner_primary_angle
            positioner_secondary_angle = event.irradeventxraymechanicaldata_set.get().positioner_secondary_angle
            positioner_primary_end_angle = event.irradeventxraymechanicaldata_set.get().positioner_primary_end_angle
            positioner_secondary_end_angle = event.irradeventxraymechanicaldata_set.get().positioner_secondary_end_angle
            column_angulation = event.irradeventxraymechanicaldata_set.get().column_angulation

        xray_filter_type = u''
        xray_filter_material = u''
        xray_filter_thickness_minimum = u''
        xray_filter_thickness_maximum = u''
        try:
            for filters in event.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                try:
                    if u"Copper" in filters.xray_filter_material.code_meaning:
                        xray_filter_type = filters.xray_filter_type
                        xray_filter_material = filters.xray_filter_material
                        xray_filter_thickness_minimum = filters.xray_filter_thickness_minimum
                        xray_filter_thickness_maximum = filters.xray_filter_thickness_maximum
                except AttributeError:
                    pass
        except ObjectDoesNotExist:
            pass

        try:
            event.irradeventxraysourcedata_set.get().kvp_set.get()
        except ObjectDoesNotExist:
            kvp = u''
        else:
            kvp = event.irradeventxraysourcedata_set.get().kvp_set.get().kvp

        try:
            event.irradeventxraysourcedata_set.get().xraytubecurrent_set.get()
        except ObjectDoesNotExist:
            xray_tube_current = u''
        else:
            xray_tube_current = event.irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current

        try:
            event.irradeventxraysourcedata_set.get().pulsewidth_set.get()
        except ObjectDoesNotExist:
            pulse_width = u''
        else:
            pulse_width = event.irradeventxraysourcedata_set.get().pulsewidth_set.get().pulse_width

        try:
            event.irradeventxraysourcedata_set.get().exposure_set.get()
        except ObjectDoesNotExist:
            exposure = u''
        else:
            exposure = event.irradeventxraysourcedata_set.get().exposure_set.get().exposure

        try:
            event.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
        except ObjectDoesNotExist:
            distance_source_to_detector = u''
            distance_source_to_isocenter = u''
            table_longitudinal_position = u''
            table_lateral_position = u''
            table_height_position = u''
        else:
            distance_source_to_detector = event.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().distance_source_to_detector
            distance_source_to_isocenter = event.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().distance_source_to_isocenter
            table_longitudinal_position = event.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().table_longitudinal_position
            table_lateral_position = event.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().table_lateral_position
            table_height_position = event.irradeventxraymechanicaldata_set.get(
            ).doserelateddistancemeasurements_set.get().table_height_position

        acquisition_protocol = export_csv_prep(return_for_export(event, 'acquisition_protocol'))

        data = [
            u'Anon',
            patient_sex,
            study.study_instance_uid,
            u'',
            event.acquisition_plane,
            event.date_time_started,
            event.irradiation_event_type,
            acquisition_protocol,
            reference_point_definition,
            event.irradiation_event_uid,
            event.dose_area_product,
            dose_rp,
            positioner_primary_angle,
            positioner_secondary_angle,
            positioner_primary_end_angle,
            positioner_secondary_end_angle,
            column_angulation,
            xray_filter_type,
            xray_filter_material,
            xray_filter_thickness_minimum,
            xray_filter_thickness_maximum,
            fluoro_mode,
            pulse_rate,
            number_of_pulses,
            kvp,
            xray_tube_current,
            exposure_time,
            pulse_width,
            exposure,
            focal_spot_size,
            irradiation_duration,
            average_xray_tube_current,
            distance_source_to_detector,
            distance_source_to_isocenter,
            table_longitudinal_position,
            table_lateral_position,
            table_height_position,
            event.target_region,
            export_csv_prep(event.comment),
        ]
        writer.writerow(data)
        tsk.progress = u"{0} of {1}".format(i, numevents)
        tsk.save()
    tsk.progress = u'All study data written.'
    tsk.save()

    csvfilename = u"OpenSkinExport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    write_export(tsk, csvfilename, tmpfile, datestamp)
