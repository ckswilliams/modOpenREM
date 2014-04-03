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
..  module:: ptsizecsv2db.
    :synopsis: Use to import height and weight data from csv file to existing studies in the database.

..  moduleauthor:: Ed McDonagh

"""

def _patientstudymoduleattributes(exam, height, weight, verbose): # C.7.2.2
    patientatt = exam.patient_study_module_attributes_set.get()
    if height and not patientatt.patient_size:
        patientatt.patient_size = height
        if verbose:
            print "Inserted height of " + height
    if weight and not patientatt.patient_weight:
        patientatt.patient_weight = weight
        if verbose:
            print "Inserted weight of " + weight
    patientatt.save()


def _ptsizeinsert(accno,height,weight,siuid, verbose):
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
                if verbose:
                    print accno + ": " + request
                _patientstudymoduleattributes(exam, height, weight, verbose)
        elif verbose:
            print "Accession number " + accno + " not found in db"
    db.reset_queries()
       

    
def csv2db(*args, **kwargs):
    """ Import patient height and weight data from csv RIS exports. Can be called from ``openrem_ptsizecsv.py`` script
        
    :param --si-uid: Use Study Instance UID instead of Accession Number. Short form -s.
    :type --si-uid: bool
    :param csvfile: relative or absolute path to csv file
    :type csvfile: str
    :param id: Accession number column header or header if -u or --si-uid is set. Quote if necessary.
    :type id: str
    :param height: Patient height column header. Create if necessary, quote if necessary.
    :type height: str
    :param weight: Patient weight column header. Create if necessary, quote if necessary.
    :type weight: str

    Example::
        
        openrem_ptsizecsv.py -s MyRISExport.csv StudyInstanceUID HEIGHT weight

    """

    import os, sys, csv
    import argparse
    import openrem_settings

    
    # Required and optional arguments
    parser = argparse.ArgumentParser(description="Import height and weight data into an OpenREM database. If either is missing just add a blank column with appropriate title.")
    parser.add_argument("-u", "--si-uid", action="store_true", help="Use Study Instance UID instead of Accession Number")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("csvfile", help="csv file containing the height and/or weight information and study identifier")
    parser.add_argument("id", help="Column title for the accession number or study instance UID")
    parser.add_argument("height", help="Column title for the patient height (DICOM size)")
    parser.add_argument("weight", help="Column title for the patient weight")
    args=parser.parse_args()
    
    openrem_settings.add_project_to_path()
    os.environ['DJANGO_SETTINGS_MODULE'] = '{0}.settings'.format(openrem_settings.name_of_project())
    
    f = open(args.csvfile, 'rb')
    try:
        dataset = csv.DictReader(f)        
        for line in dataset:
            _ptsizeinsert(line[args.id], line[args.height], line[args.weight], args.si_uid, args.verbose)
    finally:
        f.close()

if __name__ == "__main__":
    import sys
    sys.exit(csv2db())
