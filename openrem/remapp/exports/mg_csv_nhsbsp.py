def exportMG2NHSBSP(request):
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
    response = HttpResponse(mimetype='text/csv')
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
        'Survey number',
        'Patient number',
        'View code',
        'kV',
        'Anode',
        'Filter',
        'Thickness',
        'mAs',
        'large cassette used',
        'auto/man',
        'Auto mode',
        'Density setting',
        'Age',
        'Comment',
        'AEC density mode',		
        ])
    patNum = 0
    for study in s:
        e = study.projection_xray_radiation_dose_set.get().irradiation_event_xray_data_set.all()
        patNum = patNum + 1
        for exp in e:
            viewCode = str(exp.laterality)
            viewCode = viewCode[:1]
            if str(exp.image_view) == 'cranio-caudal':
			    viewCode = viewCode + 'CC'
            elif str(exp.image_view) == 'medio-lateral oblique':
                viewCode = viewCode + 'OB'
            else:
                viewCode = viewCode + str(exp.image_view)
            target = str(exp.irradiation_event_xray_source_data_set.get().anode_target_material)
            if "TUNGSTEN" in target.upper():
                target = 'W'
            elif "MOLY" in target.upper():
			    target = 'Mo'
            elif "RHOD" in target.upper():
                target = 'Rh'
            filterMat = str(exp.irradiation_event_xray_source_data_set.get().xray_filters_set.get().xray_filter_material)
            if "ALUM" in filterMat.upper():
                filterMat = 'Al'
            elif "MOLY" in filterMat.upper():
                filterMat = 'Mo'
            elif "RHOD" in filterMat.upper():
                filterMat = 'Rh'
            elif "SILV" in filterMat.upper():
                filterMat = 'Ag'
            automan = str(exp.irradiation_event_xray_source_data_set.get().exposure_control_mode)
            if "AUTO" in automan.upper():
                automan = 'AUTO'
            elif "MAN" in automan.upper():
                automan = "MANUAL"
			
            writer.writerow([
                '1',
                patNum,
                viewCode,
                exp.irradiation_event_xray_source_data_set.get().kvp_set.get().kvp,
                target,
                filterMat,
                exp.irradiation_event_xray_mechanical_data_set.get().compression_thickness,
                exp.irradiation_event_xray_source_data_set.get().exposure_set.get().exposure / 1000,
                '', # not applicable to FFDM
                automan,				
                exp.irradiation_event_xray_source_data_set.get().exposure_control_mode,
                '', # no consistent behaviour for recording density setting on FFDM units
                exp.projection_xray_radiation_dose.general_study_module_attributes.patient_study_module_attributes_set.get().patient_age_decimal,
                '', # not in DICOM headers
                '', # no consistent behaviour for recording density mode on FFDM units
                ])
    return response
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit('Error: Supply exactly one argument - the DICOM RDSR file')

    sys.exit(rdsr(sys.argv[1]))

