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
from remapp.exports.export_common import common_headers,  \
    get_common_data, get_anode_target_material, get_xray_filter_info, create_csv, write_export

logger = logging.getLogger(__name__)


def _mg_get_series_data(event):
    """Return the series level data

    :param event: event level object
    :return: series data as list of strings
    """
    try:
        compression_thickness = event.irradeventxraymechanicaldata_set.get().compression_thickness
        compression_force = event.irradeventxraymechanicaldata_set.get().compression_force
        magnification_factor = event.irradeventxraymechanicaldata_set.get().magnification_factor
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
        collimated_field_area = event.irradeventxraysourcedata_set.get().collimated_field_area
        exposure_control_mode = event.irradeventxraysourcedata_set.get().exposure_control_mode
        anode_target_material = get_anode_target_material(event.irradeventxraysourcedata_set.get())
        focal_spot_size = event.irradeventxraysourcedata_set.get().focal_spot_size
        average_xray_tube_current = event.irradeventxraysourcedata_set.get().average_xray_tube_current
        exposure_time = event.irradeventxraysourcedata_set.get().exposure_time
        average_glandular_dose = event.irradeventxraysourcedata_set.get().average_glandular_dose
    except ObjectDoesNotExist:
        collimated_field_area = None
        exposure_control_mode = None
        anode_target_material = None
        focal_spot_size = None
        average_xray_tube_current = None
        exposure_time = None
        average_glandular_dose = None

    try:
        filters, filter_thicknesses = get_xray_filter_info(event.irradeventxraysourcedata_set.get())
    except ObjectDoesNotExist:
        filters = None

    try:
        kvp = event.irradeventxraysourcedata_set.get().kvp_set.get().kvp
    except ObjectDoesNotExist:
        kvp = None

    try:
        exposure = event.irradeventxraysourcedata_set.get().exposure_set.get().exposure
    except ObjectDoesNotExist:
        exposure = None

    series_data = [
        event.image_view,
        event.laterality,
        event.acquisition_protocol,
        compression_thickness,
        radiological_thickness,
        compression_force,
        magnification_factor,
        collimated_field_area,
        exposure_control_mode,
        anode_target_material,
        filters,
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
def exportMG2excel(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered mammography database data to a single-sheet CSV file.

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
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import MGSummaryListFilter, MGFilterPlusPid
    from remapp.tools.get_values import return_for_export, export_csv_prep
    import uuid

    tsk = Exports.objects.create()
    tsk.task_id = exportMG2excel.request.id
    if tsk.task_id is None:  # Required when testing without celery
        tsk.task_id = u'NotCelery-{0}'.format(uuid.uuid4())
    tsk.modality = u"MG"
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
        df_filtered_qs = MGFilterPlusPid(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = u'MG'))
    else:
        df_filtered_qs = MGSummaryListFilter(filterdict, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact = u'MG'))
    studies = df_filtered_qs.qs

    tsk.progress = u'Required study filter complete.'
    tsk.save()
        
    numresults = studies.count()

    tsk.num_records = numresults
    tsk.save()

    headings = common_headers(modality=u"MG", pid=pid, name=name, patid=patid)

    # headings = []
    # if pid and name:
    #     headings += [u'Patient name']
    # if pid and patid:
    #     headings += [u'Patient ID']
    # headings += [
    #     u'Institution name',
    #     u'Manufacturer',
    #     u'Station name',
    #     u'Display name',
    #     u'Accession number',
    #     u'Study UID',
    #     u'Study date',
    #     u'Study time',
    # ]
    # if pid and (name or patid):
    #     headings += [
    #         u'Date of birth',
    #     ]
    # headings += [
    #     u'Patient age',
    #     u'Patient sex',
    #     u'Number of events',
    #     u'Study description',
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

    writer.writerow(headings)
    
    for study_index, exam in enumerate(studies):
        exam_data = get_common_data(u"MG", exam, pid=pid, name=name, patid=patid)
        for series in exam.projectionxrayradiationdose_set.get().irradeventxraydata_set.order_by('id'):
            series_data = _mg_get_series_data(series)
            series_data = list(exam_data) + series_data
            for index, item in enumerate(series_data):
                if item is None:
                    series_data[index] = ''
                if isinstance(item, basestring) and u',' in item:
                    series_data[index] = item.replace(u',', u';')
            writer.writerow([unicode(data_string).encode("utf-8") for data_string in series_data])

            # e = exam.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()
        # for exp in e:
        #
        #     if pid and (name or patid):
        #         try:
        #             exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get()
        #         except ObjectDoesNotExist:
        #             patient_birth_date = None
        #             if name:
        #                 patient_name = None
        #             if patid:
        #                 patient_id = None
        #         else:
        #             patient_birth_date = return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_birth_date')
        #             if name:
        #                 patient_name = export_csv_prep(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_name'))
        #             if patid:
        #                 patient_id = export_csv_prep(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_id'))
        #
        #     try:
        #         exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get()
        #     except ObjectDoesNotExist:
        #         institution_name = None
        #         manufacturer = None
        #         station_name = None
        #         display_name = None
        #     else:
        #         institution_name = export_csv_prep(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(), 'institution_name'))
        #         manufacturer = export_csv_prep(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(), 'manufacturer'))
        #         station_name = export_csv_prep(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(), 'station_name'))
        #         display_name = export_csv_prep(return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get().unique_equipment_name, 'display_name'))
        #
        #     try:
        #         exp.projection_xray_radiation_dose.general_study_module_attributes.patientstudymoduleattr_set.get()
        #     except ObjectDoesNotExist:
        #         patient_age_decimal = None
        #     else:
        #         patient_age_decimal = return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientstudymoduleattr_set.get(), 'patient_age_decimal')
        #
        #     try:
        #         exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get()
        #     except ObjectDoesNotExist:
        #         patient_sex = None
        #     else:
        #         patient_sex = return_for_export(exp.projection_xray_radiation_dose.general_study_module_attributes.patientmoduleattr_set.get(), 'patient_sex')
        #
        #     try:
        #         exp.irradeventxraymechanicaldata_set.get()
        #     except ObjectDoesNotExist:
        #         compression_thickness = None
        #         compression_force = None
        #         magnification_factor = None
        #     else:
        #         compression_thickness = return_for_export(exp.irradeventxraymechanicaldata_set.get(), 'compression_thickness')
        #         compression_force = return_for_export(exp.irradeventxraymechanicaldata_set.get(), 'compression_force')
        #         magnification_factor = return_for_export(exp.irradeventxraymechanicaldata_set.get(), 'magnification_factor')
        #
        #     try:
        #         exp.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get()
        #     except ObjectDoesNotExist:
        #         radiological_thickness = None
        #     else:
        #         radiological_thickness = return_for_export(exp.irradeventxraymechanicaldata_set.get().doserelateddistancemeasurements_set.get(), 'radiological_thickness')
        #
        #     try:
        #         exp.irradeventxraysourcedata_set.get()
        #     except ObjectDoesNotExist:
        #         collimated_field_area = None
        #         exposure_control_mode = None
        #         anode_target_material = None
        #         focal_spot_size = None
        #         average_xray_tube_current = None
        #         exposure_time = None
        #         average_glandular_dose = None
        #     else:
        #         collimated_field_area = return_for_export(exp.irradeventxraysourcedata_set.get(), 'collimated_field_area')
        #         exposure_control_mode = return_for_export(exp.irradeventxraysourcedata_set.get(), 'exposure_control_mode')
        #         anode_target_material = return_for_export(exp.irradeventxraysourcedata_set.get(), 'anode_target_material')
        #         focal_spot_size = return_for_export(exp.irradeventxraysourcedata_set.get(), 'focal_spot_size')
        #         average_xray_tube_current = return_for_export(exp.irradeventxraysourcedata_set.get(), 'average_xray_tube_current')
        #         exposure_time = return_for_export(exp.irradeventxraysourcedata_set.get(), 'exposure_time')
        #         average_glandular_dose = return_for_export(exp.irradeventxraysourcedata_set.get(), 'average_glandular_dose')
        #
        #     try:
        #         exp.irradeventxraysourcedata_set.get().xrayfilters_set.get()
        #     except ObjectDoesNotExist:
        #         xray_filter_material = None
        #     else:
        #         xray_filter_material = return_for_export(exp.irradeventxraysourcedata_set.get().xrayfilters_set.get(), 'xray_filter_material')
        #
        #     try:
        #         exp.irradeventxraysourcedata_set.get().kvp_set.get()
        #     except ObjectDoesNotExist:
        #         kvp = None
        #     else:
        #         kvp = return_for_export(exp.irradeventxraysourcedata_set.get().kvp_set.get(), 'kvp')
        #
        #     try:
        #         exp.irradeventxraysourcedata_set.get().exposure_set.get()
        #     except ObjectDoesNotExist:
        #         exposure = None
        #     else:
        #         exposure = return_for_export(exp.irradeventxraysourcedata_set.get().exposure_set.get(), 'exposure')
        #
        #     row = []
        #     if pid and name:
        #         row += [patient_name]
        #     if pid and patid:
        #         row += [patient_id]
        #     row += [
        #         institution_name,
        #         manufacturer,
        #         station_name,
        #         display_name,
        #         export_csv_prep(exp.projection_xray_radiation_dose.general_study_module_attributes.accession_number),
        #         exp.projection_xray_radiation_dose.general_study_module_attributes.study_instance_uid,
        #         exp.projection_xray_radiation_dose.general_study_module_attributes.study_date,
        #         exp.date_time_started,
        #     ]
        #     if pid and (name or patid):
        #         row += [
        #             patient_birth_date,
        #         ]
        #     row += [
        #         patient_age_decimal,
        #         patient_sex,
        #         exp.projection_xray_radiation_dose.irradeventxraydata_set.count(),
        #         export_csv_prep(exp.projection_xray_radiation_dose.general_study_module_attributes.study_description),
        #         exp.image_view,
        #         exp.laterality,
        #         export_csv_prep(exp.acquisition_protocol),
        #         compression_thickness,
        #         radiological_thickness,
        #         compression_force,
        #         magnification_factor,
        #         collimated_field_area,
        #         export_csv_prep(exposure_control_mode),
        #         anode_target_material,
        #         xray_filter_material,
        #         focal_spot_size,
        #         kvp,
        #         average_xray_tube_current,
        #         exposure_time,
        #         exposure,
        #         exp.entrance_exposure_at_rp,
        #         average_glandular_dose,
        #         exp.percent_fibroglandular_tissue,
        #         export_csv_prep(exp.comment),
        #         ]
        #     writer.writerow(row)
        tsk.progress = u"{0} of {1}".format(study_index + 1, numresults)
        tsk.save()

    tsk.progress = u'All study data written.'
    tsk.save()

    csvfilename = u"mgexport{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    write_export(tsk, csvfilename, tmpfile, datestamp)
