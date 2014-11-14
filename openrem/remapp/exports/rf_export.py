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

import csv
from xlsxwriter.workbook import Workbook
from celery import shared_task
from django.conf import settings


@shared_task
def rfcsv(filterdict):
    """Export filtered RF database data to a single-sheet CSV file.

    :param request: Query parameters from the RF filtered page URL.
    :type request: HTTP get
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import General_study_module_attributes
    from remapp.models import Exports
    from remapp.interface.mod_filters import RFSummaryListFilter

    tsk = Exports.objects.create()

    tsk.task_id = exportRF2csv.request.id
    tsk.modality = "RF"
    tsk.export_type = "CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = 'Query filters imported, task started'
    tsk.status = 'CURRENT'
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
    e = General_study_module_attributes.objects.filter(modality_type__exact = 'RF')

    f = RFSummaryListFilter.base_filters

    for filt in f:
        if filt in filterdict and filterdict[filt]:
            # One Windows user found filterdict[filt] was a list. See https://bitbucket.org/openrem/openrem/issue/123/
            if isinstance(filterdict[filt], basestring):
                filterstring = filterdict[filt]
            else:
                filterstring = (filterdict[filt])[0]
            if filterstring != '':
                e = e.filter(**{f[filt].name + '__' + f[filt].lookup_type : filterstring})

    tsk.progress = 'Required study filter complete.'
    tsk.save()
        
    numresults = e.count()

    tsk.progress = '{0} studies in query.'.format(numresults)
    tsk.num_records = numresults
    tsk.save()

    headers = [
        'Institution name', 
        'Manufacturer', 
        'Model name',
        'Station name',
        'Accession number',
        'Operator',
        'Study date',
        'Patient age', 
        'Patient height', 
        'Patient mass (kg)', 
        'Study description',
        'Requested procedure',
        'Number of events',
        'DAP total (Gy.m^2)',
    ]

    from django.db.models import Max
    max_events = e.aggregate(Max('projection_xray_radiation_dose__accumulated_xray_dose__accumulated_projection_xray_dose__total_number_of_radiographic_frames'))
    for h in xrange(max_events['projection_xray_radiation_dose__accumulated_xray_dose__accumulated_projection_xray_dose__total_number_of_radiographic_frames__max']):
        headers += [
            'E' + str(h+1) + ' Protocol',
            'E' + str(h+1) + ' Image view',
            'E' + str(h+1) + ' Exposure control mode',
            'E' + str(h+1) + ' kVp',
            'E' + str(h+1) + ' mA',
            'E' + str(h+1) + ' Exposure time (ms)',
            'E' + str(h+1) + ' Exposure index',
            'E' + str(h+1) + ' Relative x-ray exposure',
            'E' + str(h+1) + ' DAP (Gy.m^2)',
        ]
    writer.writerow(headers)

    tsk.progress = 'CSV header row written.'
    tsk.save()

    for i, exams in enumerate(e):
        examdata = [
            exams.general_equipment_module_attributes_set.get().institution_name,
            exams.general_equipment_module_attributes_set.get().manufacturer,
            exams.general_equipment_module_attributes_set.get().manufacturer_model_name,
            exams.general_equipment_module_attributes_set.get().station_name,
            exams.accession_number,
            exams.operator_name,
            exams.study_date,
            exams.patient_study_module_attributes_set.get().patient_age_decimal,
            exams.patient_study_module_attributes_set.get().patient_size,
            exams.patient_study_module_attributes_set.get().patient_weight,
            exams.study_description,
            exams.requested_procedure_code_meaning,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().total_number_of_radiographic_frames,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().dose_area_product_total,
            ]

        for s in exams.projection_xray_radiation_dose_set.get().irradiation_event_xray_data_set.all():
            examdata += [
                s.acquisition_protocol,
                s.image_view,
                s.irradiation_event_xray_source_data_set.get().exposure_control_mode,
                s.irradiation_event_xray_source_data_set.get().kvp_set.get().kvp,
                s.irradiation_event_xray_source_data_set.get().average_xray_tube_current,
                s.irradiation_event_xray_source_data_set.get().exposure_time,
                s.irradiation_event_xray_detector_data_set.get().exposure_index,
                s.irradiation_event_xray_detector_data_set.get().relative_xray_exposure,
                s.dose_area_product,
                ]

        writer.writerow(examdata)
        tsk.progress = "{0} of {1}".format(i+1, numresults)
        tsk.save()
    tsk.progress = 'All study data written.'
    tsk.save()

    csvfilename = "dxexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

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
            sheetlist[tabtext]['sheet'].set_column('G:G', 10) # Date column
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


def _rf_common_get_data(source):
    examdata = [
        source.general_equipment_module_attributes_set.get().institution_name,
        source.general_equipment_module_attributes_set.get().manufacturer,
        source.general_equipment_module_attributes_set.get().manufacturer_model_name,
        source.general_equipment_module_attributes_set.get().station_name,
        source.accession_number,
        source.operator_name,
        source.performing_physician_name,
        source.study_date,  # Is a date - cell needs formatting
        str(source.patient_study_module_attributes_set.get().patient_age_decimal),
        str(source.patient_study_module_attributes_set.get().patient_size),
        str(source.patient_study_module_attributes_set.get().patient_weight),
        source.patient_module_attributes_set.get().not_patient_indicator,
        source.study_description,
        source.requested_procedure_code_meaning,
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().dose_area_product_total),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().dose_rp_total),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().fluoro_dose_area_product_total),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().fluoro_dose_rp_total),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().total_fluoro_time),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().acquisition_dose_area_product_total),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().acquisition_dose_rp_total),
        str(source.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().total_acquisition_time),
        str(source.projection_xray_radiation_dose_set.get().irradiation_event_xray_data_set.all().count()),
    ]
    return examdata

def _rf_common_headers():
    commonheaders = [
        'Institution',
        'Manufacturer',
        'Model name',
        'Station name',
        'Accession number',
        'Operator',
        'Physician',
        'Study date',
        'Patient age',
        'Patient height',
        'Patient mass (kg)',
        'Test patient?',
        'Study description',
        'Requested procedure',
        'DAP total (Gy.m^2)',
        'Dose RP total',
        'Fluoro DAP total',
        'Fluoro dose RP total',
        'Fluoro time total',
        'Acquisition DAP total',
        'Acquisition dose RP total',
        'Acquisition time total',
        'Number of events',
        ]
    return commonheaders


@shared_task
def rfxlsx(filterdict):
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
    from remapp.models import General_study_module_attributes, Irradiation_event_xray_data
    from remapp.models import Exports
    from remapp.interface.mod_filters import RFSummaryListFilter

    tsk = Exports.objects.create()

    tsk.task_id = rfxlsx.request.id
    tsk.modality = "RF"
    tsk.export_type = "XLSX export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = 'Query filters imported, task started'
    tsk.status = 'CURRENT'
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
    e = General_study_module_attributes.objects.filter(modality_type__exact = 'RF')

    f = RFSummaryListFilter.base_filters

    for filt in f:
        if filt in filterdict and filterdict[filt]:
            # One Windows user found filterdict[filt] was a list. See https://bitbucket.org/openrem/openrem/issue/123/
            if isinstance(filterdict[filt], basestring):
                filterstring = filterdict[filt]
            else:
                filterstring = (filterdict[filt])[0]
            if filterstring != '':
                e = e.filter(**{f[filt].name + '__' + f[filt].lookup_type : filterstring})
    
    tsk.progress = 'Required study filter complete.'
    tsk.num_records = e.count()
    tsk.save()

    # Add summary sheet and all data sheet
    summarysheet = book.add_worksheet("Summary")
    wsalldata = book.add_worksheet('All data')       
    wsalldata.set_column('G:G', 10) # allow date to be displayed.

    ##################
    # All data sheet

    num_groups_max = 0
    for row,exams in enumerate(e):

        tsk.progress = 'Writing study {0} of {1} to All data sheet'.format(row + 1, e.count())
        tsk.save()

        examdata = _rf_common_get_data(exams)

        angle_range = 5.0 #plus or minus range considered to be the same position
        studyiuid = exams.study_instance_uid
        inst = Irradiation_event_xray_data.objects.filter(projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__exact=studyiuid)

        num_groups_this_exam = 0
        while inst:
            num_groups_this_exam += 1
            anglei = _get_db_value(_get_db_value(inst[0], "irradiation_event_xray_mechanical_data_set").get(), "positioner_primary_angle")
            angleii = _get_db_value(_get_db_value(inst[0], "irradiation_event_xray_mechanical_data_set").get(), "positioner_secondary_angle")
            protocol = _get_db_value(inst[0], "acquisition_protocol")
            pulse_rate = _get_db_value(_get_db_value(inst[0], "irradiation_event_xray_source_data_set").get(), "pulse_rate")
            event_type = _get_db_value(_get_db_value(inst[0], "irradiation_event_type"), "code_meaning")
            filter_material = _get_db_value(_get_db_value(_get_db_value(_get_db_value(inst[0], "irradiation_event_xray_source_data_set").get(), "xray_filters_set").get(), "xray_filter_material"), "code_meaning")
            filter_thick = _get_db_value(_get_db_value(_get_db_value(inst[0], "irradiation_event_xray_source_data_set").get(), "xray_filters_set").get(), "xray_filter_thickness_maximum")
            fieldsize = _get_db_value(_get_db_value(inst[0], "irradiation_event_xray_source_data_set").get(), "ii_field_size")

            similarexposures = inst
            if anglei:
                similarexposures = similarexposures.filter(
                    irradiation_event_xray_mechanical_data__positioner_primary_angle__range=(float(anglei) - angle_range, float(anglei) + angle_range))
            if angleii:
                similarexposures = similarexposures.filter(
                    irradiation_event_xray_mechanical_data__positioner_secondary_angle__range=(float(angleii) - angle_range, float(angleii) + angle_range))
            if protocol:
                similarexposures = similarexposures.filter(
                    acquisition_protocol__exact = protocol)
            if fieldsize:
                similarexposures = similarexposures.filter(
                    irradiation_event_xray_source_data__ii_field_size__exact = fieldsize)
            if pulse_rate:
                similarexposures = similarexposures.filter(
                    irradiation_event_xray_source_data__pulse_rate__exact = pulse_rate)
            if filter_material:
                similarexposures = similarexposures.filter(
                    irradiation_event_xray_source_data__xray_filters__xray_filter_material__code_meaning__exact = filter_material)
            if filter_thick:
                similarexposures = similarexposures.filter(
                    irradiation_event_xray_source_data__xray_filters__xray_filter_thickness_maximum__exact = filter_thick)
            if event_type:
                similarexposures = similarexposures.filter(
                    irradiation_event_type__code_meaning__exact = event_type)

            # Remove exposures included in this group from inst
            exposures_to_exclude = [o.irradiation_event_uid for o in similarexposures]
            inst = inst.exclude(irradiation_event_uid__in = exposures_to_exclude)

            angle1 = similarexposures.all().aggregate(
                Min('irradiation_event_xray_mechanical_data__positioner_primary_angle'),
                Max('irradiation_event_xray_mechanical_data__positioner_primary_angle'),
                Avg('irradiation_event_xray_mechanical_data__positioner_primary_angle'))
            angle2 = similarexposures.all().aggregate(
                Min('irradiation_event_xray_mechanical_data__positioner_secondary_angle'),
                Max('irradiation_event_xray_mechanical_data__positioner_secondary_angle'),
                Avg('irradiation_event_xray_mechanical_data__positioner_secondary_angle'))
            dap = similarexposures.all().aggregate(
                Min('dose_area_product'),
                Max('dose_area_product'),
                Avg('dose_area_product'))
            dose_rp = similarexposures.all().aggregate(
                Min('irradiation_event_xray_source_data__dose_rp'),
                Max('irradiation_event_xray_source_data__dose_rp'),
                Avg('irradiation_event_xray_source_data__dose_rp'))
            kvp = similarexposures.all().aggregate(
                Min('irradiation_event_xray_source_data__kvp__kvp'),
                Max('irradiation_event_xray_source_data__kvp__kvp'),
                Avg('irradiation_event_xray_source_data__kvp__kvp'))
            tube_current = similarexposures.all().aggregate(
                Min('irradiation_event_xray_source_data__xray_tube_current__xray_tube_current'),
                Max('irradiation_event_xray_source_data__xray_tube_current__xray_tube_current'),
                Avg('irradiation_event_xray_source_data__xray_tube_current__xray_tube_current'))
            exp_time = similarexposures.all().aggregate(
                Min('irradiation_event_xray_source_data__exposure_time'),
                Max('irradiation_event_xray_source_data__exposure_time'),
                Avg('irradiation_event_xray_source_data__exposure_time'))
            pulse_width = similarexposures.all().aggregate(
                Min('irradiation_event_xray_source_data__pulse_width__pulse_width'),
                Max('irradiation_event_xray_source_data__pulse_width__pulse_width'),
                Avg('irradiation_event_xray_source_data__pulse_width__pulse_width'))

            examdata += [
                event_type,
                protocol,
                str(similarexposures.count()),
                str(pulse_rate),
                str(fieldsize),
                filter_material,
                str(filter_thick),
                str(kvp['irradiation_event_xray_source_data__kvp__kvp__min']),
                str(kvp['irradiation_event_xray_source_data__kvp__kvp__max']),
                str(kvp['irradiation_event_xray_source_data__kvp__kvp__avg']),
                str(tube_current['irradiation_event_xray_source_data__xray_tube_current__xray_tube_current__min']),
                str(tube_current['irradiation_event_xray_source_data__xray_tube_current__xray_tube_current__max']),
                str(tube_current['irradiation_event_xray_source_data__xray_tube_current__xray_tube_current__avg']),
                str(pulse_width['irradiation_event_xray_source_data__pulse_width__pulse_width__min']),
                str(pulse_width['irradiation_event_xray_source_data__pulse_width__pulse_width__max']),
                str(pulse_width['irradiation_event_xray_source_data__pulse_width__pulse_width__avg']),
                str(exp_time['irradiation_event_xray_source_data__exposure_time__min']),
                str(exp_time['irradiation_event_xray_source_data__exposure_time__max']),
                str(exp_time['irradiation_event_xray_source_data__exposure_time__avg']),
                str(dap['dose_area_product__min']),
                str(dap['dose_area_product__max']),
                str(dap['dose_area_product__avg']),
                str(dose_rp['irradiation_event_xray_source_data__dose_rp__min']),
                str(dose_rp['irradiation_event_xray_source_data__dose_rp__max']),
                str(dose_rp['irradiation_event_xray_source_data__dose_rp__avg']),
                str(angle1['irradiation_event_xray_mechanical_data__positioner_primary_angle__min']),
                str(angle1['irradiation_event_xray_mechanical_data__positioner_primary_angle__max']),
                str(angle1['irradiation_event_xray_mechanical_data__positioner_primary_angle__avg']),
                str(angle2['irradiation_event_xray_mechanical_data__positioner_secondary_angle__min']),
                str(angle2['irradiation_event_xray_mechanical_data__positioner_secondary_angle__max']),
                str(angle2['irradiation_event_xray_mechanical_data__positioner_secondary_angle__avg']),
            ]

        if num_groups_this_exam > num_groups_max:
            num_groups_max = num_groups_this_exam

        wsalldata.write_row(row+1,0, examdata)

    tsk.progress = 'Generating headers for the all data sheet...'
    tsk.save()

    alldataheaders = _rf_common_headers()

    for h in xrange(num_groups_max):
        alldataheaders += [
            'G' + str(h+1) + ' Type',
            'G' + str(h+1) + ' Protocol',
            'G' + str(h+1) + ' No. exposures',
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
    numcolumns = (31 * num_groups_max + 23 - 1)
    numrows = e.count()
    wsalldata.autofilter(0,0,numrows,numcolumns)

        
    # Generate list of protocols in queryset and create worksheets for each
    tsk.progress = 'Generating list of protocols in the dataset...'
    tsk.save()

    protocolslist = []
    for exams in e:
        for s in exams.projection_xray_radiation_dose_set.get().irradiation_event_xray_data_set.all():
            if s.acquisition_protocol:
                safeprotocol = s.acquisition_protocol
            else:
                safeprotocol = u'Unknown'
            if safeprotocol not in protocolslist:
                protocolslist.append(safeprotocol)
    protocolslist.sort()

    tsk.progress = 'Creating an Excel safe version of protocol names and creating a worksheet for each...'
    tsk.save()

    protocolheaders = _rf_common_headers() + [
        'Time',
        'Type',
        'Protocol',
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
            p_events = Irradiation_event_xray_data.objects.filter(
                acquisition_protocol__exact = protocol
            ).filter(
                projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__in = expInclude
            )
            for event in p_events:
                sheetlist[tab]['count'] += 1
                examdata = _rf_common_get_data(event.projection_xray_radiation_dose.general_study_module_attributes)
                if event.irradiation_event_xray_source_data_set.get().xray_filters_set.get().xray_filter_material:
                    filter_material = event.irradiation_event_xray_source_data_set.get().xray_filters_set.get().xray_filter_material.code_meaning
                else: filter_material = None
                examdata += [
                    str(event.date_time_started),
                    event.irradiation_event_type.code_meaning,
                    event.acquisition_protocol,
                    str(event.irradiation_event_xray_source_data_set.get().pulse_rate),
                    str(event.irradiation_event_xray_source_data_set.get().ii_field_size),
                    filter_material,
                    str(event.irradiation_event_xray_source_data_set.get().xray_filters_set.get().xray_filter_thickness_maximum),
                    str(event.irradiation_event_xray_source_data_set.get().kvp_set.get().kvp),
                    str(event.irradiation_event_xray_source_data_set.get().xray_tube_current_set.get().xray_tube_current),
                    str(event.irradiation_event_xray_source_data_set.get().pulse_width_set.get().pulse_width),
                    str(event.irradiation_event_xray_source_data_set.get().exposure_time),
                    str(event.convert_gym2_to_cgycm2()),
                    str(event.irradiation_event_xray_source_data_set.get().dose_rp),
                    str(event.irradiation_event_xray_mechanical_data_set.get().positioner_primary_angle),
                    str(event.irradiation_event_xray_mechanical_data_set.get().positioner_secondary_angle),
                ]
                sheetlist[tab]['sheet'].write_row(sheetlist[tab]['count'],0,examdata)
        tabcolumns = (37)
        tabrows = sheetlist[tab]['count']
        sheetlist[tab]['sheet'].autofilter(0,0,tabrows,tabcolumns)

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
    linetwostring = 'OpenREM is copyright 2014 The Royal Marsden NHS Foundation Trust, and available under the GPL. See http://openrem.org'
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

    xlsxfilename = "dxexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

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