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

import csv
from xlsxwriter.workbook import Workbook
from celery import shared_task
from django.conf import settings

@shared_task
def exportDX2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered DX database data to a single-sheet CSV file.

    :param request: Query parameters from the DX filtered page URL.
    :type request: HTTP get
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import dx_acq_filter
    from remapp.tools.get_values import return_for_export, export_safe
    from django.db.models import Q # For the Q "OR" query used for DX and CR
    from django.core.exceptions import ObjectDoesNotExist

    tsk = Exports.objects.create()

    tsk.task_id = exportDX2excel.request.id
    tsk.modality = "DX"
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
        # messages.error(request, "Unexpected error creating temporary file - please contact an administrator: {0}".format(sys.exc_info()[0]))
        return redirect('/openrem/export/')
        
    # Get the data!

    e = dx_acq_filter(filterdict, pid=pid).qs

    # Remove duplicate entries from the results - hopefully no longer necessary, left here in case. Needs testing
    # e = e.filter(projectionxrayradiationdose__general_study_module_attributes__study_instance_uid__isnull = False).distinct()

    tsk.progress = 'Required study filter complete.'
    tsk.save()
        
    numresults = e.count()

    tsk.progress = '{0} studies in query.'.format(numresults)
    tsk.num_records = numresults
    tsk.save()

    pidheadings = []
    if pid and name:
        pidheadings += ['Patient name']
    if pid and patid:
        pidheadings += ['Patient ID']
    headers = pidheadings + [
        'Institution name', 
        'Manufacturer', 
        'Model name',
        'Station name',
        'Display name',
        'Accession number',
        'Operator',
        'Study date',
    ]
    if pid and (name or patid):
        headers += [
            'Date of birth',
        ]
    headers += [
        'Patient age',
        'Patient sex',
        'Patient height', 
        'Patient mass (kg)', 
        'Study description',
        'Requested procedure',
        'Number of events',
        'DAP total (cGy.cm^2)',
    ]

    from django.db.models import Max
    max_events = e.aggregate(Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames'))

    for h in xrange(max_events['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames__max']):
        headers += [
            'E' + str(h+1) + ' Protocol',
            'E' + str(h+1) + ' Image view',
            'E' + str(h+1) + ' Exposure control mode',
            'E' + str(h+1) + ' kVp',
            'E' + str(h+1) + ' mAs',
            'E' + str(h+1) + ' mA',
            'E' + str(h+1) + ' Exposure time (ms)',
            'E' + str(h+1) + ' Filters',
            'E' + str(h+1) + ' Filter thicknesses (mm)',
            'E' + str(h+1) + ' Exposure index',
            'E' + str(h+1) + ' Relative x-ray exposure',
            'E' + str(h+1) + ' DAP (cGy.cm^2)',
            ]
    writer.writerow(headers)

    tsk.progress = 'CSV header row written.'
    tsk.save()

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
            institution_name = None
            manufacturer = None
            manufacturer_model_name = None
            station_name = None
            display_name = None
        else:
            institution_name = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get(), 'institution_name'))
            manufacturer = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get(), 'manufacturer'))
            manufacturer_model_name = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get(), 'manufacturer_model_name'))
            station_name = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get(), 'station_name'))
            display_name = export_safe(return_for_export(exams.generalequipmentmoduleattr_set.get().unique_equipment_name, 'display_name'))
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
            patient_age = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_age_decimal')
            patient_size = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_size')
            patient_weight = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_weight')

        try:
            exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get()
        except ObjectDoesNotExist:
            total_number_of_radiographic_frames = None
            cgycm2 = None
        else:
            total_number_of_radiographic_frames = return_for_export(exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get(), 'total_number_of_radiographic_frames')
            dap_total = return_for_export(exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get(), 'dose_area_product_total')
            if dap_total:
                cgycm2 = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
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
            export_safe(exams.accession_number),
            export_safe(exams.operator_name),
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
            export_safe(exams.study_description),
            export_safe(exams.requested_procedure_code_meaning),
            total_number_of_radiographic_frames,
            cgycm2,
        ]

        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():

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
                average_xray_tube_current = return_for_export(s.irradeventxraysourcedata_set.get(), 'average_xray_tube_current')
                exposure_time = return_for_export(s.irradeventxraysourcedata_set.get(), 'exposure_time')
                try:
                    s.irradeventxraysourcedata_set.get().kvp_set.get()
                except ObjectDoesNotExist:
                    kvp = None
                else:
                    kvp = return_for_export(s.irradeventxraysourcedata_set.get().kvp_set.get(), 'kvp')

                try:
                    s.irradeventxraysourcedata_set.get().exposure_set.get()
                except ObjectDoesNotExist:
                    mas = None
                else:
                    uas = return_for_export(s.irradeventxraysourcedata_set.get().exposure_set.get(), 'exposure')
                    if uas:
                        mas = s.irradeventxraysourcedata_set.get().exposure_set.get().convert_uAs_to_mAs()
                    else:
                        mas = None

                try:
                    s.irradeventxraysourcedata_set.get().xrayfilters_set.all()
                except ObjectDoesNotExist:
                    filters = None
                    filter_thicknesses = None
                else:
                    filters = ''
                    filter_thicknesses = ''
                    for current_filter in s.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                        if 'Aluminum' in str(current_filter.xray_filter_material):
                            filters += 'Al'
                        elif 'Copper' in str(current_filter.xray_filter_material):
                            filters += 'Cu'
                        elif 'Tantalum' in str(current_filter.xray_filter_material):
                            filters += 'Ta'
                        elif 'Molybdenum' in str(current_filter.xray_filter_material):
                            filters += 'Mo'
                        elif 'Rhodium' in str(current_filter.xray_filter_material):
                            filters += 'Rh'
                        elif 'Silver' in str(current_filter.xray_filter_material):
                            filters += 'Ag'
                        elif 'Niobium' in str(current_filter.xray_filter_material):
                            filters += 'Nb'
                        elif 'Europium' in str(current_filter.xray_filter_material):
                            filters += 'Eu'
                        elif 'Lead' in str(current_filter.xray_filter_material):
                            filters += 'Pb'
                        filters += ' | '
                        filter_thicknesses += str(current_filter.xray_filter_thickness_maximum) + ' | '
                    filters = filters[:-3]
                    filter_thicknesses = filter_thicknesses[:-3]

            try:
                s.irradeventxraydetectordata_set.get()
            except ObjectDoesNotExist:
                exposure_index = None
                relative_xray_exposure = None
            else:
                exposure_index = return_for_export(s.irradeventxraydetectordata_set.get(), 'exposure_index')
                relative_xray_exposure = return_for_export(s.irradeventxraydetectordata_set.get(), 'relative_xray_exposure')

            cgycm2 = s.convert_gym2_to_cgycm2()

            examdata += [
                export_safe(s.acquisition_protocol),
                s.image_view,
                export_safe(exposure_control_mode),
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

@shared_task
def dxxlsx(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered DX and CR database data to multi-sheet Microsoft XSLX files.

    :param filterdict: Query parameters from the DX and CR filtered page URL.
    :type filterdict: HTTP get
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import dx_acq_filter
    from remapp.tools.get_values import return_for_export
    from django.db.models import Q # For the Q "OR" query used for DX and CR
    from django.core.exceptions import ObjectDoesNotExist

    tsk = Exports.objects.create()

    tsk.task_id = dxxlsx.request.id
    tsk.modality = "DX"
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
        # messages.error(request, "Unexpected error creating temporary file - please contact an administrator: {0}".format(sys.exc_info()[0]))
        return redirect('/openrem/export/')

    e = dx_acq_filter(filterdict, pid=pid).qs

    # Remove duplicate entries from the results - hopefully no longer necessary, left here in case. Needs testing
    # e = e.filter(projectionxrayradiationdose__general_study_module_attributes__study_instance_uid__isnull = False).distinct()

    tsk.progress = 'Required study filter complete.'
    tsk.num_records = e.count()
    tsk.save()

    # Add summary sheet and all data sheet
    summarysheet = book.add_worksheet("Summary")
    wsalldata = book.add_worksheet('All data')
    date_column = 7
    if pid and name:
        date_column += 1
    if pid and patid:
        date_column += 1
    wsalldata.set_column(date_column, date_column, 10)  # allow date to be displayed.
    if pid and (name or patid):
        wsalldata.set_column(date_column+1, date_column+1, 10) # Date column

    # Some prep
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
        'Number of events',
        'DAP total (cGy.cm^2)',
        ]
    protocolheaders = commonheaders + [
        'Protocol',
        'Anatomy',
        'Image view',
        'Exposure control mode',
        'kVp',
        'mAs',
        'mA',
        'Exposure time (ms)',
        'Filters',
        'Filter thicknesses (mm)',
        'Exposure index',
        'Relative x-ray exposure',
        'DAP (cGy.cm^2)',
        'Entrance exposure at RP',
        'SDD Detector Dist',
        'SPD Patient Dist',
        'SIsoD Isocentre Dist',
        'Table Height',
        'Comment'
        ]
        
    # Generate list of protocols in queryset and create worksheets for each
    tsk.progress = 'Generating list of protocols in the dataset...'
    tsk.save()

    sheetlist = {}
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
            sheetlist[tabtext]['sheet'].set_column(date_column, date_column, 10) # Date column
            if pid and (name or patid):
                sheetlist[tabtext]['sheet'].set_column(date_column+1, date_column+1, 10) # Date column
        else:
            if protocol not in sheetlist[tabtext]['protocolname']:
                sheetlist[tabtext]['protocolname'].append(protocol)



    ##################
    # All data sheet

    from django.db.models import Max
    max_events = e.aggregate(Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames'))

    alldataheaders = commonheaders

    tsk.progress = 'Generating headers for the all data sheet...'
    tsk.save()

    for h in xrange(max_events['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames__max']):
        alldataheaders += [
            'E' + str(h+1) + ' Protocol',
            'E' + str(h+1) + ' Anatomy',
            'E' + str(h+1) + ' Image view',
            'E' + str(h+1) + ' Exposure control mode',
            'E' + str(h+1) + ' kVp',
            'E' + str(h+1) + ' mAs',
            'E' + str(h+1) + ' mA',
            'E' + str(h+1) + ' Exposure time (ms)',
            'E' + str(h+1) + ' Filters',
            'E' + str(h+1) + ' Filter thicknesses (mm)',
            'E' + str(h+1) + ' Exposure index',
            'E' + str(h+1) + ' Relative x-ray exposure',
            'E' + str(h+1) + ' DAP (cGy.cm^2)',
            'E' + str(h+1) + ' Entrance Exposure at RP (mGy)',
            'E' + str(h+1) + ' SDD Detector Dist',
            'E' + str(h+1) + ' SPD Patient Dist',
            'E' + str(h+1) + ' SIsoD Isocentre Dist',
            'E' + str(h+1) + ' Table Height',
            'E' + str(h+1) + ' Comment',
            ]
    wsalldata.write_row('A1', alldataheaders)
    wsalldata.set_column(date_column, date_column, 10) # allow date to be displayed.
    if pid and (name or patid):
        wsalldata.set_column(date_column+1, date_column+1, 10) # allow date to be displayed.
    numcolumns = (29 * max_events['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__total_number_of_radiographic_frames__max']) + date_column + 8
    numrows = e.count()
    wsalldata.autofilter(0,0,numrows,numcolumns)

    for row, exams in enumerate(e):

        tsk.progress = 'Writing study {0} of {1} to All data sheet and individual protocol sheets'.format(row + 1, numrows)
        tsk.save()

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
            patient_age  = None
            patient_size = None
            patient_weight = None
        else:
            patient_age = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_age_decimal')
            patient_size = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_size')
            patient_weight = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_weight')

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
            total_number_of_radiographic_frames = return_for_export(exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get(), 'total_number_of_radiographic_frames')
            dap_total = return_for_export(exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get(), 'dose_area_product_total')
            if dap_total:
                cgycm2 = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
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
            exams.study_date,  # Is a date - cell needs formatting
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
        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():

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
                average_xray_tube_current = str(s.irradeventxraysourcedata_set.get().average_xray_tube_current)
                exposure_time = str(s.irradeventxraysourcedata_set.get().exposure_time)
                try:
                    s.irradeventxraysourcedata_set.get().kvp_set.get()
                except ObjectDoesNotExist:
                    kvp = None
                else:
                    kvp = return_for_export(s.irradeventxraysourcedata_set.get().kvp_set.get(), 'kvp')

                try:
                    s.irradeventxraysourcedata_set.get().exposure_set.get()
                except ObjectDoesNotExist:
                    mas = None
                else:
                    uas = return_for_export(s.irradeventxraysourcedata_set.get().exposure_set.get(), 'exposure')
                    if uas:
                        mas = s.irradeventxraysourcedata_set.get().exposure_set.get().convert_uAs_to_mAs()
                    else:
                        mas = None

                try:
                    s.irradeventxraysourcedata_set.get().xrayfilters_set.all()
                except ObjectDoesNotExist:
                    filters = None
                    filter_thicknesses = None
                else:
                    filters = ''
                    filter_thicknesses = ''
                    for current_filter in s.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                        if 'Aluminum' in str(current_filter.xray_filter_material):
                            filters += 'Al'
                        elif 'Copper' in str(current_filter.xray_filter_material):
                            filters += 'Cu'
                        elif 'Tantalum' in str(current_filter.xray_filter_material):
                            filters += 'Ta'
                        elif 'Molybdenum' in str(current_filter.xray_filter_material):
                            filters += 'Mo'
                        elif 'Rhodium' in str(current_filter.xray_filter_material):
                            filters += 'Rh'
                        elif 'Silver' in str(current_filter.xray_filter_material):
                            filters += 'Ag'
                        elif 'Niobium' in str(current_filter.xray_filter_material):
                            filters += 'Nb'
                        elif 'Europium' in str(current_filter.xray_filter_material):
                            filters += 'Eu'
                        elif 'Lead' in str(current_filter.xray_filter_material):
                            filters += 'Pb'
                        filters += ' | '
                        filter_thicknesses += str(current_filter.xray_filter_thickness_maximum) + ' | '
                    filters = filters[:-3]
                    filter_thicknesses = filter_thicknesses[:-3]

            try:
                s.irradeventxraydetectordata_set.get()
            except ObjectDoesNotExist:
                exposure_index = None
                relative_xray_exposure = None
            else:
                exposure_index = return_for_export(s.irradeventxraydetectordata_set.get(), 'exposure_index')
                relative_xray_exposure = return_for_export(s.irradeventxraydetectordata_set.get(), 'relative_xray_exposure')

            cgycm2 = str(s.convert_gym2_to_cgycm2())


            entrance_exposure_at_rp = return_for_export(s, 'entrance_exposure_at_rp')

            try:
                s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
            except:
                distance_source_to_detector = None
                distance_source_to_entrance_surface = None
                distance_source_to_isocenter = None
                table_height_position = None
            else:
                distance_source_to_detector = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'distance_source_to_detector')
                distance_source_to_entrance_surface = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'distance_source_to_entrance_surface')
                distance_source_to_isocenter = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'distance_source_to_isocenter')
                table_height_position = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'table_height_position')

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
        
        for s in exams.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
            protocol = s.acquisition_protocol
            if not protocol:
                protocol = u'Unknown'
            tabtext = protocol.lower().replace(" ","_")
            translation_table = {ord('['):ord('('), ord(']'):ord(')'), ord(':'):ord(';'), ord('*'):ord('#'), ord('?'):ord(';'), ord('/'):ord('|'), ord('\\'):ord('|')}
            tabtext = tabtext.translate(translation_table) # remove illegal characters
            tabtext = tabtext[:31]
            sheetlist[tabtext]['count'] += 1

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
                patient_age = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_age_decimal')
                patient_size = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_size')
                patient_weight = return_for_export(exams.patientstudymoduleattr_set.get(), 'patient_weight')

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
                total_number_of_radiographic_frames = return_for_export(exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get(), 'total_number_of_radiographic_frames')
                dap_total = return_for_export(exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get(), 'dose_area_product_total')
                if dap_total:
                    cgycm2 = exams.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
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
                exams.study_date,  # Is a date - cell needs formatting
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
                average_xray_tube_current = return_for_export(s.irradeventxraysourcedata_set.get(), 'average_xray_tube_current')
                exposure_time = return_for_export(s.irradeventxraysourcedata_set.get(), 'exposure_time')
                try:
                    s.irradeventxraysourcedata_set.get().kvp_set.get()
                except ObjectDoesNotExist:
                    kvp = None
                else:
                    kvp = return_for_export(s.irradeventxraysourcedata_set.get().kvp_set.get(), 'kvp')

                try:
                    s.irradeventxraysourcedata_set.get().exposure_set.get()
                except ObjectDoesNotExist:
                    mas = None
                else:
                    uas = return_for_export(s.irradeventxraysourcedata_set.get().exposure_set.get(), 'exposure')
                    if uas:
                        mas = s.irradeventxraysourcedata_set.get().exposure_set.get().convert_uAs_to_mAs()
                    else:
                        mas = None

                try:
                    s.irradeventxraysourcedata_set.get().xrayfilters_set.all()
                except ObjectDoesNotExist:
                    filters = None
                    filter_thicknesses = None
                else:
                    filters = ''
                    filter_thicknesses = ''
                    for current_filter in s.irradeventxraysourcedata_set.get().xrayfilters_set.all():
                        if 'Aluminum' in str(current_filter.xray_filter_material):
                            filters += 'Al'
                        elif 'Copper' in str(current_filter.xray_filter_material):
                            filters += 'Cu'
                        elif 'Tantalum' in str(current_filter.xray_filter_material):
                            filters += 'Ta'
                        elif 'Molybdenum' in str(current_filter.xray_filter_material):
                            filters += 'Mo'
                        elif 'Rhodium' in str(current_filter.xray_filter_material):
                            filters += 'Rh'
                        elif 'Silver' in str(current_filter.xray_filter_material):
                            filters += 'Ag'
                        elif 'Niobium' in str(current_filter.xray_filter_material):
                            filters += 'Nb'
                        elif 'Europium' in str(current_filter.xray_filter_material):
                            filters += 'Eu'
                        elif 'Lead' in str(current_filter.xray_filter_material):
                            filters += 'Pb'
                        filters += ' | '
                        filter_thicknesses += str(current_filter.xray_filter_thickness_maximum) + ' | '
                    filters = filters[:-3]
                    filter_thicknesses = filter_thicknesses[:-3]

            try:
                s.irradeventxraydetectordata_set.get()
            except ObjectDoesNotExist:
                exposure_index = None
                relative_xray_exposure = None
            else:
                exposure_index = return_for_export(s.irradeventxraydetectordata_set.get(), 'exposure_index')
                relative_xray_exposure = return_for_export(s.irradeventxraydetectordata_set.get(), 'relative_xray_exposure')

            cgycm2 = s.convert_gym2_to_cgycm2()

            entrance_exposure_at_rp = return_for_export(s, 'entrance_exposure_at_rp')

            try:
                s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
            except:
                distance_source_to_detector = None
                distance_source_to_entrance_surface = None
                distance_source_to_isocenter = None
                table_height_position = None
            else:
                distance_source_to_detector = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'distance_source_to_detector')
                distance_source_to_entrance_surface = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'distance_source_to_entrance_surface')
                distance_source_to_isocenter = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'distance_source_to_isocenter')
                table_height_position = return_for_export(s.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'table_height_position')

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

            sheetlist[tabtext]['sheet'].write_row(sheetlist[tabtext]['count'],0,examdata)

    # Could at this point go through each sheet adding on the auto filter as we now know how many of each there are...
    
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

    xlsxfilename = "dxexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(xlsxfilename,File(tmpxlsx))
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
