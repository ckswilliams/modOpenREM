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
def exportFL2excel(request):
    """Export filtered fluoro database data to a single-sheet CSV file.

    :param request: Query parameters from the fluoro filtered page URL.
    :type request: HTTP get
    
    """

    from django.http import HttpResponse
    from django.shortcuts import render
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from remapp.models import General_study_module_attributes


    # Get the database query filters
    f_date_after = request.GET.get('date_after')
    f_date_before = request.GET.get('date_before')
    f_institution_name = request.GET.get('general_equipment_module_attributes__institution_name')
    f_study_description = request.GET.get('study_description')
    f_age_min = request.GET.get('patient_age_min')
    f_age_max = request.GET.get('patient_age_max')
    f_performing_physician_name = request.GET.get('performing_physician_name')
    f_manufacturer = request.GET.get('general_equipment_module_attributes__manufacturer')
    f_manufacturer_model_name = request.GET.get('general_equipment_module_attributes__manufacturer_model_name')
    f_station_name = request.GET.get('general_equipment_module_attributes__station_name')
    f_accession_number = request.GET.get('accession_number')
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    # Get the data!
    from remapp.models import General_study_module_attributes

    e = General_study_module_attributes.objects.filter(modality_type__exact = 'RF')
    
    if f_institution_name:
        e = e.filter(general_equipment_module_attributes__institution_name__icontains = f_institution_name)
    if f_study_description:
        e = e.filter(study_description__icontains = f_study_description)
    if f_performing_physician_name:
        e = e.filter(performing_physician_name__icontains = f_performing_physician_name)
    if f_manufacturer:
        e = e.filter(general_equipment_module_attributes__manufacturer__icontains = f_manufacturer)
    if f_manufacturer_model_name:
        e = e.filter(general_equipment_module_attributes__manufacturer_model_name__icontains = f_manufacturer_model_name)
    if f_station_name:
        e = e.filter(general_equipment_module_attributes__station_name__icontains = f_station_name)
    if f_accession_number:
        e = e.filter(accession_number__icontains = f_accession_number)
    if f_date_after:
        e = e.filter(study_date__gte = f_date_after)
    if f_date_before:
        e = e.filter(study_date__lte = f_date_before)
    if f_age_min:
        e = e.filter(patient_study_module_attributes__patient_age_decimal__gte = f_age_min)
    if f_age_max:
        e = e.filter(patient_study_module_attributes__patient_age_decimal__lte = f_age_max)

    writer = csv.writer(response)
    writer.writerow([
        'Manufacturer', 
        'Model name',
        'Institution name', 
        'Study date',
        'Accession number',
        'Patient age', 
        'Patient height', 
        'Patient mass (kg)', 
        'Study description',
        'Number of events',
        'DAP total (Gy.m2)',
        'RP dose total (Gy)',
        'Fluoro DAP total (Gy.m2)',
        'Fluoro RP dose total (Gy)',
        'Total fluoro time (ms)',
        'Acquisition DAP total (Gy.m2)',
        'Acquisition RP dose total (Gy)',
        'Total acquisition time (ms)',
        'RP definition',
        'Physician',
        'Operator'])
    for exams in e:
        writer.writerow([
            exams.general_equipment_module_attributes_set.get().manufacturer, 
            exams.projection_xray_radiation_dose_set.get().observer_context_set.get().device_observer_name,
            exams.general_equipment_module_attributes_set.get().institution_name,
            exams.study_date,
            exams.accession_number, 
            exams.patient_study_module_attributes_set.get().patient_age_decimal,
            exams.patient_study_module_attributes_set.get().patient_size,
            exams.patient_study_module_attributes_set.get().patient_weight,
            exams.study_description,
            exams.projection_xray_radiation_dose_set.get().irradiation_event_xray_data_set.count(),
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().dose_area_product_total,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().dose_rp_total,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().fluoro_dose_area_product_total,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().fluoro_dose_rp_total,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().total_fluoro_time,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().acquisition_dose_area_product_total,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().acquisition_dose_rp_total,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().total_acquisition_time,
            exams.projection_xray_radiation_dose_set.get().accumulated_xray_dose_set.get().accumulated_projection_xray_dose_set.get().reference_point_definition_code,
            exams.performing_physician_name,
            exams.operator_name,
            ])
    return response

from celery import shared_task, current_task



@shared_task
def exportCT2excel(query_filters):
    """Export filtered CT database data to a single-sheet CSV file.

    :param request: Query parameters from the CT filtered page URL.
    :type request: HTTP get
    
    """

    from django.http import HttpResponse
    from django.shortcuts import render
    from django.shortcuts import render_to_response
    from django.conf import settings
    from remapp.models import General_study_module_attributes
    import os

    current_task.update_state(state='PROGRESS', meta={'status': 'Query filters imported, task started'})

    # Create the HttpResponse object with the appropriate CSV header.
#    response = HttpResponse(content_type="text/csv")
#    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    csvfilename = "ctexport.csv"
    csvfile = open(os.path.join(settings.MEDIA_ROOT,csvfilename),"w")

    writer = csv.writer(csvfile)
    
    current_task.update_state(state='PROGRESS', meta={'status': 'CSV file created'})
    
    # Get the data!
    from remapp.models import General_study_module_attributes

    e = General_study_module_attributes.objects.filter(modality_type__exact = 'CT')
    
    if query_filters['institution_name']:
        e = e.filter(general_equipment_module_attributes__institution_name__icontains = query_filters['institution_name'])
    if query_filters['study_description']:
        e = e.filter(study_description__icontains = query_filters['study_description'])
    if query_filters['manufacturer']:
        e = e.filter(general_equipment_module_attributes__manufacturer__icontains = query_filters['manufacturer'])
    if query_filters['manufacturer_model_name']:
        e = e.filter(general_equipment_module_attributes__manufacturer_model_name__icontains = query_filters['manufacturer_model_name'])
    if query_filters['station_name']:
        e = e.filter(general_equipment_module_attributes__station_name__icontains = query_filters['station_name'])
    if query_filters['accession_number']:
        e = e.filter(accession_number__icontains = query_filters['accession_number'])
    if query_filters['date_after']:
        e = e.filter(study_date__gte = query_filters['date_after'])
    if query_filters['date_before']:
        e = e.filter(study_date__lte = query_filters['date_before'])
    if query_filters['age_min']:
        e = e.filter(patient_study_module_attributes__patient_age_decimal__gte = query_filters['age_min'])
    if query_filters['age_max']:
        e = e.filter(patient_study_module_attributes__patient_age_decimal__lte = query_filters['age_max'])

    current_task.update_state(state='PROGRESS', meta={'status': 'Required study filter complete.'})

        
    numresults = e.count()

    current_task.update_state(state='PROGRESS', meta={'status': '{0} studies in query.'.format(numresults)})

#    writer.writerow([f_institution_name,f_study_date_0,f_study_date_1,f_study_description,f_manufacturer,f_model,f_device_observer_name])
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
        'DLP total (mGy.cm)',
        ]

    from django.db.models import Max
    max_events = e.aggregate(Max('ct_radiation_dose__ct_accumulated_dose_data__total_number_of_irradiation_events'))

    for h in xrange(max_events['ct_radiation_dose__ct_accumulated_dose_data__total_number_of_irradiation_events__max']):
        headers += [
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
    writer.writerow(headers)

    current_task.update_state(state='PROGRESS', meta={'status': 'CSV header row written.'})

    for exams in e:
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
            exams.ct_radiation_dose_set.get().ct_accumulated_dose_data_set.get().total_number_of_irradiation_events,
            exams.ct_radiation_dose_set.get().ct_accumulated_dose_data_set.get().ct_dose_length_product_total,
			]
        for s in exams.ct_radiation_dose_set.get().ct_irradiation_event_data_set.all():
            examdata += [
                s.acquisition_protocol,
                s.ct_acquisition_type,
                s.exposure_time,
                s.scanning_length_set.get().scanning_length,
                s.nominal_single_collimation_width,
                s.nominal_total_collimation_width,
                s.pitch_factor,
                s.number_of_xray_sources,
                s.mean_ctdivol,
                s.dlp,
                ]
            if s.number_of_xray_sources > 1:
                for source in s.ct_xray_source_parameters_set.all():
                    examdata += [
                        source.identification_of_the_xray_source,
                        source.kvp,
                        source.maximum_xray_tube_current,
                        source.xray_tube_current,
                        source.exposure_time_per_rotation,
                        ]
            else:
                try:
                    examdata += [
                        s.ct_xray_source_parameters_set.get().identification_of_the_xray_source,
                        s.ct_xray_source_parameters_set.get().kvp,
                        s.ct_xray_source_parameters_set.get().maximum_xray_tube_current,
                        s.ct_xray_source_parameters_set.get().xray_tube_current,
                        s.ct_xray_source_parameters_set.get().exposure_time_per_rotation,
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
        current_task.update_state(state='PROGRESS', meta={'status': 'All study data written.'})

def exportMG2excel(request):
    """Export filtered mammography database data to a single-sheet CSV file.

    :param request: Query parameters from the mammo filtered page URL.
    :type request: HTTP get
    
    """

    from django.http import HttpResponse
    from django.shortcuts import render
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from remapp.models import General_study_module_attributes

    f_institution_name = request.GET.get('general_equipment_module_attributes__institution_name')
    f_date_after = request.GET.get('date_after')
    f_date_before = request.GET.get('date_before')
    f_procedure_code_meaning = request.GET.get('procedure_code_meaning')
    f_age_min = request.GET.get('patient_age_min')
    f_age_max = request.GET.get('patient_age_max')
    f_manufacturer = request.GET.get('general_equipment_module_attributes__manufacturer')
    f_manufacturer_model_name = request.GET.get('general_equipment_module_attributes__manufacturer_model_name')
    f_station_name = request.GET.get('general_equipment_module_attributes__station_name')
    f_accession_number = request.GET.get('accession_number')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    # Get the data!
    from remapp.models import General_study_module_attributes

    s = General_study_module_attributes.objects.filter(modality_type__exact = 'MG')
    
    if f_institution_name:
        s = s.filter(general_equipment_module_attributes__institution_name__icontains = f_institution_name)
    if f_procedure_code_meaning:
        s = s.filter(procedure_code_meaning__icontains = f_procedure_code_meaning)
    if f_manufacturer:
        s = s.filter(general_equipment_module_attributes__manufacturer__icontains = f_manufacturer)
    if f_manufacturer_model_name:
        s = s.filter(general_equipment_module_attributes__manufacturer_model_name__icontains = f_manufacturer_model_name)
    if f_station_name:
        s = s.filter(general_equipment_module_attributes__station_name__icontains = f_station_name)
    if f_accession_number:
        s = s.filter(accession_number__icontains = f_accession_number)
    if f_date_after:
        s = s.filter(study_date__gte = f_date_after)
    if f_date_before:
        s = s.filter(study_date__lte = f_date_before)
    if f_age_min:
        s = s.filter(patient_study_module_attributes__patient_age_decimal__gte = f_age_min)
    if f_age_max:
        s = s.filter(patient_study_module_attributes__patient_age_decimal__lte = f_age_max)

    writer = csv.writer(response)
    writer.writerow([
        'Institution name', 
        'Manufacturer', 
        'Station name',
        'Accession number',
        'Study UID',
        'Study date',
        'Study time',
        'Patient age', 
        'Patient sex', 
        'Number of events',
        'View',
        'Aquisition',
        'Thickness',
        'Radiological Thickness',
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
        '% Fibroglandular Tissue'
        'Exposure Mode Description'
        ])
    
    for study in s:
        e = study.projection_xray_radiation_dose_set.get().irradiation_event_xray_data_set.all()
        for exp in e:
            writer.writerow([
                exp.projection_xray_radiation_dose.general_study_module_attributes.general_equipment_module_attributes_set.get().institution_name,
                exp.projection_xray_radiation_dose.general_study_module_attributes.general_equipment_module_attributes_set.get().manufacturer, 
                exp.projection_xray_radiation_dose.general_study_module_attributes.general_equipment_module_attributes_set.get().station_name,
                exp.projection_xray_radiation_dose.general_study_module_attributes.accession_number, 
                exp.projection_xray_radiation_dose.general_study_module_attributes.study_instance_uid,
                exp.projection_xray_radiation_dose.general_study_module_attributes.study_date,
                exp.date_time_started,
                exp.projection_xray_radiation_dose.general_study_module_attributes.patient_study_module_attributes_set.get().patient_age_decimal,
                exp.projection_xray_radiation_dose.general_study_module_attributes.patient_module_attributes_set.get().patient_sex,
                exp.projection_xray_radiation_dose.irradiation_event_xray_data_set.count(),
                exp.image_view,
                exp.acquisition_protocol,
                exp.irradiation_event_xray_mechanical_data_set.get().compression_thickness,
                exp.irradiation_event_xray_mechanical_data_set.get().dose_related_distance_measurements_set.get().radiological_thickness,
                exp.irradiation_event_xray_mechanical_data_set.get().compression_force,
                exp.irradiation_event_xray_mechanical_data_set.get().magnification_factor,
                exp.irradiation_event_xray_source_data_set.get().collimated_field_area,
                exp.irradiation_event_xray_source_data_set.get().exposure_control_mode,
                exp.irradiation_event_xray_source_data_set.get().anode_target_material,
                exp.irradiation_event_xray_source_data_set.get().xray_filters_set.get().xray_filter_material,
                exp.irradiation_event_xray_source_data_set.get().focal_spot_size,
                exp.irradiation_event_xray_source_data_set.get().kvp_set.get().kvp,
                exp.irradiation_event_xray_source_data_set.get().average_xray_tube_current,
                exp.irradiation_event_xray_source_data_set.get().exposure_time,
                exp.irradiation_event_xray_source_data_set.get().exposure_set.get().exposure,
                exp.entrance_exposure_at_rp,
                exp.irradiation_event_xray_source_data_set.get().average_glandular_dose,
                exp.percent_fibroglandular_tissue,
                exp.comment,
                ])
    return response


def getQueryFilters(request):
    from django.template import RequestContext

    query_filters = {
        'institution_name'        : request.GET.get('general_equipment_module_attributes__institution_name'),
        'date_after'              : request.GET.get('date_after'),
        'date_before'             : request.GET.get('date_before'),
        'study_description'       : request.GET.get('study_description'),
        'age_min'                 : request.GET.get('patient_age_min'),
        'age_max'                 : request.GET.get('patient_age_max'),
        'manufacturer'            : request.GET.get('general_equipment_module_attributes__manufacturer'),
        'manufacturer_model_name' : request.GET.get('general_equipment_module_attributes__manufacturer_model_name'),
        'station_name'            : request.GET.get('general_equipment_module_attributes__station_name'),
        'accession_number'        : request.GET.get('accession_number'),
    }
    return query_filters



