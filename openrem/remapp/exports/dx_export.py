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

logger = logging.getLogger(__name__)


def _get_xray_filterinfo(source):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        filters = u''
        filter_thicknesses = u''
        for current_filter in source.xrayfilters_set.all():
            if 'Aluminum' in str(current_filter.xray_filter_material):
                filters += u'Al'
            elif 'Copper' in str(current_filter.xray_filter_material):
                filters += u'Cu'
            elif 'Tantalum' in str(current_filter.xray_filter_material):
                filters += u'Ta'
            elif 'Molybdenum' in str(current_filter.xray_filter_material):
                filters += u'Mo'
            elif 'Rhodium' in str(current_filter.xray_filter_material):
                filters += u'Rh'
            elif 'Silver' in str(current_filter.xray_filter_material):
                filters += u'Ag'
            elif 'Niobium' in str(current_filter.xray_filter_material):
                filters += u'Nb'
            elif 'Europium' in str(current_filter.xray_filter_material):
                filters += u'Eu'
            elif 'Lead' in str(current_filter.xray_filter_material):
                filters += u'Pb'
            else:
                filters += str(current_filter.xray_filter_material)
            filters += u' | '
            thicknesses = [current_filter.xray_filter_thickness_minimum,
                           current_filter.xray_filter_thickness_maximum]
            if thicknesses[0] is not None and thicknesses[1] is not None:
                thick = sum(thicknesses) / len(thicknesses)
            elif thicknesses[0] is None and thicknesses[1] is None:
                thick = ''
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


@shared_task
def exportDX2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered DX database data to a single-sheet CSV file.

    :param request: Query parameters from the DX filtered page URL.
    :type request: HTTP get
    
    """

    import datetime
    import sys
    from tempfile import TemporaryFile
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import Exports
    from remapp.interface.mod_filters import dx_acq_filter
    from django.core.exceptions import ObjectDoesNotExist

    tsk = Exports.objects.create()

    tsk.task_id = exportDX2excel.request.id
    tsk.modality = u"DX"
    tsk.export_type = u"CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = u'Query filters imported, task started'
    tsk.status = u'CURRENT'
    if pid and (name or patid):
        tsk.includes_pid = True
    else:
        tsk.includes_pid = False
    tsk.export_user_id = user
    tsk.save()

    try:
        tmpfile = TemporaryFile()
        writer = csv.writer(tmpfile, dialect=csv.excel)

        tsk.progress = u'CSV file created'
        tsk.save()
    except:
        # messages.error(request, "Unexpected error creating temporary file - please contact an administrator: {0}".format(sys.exc_info()[0]))
        return redirect('/openrem/export/')
        
    # Get the data!

    e = dx_acq_filter(filterdict, pid=pid).qs

    # Remove duplicate entries from the results - hopefully no longer necessary, left here in case. Needs testing
    # e = e.filter(projectionxrayradiationdose__general_study_module_attributes__study_instance_uid__isnull = False).distinct()

    tsk.progress = u'Required study filter complete.'
    tsk.save()
        
    numresults = e.count()

    tsk.progress = u'{0} studies in query.'.format(numresults)
    tsk.num_records = numresults
    tsk.save()

    pidheadings = []
    if pid and name:
        pidheadings += [u'Patient name']
    if pid and patid:
        pidheadings += [u'Patient ID']
    headers = pidheadings + [
        u'Institution name',
        u'Manufacturer',
        u'Model name',
        u'Station name',
        u'Display name',
        u'Accession number',
        u'Operator',
        u'Study date',
    ]
    if pid and (name or patid):
        headers += [
            u'Date of birth',
        ]
    headers += [
        u'Patient age',
        u'Patient sex',
        u'Patient height',
        u'Patient mass (kg)',
        u'Study description',
        u'Requested procedure',
        u'Number of events',
        u'DAP total (cGy.cm^2)',
    ]

    from django.db.models import Max
    max_events = e.aggregate(Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames'))

    for h in xrange(max_events['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames__max']):
        headers += [
            'E' + str(h+1) + u' Protocol',
            'E' + str(h+1) + u' Image view',
            'E' + str(h+1) + u' Exposure control mode',
            'E' + str(h+1) + u' kVp',
            'E' + str(h+1) + u' mAs',
            'E' + str(h+1) + u' mA',
            'E' + str(h+1) + u' Exposure time (ms)',
            'E' + str(h+1) + u' Filters',
            'E' + str(h+1) + u' Filter thicknesses average (mm)',
            'E' + str(h+1) + u' Exposure index',
            'E' + str(h+1) + u' Relative x-ray exposure',
            'E' + str(h+1) + u' DAP (cGy.cm^2)',
            ]

    writer.writerow([unicode(header).encode("utf-8") for header in headers])

    tsk.progress = u'CSV header row written.'
    tsk.save()

    for i, exams in enumerate(e):
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
            patient_age = exams.patientstudymoduleattr_set.get().patient_age_decimal
            patient_size = exams.patientstudymoduleattr_set.get().patient_size
            patient_weight = exams.patientstudymoduleattr_set.get().patient_weight
        except ObjectDoesNotExist:
            patient_age = None
            patient_size = None
            patient_weight = None
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
        ]
        if pid and (name or patid):
            examdata += [
                patient_birth_date,
            ]
        examdata += [
            patient_age,
            patient_sex,
            patient_size,
            patient_weight,
            exams.study_description,
            exams.requested_procedure_code_meaning,
            total_number_of_radiographic_frames,
            cgycm2,
        ]

        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):

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
                filters, filter_thicknesses = _get_xray_filterinfo(s.irradeventxraysourcedata_set.get())
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

            examdata += [
                s.acquisition_protocol,
                ]
            try:
                examdata += [
                s.image_view.code_meaning,
                ]
            except AttributeError:
                pass
            examdata += [
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
                ]

        for index, item in enumerate(examdata):
            if item is None:
                examdata[index] = ''
            if isinstance(item, basestring) and u',' in item:
                examdata[index] = item.replace(u',', u';')
        writer.writerow([unicode(datastring).encode("utf-8") for datastring in examdata])
        tsk.progress = u"{0} of {1}".format(i+1, numresults)
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

    :param filterdict: Query parameters from the DX and CR filtered page URL.
    :type filterdict: HTTP get
    
    """

    import datetime
    import sys
    from tempfile import TemporaryFile
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.exports.export_common import text_and_date_formats, common_headers, generate_sheets
    from remapp.models import Exports
    from remapp.interface.mod_filters import dx_acq_filter
    from remapp.tools.get_values import return_for_export, string_to_float
    from django.core.exceptions import ObjectDoesNotExist
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
    if pid and (name or patid):
        tsk.includes_pid = True
    else:
        tsk.includes_pid = False
    tsk.export_user_id = user
    tsk.save()

    try:
        tmpxlsx = TemporaryFile()
        book = Workbook(tmpxlsx, {'strings_to_numbers': False})
        tsk.progress = u'Workbook created'
        tsk.save()
    except:
        logger.error("Unexpected error creating temporary file - please contact an administrator: {0}".format(
            sys.exc_info()[0]))
        return redirect('/openrem/export/')

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

    book, sheet_list = generate_sheets(e, book, protocolheaders, pid=pid, name=name, patid=patid)

    ##################
    # All data sheet

    from django.db.models import Max
    max_events = e.aggregate(Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                                 'total_number_of_radiographic_frames'))

    alldataheaders = list(commonheaders)

    tsk.progress = u'Generating headers for the all data sheet...'
    tsk.save()


    for h in xrange(max_events['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                               'total_number_of_radiographic_frames__max']):
        alldataheaders += [
            u'E' + str(h+1) + u' Protocol',
            u'E' + str(h+1) + u' Anatomy',
            u'E' + str(h+1) + u' Image view',
            u'E' + str(h+1) + u' Exposure control mode',
            u'E' + str(h+1) + u' kVp',
            u'E' + str(h+1) + u' mAs',
            u'E' + str(h+1) + u' mA',
            u'E' + str(h+1) + u' Exposure time (ms)',
            u'E' + str(h+1) + u' Filters',
            u'E' + str(h+1) + u' Filter thicknesses (mm)',
            u'E' + str(h+1) + u' Exposure index',
            u'E' + str(h+1) + u' Relative x-ray exposure',
            u'E' + str(h+1) + u' DAP (cGy.cm^2)',
            u'E' + str(h+1) + u' Entrance Exposure at RP (mGy)',
            u'E' + str(h+1) + u' SDD Detector Dist',
            u'E' + str(h+1) + u' SPD Patient Dist',
            u'E' + str(h+1) + u' SIsoD Isocentre Dist',
            u'E' + str(h+1) + u' Table Height',
            u'E' + str(h+1) + u' Comment',
            ]
    wsalldata.write_row('A1', alldataheaders)
    numcolumns = (19 * max_events['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__'
                                  'total_number_of_radiographic_frames__max']) + len(commonheaders) - 1
    numrows = e.count()
    wsalldata.autofilter(0, 0, numrows, numcolumns)

    for row, exams in enumerate(e):

        tsk.progress = u'Writing study {0} of {1} to All data sheet and individual protocol sheets'.format(
            row + 1, numrows)
        tsk.save()

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
            patient_age = string_to_float(exams.patientstudymoduleattr_set.get().patient_age_decimal)
            patient_size = string_to_float(exams.patientstudymoduleattr_set.get().patient_size)
            patient_weight = string_to_float(exams.patientstudymoduleattr_set.get().patient_weight)
        except ObjectDoesNotExist:
            patient_age  = None
            patient_size = None
            patient_weight = None

        try:
            not_patient_indicator = exams.patientmoduleattr_set.get().not_patient_indicator
        except ObjectDoesNotExist:
            not_patient_indicator = None

        try:
            try:
                total_number_of_radiographic_frames = int(exams.projectionxrayradiationdose_set.get(
                    ).accumxraydose_set.get().accumintegratedprojradiogdose_set.get().total_number_of_radiographic_frames)
            except TypeError:
                total_number_of_radiographic_frames = None
            if exams.projectionxrayradiationdose_set.get(
                ).accumxraydose_set.get().accumintegratedprojradiogdose_set.get().dose_area_product_total is not None:
                cgycm2 = string_to_float(exams.projectionxrayradiationdose_set.get(
                    ).accumxraydose_set.get().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2())
            else:
                cgycm2 = None
        except ObjectDoesNotExist:
            total_number_of_radiographic_frames = None
            cgycm2 = None

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
            patient_age,
            patient_sex,
            patient_size,
            patient_weight,
            not_patient_indicator,
            exams.study_description,
            exams.requested_procedure_code_meaning,
            total_number_of_radiographic_frames,
            cgycm2,
        ]
        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):

            try:
                exposure_control_mode = s.irradeventxraysourcedata_set.get().exposure_control_mode
                average_xray_tube_current = string_to_float(
                    s.irradeventxraysourcedata_set.get().average_xray_tube_current)
                exposure_time = string_to_float(s.irradeventxraysourcedata_set.get().exposure_time)
                try:
                    kvp = string_to_float(s.irradeventxraysourcedata_set.get().kvp_set.get().kvp)
                except ObjectDoesNotExist:
                    kvp = None

                try:
                    if s.irradeventxraysourcedata_set.get().exposure_set.get().exposure is not None:
                        mas = string_to_float(
                            s.irradeventxraysourcedata_set.get().exposure_set.get().convert_uAs_to_mAs())
                    else:
                        mas = None
                except ObjectDoesNotExist:
                    mas = None
                filters, filter_thicknesses = _get_xray_filterinfo(s.irradeventxraysourcedata_set.get())
            except ObjectDoesNotExist:
                exposure_control_mode = None
                kvp = None
                average_xray_tube_current = None
                exposure_time = None
                mas = None
                filters = None
                filter_thicknesses = None

            try:
                exposure_index = string_to_float(s.irradeventxraydetectordata_set.get().exposure_index)
                relative_xray_exposure = string_to_float(s.irradeventxraydetectordata_set.get().relative_xray_exposure)
            except ObjectDoesNotExist:
                exposure_index = None
                relative_xray_exposure = None

            cgycm2 = string_to_float(s.convert_gym2_to_cgycm2())

            entrance_exposure_at_rp = string_to_float(s.entrance_exposure_at_rp)

            try:
                s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
            except:
                distance_source_to_detector = None
                distance_source_to_entrance_surface = None
                distance_source_to_isocenter = None
                table_height_position = None
            else:
                distance_source_to_detector = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'distance_source_to_detector'))
                distance_source_to_entrance_surface = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'distance_source_to_entrance_surface'))
                distance_source_to_isocenter = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'distance_source_to_isocenter'))
                table_height_position = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'table_height_position'))

            examdata += [
                s.acquisition_protocol,
                str(s.anatomical_structure),
                str(s.image_view),
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

        wsalldata.write_row(row+1,0, examdata)
        
        # Now we need to write a sheet per series protocol for each 'exams'.
        
        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):
            protocol = s.acquisition_protocol
            if not protocol:
                protocol = u'Unknown'
            tabtext = protocol.lower().replace(u" ", u"_")
            translation_table = {ord('['):ord('('), ord(']'):ord(')'), ord(':'):ord(';'), ord('*'):ord('#'),
                                 ord('?'):ord(';'), ord('/'):ord('|'), ord('\\'):ord('|')}
            tabtext = tabtext.translate(translation_table)  # remove illegal characters
            tabtext = tabtext[:31]
            sheet_list[tabtext]['count'] += 1

            if pid and (name or patid):
                try:
                    exams.patientmoduleattr_set.get()
                except ObjectDoesNotExist:
                    if name:
                        patient_name = None
                    if patid:
                        patient_id = None
                else:
                    if name:
                        patient_name = return_for_export(exams.patientmoduleattr_set.get(), 'patient_name')
                    if patid:
                        patient_id = return_for_export(exams.patientmoduleattr_set.get(), 'patient_id')
            try:
                exams.generalequipmentmoduleattr_set.get()
            except ObjectDoesNotExist:
                institution_name = None
                manufacturer = None
                manufacturer_model_name = None
                station_name = None
                display_name = None
            else:
                institution_name = return_for_export(exams.generalequipmentmoduleattr_set.get(), 'institution_name')
                manufacturer = return_for_export(exams.generalequipmentmoduleattr_set.get(), 'manufacturer')
                manufacturer_model_name = return_for_export(exams.generalequipmentmoduleattr_set.get(), 'manufacturer_model_name')
                station_name = return_for_export(exams.generalequipmentmoduleattr_set.get(), 'station_name')
                display_name = return_for_export(exams.generalequipmentmoduleattr_set.get().unique_equipment_name, 'display_name')

            try:
                exams.patientmoduleattr_set.get()
            except ObjectDoesNotExist:
                patient_sex = None
            else:
                patient_sex = return_for_export(exams.patientmoduleattr_set.get(), 'patient_sex')

            try:
                exams.patientstudymoduleattr_set.get()
            except ObjectDoesNotExist:
                patient_age = None
                patient_size = None
                patient_weight = None
            else:
                patient_age = string_to_float(return_for_export(exams.patientstudymoduleattr_set.get(),
                                                                'patient_age_decimal'))
                patient_size = string_to_float(return_for_export(exams.patientstudymoduleattr_set.get(),
                                                                 'patient_size'))
                patient_weight = string_to_float(return_for_export(exams.patientstudymoduleattr_set.get(),
                                                                   'patient_weight'))

            try:
                exams.patientmoduleattr_set.get()
            except ObjectDoesNotExist:
                not_patient_indicator = None
            else:
                not_patient_indicator = return_for_export(exams.patientmoduleattr_set.get(), 'not_patient_indicator')

            try:
                exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get()
            except ObjectDoesNotExist:
                total_number_of_radiographic_frames = None
                cgycm2 = None
            else:
                try:
                    total_number_of_radiographic_frames = int(return_for_export(
                        exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                        ).accumintegratedprojradiogdose_set.get(), 'total_number_of_radiographic_frames'))
                except TypeError:
                    total_number_of_radiographic_frames = None
                dap_total = return_for_export(
                    exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                    ).accumintegratedprojradiogdose_set.get(), 'dose_area_product_total')
                if dap_total:
                    cgycm2 = string_to_float(
                        exams.projectionxrayradiationdose_set.get().accumxraydose_set.get(
                        ).accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2())
                else:
                    cgycm2 = None

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
                patient_age,
                patient_sex,
                patient_size,
                patient_weight,
                not_patient_indicator,
                exams.study_description,
                exams.requested_procedure_code_meaning,
                total_number_of_radiographic_frames,
                cgycm2,
                ]

            try:
                s.irradeventxraysourcedata_set.get()
            except ObjectDoesNotExist:
                exposure_control_mode = None
                kvp = None
                average_xray_tube_current = None
                exposure_time = None
                mas = None
                filters = None
                filter_thicknesses = None
            else:
                exposure_control_mode = return_for_export(s.irradeventxraysourcedata_set.get(), 'exposure_control_mode')
                average_xray_tube_current = string_to_float(return_for_export(s.irradeventxraysourcedata_set.get(),
                                                                              'average_xray_tube_current'))
                exposure_time = string_to_float(return_for_export(s.irradeventxraysourcedata_set.get(),
                                                                  'exposure_time'))
                try:
                    s.irradeventxraysourcedata_set.get().kvp_set.get()
                except ObjectDoesNotExist:
                    kvp = None
                else:
                    kvp = string_to_float(return_for_export(s.irradeventxraysourcedata_set.get().kvp_set.get(), 'kvp'))

                try:
                    s.irradeventxraysourcedata_set.get().exposure_set.get()
                except ObjectDoesNotExist:
                    mas = None
                else:
                    uas = return_for_export(s.irradeventxraysourcedata_set.get().exposure_set.get(), 'exposure')
                    if uas:
                        mas = string_to_float(
                            s.irradeventxraysourcedata_set.get().exposure_set.get().convert_uAs_to_mAs())
                    else:
                        mas = None
                filters, filter_thicknesses = _get_xray_filterinfo(s.irradeventxraysourcedata_set.get())
            try:
                s.irradeventxraydetectordata_set.get()
            except ObjectDoesNotExist:
                exposure_index = None
                relative_xray_exposure = None
            else:
                exposure_index = string_to_float(return_for_export(s.irradeventxraydetectordata_set.get(),
                                                                   'exposure_index'))
                relative_xray_exposure = string_to_float(return_for_export(s.irradeventxraydetectordata_set.get(),
                                                                           'relative_xray_exposure'))

            cgycm2 = string_to_float(s.convert_gym2_to_cgycm2())

            entrance_exposure_at_rp = string_to_float(return_for_export(s, 'entrance_exposure_at_rp'))

            try:
                s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
            except:
                distance_source_to_detector = None
                distance_source_to_entrance_surface = None
                distance_source_to_isocenter = None
                table_height_position = None
            else:
                distance_source_to_detector = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'distance_source_to_detector'))
                distance_source_to_entrance_surface = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'distance_source_to_entrance_surface'))
                distance_source_to_isocenter = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'distance_source_to_isocenter'))
                table_height_position = string_to_float(return_for_export(
                    s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(),
                    'table_height_position'))

            examdata += [
                s.acquisition_protocol,
                str(s.anatomical_structure),
                str(s.image_view),
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

            sheet_list[tabtext]['sheet'].write_row(sheet_list[tabtext]['count'], 0, examdata)

    # Could at this point go through each sheet adding on the auto filter as we now know how many of each there are...
    
    # Populate summary sheet
    tsk.progress = u'Now populating the summary sheet...'
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
    toplinestring = u'XLSX Export from OpenREM version {0} on {1}'.format(version, str(datetime.datetime.now()))
    linetwostring = u'OpenREM is copyright 2016 The Royal Marsden NHS Foundation Trust, and available under the GPL. See http://openrem.org'
    summarysheet.write(0,0, toplinestring, titleformat)
    summarysheet.write(1,0, linetwostring)

    # Number of exams
    summarysheet.write(3,0, u"Total number of exams")
    summarysheet.write(3,1,e.count())

    # Generate list of Study Descriptions
    summarysheet.write(5,0, u"Study Description")
    summarysheet.write(5,1, u"Frequency")
    from django.db.models import Count
    study_descriptions = e.values("study_description").annotate(n=Count("pk"))
    for row, item in enumerate(study_descriptions.order_by('n').reverse()):
        summarysheet.write(row+6,0,item['study_description'])
        summarysheet.write(row+6,1,item['n'])
    summarysheet.set_column('A:A', 25)

    # Generate list of Requested Procedures
    summarysheet.write(5,3, u"Requested Procedure")
    summarysheet.write(5,4, u"Frequency")
    from django.db.models import Count
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
