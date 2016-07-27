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
import csv
from xlsxwriter.workbook import Workbook
from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from remapp.tools.get_values import return_for_export

logger = logging.getLogger(__name__)


def _create_sheets(book, protocolslist, protocolheaders):
    """
    Creates sheets from sanitised versions of the protocol names

    :rtype : dict
    :param protocolslist: List of protocols
    :return:sheetlist - Dictionary of sheet names and a list of the protocol names that they correspond to
    """
    sheetlist = {}
    for protocol in protocolslist:
        tabtext = protocol.lower().replace(" ","_")
        translation_table = {ord('['):ord('('), ord(']'):ord(')'), ord(':'):ord(';'), ord('*'):ord('#'), ord('?'):ord(';'), ord('/'):ord('|'), ord('\\'):ord('|')}
        tabtext = tabtext.translate(translation_table) # remove illegal characters
        tabtext = tabtext[:31]
        if tabtext not in sheetlist:
            sheetlist[tabtext] = {
                'sheet': book.add_worksheet(tabtext),
                'count':0,
                'protocolname':[protocol]}
            sheetlist[tabtext]['sheet'].write_row(0,0,protocolheaders)
        else:
            if protocol not in sheetlist[tabtext]['protocolname']:
                sheetlist[tabtext]['protocolname'].append(protocol)
    return sheetlist


def _get_db_value(qs, location):
    """Get value from database, testing to see if it exists
    
    :rtype : attribute or queryset
    """
    try:
        v = getattr(qs, location)
        return v
    except:
        pass


def _get_accumulated_data(accumXrayDose):
    from django.core.exceptions import ObjectDoesNotExist
    from remapp.tools.get_values import return_for_export
    accum = {}
    accum['plane'] = accumXrayDose.acquisition_plane.code_meaning
    try:
        accum['dose_area_product_total'] = return_for_export(accumXrayDose.accumintegratedprojradiogdose_set.get(), 'dose_area_product_total')
        accum['dose_rp_total'] = return_for_export(accumXrayDose.accumintegratedprojradiogdose_set.get(), 'dose_rp_total')
        accum['reference_point_definition'] = return_for_export(accumXrayDose.accumintegratedprojradiogdose_set.get(), 'reference_point_definition_code')
        if not accum['reference_point_definition']:
            accum['reference_point_definition'] = return_for_export(accumXrayDose.accumintegratedprojradiogdose_set.get(), 'reference_point_definition')
    except ObjectDoesNotExist:
        accum['dose_area_product_total'] = None
        accum['dose_rp_total'] = None
        accum['reference_point_definition_code'] = None
    try:
        accum['fluoro_dose_area_product_total'] = return_for_export(accumXrayDose.accumprojxraydose_set.get(), 'fluoro_dose_area_product_total')
        accum['fluoro_dose_rp_total'] = return_for_export(accumXrayDose.accumprojxraydose_set.get(), 'fluoro_dose_rp_total')
        accum['total_fluoro_time'] = return_for_export(accumXrayDose.accumprojxraydose_set.get(), 'total_fluoro_time')
        accum['acquisition_dose_area_product_total'] = return_for_export(accumXrayDose.accumprojxraydose_set.get(), 'acquisition_dose_area_product_total')
        accum['acquisition_dose_rp_total'] = return_for_export(accumXrayDose.accumprojxraydose_set.get(), 'acquisition_dose_rp_total')
        accum['total_acquisition_time'] = return_for_export(accumXrayDose.accumprojxraydose_set.get(), 'total_acquisition_time')
    except ObjectDoesNotExist:
        accum['fluoro_dose_area_product_total'] = None
        accum['fluoro_dose_rp_total'] = None
        accum['total_fluoro_time'] = None
        accum['acquisition_dose_area_product_total'] = None
        accum['acquisition_dose_rp_total'] = None
        accum['total_acquisition_time'] = None

    try:
        accumXrayDose.projection_xray_radiation_dose.irradeventxraydata_set.all()
    except ObjectDoesNotExist:
        accum['eventcount'] = None
    else:
        accum['eventcount'] = str(accumXrayDose.projection_xray_radiation_dose.irradeventxraydata_set.filter(acquisition_plane__code_meaning__exact = accum['plane']).count())

    return accum


def _rf_common_get_data(source, pid=None, name=None, patid=None):
    if pid and (name or patid):
        try:
            source.patientmoduleattr_set.get()
        except ObjectDoesNotExist:
            patient_birth_date = None
            if name:
                patient_name = None
            if patid:
                patient_id = None
        else:
            patient_birth_date = return_for_export(source.patientmoduleattr_set.get(), 'patient_birth_date')
            if name:
                patient_name = return_for_export(source.patientmoduleattr_set.get(), 'patient_name')
            if patid:
                patient_id = return_for_export(source.patientmoduleattr_set.get(), 'patient_id')
    try:
        source.generalequipmentmoduleattr_set.get()
    except ObjectDoesNotExist:
        institution_name = None
        manufacturer = None
        manufacturer_model_name = None
        station_name = None
        display_name = None
    else:
        institution_name = return_for_export(source.generalequipmentmoduleattr_set.get(), 'institution_name')
        manufacturer = return_for_export(source.generalequipmentmoduleattr_set.get(), 'manufacturer')
        manufacturer_model_name = return_for_export(source.generalequipmentmoduleattr_set.get(), 'manufacturer_model_name')
        station_name = return_for_export(source.generalequipmentmoduleattr_set.get(), 'station_name')
        display_name = return_for_export(source.generalequipmentmoduleattr_set.get().unique_equipment_name, 'display_name')

    try:
        source.patientmoduleattr_set.get()
    except ObjectDoesNotExist:
        patient_sex = None
        not_patient_indicator = None
    else:
        patient_sex = return_for_export(source.patientmoduleattr_set.get(), 'patient_sex')
        not_patient_indicator = return_for_export(source.patientmoduleattr_set.get(), 'not_patient_indicator')

    try:
        source.patientstudymoduleattr_set.get()
    except ObjectDoesNotExist:
        patient_age_decimal = None
        patient_size = None
        patient_weight = None
    else:
        patient_age_decimal = return_for_export(source.patientstudymoduleattr_set.get(), 'patient_age_decimal')
        patient_size = return_for_export(source.patientstudymoduleattr_set.get(), 'patient_size')
        patient_weight = return_for_export(source.patientstudymoduleattr_set.get(), 'patient_weight')

    try:
        source.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()
    except ObjectDoesNotExist:
        eventcount = None
    else:
        eventcount = str(source.projectionxrayradiationdose_set.get().irradeventxraydata_set.all().count())

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
        return_for_export(source, 'accession_number'),
        return_for_export(source, 'operator_name'),
        return_for_export(source, 'performing_physician_name'),
        source.study_date,  # Is a date - needs to be a datetime object for formatting
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
        return_for_export(source, 'study_description'),
        return_for_export(source, 'requested_procedure_code_meaning'),
    ]
    for plane in source.projectionxrayradiationdose_set.get().accumxraydose_set.all():
        accum = _get_accumulated_data(plane)
        examdata += [
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
            examdata += [
                '','','','','','','','',''
            ]

    return examdata


def _rf_common_headers(pid=None, name=None, patid=None):
    pidheadings = []
    if pid and name:
        pidheadings += ['Patient name']
    if pid and patid:
        pidheadings += ['Patient ID']
    commonheaders = pidheadings + [
        'Institution',
        'Manufacturer',
        'Model name',
        'Station name',
        'Display name',
        'Accession number',
        'Operator',
        'Physician',
        'Study date',
    ]
    if pid and (name or patid):
        commonheaders += [
            'Date of birth',
        ]
    commonheaders += [
        'Patient age',
        'Patient sex',
        'Patient height',
        'Patient mass (kg)',
        'Test patient?',
        'Study description',
        'Requested procedure',
        'A DAP total (Gy.m^2)',
        'A Dose RP total',
        'A Fluoro DAP total',
        'A Fluoro dose RP total',
        'A Fluoro time total',
        'A Acquisition DAP total',
        'A Acquisition dose RP total',
        'A Acquisition time total',
        'A Number of events',
        'B DAP total (Gy.m^2)',
        'B Dose RP total',
        'B Fluoro DAP total',
        'B Fluoro dose RP total',
        'B Fluoro time total',
        'B Acquisition DAP total',
        'B Acquisition dose RP total',
        'B Acquisition time total',
        'B Number of events',
    ]
    return commonheaders


@shared_task
def rfxlsx(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered RF database data to multi-sheet Microsoft XSLX files.

    :param filterdict: Query parameters from the RF filtered page URL.
    :type filterdict: HTTP get

    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from django.db.models import Max, Min, Avg
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr, IrradEventXRayData
    from remapp.models import Exports
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid

    tsk = Exports.objects.create()

    tsk.task_id = rfxlsx.request.id
    tsk.modality = "RF"
    tsk.export_type = "XLSX export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = 'Query filters imported, task started'
    tsk.status = 'CURRENT'
    if pid and (name or patid):
        tsk.includes_pid = True
    else:
        tsk.includes_pid = False
    tsk.export_user_id = user
    tsk.save()

    try:
        tmpxlsx = TemporaryFile()
        book = Workbook(tmpxlsx, {'default_date_format': 'dd/mm/yyyy',
                                 'strings_to_numbers':  True})
        tsk.progress = 'Workbook created'
        tsk.save()
    except:
        messages.error(request, "Unexpected error creating temporary file - please contact an administrator: {0}".format(sys.exc_info()[0]))
        return redirect('/openrem/export/')

    # Get the data
    if pid:
        df_filtered_qs = RFFilterPlusPid(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'RF'))
    else:
        df_filtered_qs = RFSummaryListFilter(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'RF'))
    e = df_filtered_qs.qs
    
    tsk.progress = 'Required study filter complete.'
    tsk.num_records = e.count()
    tsk.save()

    # Add summary sheet and all data sheet
    summarysheet = book.add_worksheet("Summary")
    wsalldata = book.add_worksheet('All data')
    date_column = 8
    if pid and name:
        date_column += 1
    if pid and patid:
        date_column += 1
    wsalldata.set_column(date_column, date_column, 10) # allow date to be displayed.
    if pid and (name or patid):
        wsalldata.set_column(date_column+1, date_column+1, 10) # Date of birth column, exported if either pid option is chosen

    ##################
    # All data sheet

    num_groups_max = 0
    for row,exams in enumerate(e):

        tsk.progress = 'Writing study {0} of {1} to All data sheet'.format(row + 1, e.count())
        tsk.save()

        examdata = _rf_common_get_data(exams, pid, name, patid)

        angle_range = 5.0 #plus or minus range considered to be the same position
        studyiuid = exams.study_instance_uid
        inst = IrradEventXRayData.objects.filter(projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__exact=studyiuid)

        num_groups_this_exam = 0
        while inst:  # ie while there are events still left that haven't been matched into a group
            num_groups_this_exam += 1
            plane = _get_db_value(_get_db_value(inst[0], "acquisition_plane"), "code_meaning")
            try:
                inst[0].irradeventxraymechanicaldata_set.get()
            except ObjectDoesNotExist:
                anglei = None
                angleii = None
            else:
                anglei = _get_db_value(_get_db_value(inst[0], "irradeventxraymechanicaldata_set").get(), "positioner_primary_angle")
                angleii = _get_db_value(_get_db_value(inst[0], "irradeventxraymechanicaldata_set").get(), "positioner_secondary_angle")

            try:
                inst[0].irradeventxraysourcedata_set.get()
            except ObjectDoesNotExist:
                pulse_rate = None
                fieldsize = None
            else:
                pulse_rate = _get_db_value(_get_db_value(inst[0], "irradeventxraysourcedata_set").get(), "pulse_rate")
                fieldsize = _get_db_value(_get_db_value(inst[0], "irradeventxraysourcedata_set").get(), "ii_field_size")

            try:
                inst[0].irradeventxraysourcedata_set.get().xrayfilters_set.get()
            except ObjectDoesNotExist:
                filter_material = None
                filter_thick = None
            else:
                filter_material = _get_db_value(_get_db_value(_get_db_value(_get_db_value(inst[0], "irradeventxraysourcedata_set").get(), "xrayfilters_set").get(), "xray_filter_material"), "code_meaning")
                filter_thick = _get_db_value(_get_db_value(_get_db_value(inst[0], "irradeventxraysourcedata_set").get(), "xrayfilters_set").get(), "xray_filter_thickness_maximum")

            protocol = _get_db_value(inst[0], "acquisition_protocol")
            event_type = _get_db_value(_get_db_value(inst[0], "irradiation_event_type"), "code_meaning")

            similarexposures = inst
            if plane:
                similarexposures = similarexposures.filter(
                    acquisition_plane__code_meaning__exact = plane)
            if anglei:
                similarexposures = similarexposures.filter(
                    irradeventxraymechanicaldata__positioner_primary_angle__range=(float(anglei) - angle_range, float(anglei) + angle_range))
            if angleii:
                similarexposures = similarexposures.filter(
                    irradeventxraymechanicaldata__positioner_secondary_angle__range=(float(angleii) - angle_range, float(angleii) + angle_range))
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
                similarexposures = similarexposures.filter(
                    irradeventxraysourcedata__xrayfilters__xray_filter_material__code_meaning__exact = filter_material)
            if filter_thick:
                similarexposures = similarexposures.filter(
                    irradeventxraysourcedata__xrayfilters__xray_filter_thickness_maximum__exact = filter_thick)
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
                str(similarexposures.count()),
                str(plane),
                str(pulse_rate),
                str(fieldsize),
                filter_material,
                str(filter_thick),
                str(kvp['irradeventxraysourcedata__kvp__kvp__min']),
                str(kvp['irradeventxraysourcedata__kvp__kvp__max']),
                str(kvp['irradeventxraysourcedata__kvp__kvp__avg']),
                str(tube_current['irradeventxraysourcedata__xraytubecurrent__xray_tube_current__min']),
                str(tube_current['irradeventxraysourcedata__xraytubecurrent__xray_tube_current__max']),
                str(tube_current['irradeventxraysourcedata__xraytubecurrent__xray_tube_current__avg']),
                str(pulse_width['irradeventxraysourcedata__pulsewidth__pulse_width__min']),
                str(pulse_width['irradeventxraysourcedata__pulsewidth__pulse_width__max']),
                str(pulse_width['irradeventxraysourcedata__pulsewidth__pulse_width__avg']),
                str(exp_time['irradeventxraysourcedata__exposure_time__min']),
                str(exp_time['irradeventxraysourcedata__exposure_time__max']),
                str(exp_time['irradeventxraysourcedata__exposure_time__avg']),
                str(dap['dose_area_product__min']),
                str(dap['dose_area_product__max']),
                str(dap['dose_area_product__avg']),
                str(dose_rp['irradeventxraysourcedata__dose_rp__min']),
                str(dose_rp['irradeventxraysourcedata__dose_rp__max']),
                str(dose_rp['irradeventxraysourcedata__dose_rp__avg']),
                str(angle1['irradeventxraymechanicaldata__positioner_primary_angle__min']),
                str(angle1['irradeventxraymechanicaldata__positioner_primary_angle__max']),
                str(angle1['irradeventxraymechanicaldata__positioner_primary_angle__avg']),
                str(angle2['irradeventxraymechanicaldata__positioner_secondary_angle__min']),
                str(angle2['irradeventxraymechanicaldata__positioner_secondary_angle__max']),
                str(angle2['irradeventxraymechanicaldata__positioner_secondary_angle__avg']),
            ]

        if num_groups_this_exam > num_groups_max:
            num_groups_max = num_groups_this_exam

        wsalldata.write_row(row+1,0, examdata)

    tsk.progress = 'Generating headers for the all data sheet...'
    tsk.save()

    alldataheaders = _rf_common_headers(pid, name, patid)

    for h in xrange(num_groups_max):
        alldataheaders += [
            'G' + str(h+1) + ' Type',
            'G' + str(h+1) + ' Protocol',
            'G' + str(h+1) + ' No. exposures',
            'G' + str(h+1) + ' Plane',
            'G' + str(h+1) + ' Pulse rate',
            'G' + str(h+1) + ' Field size',
            'G' + str(h+1) + ' Filter material',
            'G' + str(h+1) + ' Filter thickness',
            'G' + str(h+1) + ' kVp min',
            'G' + str(h+1) + ' kVp max',
            'G' + str(h+1) + ' kVp mean',
            'G' + str(h+1) + ' mA min',
            'G' + str(h+1) + ' mA max',
            'G' + str(h+1) + ' mA mean',
            'G' + str(h+1) + ' pulse width min',
            'G' + str(h+1) + ' pulse width max',
            'G' + str(h+1) + ' pulse width mean',
            'G' + str(h+1) + ' Exp time min (ms)',
            'G' + str(h+1) + ' Exp time max (ms)',
            'G' + str(h+1) + ' Exp time mean (ms)',
            'G' + str(h+1) + ' DAP min (Gy.m^2)',
            'G' + str(h+1) + ' DAP max (Gy.m^2)',
            'G' + str(h+1) + ' DAP mean (Gy.m^2)',
            'G' + str(h+1) + ' Ref point dose min (Gy)',
            'G' + str(h+1) + ' Ref point dose max (Gy)',
            'G' + str(h+1) + ' Ref point dose mean (Gy)',
            'G' + str(h+1) + ' Primary angle min',
            'G' + str(h+1) + ' Primary angle max',
            'G' + str(h+1) + ' Primary angle mean',
            'G' + str(h+1) + ' Secondary angle min',
            'G' + str(h+1) + ' Secondary angle max',
            'G' + str(h+1) + ' Secondary angle mean',
            ]
    wsalldata.write_row('A1', alldataheaders)
    common_header_columns = 32
    if pid and name:
        common_header_columns += 1
    if pid and patid:
        common_header_columns += 1
    if pid and (name or patid):
        common_header_columns += 1
    numcolumns = (31 * (num_groups_max + 1) + common_header_columns)
    numrows = e.count()
    wsalldata.autofilter(0,0,numrows,numcolumns)

        
    # Generate list of protocols in queryset and create worksheets for each
    tsk.progress = 'Generating list of protocols in the dataset...'
    tsk.save()

    protocolslist = []
    for exams in e:
        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
            if s.acquisition_protocol:
                safeprotocol = s.acquisition_protocol
            else:
                safeprotocol = u'Unknown'
            if safeprotocol not in protocolslist:
                protocolslist.append(safeprotocol)
    protocolslist.sort()

    tsk.progress = 'Creating an Excel safe version of protocol names and creating a worksheet for each...'
    tsk.save()

    protocolheaders = _rf_common_headers(pid, name, patid) + [
        'Time',
        'Type',
        'Protocol',
        'Plane',
        'Pulse rate',
        'Field size',
        'Filter material',
        'Filter thickness',
        'kVp',
        'mA',
        'Pulse width',
        'Exposure time',
        'DAP (cGy.cm^2)',
        'Ref point dose (Gy)',
        'Primary angle',
        'Secondary angle',
    ]

    sheetlist = _create_sheets(book, protocolslist, protocolheaders)

    expInclude = [o.study_instance_uid for o in e]

    for tab in sheetlist:
        for protocol in sheetlist[tab]['protocolname']:
            tsk.progress = 'Populating the protocol sheet for protocol {0}'.format(protocol)
            tsk.save()
            p_events = IrradEventXRayData.objects.filter(
                acquisition_protocol__exact = protocol
            ).filter(
                projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__in = expInclude
            )
            for event in p_events:
                sheetlist[tab]['count'] += 1
                examdata = _rf_common_get_data(event.projection_xray_radiation_dose.general_study_module_attributes,
                                               pid, name, patid)
                if event.irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material:
                    filter_material = event.irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning
                else: filter_material = None
                examdata += [
                    str(event.date_time_started),
                    event.irradiation_event_type.code_meaning,
                    event.acquisition_protocol,
                    event.acquisition_plane.code_meaning,
                    str(event.irradeventxraysourcedata_set.get().pulse_rate),
                    str(event.irradeventxraysourcedata_set.get().ii_field_size),
                    filter_material,
                    str(event.irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_thickness_maximum),
                    str(event.irradeventxraysourcedata_set.get().kvp_set.get().kvp),
                    str(event.irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current),
                    str(event.irradeventxraysourcedata_set.get().pulsewidth_set.get().pulse_width),
                    str(event.irradeventxraysourcedata_set.get().exposure_time),
                    str(event.convert_gym2_to_cgycm2()),
                    str(event.irradeventxraysourcedata_set.get().dose_rp),
                    str(event.irradeventxraymechanicaldata_set.get().positioner_primary_angle),
                    str(event.irradeventxraymechanicaldata_set.get().positioner_secondary_angle),
                ]
                sheetlist[tab]['sheet'].write_row(sheetlist[tab]['count'],0,examdata)
        tabcolumns = 49
        if pid and name:
            tabcolumns += 1
        if pid and patid:
            tabcolumns += 1
        if pid and (name or patid):
            tabcolumns += 1
        tabrows = sheetlist[tab]['count']
        sheetlist[tab]['sheet'].autofilter(0,0,tabrows,tabcolumns)
        sheetlist[tab]['sheet'].set_column(date_column, date_column, 10) # allow date to be displayed.
        if pid and (name or patid):
            sheetlist[tab]['sheet'].set_column(date_column+1, date_column+1, 10) # DOB column

    # Populate summary sheet
    tsk.progress = 'Now populating the summary sheet...'
    tsk.save()

    import pkg_resources  # part of setuptools
    import datetime

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''

    version = vers
    titleformat = book.add_format()
    titleformat.set_font_size=(22)
    titleformat.set_font_color=('#FF0000')
    titleformat.set_bold()
    toplinestring = 'XLSX Export from OpenREM version {0} on {1}'.format(version, str(datetime.datetime.now()))
    linetwostring = 'OpenREM is copyright 2016 The Royal Marsden NHS Foundation Trust, and available under the GPL. See http://openrem.org'
    summarysheet.write(0,0, toplinestring, titleformat)
    summarysheet.write(1,0, linetwostring)

    # Number of exams
    summarysheet.write(3,0,"Total number of exams")
    summarysheet.write(3,1,e.count())

    # Generate list of Study Descriptions
    summarysheet.write(5,0,"Study Description")
    summarysheet.write(5,1,"Frequency")
    from django.db.models import Count
    study_descriptions = e.values("study_description").annotate(n=Count("pk"))
    for row, item in enumerate(study_descriptions.order_by('n').reverse()):
        summarysheet.write(row+6,0,item['study_description'])
        summarysheet.write(row+6,1,item['n'])
    summarysheet.set_column('A:A', 25)

    # Generate list of Requested Procedures
    summarysheet.write(5,3,"Requested Procedure")
    summarysheet.write(5,4,"Frequency")
    from django.db.models import Count
    requested_procedure = e.values("requested_procedure_code_meaning").annotate(n=Count("pk"))
    for row, item in enumerate(requested_procedure.order_by('n').reverse()):
        summarysheet.write(row+6,3,item['requested_procedure_code_meaning'])
        summarysheet.write(row+6,4,item['n'])
    summarysheet.set_column('D:D', 25)

    # Generate list of Series Protocols
    summarysheet.write(5,6,"Series Protocol")
    summarysheet.write(5,7,"Frequency")
    sortedprotocols = sorted(sheetlist.iteritems(), key=lambda (k,v): v['count'], reverse=True)
    for row, item in enumerate(sortedprotocols):
        summarysheet.write(row+6,6,', '.join(item[1]['protocolname'])) # Join as can't write a list to a single cell.
        summarysheet.write(row+6,7,item[1]['count'])
    summarysheet.set_column('G:G', 15)


    book.close()
    tsk.progress = 'XLSX book written.'
    tsk.save()

    xlsxfilename = "rfexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(xlsxfilename,File(tmpxlsx))
    except OSError as e:
        tsk.progress = "Errot saving export file - please contact an administrator. Error({0}): {1}".format(e.errno, e.strerror)
        tsk.status = 'ERROR'
        tsk.save()
        return
    except:
        tsk.progress = "Unexpected error saving export file - please contact an administrator: {0}".format(sys.exc_info()[0])
        tsk.status = 'ERROR'
        tsk.save()
        return

    tsk.status = 'COMPLETE'
    tsk.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    tsk.save()


@shared_task
def exportFL2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered fluoro database data to a single-sheet CSV file.

    :param request: Query parameters from the fluoro filtered page URL.
    :type request: HTTP get

    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid
    from remapp.tools.get_values import return_for_export, export_safe
    from django.core.exceptions import ObjectDoesNotExist

    tsk = Exports.objects.create()

    tsk.task_id = exportFL2excel.request.id
    tsk.modality = "RF"
    tsk.export_type = "CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = 'Query filters imported, task started'
    tsk.status = 'CURRENT'
    if pid and (name or patid):
        tsk.includes_pid = True
    else:
        tsk.includes_pid = False
    tsk.export_user_id = user
    tsk.save()

    try:
        tmpfile = TemporaryFile()
        writer = csv.writer(tmpfile)

        tsk.progress = 'CSV file created'
        tsk.save()
    except:
        messages.error(request, "Unexpected error creating temporary file - please contact an administrator: {0}".format(sys.exc_info()[0]))
        return redirect('/openrem/export/')

    # Get the data!

    if pid:
        df_filtered_qs = RFFilterPlusPid(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'RF'))
    else:
        df_filtered_qs = RFSummaryListFilter(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'RF'))
    e = df_filtered_qs.qs

    tsk.progress = 'Required study filter complete.'
    tsk.save()

    numresults = e.count()

    tsk.num_records = numresults
    tsk.save()

    headings = []
    if pid and name:
        headings += ['Patient name']
    if pid and patid:
        headings += ['Patient ID']
    headings += [
        'Manufacturer',
        'Model name',
        'Institution name',
        'Display name',
        'Accession number',
        'Study date',
    ]
    if pid and (name or patid):
        headings += [
            'Date of birth',
        ]
    headings += [
        'Patient age',
        'Patient sex',
        'Patient height',
        'Patient mass (kg)',
        'Not patient?',
        'Study description',
        'Physician',
        'Operator',
        'Number of events',
        'Plane',
        'DAP total (Gy.m2)',
        'RP dose total (Gy)',
        'Fluoro DAP total (Gy.m2)',
        'Fluoro RP dose total (Gy)',
        'Total fluoro time (ms)',
        'Acquisition DAP total (Gy.m2)',
        'Acquisition RP dose total (Gy)',
        'Total acquisition time (ms)',
        'RP definition',
        'Plane (if bi-plane)',
        'DAP total (Gy.m2)',
        'RP dose total (Gy)',
        'Fluoro DAP total (Gy.m2)',
        'Fluoro RP dose total (Gy)',
        'Total fluoro time (ms)',
        'Acquisition DAP total (Gy.m2)',
        'Acquisition RP dose total (Gy)',
        'Total acquisition time (ms)',
        'RP definition',
    ]
    writer.writerow(headings)
    for i, exams in enumerate(e):

        if pid and (name or patid):
            try:
                exams.patientmoduleattr_set.get()
            except ObjectDoesNotExist:
                patient_birth_date = None
                if name:
                    patient_name = None
                if patid:
                    patient_id = None
            else:
                patient_birth_date = return_for_export(exams.patientmoduleattr_set.get(), 'patient_birth_date')
                if name:
                    patient_name = export_safe(return_for_export(exams.patientmoduleattr_set.get(), 'patient_name'))
                if patid:
                    patient_id = export_safe(return_for_export(exams.patientmoduleattr_set.get(), 'patient_id'))

        try:
            exams.generalequipmentmoduleattr_set.get()
        except ObjectDoesNotExist:
            manufacturer = None
        else:
            manufacturer = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get(), 'manufacturer'))

        try:
            exams.projectionxrayradiationdose_set.get().observercontext_set.get()
        except ObjectDoesNotExist:
            device_observer_name = None
        else:
            device_observer_name = export_safe(return_for_export(exams.projectionxrayradiationdose_set.get().observercontext_set.get(), 'device_observer_name'))

        try:
            exams.generalequipmentmoduleattr_set.get()
        except ObjectDoesNotExist:
            institution_name = None
            display_name = None
        else:
            institution_name = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get(), 'institution_name'))
            display_name = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get().unique_equipment_name, 'display_name'))

        try:
            exams.patientmoduleattr_set.get()
        except ObjectDoesNotExist:
            patient_sex = None
            not_patient = None
        else:
            patient_sex = return_for_export(exams.patientmoduleattr_set.get(), 'patient_sex')
            not_patient = return_for_export(exams.patientmoduleattr_set.get(), 'not_patient_indicator')

        try:
            exams.patientstudymoduleattr_set.get()
        except ObjectDoesNotExist:
            patient_age_decimal = None
            patient_size = None
            patient_weight = None
        else:
            patient_age_decimal = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_age_decimal')
            patient_size = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_size')
            patient_weight = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_weight')

        try:
            exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.count()
        except ObjectDoesNotExist:
            count = None
        else:
            count = exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.count()

        row = []
        if pid and name:
            row += [patient_name]
        if pid and patid:
            row += [patient_id]
        row += [
            manufacturer,
            device_observer_name,
            institution_name,
            display_name,
            export_safe(exams.accession_number),
            exams.study_date,
        ]
        if pid and (name or patid):
            row += [
                patient_birth_date,
            ]
        row += [
            patient_age_decimal,
            patient_sex,
            patient_size,
            patient_weight,
            export_safe(not_patient),
            export_safe(exams.study_description),
            export_safe(exams.performing_physician_name),
            export_safe(exams.operator_name),
            count,
        ]

        for plane in exams.projectionxrayradiationdose_set.get().accumxraydose_set.all():
            accum = _get_accumulated_data(plane)
            row += [
                accum['plane'],
                accum['dose_area_product_total'],
                accum['dose_rp_total'],
                accum['fluoro_dose_area_product_total'],
                accum['fluoro_dose_rp_total'],
                accum['total_fluoro_time'],
                accum['acquisition_dose_area_product_total'],
                accum['acquisition_dose_rp_total'],
                accum['total_acquisition_time'],
                accum['reference_point_definition'],
            ]
        writer.writerow(row)
        tsk.progress = "{0} of {1}".format(i+1, numresults)
        tsk.save()


    tsk.progress = 'All study data written.'
    tsk.save()

    csvfilename = "rfexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(csvfilename,File(tmpfile))
    except OSError as e:
        tsk.progress = "Error saving export file - please contact an administrator. Error({0}): {1}".format(e.errno, e.strerror)
        tsk.status = 'ERROR'
        tsk.save()
        return
    except:
        tsk.progress = "Unexpected error saving export file - please contact an administrator: {0}".format(sys.exc_info()[0])
        tsk.status = 'ERROR'
        tsk.save()
        return


    tsk.status = 'COMPLETE'
    tsk.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    tsk.save()


@shared_task
def rfopenskin(studyid):
    """Export filtered RF database data to multi-sheet Microsoft XSLX files.

    :param studyid: RF study database ID.
    :type studyud: int

    """

    import sys, datetime
    from tempfile import TemporaryFile
    from django.contrib import messages
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.tools.get_values import export_safe

    tsk = Exports.objects.create()

    tsk.task_id = rfopenskin.request.id
    tsk.modality = "RF"
    tsk.export_type = "OpenSkin RF csv export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = 'Query filters imported, task started'
    tsk.status = 'CURRENT'
    tsk.save()

    try:
        tmpfile = TemporaryFile()
        writer = csv.writer(tmpfile)

        tsk.progress = 'CSV file created, starting to populate with events'
        tsk.save()
    except:
        messages.error(request, "Unexpected error creating temporary file - please contact an administrator: {0}".format(sys.exc_info()[0]))
        return redirect('/openrem/export/')

    # Get the data
    study = GeneralStudyModuleAttr.objects.get(pk=studyid)
    numevents = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.count()
    tsk.num_records = numevents
    tsk.save()

    for i, event in enumerate(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()):
        try:
            study.patientmoduleattr_set.get()
        except ObjectDoesNotExist:
            patient_sex = ''
        else:
            patient_sex = study.patientmoduleattr_set.get().patient_sex

        try:
            event.irradeventxraysourcedata_set.get()
        except ObjectDoesNotExist:
            reference_point_definition = ''
            dose_rp = ''
            fluoro_mode = ''
            pulse_rate = ''
            number_of_pulses = ''
            exposure_time = ''
            focal_spot_size = ''
            irradiation_duration = ''
            average_xray_tube_current = ''
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
            positioner_primary_angle = ''
            positioner_secondary_angle = ''
            positioner_primary_end_angle = ''
            positioner_secondary_end_angle = ''
            column_angulation = ''
        else:
            positioner_primary_angle = event.irradeventxraymechanicaldata_set.get().positioner_primary_angle
            positioner_secondary_angle = event.irradeventxraymechanicaldata_set.get().positioner_secondary_angle
            positioner_primary_end_angle = event.irradeventxraymechanicaldata_set.get().positioner_primary_end_angle
            positioner_secondary_end_angle = event.irradeventxraymechanicaldata_set.get().positioner_secondary_end_angle
            column_angulation = event.irradeventxraymechanicaldata_set.get().column_angulation

        try:
            for filter in event.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                try:
                    if "Copper" in filter.xray_filter_material.code_meaning:
                        xray_filter_type = filter.xray_filter_type
                        xray_filter_material = filter.xray_filter_material
                        xray_filter_thickness_minimum = filter.xray_filter_thickness_minimum
                        xray_filter_thickness_maximum = filter.xray_filter_thickness_maximum
                except AttributeError:
                        xray_filter_type = ''
                        xray_filter_material = ''
                        xray_filter_thickness_minimum = ''
                        xray_filter_thickness_maximum = ''
        except ObjectDoesNotExist:
            xray_filter_type = ''
            xray_filter_material = ''
            xray_filter_thickness_minimum = ''
            xray_filter_thickness_maximum = ''

        try:
            event.irradeventxraysourcedata_set.get().kvp_set.get()
        except ObjectDoesNotExist:
            kvp = ''
        else:
            kvp = event.irradeventxraysourcedata_set.get().kvp_set.get().kvp

        try:
            event.irradeventxraysourcedata_set.get().xraytubecurrent_set.get()
        except ObjectDoesNotExist:
            xray_tube_current = ''
        else:
            xray_tube_current = event.irradeventxraysourcedata_set.get().xraytubecurrent_set.get().xray_tube_current

        try:
            event.irradeventxraysourcedata_set.get().pulsewidth_set.get()
        except ObjectDoesNotExist:
            pulse_width = ''
        else:
            pulse_width = event.irradeventxraysourcedata_set.get().pulsewidth_set.get().pulse_width

        try:
            event.irradeventxraysourcedata_set.get().exposure_set.get()
        except ObjectDoesNotExist:
            exposure = ''
        else:
            exposure = event.irradeventxraysourcedata_set.get().exposure_set.get().exposure

        try:
            event.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
        except ObjectDoesNotExist:
            distance_source_to_detector = ''
            distance_source_to_isocenter = ''
            table_longitudinal_position = ''
            table_lateral_position = ''
            table_height_position = ''
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

        acquisition_protocol = export_safe(return_for_export(event, 'acquisition_protocol'))

        data = [
            'Anon',
            patient_sex,
            study.study_instance_uid,
            '',
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
            export_safe(event.comment),
        ]
        writer.writerow(data)
        tsk.progress = "{0} of {1}".format(i, numevents)
        tsk.save()
    tsk.progress = 'All study data written.'
    tsk.save()

    csvfilename = "OpenSkinExport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(csvfilename,File(tmpfile))
    except OSError as e:
        tsk.progress = "Error saving export file - please contact an administrator. Error({0}): {1}".format(e.errno, e.strerror)
        tsk.status = 'ERROR'
        tsk.save()
        return
    except:
        tsk.progress = "Unexpected error saving export file - please contact an administrator: {0}".format(sys.exc_info()[0])
        tsk.status = 'ERROR'
        tsk.save()
        return

    tsk.status = 'COMPLETE'
    tsk.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    tsk.save()

