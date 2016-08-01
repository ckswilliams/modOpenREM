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

import csv
import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def exportCT2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered CT database data to a single-sheet CSV file.

    :param request: Query parameters from the CT filtered page URL.
    :type request: HTTP get
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from django.core.exceptions import ObjectDoesNotExist
    from django.contrib import messages
    from remapp.models import Exports
    from remapp.tools.get_values import return_for_export, export_safe
    from remapp.interface.mod_filters import ct_acq_filter

    tsk = Exports.objects.create()

    tsk.task_id = exportCT2excel.request.id
    tsk.modality = "CT"
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
    e = ct_acq_filter(filterdict, pid=pid).qs

    tsk.progress = 'Required study filter complete.'
    tsk.save()
        
    numresults = e.count()

    tsk.progress = '{0} studies in query.'.format(numresults)
    tsk.num_records = numresults
    tsk.save()

    headings = []
    if pid and name:
        headings += ['Patient name']
    if pid and patid:
        headings += ['Patient ID']
    headings += [
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
        headings += [
            'Date of birth',
        ]
    headings += [
        'Patient age',
        'Patient sex',
        'Patient height', 
        'Patient mass (kg)',
        'Test patient?',
        'Study description',
        'Requested procedure',
        'Number of events',
        'DLP total (mGy.cm)',
        ]

    from django.db.models import Max
    max_events = e.aggregate(Max('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events'))

    for h in xrange(max_events['ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events__max']):
        headings += [
            'E' + str(h+1) + ' Protocol',
            'E' + str(h+1) + ' Type',
            'E' + str(h+1) + ' Exposure time',
            'E' + str(h+1) + ' Scanning length',
            'E' + str(h+1) + ' Slice thickness',
            'E' + str(h+1) + ' Total collimation',
            'E' + str(h+1) + ' Pitch',
            'E' + str(h+1) + ' No. sources',
            'E' + str(h+1) + ' CTDIvol',
            'E' + str(h+1) + ' DLP',
            'E' + str(h+1) + ' S1 name',
            'E' + str(h+1) + ' S1 kVp',
            'E' + str(h+1) + ' S1 max mA',
            'E' + str(h+1) + ' S1 mA',
            'E' + str(h+1) + ' S1 Exposure time/rotation',
            'E' + str(h+1) + ' S2 name',
            'E' + str(h+1) + ' S2 kVp',
            'E' + str(h+1) + ' S2 max mA',
            'E' + str(h+1) + ' S2 mA',
            'E' + str(h+1) + ' S2 Exposure time/rotation',
            'E' + str(h+1) + ' mA Modulation type',
            ]
    writer.writerow(headings)

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
            not_patient = None
        else:
            patient_sex = return_for_export(exams.patientmoduleattr_set.get(), 'patient_sex')
            not_patient = export_safe(return_for_export(exams.patientmoduleattr_set.get(), 'not_patient_indicator'))

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
            exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get()
        except ObjectDoesNotExist:
            total_number_of_irradiation_events = None
            ct_dose_length_product_total = None
        else:
            total_number_of_irradiation_events = return_for_export(exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get(), 'total_number_of_irradiation_events')
            ct_dose_length_product_total = return_for_export(exams.ctradiationdose_set.get().ctaccumulateddosedata_set.get(), 'ct_dose_length_product_total')

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
            patient_age_decimal,
            patient_sex,
            patient_size,
            patient_weight,
            not_patient,
            export_safe(exams.study_description),
            export_safe(exams.requested_procedure_code_meaning),
            total_number_of_irradiation_events,
            ct_dose_length_product_total,
            ]

        for s in exams.ctradiationdose_set.get().ctirradiationeventdata_set.all():

            try:
                s.scanninglength_set.get()
            except ObjectDoesNotExist:
                scanning_length = None
            else:
                scanning_length = s.scanninglength_set.get().scanning_length

            examdata += [
                export_safe(s.acquisition_protocol),
                s.ct_acquisition_type,
                s.exposure_time,
                scanning_length,
                s.nominal_single_collimation_width,
                s.nominal_total_collimation_width,
                s.pitch_factor,
                s.number_of_xray_sources,
                s.mean_ctdivol,
                s.dlp,
                ]
            if s.number_of_xray_sources > 1:
                for source in s.ctxraysourceparameters_set.all():
                    examdata += [
                        source.identification_of_the_xray_source,
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
                        identification_of_the_xray_source = return_for_export(s.ctxraysourceparameters_set.get(), 'identification_of_the_xray_source')
                        kvp = return_for_export(s.ctxraysourceparameters_set.get(), 'kvp')
                        maximum_xray_tube_current = return_for_export(s.ctxraysourceparameters_set.get(), 'maximum_xray_tube_current')
                        xray_tube_current = return_for_export(s.ctxraysourceparameters_set.get(), 'xray_tube_current')
                        exposure_time_per_rotation = return_for_export(s.ctxraysourceparameters_set.get(), 'exposure_time_per_rotation')

                    examdata += [
                        identification_of_the_xray_source,
                        kvp,
                        maximum_xray_tube_current,
                        xray_tube_current,
                        exposure_time_per_rotation,
                        'n/a',
                        'n/a',
                        'n/a',
                        'n/a',
                        'n/a',
                        ]
                except:
                        examdata += ['n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a',]
            examdata += [s.xray_modulation_type,]

        writer.writerow(examdata)
        tsk.progress = "{0} of {1}".format(i+1, numresults)
        tsk.save()
    tsk.progress = 'All study data written.'
    tsk.save()

    csvfilename = "ctexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

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
def exportMG2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered mammography database data to a single-sheet CSV file.

    :param filterdict: Query parameters from the mammo filtered page URL.
    :type filterdict: HTTP get
    :param pid: True if user in pidgroup
    :type pid: bool
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import MGSummaryListFilter, MGFilterPlusPid
    from remapp.tools.get_values import return_for_export, export_safe
    from django.core.exceptions import ObjectDoesNotExist

    tsk = Exports.objects.create()

    tsk.task_id = exportMG2excel.request.id
    tsk.modality = "MG"
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
        df_filtered_qs = MGFilterPlusPid(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'MG'))
    else:
        df_filtered_qs = MGSummaryListFilter(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'MG'))
    s = df_filtered_qs.qs

    tsk.progress = 'Required study filter complete.'
    tsk.save()
        
    numresults = s.count()

    tsk.num_records = numresults
    tsk.save()

    headings = []
    if pid and name:
        headings += ['Patient name']
    if pid and patid:
        headings += ['Patient ID']
    headings += [
        'Institution name',
        'Manufacturer',
        'Station name',
        'Display name',
        'Accession number',
        'Study UID',
        'Study date',
        'Study time',
    ]
    if pid and (name or patid):
        headings += [
            'Date of birth',
        ]
    headings += [
        'Patient age',
        'Patient sex',
        'Number of events',
        'Study description',
        'View',
        'Laterality',
        'Acquisition',
        'Thickness',
        'Radiological thickness',
        'Force',
        'Mag',
        'Area',
        'Mode',
        'Target',
        'Filter',
        'Focal spot size',
        'kVp',
        'mA',
        'ms',
        'uAs',
        'ESD',
        'AGD',
        '% Fibroglandular tissue',
        'Exposure mode description'
        ]

    writer.writerow(headings)
    
    for i, study in enumerate(s):
        e = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()
        for exp in e:

            if pid and (name or patid):
                try:
                    exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get()
                except ObjectDoesNotExist:
                    patient_birth_date = None
                    if name:
                        patient_name = None
                    if patid:
                        patient_id = None
                else:
                    patient_birth_date = return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_birth_date')
                    if name:
                        patient_name = export_safe(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_name'))
                    if patid:
                        patient_id = export_safe(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_id'))

            try:
                exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get()
            except ObjectDoesNotExist:
                institution_name = None
                manufacturer = None
                station_name = None
                display_name = None
            else:
                institution_name = export_safe(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(), 'institution_name'))
                manufacturer = export_safe(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(), 'manufacturer'))
                station_name = export_safe(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(), 'station_name'))
                display_name = export_safe(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get().unique_equipment_name, 'display_name'))

            try:
                exp.projection_xray_radiation_dose.general_study_module_attributes.patientstudymoduleattr_set.get()
            except ObjectDoesNotExist:
                patient_age_decimal = None
            else:
                patient_age_decimal = return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientstudymoduleattr_set.get(), 'patient_age_decimal')

            try:
                exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get()
            except ObjectDoesNotExist:
                patient_sex = None
            else:
                patient_sex = return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_sex')

            try:
                exp.irradeventxraymechanicaldata_set.get()
            except ObjectDoesNotExist:
                compression_thickness = None
                compression_force = None
                magnification_factor = None
            else:
                compression_thickness = return_for_export(exp.irradeventxraymechanicaldata_set.get(), 'compression_thickness')
                compression_force = return_for_export(exp.irradeventxraymechanicaldata_set.get(), 'compression_force')
                magnification_factor = return_for_export(exp.irradeventxraymechanicaldata_set.get(), 'magnification_factor')

            try:
                exp.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
            except ObjectDoesNotExist:
                radiological_thickness = None
            else:
                radiological_thickness = return_for_export(exp.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'radiological_thickness')

            try:
                exp.irradeventxraysourcedata_set.get()
            except ObjectDoesNotExist:
                collimated_field_area = None
                exposure_control_mode = None
                anode_target_material = None
                focal_spot_size = None
                average_xray_tube_current = None
                exposure_time = None
                average_glandular_dose = None
            else:
                collimated_field_area = return_for_export(exp.irradeventxraysourcedata_set.get(), 'collimated_field_area')
                exposure_control_mode = return_for_export(exp.irradeventxraysourcedata_set.get(), 'exposure_control_mode')
                anode_target_material = return_for_export(exp.irradeventxraysourcedata_set.get(), 'anode_target_material')
                focal_spot_size = return_for_export(exp.irradeventxraysourcedata_set.get(), 'focal_spot_size')
                average_xray_tube_current = return_for_export(exp.irradeventxraysourcedata_set.get(), 'average_xray_tube_current')
                exposure_time = return_for_export(exp.irradeventxraysourcedata_set.get(), 'exposure_time')
                average_glandular_dose = return_for_export(exp.irradeventxraysourcedata_set.get(), 'average_glandular_dose')

            try:
                exp.irradeventxraysourcedata_set.get().xrayfilters_set.get()
            except ObjectDoesNotExist:
                xray_filter_material = None
            else:
                xray_filter_material = return_for_export(exp.irradeventxraysourcedata_set.get().xrayfilters_set.get(), 'xray_filter_material')

            try:
                exp.irradeventxraysourcedata_set.get().kvp_set.get()
            except ObjectDoesNotExist:
                kvp = None
            else:
                kvp = return_for_export(exp.irradeventxraysourcedata_set.get().kvp_set.get(), 'kvp')

            try:
                exp.irradeventxraysourcedata_set.get().exposure_set.get()
            except ObjectDoesNotExist:
                exposure = None
            else:
                exposure = return_for_export(exp.irradeventxraysourcedata_set.get().exposure_set.get(), 'exposure')

            row = []
            if pid and name:
                row += [patient_name]
            if pid and patid:
                row += [patient_id]
            row += [
                institution_name,
                manufacturer,
                station_name,
                display_name,
                export_safe(exp.projection_xray_radiation_dose.general_study_module_attributes.accession_number),
                exp.projection_xray_radiation_dose.general_study_module_attributes.study_instance_uid,
                exp.projection_xray_radiation_dose.general_study_module_attributes.study_date,
                exp.date_time_started,
            ]
            if pid and (name or patid):
                row += [
                    patient_birth_date,
                ]
            row += [
                patient_age_decimal,
                patient_sex,
                exp.projection_xray_radiation_dose.irradeventxraydata_set.count(),
                export_safe(exp.projection_xray_radiation_dose.general_study_module_attributes.study_description),
                exp.image_view,
                exp.laterality,
                export_safe(exp.acquisition_protocol),
                compression_thickness,
                radiological_thickness,
                compression_force,
                magnification_factor,
                collimated_field_area,
                export_safe(exposure_control_mode),
                anode_target_material,
                xray_filter_material,
                focal_spot_size,
                kvp,
                average_xray_tube_current,
                exposure_time,
                exposure,
                exp.entrance_exposure_at_rp,
                average_glandular_dose,
                exp.percent_fibroglandular_tissue,
                export_safe(exp.comment),
                ]
            writer.writerow(row)
        tsk.progress = "{0} of {1}".format(i+1, numresults)
        tsk.save()

    tsk.progress = 'All study data written.'
    tsk.save()

    csvfilename = "mgexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

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

