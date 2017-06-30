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
..  module:: not_patient_indicators.
    :synopsis: Looks for indications that a study might be a test or QA study.

..  moduleauthor:: Ed McDonagh

"""


def get_not_pt(dataset):
    """Looks for indications that a study might be a test or QA study.
    
    Some values that might indicate a study was for QA or similar purposes
    are not recorded in the database, for example patient name. Therefore
    this module attempts to find such indications and creates an xml
    style string that can be recorded in the database on study import.

    :param dataset:     The DICOM dataset.
    :type dataset:      dataset
    :returns:           str. -- xml style string if any trigger values are found.
    """
    import fnmatch
    from remapp.tools.get_values import get_value_kw
    from remapp.models import NotPatientIndicatorsID, NotPatientIndicatorsName

    patient_id = get_value_kw('PatientID', dataset)
    patient_name = get_value_kw('PatientName', dataset)

    id_indicators = NotPatientIndicatorsID.objects.all()
    name_indicators = NotPatientIndicatorsName.objects.all()

    id_contains = []
    name_contains = []

    if patient_id:
        for pattern in id_indicators:
            if fnmatch.fnmatch(patient_id.lower(), pattern.lower()):
                id_contains += pattern

    if patient_name:
        for pattern in name_indicators:
            if fnmatch.fnmatch(patient_name.lower(), pattern.lower()):
                name_contains += pattern

    if id_contains or name_contains:
        return u'IDs: {0} | Names: {1}'.format(unicode(id_contains)[1:-1], unicode(name_contains)[1:-1])

        # return u'<IDContains Data="{0}" /> <NameContains Data="{1}" />'.format(str(id_contains)[1:-1],
        #                                                                        str(name_contains)[1:-1])
