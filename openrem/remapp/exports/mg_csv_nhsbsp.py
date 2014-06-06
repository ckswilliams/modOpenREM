import csv
from celery import shared_task


@shared_task
def mg_csv_nhsbsp(filterdict):
    """Export filtered mammography database data to a single-sheet CSV file.

    :param request: Query parameters from the mammo filtered page URL.
    :type request: HTTP get
    
    """

    import os, datetime
    from django.conf import settings
    from remapp.models import General_study_module_attributes
    from remapp.models import Exports
    from remapp.interface.mod_filters import MGSummaryListFilter

    tsk = Exports.objects.create()

    tsk.task_id = exportMG2excel.request.id
    tsk.modality = "MG"
    tsk.export_type = "NHSBSP CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = 'Query filters imported, task started'
    tsk.status = 'CURRENT'
    tsk.save()

    csvfilename = "mg_nhsbsp_{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))
    tsk.progress = 'Query filters imported, task started'
    csvfile = open(os.path.join(settings.MEDIA_ROOT,csvfilename),"w")
    tsk.filename = csvfilename
    tsk.save()
    
    writer = csv.writer(csvfile)
    
    tsk.progress = 'CSV file created'
    tsk.save()
        
    # Get the data!
    
    s = General_study_module_attributes.objects.filter(modality_type__exact = 'MG')
    f = MGSummaryListFilter.base_filters

    for filt in f:
        if filt in filterdict and filterdict[filt]:
            s = s.filter(**{f[filt].name + '__' + f[filt].lookup_type : filterdict[filt]})
    
    tsk.progress = 'Required study filter complete.'
    tsk.save()
        
    numresults = s.count()

    tsk.num_records = numresults
    tsk.save()

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
        tsk.progress = "{0} of {1}".format(i+1, numresults)
        tsk.save()

    tsk.progress = 'All study data written.'
    tsk.status = 'COMPLETE'
    tsk.save()
    
if __name__ == "__main__":
    import sys
    sys.exit(mg_csv_nhsbsp(filterdict))

