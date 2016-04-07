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
..  module:: xlsx.
    :synopsis: Module to export database data to multi-sheet Microsoft XLSX files.

..  moduleauthor:: Ed McDonagh

"""


from xlsxwriter.workbook import Workbook
from celery import shared_task
from django.conf import settings

def _ct_common_get_data(exams, pid, name, patid):
    from django.core.exceptions import ObjectDoesNotExist
    from remapp.tools.get_values import return_for_export

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
        not_patient = None
    else:
        patient_sex = return_for_export(exams.patientmoduleattr_set.get(), 'patient_sex')
        not_patient = return_for_export(exams.patientmoduleattr_set.get(), 'not_patient_indicator')

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
        exams.accession_number,
        exams.operator_name,
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
        exams.study_description,
        exams.requested_procedure_code_meaning,
        total_number_of_irradiation_events,
        ct_dose_length_product_total,
    ]

    return examdata

def _ct_get_series_data(s):
    from django.core.exceptions import ObjectDoesNotExist
    from remapp.tools.get_values import return_for_export
    seriesdata = [
        s.acquisition_protocol,
        str(s.ct_acquisition_type),
        str(s.exposure_time),
        str(s.scanninglength_set.get().scanning_length),
        str(s.nominal_single_collimation_width),
        str(s.nominal_total_collimation_width),
        str(s.pitch_factor),
        str(s.number_of_xray_sources),
        str(s.mean_ctdivol),
        str(s.dlp),
        ]
    if s.number_of_xray_sources > 1:
        for source in s.ctxraysourceparameters_set.all():
            seriesdata += [
                str(source.identification_of_the_xray_source),
                str(source.kvp),
                str(source.maximum_xray_tube_current),
                str(source.xray_tube_current),
                str(source.exposure_time_per_rotation),
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

            seriesdata += [
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
                seriesdata += ['n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a',]
    seriesdata += [
        s.xray_modulation_type,
        str(s.comment),
        ]
    return seriesdata



@shared_task
def ctxlsx(filterdict, pid=False, name=None, patid=None, user=None):
    """Export filtered CT database data to multi-sheet Microsoft XSLX files.

    :param filterdict: Query parameters from the CT filtered page URL.
    :type filterdict: HTTP get
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import ct_acq_filter

    tsk = Exports.objects.create()

    tsk.task_id = ctxlsx.request.id
    tsk.modality = "CT"
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

    # Get the data!
    e = ct_acq_filter(filterdict, pid=pid).qs

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
        'Model',
        'Station name',
        'Display name',
        'Accession number',
        'Operator',
        'Study Date',
    ]
    if pid and (name or patid):
        commonheaders += [
            'Date of birth',
        ]
    commonheaders += [
        'Age',
        'Sex',
        'Height', 
        'Mass (kg)', 
        'Test patient?',
        'Study description',
        'Requested procedure',
        'No. events',
        'DLP total (mGy.cm)',
        ]
    protocolheaders = commonheaders + [
        'Protocol',
        'Type',
        'Exposure time',
        'Scanning length',
        'Slice thickness',
        'Total collimation',
        'Pitch',
        'No. sources',
        'CTDIvol',
        'DLP',
        'S1 name',
        'S1 kVp',
        'S1 max mA',
        'S1 mA',
        'S1 Exposure time/rotation',
        'S2 name',
        'S2 kVp',
        'S2 max mA',
        'S2 mA',
        'S2 Exposure time/rotation',
        'mA Modulation type',
        'Comments',
        ]
        
    # Generate list of protocols in queryset and create worksheets for each
    tsk.progress = 'Generating list of protocols in the dataset...'
    tsk.save()

    sheetlist = {}
    protocolslist = []
    for exams in e:
        for s in exams.ctradiationdose_set.get().ctirradiationeventdata_set.all():
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

    from django.db.models import Max
    max_events = e.aggregate(Max('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events'))

    alldataheaders = commonheaders

    tsk.progress = 'Generating headers for the all data sheet...'
    tsk.save()

    for h in xrange(max_events['ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events__max']):
        alldataheaders += [
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
            'E' + str(h+1) + ' Comments',
            ]
    wsalldata.write_row('A1', alldataheaders)
    wsalldata.set_column(date_column, date_column, 10) # allow date to be displayed.
    numcolumns = (22 * max_events['ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events__max']) + date_column + 8
    numrows = e.count()
    wsalldata.autofilter(0,0,numrows,numcolumns)

    for row,exams in enumerate(e):

        tsk.progress = 'Writing study {0} of {1} to All data sheet and individual protocol sheets'.format(row + 1, numrows)
        tsk.save()

        allexamdata = _ct_common_get_data(exams, pid, name, patid)

        # Now we need to write a sheet per series protocol for each 'exams'.
        
        for s in exams.ctradiationdose_set.get().ctirradiationeventdata_set.all():
            # Add series to all data
            allexamdata += _ct_get_series_data(s)
            # Add series data to series tab
            protocol = s.acquisition_protocol
            if not protocol:
                protocol = u'Unknown'
            tabtext = protocol.lower().replace(" ","_")
            translation_table = {ord('['):ord('('), ord(']'):ord(')'), ord(':'):ord(';'), ord('*'):ord('#'), ord('?'):ord(';'), ord('/'):ord('|'), ord('\\'):ord('|')}
            tabtext = tabtext.translate(translation_table) # remove illegal characters
            tabtext = tabtext[:31]
            sheetlist[tabtext]['count'] += 1
            
            examdata = _ct_common_get_data(exams, pid, name, patid)
            examdata += _ct_get_series_data(s)

            sheetlist[tabtext]['sheet'].write_row(sheetlist[tabtext]['count'],0,examdata)

        wsalldata.write_row(row+1,0, allexamdata)


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

    xlsxfilename = "ctexport{0}.xlsx".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(xlsxfilename,File(tmpxlsx))
    except OSError as e:
        tsk.progress = "Errot saving export file - please contact an administrator. Error({0}): {1}".format(e.errno, e.strerror)
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

