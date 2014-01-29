def _patientstudymoduleattributes(exam, height, weight): # C.7.2.2
    patientatt = exam.patient_study_module_attributes_set.get()
    if height and not patientatt.patient_size:
        patientatt.patient_size = height
        print "Inserted height of " + height
    if weight and not patientatt.patient_weight:
        patientatt.patient_weight = weight
        print "Inserted weight of " + weight
    patientatt.save()


def _ptsizeinsert(accno,height,weight):
    from django.db import models
    from remapp.models import General_study_module_attributes
    from django import db
    
    if (height or weight) and accno:
        e = General_study_module_attributes.objects.filter(accession_number__exact = accno)
        if e:
            for exam in e:
                print accno + ":"
                _patientstudymoduleattributes(exam, height, weight)
        else:
            print "Accession number " + accno + " not found in db"
    db.reset_queries()
       

    
def _add_project_to_path():
    import os, sys
    # Add project to path, assuming openrem app has been installed within project
    basepath = os.path.dirname(__file__)
    projectpath = os.path.abspath(os.path.join(basepath, "..","openrem"))
    if projectpath not in sys.path:
        sys.path.append(projectpath)


def _ptsizecsv(csv_file):
    """ Import patient height and weight data from csv RIS exports
        
    Arguments:
    filename : relative or absolute path to csv file.
    
    Limitations:
    Currently expects a column named 'PACS_SPS_ID' containing the accession
    number as held by the database, and two columns named 'HEIGHT' and 'WEIGHT'.
    """

    import os, csv
    _add_project_to_path()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'openrem.settings'
    
    f = open(csv_file, 'rb')
    try:
        dataset = csv.DictReader(f)        
        for line in dataset:
            _ptsizeinsert(line['PACS_SPS_ID'], line['HEIGHT'], line['WEIGHT'])
    finally:
        f.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit('Error: Supply one argument: the csv file')
    sys.exit(_ptsizecsv(sys.argv[1]))
