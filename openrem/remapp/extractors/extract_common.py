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
..  module:: extract-common
    :synopsis: Module of functions common to multiple extractor routines
"""

import logging


def get_study_check_dup(dataset, modality='DX'):
    """
    If study exists, create new event
    :param dataset: DICOM object
    :param modality: Modality of image object being imported; 'MG' or 'DX'
    :return: Study object to proceed with
    """
    from remapp.models import GeneralStudyModuleAttr
    from remapp.tools import check_uid
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.dcmdatetime import make_date_time

    if modality == 'MG':
        logger = logging.getLogger('remapp.extractors.mam')
    else:
        logger = logging.getLogger('remapp.extractors.dx')

    study_uid = get_value_kw('StudyInstanceUID', dataset)
    event_uid = get_value_kw('SOPInstanceUID', dataset)
    logger.debug(u"In get_study_check_dup for {0}. Study UID {1}, event UID {2}".format(
        modality, study_uid, event_uid))
    this_study = None
    same_study_uid = GeneralStudyModuleAttr.objects.filter(study_instance_uid__exact=study_uid).order_by('pk')
    if same_study_uid.count() > 1:
        logger.warning(u"Duplicate DX study UID {0} in database - could be a problem! There are {1} copies.".format(
            study_uid, same_study_uid.count()))
        # Studies are ordered by study level pk. FInd the first one that has a modality type, and replace our
        # filter_set with the study we have found.
        for study in same_study_uid.order_by('pk'):
            if study.modality_type:
                this_study = study
                logger.debug(u"Duplicate {3} study UID {0} - first instance (pk={1}) with modality type assigned ({2}) "
                             u"selected to import new event into.".format(
                                study_uid, study.pk, study.modality_type, modality))
                break
        if not this_study:
            logger.warning(u"Duplicate {1} study UID {0}, none of which have modality_type assigned!"
                           u" Setting first instance to DX".format(study_uid, modality))
            this_study = same_study_uid[0]
            this_study.modality_type = modality
            this_study.save()
    elif same_study_uid.count() == 1:
        logger.debug(u"Importing event {0} into study {1}".format(event_uid, study_uid))
        this_study = same_study_uid[0]
    else:
        logger.error(u"Attempting to add {0} event {1} to study UID {2}, but it isn't there anymore. Stopping.".format(
            modality, event_uid, study_uid))
        return 0
    existing_sop_instance_uids = set()
    for previous_object in this_study.objectuidsprocessed_set.all():
        existing_sop_instance_uids.add(previous_object.sop_instance_uid)
    if event_uid in existing_sop_instance_uids:
        # We might get here if object has previously been rejected for being a for processing/presentation duplicate
        logger.debug(u"{2} instance UID {0} of study UID {1} previously processed, stopping.".format(
            event_uid, study_uid, modality))
        return 0
    # New event - record the SOP instance UID
    logger.debug(u"{0} Event {1} we haven't seen before. Adding to list for study {2}".format(
        modality, event_uid, study_uid))
    check_uid.record_sop_instance_uid(this_study, event_uid)
    # further check required to ensure 'for processing' and 'for presentation'
    # versions of the same irradiation event don't get imported twice
    # Also check it isn't a Hologic SC tomo file
    if modality == u'DX' or (modality == u'MG' and dataset.SOPClassUID != '1.2.840.10008.5.1.4.1.1.7'):
        event_time = get_value_kw('AcquisitionTime', dataset)
        if not event_time:
            event_time = get_value_kw('ContentTime', dataset)
        event_date = get_value_kw('AcquisitionDate', dataset)
        if not event_date:
            event_date = get_value_kw('ContentDate', dataset)
        event_date_time = make_date_time('{0}{1}'.format(event_date, event_time))
        for events in this_study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
            if event_date_time == events.date_time_started:
                logger.debug(u"A previous {2} object with this study UID ({0}) and time ({1}) has been imported."
                             u" Stopping".format(study_uid, event_date_time.isoformat(), modality))
                return 0
    # study exists, but event doesn't
    return this_study
