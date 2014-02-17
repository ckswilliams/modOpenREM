#!/usr/local/bin/python

def _patientstudymoduleattributes(exam, height, weight): # C.7.2.2
    patientatt = exam.patient_study_module_attributes_set.get()
    if height and not patientatt.patient_size:
        patientatt.patient_size = height
        print "Inserted height of " + height
    if weight and not patientatt.patient_weight:
        patientatt.patient_weight = weight
        print "Inserted weight of " + weight
    patientatt.save()


def _ptsizeinsert(accno,height,weight,siuid):
    from django.db import models
    from remapp.models import General_study_module_attributes
    from django import db
    
    if (height or weight) and accno:
        if not siuid:
            e = General_study_module_attributes.objects.filter(accession_number__exact = accno)
        else:
            e = General_study_module_attributes.objects.filter(study_instance_uid__exact = accno)
        if e:
            for exam in e:
                print accno + ":"
                _patientstudymoduleattributes(exam, height, weight)
        else:
            print "Accession number " + accno + " not found in db"
    db.reset_queries()
       

    
def _ptsizecsv():
    """ Import patient height and weight data from csv RIS exports
        
    Arguments:
    filename : relative or absolute path to csv file.
    
    Limitations:
    Currently expects a column named 'PACS_SPS_ID' containing the accession
    number as held by the database, and two columns named 'HEIGHT' and 'WEIGHT'.
    """

    import os, csv
    import argparse
    
    # Required and optional arguments
    parser = argparse.ArgumentParser(description="Import height and weight data into an OpenREM database. If either is missing just add a blank column with appropriate title.")
    parser.add_argument("-u", "--si-uid", action="store_true", help="Use Study Instance UID instead of Accession Number")
    parser.add_argument("csvfile", help="csv file containing the height and/or weight information and study identifier")
    parser.add_argument("id", help="Column title for the accession number or study instance UID")
    parser.add_argument("height", help="Column title for the patient height (DICOM size)")
    parser.add_argument("weight", help="Column title for the patient weight")
    args=parser.parse_args()
    
    # This section attempts to place the openrem folder onto the python path
    # so that openrem.settings can be found.
    sitepaths = []
    openrempathset=0
    for paths in sys.path:
        if paths.endswith('site-packages'):
            sitepaths.append(paths)
        if paths.endswith('openrem'):
            openrempathset = 1
        
    if sitepaths and not openrempathset:
        for paths in sitepaths:
            sys.path.insert(1,os.path.join(paths,'openrem'))

    os.environ['DJANGO_SETTINGS_MODULE'] = 'openrem.settings'
    
    f = open(args.csvfile, 'rb')
    try:
        dataset = csv.DictReader(f)        
        for line in dataset:
            _ptsizeinsert(line[args.id], line[args.height], line[args.weight], args.si_uid)
    finally:
        f.close()

if __name__ == "__main__":
    import sys
    sys.exit(_ptsizecsv())
