# This Python file uses the following encoding: utf-8
#    OpenREM - Radiation Exposure Monitoring tools for the physicist
#    Copyright (C) 2014  The Royal Marsden NHS Foundation Trust and Jonathan Cole
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
..  module:: mg_csv_nhsbsp.
    :synopsis: Module to export mammography data to CSV files in the NHSBSP format.

..  moduleauthor:: Ed McDonagh and Jonathan Cole

"""

import csv
from celery import shared_task
from django.conf import settings


@shared_task
def mg_csv_nhsbsp(filterdict, user=None):
    """Export filtered mammography database data to a NHSBSP formatted single-sheet CSV file.

    :param filterdict: Dictionary of query parameters from the mammo filtered page URL.
    :type filterdict: dict
    :returns: None - file is saved to disk and location is stored in database
    
    """

    import os, sys, datetime
    from tempfile import TemporaryFile
    from django.conf import settings
    from django.core.files import File
    from django.shortcuts import redirect
    from remapp.models import GeneralStudyModuleAttr
    from remapp.models import Exports
    from remapp.interface.mod_filters import MGSummaryListFilter

    tsk = Exports.objects.create()

    tsk.task_id = mg_csv_nhsbsp.request.id
    tsk.modality = u"MG"
    tsk.export_type = u"NHSBSP CSV export"
    datestamp = datetime.datetime.now()
    tsk.export_date = datestamp
    tsk.progress = u'Query filters imported, task started'
    tsk.status = u'CURRENT'
    tsk.includes_pid = False
    tsk.export_user_id = user
    tsk.save()

    try:
        tmpfile = TemporaryFile()
        writer = csv.writer(tmpfile)

        tsk.progress = u'CSV file created'
        tsk.save()
    except:
        messages.error(request,
                       u"Unexpected error creating temporary file - please contact an administrator: {0}".format(
                           sys.exc_info()[0]))
        return redirect('/openrem/export/')

    # Get the data!

    s = GeneralStudyModuleAttr.objects.filter(modality_type__exact='MG')
    f = MGSummaryListFilter.base_filters

    for filt in f:
        if filt in filterdict and filterdict[filt]:
            # One Windows user found filterdict[filt] was a list. See https://bitbucket.org/openrem/openrem/issue/123/
            if isinstance(filterdict[filt], basestring):
                filterstring = filterdict[filt]
            else:
                filterstring = (filterdict[filt])[0]
            if filterstring != u'':
                s = s.filter(**{f[filt].name + u'__' + f[filt].lookup_type: filterstring})

    tsk.progress = u'Required study filter complete.'
    tsk.save()

    numresults = s.count()

    tsk.num_records = numresults
    tsk.save()

    writer.writerow([
        u'Survey number',
        u'Patient number',
        u'View code',
        u'kV',
        u'Anode',
        u'Filter',
        u'Thickness',
        u'mAs',
        u'large cassette used',
        u'auto/man',
        u'Auto mode',
        u'Density setting',
        u'Age',
        u'Comment',
        u'AEC density mode',
    ])

    for i, study in enumerate(s):
        exposures = study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all()
        for exp in exposures:
            try:
                laterality = exp.laterality.code_meaning
            except AttributeError:
                exp.nccpm_view = None
                continue
            exp.nccpm_view = laterality[:1]
            views = {u'cranio-caudal': u'CC',
                     u'medio-lateral oblique': u'OB',
                     u'medio-lateral': u'ML',
                     u'latero-medial': u'LM',
                     u'latero-medial oblique': u'LMO',
                     u'caudo-cranial (from below)': u'FB',
                     u'superolateral to inferomedial oblique': u'SIO',
                     u'inferomedial to superolateral oblique': u'ISO',
                     u'cranio-caudal exaggerated laterally': u'XCCL',
                     u'cranio-caudal exaggerated medially': u'XCCM'
                     }  # See http://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_CID_4014.html
            try:
                if exp.image_view.code_meaning in views:
                    exp.nccpm_view += views[exp.image_view.code_meaning]
                else:
                    exp.nccpm_view += exp.image_view.code_meaning
            except AttributeError:
                exp.nccpm_view = None
                continue  # Avoid exporting exposures with no image_view recorded
            if u'specimen' in exp.image_view.code_meaning:
                exp.nccpm_view = None
                continue  # No point including these in the export
            bad_acq_words = [
                u'scout', u'postclip', u'prefire', u'biopsy', u'postfire', u'stereo', u'specimen', u'artefact']
            if any(word in exp.acquisition_protocol.lower() for word in bad_acq_words):
                exp.nccpm_view = None
                continue  # Avoid exporting biopsy related exposures
            try:
                target = exp.irradeventxraysourcedata_set.get().anode_target_material.code_meaning
            except AttributeError:
                exp.nccpm_view = None
                continue  # Avoid exporting exposures with no anode material recorded
            if u"TUNGSTEN" in target.upper():
                target = u'W'
            elif u"MOLY" in target.upper():
                target = u'Mo'
            elif u"RHOD" in target.upper():
                target = u'Rh'
            try:
                filter_mat = exp.irradeventxraysourcedata_set.get().xrayfilters_set.get().xray_filter_material.code_meaning
            except AttributeError:
                exp.nccpm_view = None
                continue  # Avoid exporting exposures with no filter material recorded
            if u"ALUM" in filter_mat.upper():
                filter_mat = u'Al'
            elif u"MOLY" in filter_mat.upper():
                filter_mat = u'Mo'
            elif u"RHOD" in filter_mat.upper():
                filter_mat = u'Rh'
            elif u"SILV" in filter_mat.upper():
                filter_mat = u'Ag'
        unique_views = set()
        for exp in exposures:
            if exp.nccpm_view:
                if exp.nccpm_view not in unique_views:
                    unique_views.add(exp.nccpm_view)
                else:
                    for x in range(20):
                        if exp.nccpm_view + str(x+2) not in unique_views:
                            exp.nccpm_view += str(x+2)
                            unique_views.add(exp.nccpm_view)
                            break
        for exp in exposures:
            if not exp.nccpm_view:
                continue  # Avoid exporting exposures with no view code
            automan = exp.irradeventxraysourcedata_set.get().exposure_control_mode
            if u"AUTO" in automan.upper():
                automan = u'AUTO'
            elif u"MAN" in automan.upper():
                automan = u"MANUAL"

            writer.writerow([
                u'1',
                i + 1,
                exp.nccpm_view,
                exp.irradeventxraysourcedata_set.get().kvp_set.get().kvp,
                target,
                filter_mat,
                exp.irradeventxraymechanicaldata_set.get().compression_thickness,
                exp.irradeventxraysourcedata_set.get().exposure_set.get().exposure / 1000,
                u'',  # not applicable to FFDM
                automan,
                exp.irradeventxraysourcedata_set.get().exposure_control_mode,
                u'',  # no consistent behaviour for recording density setting on FFDM units
                exp.projection_xray_radiation_dose.general_study_module_attributes.patientstudymoduleattr_set.get().patient_age_decimal,
                u'',  # not in DICOM headers
                u'',  # no consistent behaviour for recording density mode on FFDM units
            ])
        tsk.progress = u"{0} of {1}".format(i + 1, numresults)
        tsk.save()

    tsk.progress = u'All study data written.'
    tsk.save()

    csvfilename = u"mg_nhsbsp_{0}.csv".format(datestamp.strftime("%Y%m%d-%H%M%S%f"))

    try:
        tsk.filename.save(csvfilename, File(tmpfile))
    except OSError as e:
        tsk.progress = u"Errot saving export file - please contact an administrator. Error({0}): {1}".format(e.errno,
                                                                                                            e.strerror)
        tsk.status = u'ERROR'
        tsk.save()
        return
    except:
        tsk.progress = u"Unexpected error saving export file - please contact an administrator: {0}".format(
            sys.exc_info()[0])
        tsk.status = u'ERROR'
        tsk.save()
        return
    tsk.status = u'COMPLETE'
    tsk.processtime = (datetime.datetime.now() - datestamp).total_seconds()
    tsk.save()
