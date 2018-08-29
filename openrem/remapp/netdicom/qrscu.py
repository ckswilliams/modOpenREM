# This Python file uses the following encoding: utf-8
#!/usr/bin/python

"""
Query/Retrieve SCU AE

Specialised QR routine to get just the objects that might be useful for dose related metrics from a remote PACS or
modality
"""

from celery import shared_task
import django
import logging
import os
import sys
import uuid
import collections
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger('remapp.netdicom.qrscu')  # Explicitly named so that it is still handled when using __main__
# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

from remapp.netdicom.tools import create_ae


def _generate_modalities_in_study(study_rsp):
    """Generates modalities in study from series level Modality information

    :param study_rsp: study level C-Find response object in database
    :return: response updated with ModalitiesInStudy
    """
    logger.debug(u"modalities_returned = False, so building from series info")
    series_rsp = study_rsp.dicomqrrspseries_set.all()
    study_rsp.set_modalities_in_study(list(set(val for dic in series_rsp.values('modality') for val in dic.values())))
    study_rsp.save()


def _remove_duplicates(query, study_rsp, assoc, query_id):
    """
    Checks for objects in C-Find response already being in the OpenREM database to remove them from the C-Move request
    :param query: Query object in database
    :param study_rsp: study level C-Find response object in database
    :param assoc: current DICOM Query object
    :param query_id: current query ID for logging
    :return: Study, series and image level responses deleted if not useful
    """
    from remapp.models import GeneralStudyModuleAttr

    logger.debug(u"About to remove any studies we already have in the database")
    query.stage = u'Checking to see if any response studies are already in the OpenREM database'
    try:
        query.save()
    except Exception as e:
        logger.error(u"query.save in remove duplicates didn't work because of {0}".format(e))
    logger.info(
        u'Checking to see if any of the {0} studies are already in the OpenREM database'.format(study_rsp.count()))
    for study_number, study in enumerate(study_rsp):
        existing_studies = GeneralStudyModuleAttr.objects.filter(study_instance_uid=study.study_instance_uid)
        if existing_studies.exists():
            logger.debug(u"Study {0} {1} exists in database already".format(study_number, study.study_instance_uid))
            for existing_study in existing_studies:
                existing_sop_instance_uids = set()
                for previous_object in existing_study.objectuidsprocessed_set.all():
                    existing_sop_instance_uids.add(previous_object.sop_instance_uid)
                logger.debug(u"Study {0} {1} has previously processed the following SOPInstanceUIDs: {2}".format(
                    study_number, study.study_instance_uid, existing_sop_instance_uids))
                for series_rsp in study.dicomqrrspseries_set.all():
                    if series_rsp.modality == 'SR':
                        for image_rsp in series_rsp.dicomqrrspimage_set.all():
                            logger.debug(u"Study {0} {1} Checking for SOPInstanceUID {2}".format(
                                study_number, study.study_instance_uid, image_rsp.sop_instance_uid))
                            if image_rsp.sop_instance_uid in existing_sop_instance_uids:
                                logger.debug(u"Study {0} {1} Found SOPInstanceUID processed before, "
                                             u"won't ask for this one".format(study_number, study.study_instance_uid))
                                image_rsp.delete()
                                series_rsp.image_level_move = True  # If we have deleted images we need to set this flag
                                series_rsp.save()
                        if not series_rsp.dicomqrrspimage_set.order_by('pk'):
                            series_rsp.delete()
                    elif series_rsp.modality in ['MG', 'DX', 'CR']:
                        logger.debug(u"Study {0} {1} about to query at image level to get SOPInstanceUID".format(
                            study_number, study.study_instance_uid))
                        _query_images(assoc, series_rsp, query_id)
                        for image_rsp in series_rsp.dicomqrrspimage_set.all():
                            logger.debug(u"Study {0} {1} Checking for SOPInstanceUID {2}".format(
                                study_number, study.study_instance_uid, image_rsp.sop_instance_uid))
                            if image_rsp.sop_instance_uid in existing_sop_instance_uids:
                                logger.debug(u"Study {0} {1} Found SOPInstanceUID processed before, "
                                             u"won't ask for this one".format(study_number, study.study_instance_uid))
                                image_rsp.delete()
                                series_rsp.image_level_move = True  # If we have deleted images we need to set this flag
                                series_rsp.save()
                        if not series_rsp.dicomqrrspimage_set.order_by('pk'):
                            series_rsp.delete()
                    else:
                        series_rsp.delete()
        if not study.dicomqrrspseries_set.order_by('pk'):
            study.delete()

    study_rsp = query.dicomqrrspstudy_set.all()
    logger.info(u'After removing studies we already have in the db, {0} studies are left'.format(study_rsp.count()))


def _filter(query, level, filter_name, filter_list, filter_type):
    """
    Reduces Study or Series level UIDs that will have a Move command sent for by filtering against one of three
    variables that can be 'include only' or 'exclude'
    :param query: Query object in database
    :param level: 'series' or 'study'
    :param filter_name: 'station_name', 'sop_classes_in_study', or 'study_description'
    :param filter_list: list of lower case search words or phrases, or SOP classes
    :param filter_type: 'exclude', 'include'
    :return: None
    """
    if filter_type == 'exclude':
        filtertype = True
    elif filter_type == 'include':
        filtertype = False

    study_rsp = query.dicomqrrspstudy_set.all()
    query.stage = u"Filter at {0} level on {1} that {2} {3}".format(level, filter_name, filter_type, filter_list)
    logger.info(u"Filter at {0} level on {1} that {2} {3}".format(level, filter_name, filter_type, filter_list))
    for study in study_rsp:
        if level == 'study':
            if any(term in (getattr(study, filter_name) or '').lower() for term in filter_list) is filtertype:
                study.delete()
        elif level == 'series':
            series = study.dicomqrrspseries_set.all()
            for s in series:
                if any(term in (getattr(s,filter_name) or '').lower() for term in filter_list) is filtertype:
                    s.delete()
            nr_series_remaining = study.dicomqrrspseries_set.all().count()
            if (nr_series_remaining==0):
                study.delete()
    study_rsp = query.dicomqrrspstudy_set.all()
    logger.info(u'Now have {0} studies'.format(study_rsp.count()))


def _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images):
    """
    For each study level response, remove any series that we know can't be used.
    :param query: Current DicomQuery object
    :param all_mods: Ordered dict of dicts detailing modalities we are interested in
    :param filters: Include and exclude lists for StationName (and StudyDescription)
    :param get_toshiba_images: Bool, whether to try to get Toshiba dose summary images
    :return Series level response database rows are deleted if not useful
    """
    query.stage = u"Deleting series we can't use"
    query.save()
    logger.info(u"Deleting series we can't use")

    study_rsp = query.dicomqrrspstudy_set.all()

    if filters['stationname_inc']:
        _filter(query, level='series', filter_name='station_name', filter_list=filters['stationname_inc'],
                filter_type='include')

    if filters['stationname_exc']:
        _filter(query, level='series', filter_name='station_name', filter_list=filters['stationname_exc'],
                filter_type='exclude')

    for study in study_rsp:
        logger.debug("at study in study_resp in series prune. modalities in study are: {0}".format(study.get_modalities_in_study()))
        if all_mods['MG']['inc'] and 'MG' in study.get_modalities_in_study():
            # If _check_sr_type_in_study returns an RDSR, all other SR series will have been deleted and then all images
            # are deleted. If _check_sr_type_in_study returns an ESR or no_dose_report, everything else is kept.
            study.modality = u'MG'
            study.save()

            if 'SR' in study.get_modalities_in_study() and _check_sr_type_in_study(assoc, study,
                                                                                   query.query_id) == 'RDSR':
                logger.debug(u"Found RDSR in MG study, so keep SR and delete all other series")
                series = study.dicomqrrspseries_set.all()
                series.exclude(modality__exact='SR').delete()
            # ToDo: see if there is a mechanism to remove duplicate 'for processing' 'for presentation' images.

        elif all_mods['DX']['inc'] and any(mod in study.get_modalities_in_study() for mod in ('CR', 'DX')):
            # If _check_sr_type_in_study returns an RDSR, all other SR series will have been deleted and then all images
            # are deleted. If _check_sr_type_in_study returns an ESR or no_dose_report, everything else is kept.
            study.modality = u'DX'
            study.save()

            if 'SR' in study.get_modalities_in_study() and _check_sr_type_in_study(assoc, study,
                                                                                   query.query_id) == 'RDSR':
                logger.debug(u"Found RDSR in DX study, so keep SR and delete all other series")
                series = study.dicomqrrspseries_set.all()
                series.exclude(modality__exact='SR').delete()

        elif all_mods['FL']['inc'] and any(mod in study.get_modalities_in_study() for mod in ('XA', 'RF')):
            # _check_sr_type_in_study will delete any SR that is not RDSR or ESR. All other series are then deleted.
            study.modality = 'FL'
            study.save()
            sr_type = _check_sr_type_in_study(assoc, study, query.query_id)
            logger.debug(u"FL study, check_sr_type returned {0}".format(sr_type))
            series = study.dicomqrrspseries_set.all()
            series.exclude(modality__exact='SR').delete()

        elif all_mods['CT']['inc'] and 'CT' in study.get_modalities_in_study():
            # If _check_sr_type_in_study returns RDSR, all other SR series responses will have been deleted and then all
            # other series responses will be deleted too.
            # If _check_sr_type_in_study returns ESR, all other SR series responses will have been deleted and then all
            # other series responses will be deleted too.
            # Otherwise, we pass the study response to _get_philips_dose_images to see if there is a Philips dose info
            # series and optionally get samples from each series for the Toshiba RDSR creation routine.
            study.modality = 'CT'
            study.save()
            logger.debug("Filtering CT at series level")
            series = study.dicomqrrspseries_set.all()
            if 'SR' in study.get_modalities_in_study():
                sr_type = _check_sr_type_in_study(assoc, study, query.query_id)
                if sr_type == 'RDSR':
                    logger.debug(u"Found RDSR in CT study, so keep SR and delete all other series")
                    series.exclude(modality__exact='SR').delete()
                elif sr_type == 'ESR':  # GE CT's with ESR instead of RDSR
                    logger.debug(u"Found ESR in CT study, so keep SR and delete all other series")
                    series.exclude(modality__exact='SR').delete()
                else:
                    _get_philips_dose_images(series, get_toshiba_images, assoc, query.query_id)
            else:
                # if SR not present in study
                _get_philips_dose_images(series, get_toshiba_images, assoc, query.query_id)

        elif all_mods['SR']['inc']:
            sr_type = _check_sr_type_in_study(assoc, study, query.query_id)
            if sr_type == 'RDSR':
                logger.debug(u"SR only query, found RDSR, deleted other SRs")
            elif sr_type == 'ESR':
                logger.debug(u"SR only query, found ESR, deleted other SRs")
            elif sr_type == 'no_dose_report':
                logger.debug(u"No RDSR or ESR found. Study will be deleted.")

        nr_series_remaining = study.dicomqrrspseries_set.all().count()
        if (nr_series_remaining==0):
            logger.debug(u"Deleting empty study with suid {0}".format(study.study_instance_uid))
            study.delete()


def _get_philips_dose_images(series, get_toshiba_images, assoc, query_id):
    """
    Remove series that are not likely to be Philips Dose Info series
    :param series: database set
    :param get_toshiba_images: Bool, whether to try to get Toshiba dose summary images
    :return: None. Entries will be removed from database
    """
    series_descriptions = set(val for dic in series.values('series_description') for val in dic.values())
    logger.debug("In _get_philips_dose_images. series_descriptions are {0}".format(series_descriptions))
    if series_descriptions != {None}:
        if series.filter(series_description__iexact='dose info'):
            series.exclude(series_description__iexact='dose info').delete()
        elif get_toshiba_images:
            _get_toshiba_dose_images(series, assoc, query_id)
        else:
            series.delete()
    elif get_toshiba_images:
        _get_toshiba_dose_images(series, assoc, query_id)
    else:
        series.filter(number_of_series_related_instances__gt=5).delete()


def _get_toshiba_dose_images(study_series, assoc, query_id):
    """
    Get images for Toshiba studies with no RDSR
    :param study_series: database set
    :return: None. Non-useful entries will be removed from database
    """

    for index, series in enumerate(study_series):
        _query_images(assoc, series, query_id, initial_image_only=True, msg_id=index+1)
        images = series.dicomqrrspimage_set.all()
        logger.debug(u"Query_id {0}: Query for Toshiba images. Have {1} in this series.".format(
            query_id, images.count()))
        if images.count() == 0:
            logger.debug("Query_id {0}: No images in series! Deleting series.".format(query_id))
            series.delete()
            continue
        if images[0].sop_class_uid != '1.2.840.10008.5.1.4.1.1.7':
            logger.debug("Query_id {0}: In non secondary capture series, SOPClassUID {1}. "
                         "Will delete all but first image.".format(query_id, images[0].sop_class_uid))
            images.exclude(sop_instance_uid__exact=images[0].sop_instance_uid).delete()
            logger.debug("Query_id {0}: Deleted other images, now {1} remaining (should be 1)".format(
                query_id, images.count()))
            series.image_level_move = True
            series.save()
        else:
            logger.debug("Query_id {0}: In secondary capture series, SOPClassUID {1}. "
                         "Will not delete any images.".format(query_id, images[0].sop_class_uid))
            logger.debug("Query_id {0}: {1} images in this SC series".format(
                query_id, images.count()))
            # series.image_level_move = True
            # series.save()


def _prune_study_responses(query, filters):

    if filters['study_desc_inc']:
        logger.debug(u"About to filter on study_desc_inc: {0}, currently have {1} studies.".format(
            filters['study_desc_inc'], query.dicomqrrspstudy_set.all().count()))
        _filter(query, level='study', filter_name='study_description',
                filter_list=filters['study_desc_inc'], filter_type='include')
        logger.debug(u"Filtering done. Now have {0} studies".format(query.dicomqrrspstudy_set.all().count()))
    if filters['study_desc_exc']:
        logger.debug(u"About to filter on study_desc_exc: {0}, currently have {1} studies.".format(
            filters['study_desc_exc'], query.dicomqrrspstudy_set.all().count()))
        _filter(query, level='study', filter_name='study_description',
                filter_list=filters['study_desc_exc'], filter_type='exclude')
        logger.debug(u"Filtering done. Now have {0} studies".format(query.dicomqrrspstudy_set.all().count()))
    if filters['stationname_inc']:
        logger.debug(u"About to filter on stationname_inc: {0}, currently have {1} studies.".format(
            filters['stationname_inc'], query.dicomqrrspstudy_set.all().count()))
        _filter(query, level='study', filter_name='station_name',
                filter_list=filters['stationname_inc'], filter_type='include')
        logger.debug(u"Filtering done. Now have {0} studies".format(query.dicomqrrspstudy_set.all().count()))
    if filters['stationname_exc']:
        logger.debug(u"About to filter on stationname_exc: {0}, currently have {1} studies.".format(
            filters['stationname_exc'], query.dicomqrrspstudy_set.all().count()))
        _filter(query, level='study', filter_name='station_name',
                filter_list=filters['stationname_exc'], filter_type='exclude')
        logger.debug(u"Filtering done. Now have {0} studies".format(query.dicomqrrspstudy_set.all().count()))


# returns SR-type: RDSR or ESR; otherwise returns 'no_dose_report'
def _check_sr_type_in_study(assoc, study, query_id):
    """Checks at an image level whether SR in study is RDSR, ESR, or something else (Radiologist's report for example)

    * If RDSR is found, all non-RDSR SR series responses are deleted
    * Otherwise, if an ESR is found, all non-ESR series responses are deleted
    * Otherwise, all SR series responses are deleted

    The function returns one of 'RDSR', 'ESR', 'no_dose_report'.

    :param assoc: Current DICOM query object
    :param study: study level C-Find response object in database
    :param query_id: current query ID for logging
    :return: string indicating SR type remaining in study
    """
    series_sr = study.dicomqrrspseries_set.filter(modality__exact='SR')
    logger.debug(u"Number of series with SR {0}".format(series_sr.count()))
    sopclasses = set()
    for sr in series_sr:
        _query_images(assoc, sr, query_id)
        images = sr.dicomqrrspimage_set.all()
        if images.count() == 0:
            logger.debug(u"Oops, series {0} of study instance UID {1} doesn't have any objects in!".format(
                sr.series_number, study.study_instance_uid))
            continue
        sopclasses.add(images[0].sop_class_uid)
        sr.sop_class_in_series = images[0].sop_class_uid
        sr.save()
        logger.debug(u"studyuid: {0}   seriesuid: {1}   nrimages: {2}   sopclasses: {3}".format(
            study.study_instance_uid, sr.series_instance_uid, images.count(), sopclasses))
    logger.debug(u"sopclasses: {0}".format(sopclasses))
    if '1.2.840.10008.5.1.4.1.1.88.67' in sopclasses:
        for sr in series_sr:
            if sr.sop_class_in_series != '1.2.840.10008.5.1.4.1.1.88.67':
                logger.debug(u"Have RDSR, deleting non-RDSR SR")
                sr.delete()
        return 'RDSR'
    elif '1.2.840.10008.5.1.4.1.1.88.22' in sopclasses:
        for sr in series_sr:
            if sr.sop_class_in_series != '1.2.840.10008.5.1.4.1.1.88.22':
                logger.debug(u"Have ESR, deleting non-RDSR, non-ESR SR")
                sr.delete()
        return 'ESR'
    else:
        for sr in series_sr:
            logger.debug(u"Deleting non-RDSR, non-ESR SR")
            sr.delete()
        return 'no_dose_report'


def _query_images(assoc, seriesrsp, query_id, initial_image_only=False, msg_id=None):
    from remapp.models import DicomQRRspImage
    from dicom.dataset import Dataset

    logger.debug(u'Query_id {0}: In _query_images'.format(query_id))

    d3 = Dataset()
    d3.QueryRetrieveLevel = "IMAGE"
    d3.SeriesInstanceUID = seriesrsp.series_instance_uid
    d3.StudyInstanceUID = seriesrsp.dicom_qr_rsp_study.study_instance_uid
    d3.SOPInstanceUID = ''
    d3.SOPClassUID = ''
    d3.InstanceNumber = ''
    d3.SpecificCharacterSet = ''

    if initial_image_only:
        d3.InstanceNumber = '1'
    if not msg_id:
        msg_id = 1

    logger.debug(u'Query_id {0}: query is {1}, intial_imge_only is {2}, msg_id is {3}'.format(
                    query_id, d3, initial_image_only, msg_id))

    st3 = assoc.StudyRootFindSOPClass.SCU(d3, msg_id)

    query_id = uuid.uuid4()

    imRspNo = 0

    for images in st3:
        if not images[1]:
            continue
        images[1].decode()
        imRspNo += 1
        logger.debug(u"Query_id {0}: Image Response {1}: {2}".format(query_id, imRspNo, images[1]))
        imagesrsp = DicomQRRspImage.objects.create(dicom_qr_rsp_series=seriesrsp)
        imagesrsp.query_id = query_id
        # Mandatory tags
        imagesrsp.sop_instance_uid = images[1].SOPInstanceUID
        imagesrsp.sop_class_uid = images[1].SOPClassUID
        imagesrsp.instance_number = images[1].InstanceNumber
        if not imagesrsp.instance_number:  # just in case!!
            imagesrsp.instance_number = None  # integer so can't be ''
        imagesrsp.save()


def _query_series(assoc, d2, studyrsp, query_id):
    from remapp.tools.dcmdatetime import get_time
    from remapp.tools.get_values import get_value_kw
    from remapp.models import DicomQRRspSeries
    d2.QueryRetrieveLevel = "SERIES"
    d2.SeriesDescription = ''
    d2.SeriesNumber = ''
    d2.SeriesInstanceUID = ''
    d2.Modality = ''
    d2.NumberOfSeriesRelatedInstances = ''
    d2.StationName = ''
    d2.SpecificCharacterSet = ''
    d2.SeriesTime = ''

    logger.debug(u'Query_id {0}: In _query_series'.format(query_id))
    logger.debug(u'Query_id {0}: series query is {1}'.format(query_id, d2))

    st2 = assoc.StudyRootFindSOPClass.SCU(d2, 1)

    series_query_id = uuid.uuid4()

    seRspNo = 0

    for series in st2:
        if not series[1]:
            continue
        series[1].decode()
        seRspNo += 1
        seriesrsp = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=studyrsp)
        seriesrsp.query_id = series_query_id
        # Mandatory tags
        seriesrsp.series_instance_uid = series[1].SeriesInstanceUID
        seriesrsp.modality = series[1].Modality
        seriesrsp.series_number = series[1].SeriesNumber
        if not seriesrsp.series_number:  # despite it being mandatory!
            seriesrsp.series_number = None  # integer so can't be ''
        # Optional useful tags
        seriesrsp.series_description = get_value_kw(u'SeriesDescription', series[1])
        if seriesrsp.series_description:
            seriesrsp.series_description = ''.join(seriesrsp.series_description).strip().lower()
        seriesrsp.number_of_series_related_instances = get_value_kw('NumberOfSeriesRelatedInstances', series[1])
        if not seriesrsp.number_of_series_related_instances:
            seriesrsp.number_of_series_related_instances = None  # integer so can't be ''
        seriesrsp.station_name = get_value_kw('StationName', series[1])
        seriesrsp.series_time = get_time('SeriesTime', series[1])
        logger.debug(u"Series Response {0}: Modality {1}, StationName {2}, StudyUID {3}, Series No. {4}, "
                     u"Series description {5}".format(
                            seRspNo, seriesrsp.modality, seriesrsp.station_name, d2.StudyInstanceUID,
                            seriesrsp.series_number, seriesrsp.series_description))

        seriesrsp.save()


def _query_study(assoc, d, query, query_id):
    from remapp.models import DicomQRRspStudy
    from remapp.tools.get_values import get_value_kw
    d.QueryRetrieveLevel = "STUDY"
    d.PatientName = ''
    d.PatientID = ''
    d.AccessionNumber = ''
    d.StudyDescription = ''
    d.StudyID = ''
    d.StudyInstanceUID = ''
    d.StudyTime = ''
    d.PatientAge = ''
    d.PatientBirthDate = ''
    d.NumberOfStudyRelatedSeries = ''
    d.StationName = ''
    d.SpecificCharacterSet = ''

    logger.debug(u'Query_id {0}: Study level association requested'.format(query_id))
    st = assoc.StudyRootFindSOPClass.SCU(d, 1)
    logger.debug(u'Query_id {0}: _query_study done with status {1}'.format(query_id, st))

    # TODO: Replace the code below to deal with find failure
    # if not st:
    #     query.failed = True
    #     query.message = "Study Root Find unsuccessful"
    #     query.complete = True
    #     query.save()
    #     MyAE.Quit()
    #     return

    rspno = 0

    logger.debug(u'Processing the study level responses')
    for ss in st:
        if not ss[1]:
            continue
        ss[1].decode()
        rspno += 1
        rsp = DicomQRRspStudy.objects.create(dicom_query=query)
        rsp.query_id = query_id
        # Unique key
        rsp.study_instance_uid = ss[1].StudyInstanceUID
        # Required keys - none of interest
        logger.debug(u"Response {0}, StudyUID: {1}".format(rspno, rsp.study_instance_uid))

        # Optional and special keys
        rsp.study_description = get_value_kw(u"StudyDescription", ss[1])
        rsp.station_name = get_value_kw('StationName', ss[1])
        logger.debug(u"Study Description: {0}; Station Name: {1}".format(rsp.study_description, rsp.station_name))

        # Populate modalities_in_study, stored as JSON
        if isinstance(ss[1].ModalitiesInStudy, str):   # if single modality, then type = string ('XA')
            rsp.set_modalities_in_study(ss[1].ModalitiesInStudy.split(u','))
        else:   # if multiple modalities, type = MultiValue (['XA', 'RF'])
            rsp.set_modalities_in_study(ss[1].ModalitiesInStudy)
        logger.debug(u"ModalitiesInStudy: {0}".format(rsp.get_modalities_in_study()))

        rsp.modality = None  # Used later
        rsp.save()


def _create_association(my_ae, remote_host, remote_port, remote_ae, query):
    # create association with remote AE
    logger.info(u"Query_id {0}: Request association with {1} ({2} {3} from {4})".format(
        query.query_id, remote_ae, remote_host, remote_port, my_ae))
    assoc = my_ae.RequestAssociation(remote_ae)
    if assoc:
        logger.debug(u"Query_id {0}: Association created: {1}".format(query.query_id, assoc))
    else:
        query.failed = True
        query.message = u"Query_id {0}: Association unsuccessful".format(query.query_id)
        query.complete = True
        query.save()
        my_ae.Quit()
        logger.error(u"Query_id {0} to {1} failed as association was unsuccessful".format(query.query_id, remote_ae))
        return
    return assoc


def _echo(assoc, query_id):
    echo = assoc.VerificationSOPClass.SCU(1)
    logger.debug(u"Query_id {0}: DICOM echo was returned with status {1}".format(query_id, echo.Type))
    return echo


def _query_for_each_modality(all_mods, query, d, assoc):
    """
    Uses _query_study for each modality we've asked for, and populates study level response data in the database
    :param all_mods: dict of dicts indicating which modalities to request
    :param query: DicomQuery object
    :param d: Dataset object containing StudyDate
    :param assoc: Established association with remote host
    :return: modalities_returned = whether ModalitiesInStudy is returned populated; modality_matching = whether
             responses have been filtered based on requested modality
    """

    # Assume that ModalitiesInStudy is a Matching Key Attribute
    # If not, 1 query is sufficient to retrieve all relevant studies
    modality_matching = True
    modalities_returned = False

    # query for all requested studies
    # if ModalitiesInStudy is not supported by the PACS set modality_matching to False and stop querying further
    for selection, details in all_mods.items():
        if details['inc']:
            for mod in details['mods']:
                if modality_matching:
                    query.stage = u'Currently querying for {0} studies...'.format(mod)
                    query.save()
                    logger.info(u'Currently querying for {0} studies...'.format(mod))
                    d.ModalitiesInStudy = mod
                    if query.qr_scp_fk.use_modality_tag:
                        logger.debug(u'Using modality tag in study query.')
                        d.Modality = ''
                    query_id = uuid.uuid4()
                    _query_study(assoc, d, query, query_id)
                    study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
                    logger.debug(u"Queried for {0}, now have {1} study level responses".format(mod, study_rsp.count()))
                    for rsp in study_rsp:  # First check if modalities in study has been populated
                        if rsp.get_modalities_in_study() and rsp.get_modalities_in_study()[0] != u'':
                            modalities_returned = True
                            # Then check for inappropriate responses
                            if mod not in rsp.get_modalities_in_study():
                                modality_matching = False
                                logger.debug(u"Remote node returns but doesn't match against ModalitiesInStudy")
                                break  # This indicates that there was no modality match, so we have everything already
    logger.debug(u"modalities_returned: {0}; modality_matching: {1}".format(modalities_returned, modality_matching))
    return modalities_returned, modality_matching


@shared_task(name='remapp.netdicom.qrscu.qrscu')  # (name='remapp.netdicom.qrscu.qrscu', queue='qr')
def qrscu(
        qr_scp_pk=None, store_scp_pk=None,
        implicit=False, explicit=False, move=False, query_id=None,
        date_from=None, date_until=None, modalities=None, inc_sr=False, remove_duplicates=True, filters=None,
        get_toshiba_images=False,
        *args, **kwargs):
    """Query retrieve service class user function

    Queries a pre-configured remote query retrieve service class provider for dose metric related objects,
    making use of the filter parameters provided. Can automatically trigger a c-move (retrieve) operation.

    Args:
      qr_scp_pk(int, optional): Database ID/pk of the remote QR SCP (Default value = None)
      store_scp_pk(int, optional): Database ID/pk of the local store SCP (Default value = None)
      implicit(bool, optional): Prefer implicit transfer syntax (preference possibly not implemented) (Default value = False)
      explicit(bool, optional): Prefer explicit transfer syntax (preference possibly not implemented) (Default value = False)
      move(bool, optional): Automatically trigger move request when query is complete (Default value = False)
      query_id(str, optional): UID of query if generated by web interface (Default value = None)
      date_from(str, optional): Date to search from, format yyyy-mm-dd (Default value = None)
      date_until(str, optional): Date to search until, format yyyy-mm-dd (Default value = None)
      modalities(list, optional): Modalities to search for, options are CT, MG, DX and FL (Default value = None)
      inc_sr(bool, optional): Only include studies that only have structured reports in (unknown modality) (Default value = False)
      remove_duplicates(bool, optional): If True, studies that already exist in the database are removed from the query results (Default value = True)
      filters(dictionary list, optional): include and exclude lists for StationName and StudyDescription (Default value = None)
      get_toshiba_images(bool, optional): Whether to try to get Toshiba dose summary images

      *args:
      **kwargs:

    Returns:
      : Series Instance UIDs are stored as rows in the database to be used by a move request. Move request is
      optionally triggered automatically.

    """

    from datetime import datetime

    from dicom.dataset import Dataset
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import DicomQuery, DicomRemoteQR, DicomStoreSCP
    from remapp.tools.dcmdatetime import make_dcm_date_range

    debug_timer = datetime.now()
    logger.debug(u"qrscu args passed: qr_scp_pk={0}, store_scp_pk={1}, implicit={2}, explicit={3}, move={4}, "
                 u"queryID={5}, date_from={6}, date_until={7}, modalities={8}, inc_sr={9}, remove_duplicates={10}, "
                 u"filters={11}".format(qr_scp_pk, store_scp_pk, implicit, explicit, move, query_id,
                                       date_from, date_until, modalities, inc_sr, remove_duplicates, filters))

    # Currently, if called from qrscu_script modalities will either be a list of modalities or it will be "SR".
    # Web interface hasn't changed, so will be a list of modalities and or the inc_sr flag
    # Need to normalise one way or the other.
    logger.debug(u"Checking for modality selection and sr_only clash")
    if modalities is None and inc_sr is False:
        logger.error(u"Query retrieve routine called with no modalities selected")
        return
    elif modalities is not None and inc_sr is True:
        logger.error(u"Query retrieve routine should be called with a modality selection _or_ SR only query, not both"
                     u"Modalities is {0}, inc_sr is {1}".format(modalities, inc_sr))
        return
    elif modalities is None and inc_sr is True:
        modalities = ["SR"]

    qr_scp = DicomRemoteQR.objects.get(pk=qr_scp_pk)
    if qr_scp.hostname:
        rh = qr_scp.hostname
    else:
        rh = qr_scp.ip
    rp = qr_scp.port
    aec = qr_scp.aetitle
    aet = qr_scp.callingaet
    if not aet:
        aet = "OPENREMDEFAULT"

    if implicit:
        ts = [ImplicitVRLittleEndian]
    elif explicit:
        ts = [ExplicitVRLittleEndian]
    else:
        ts = [
            ExplicitVRLittleEndian,
            ImplicitVRLittleEndian,
            ExplicitVRBigEndian
        ]

    my_ae = create_ae(aet.encode('ascii', 'ignore'), transfer_syntax=ts)
    my_ae.start()
    logger.debug(u"my_ae {0} started".format(my_ae))

    # remote application entity
    remote_ae = dict(Address=rh, Port=rp, AET=aec.encode('ascii', 'ignore'))
    logger.debug(u"Remote AE is {0}".format(remote_ae))

    if not query_id:
        query_id = uuid.uuid4()
    logger.debug(u"Query_id is {0}".format(query_id))

    query = DicomQuery.objects.create()
    query.query_id = query_id
    query.complete = False
    query.store_scp_fk = DicomStoreSCP.objects.get(pk=store_scp_pk)
    query.qr_scp_fk = qr_scp
    query.save()

    assoc = _create_association(my_ae, rh, rp, remote_ae, query)
    if not assoc:
        logger.warning(u"Query_id {0}: Query aborted as could not create initial association.")
        return

    # perform a DICOM ECHO
    logger.info(u"DICOM Echo ... ")
    echo_response = _echo(assoc, query_id)
    if echo_response.Type != u'Success':
        logger.error(u"Echo response was {0} instead of Success. Aborting query".format(echo_response))
        query.stage = u"Echo response was {0} instead of Success. Aborting query".format(echo_response)
        query.complete = True
        query.save()
        my_ae.Quit()
        return

    # logger.info(u"Query_id {0}: Releasing initial association (we'll start another one for C-Find)".format(query_id))
    # assoc.Release(0)

    logger.info(u"DICOM FindSCU ... ")
    d = Dataset()
    d.StudyDate = str(make_dcm_date_range(date_from, date_until) or '')

    all_mods = collections.OrderedDict()
    all_mods['CT'] = {'inc': False, 'mods': ['CT']}
    all_mods['MG'] = {'inc': False, 'mods': ['MG']}
    all_mods['FL'] = {'inc': False, 'mods': ['RF', 'XA']}
    all_mods['DX'] = {'inc': False, 'mods': ['DX', 'CR']}
    all_mods['SR'] = {'inc': False, 'mods': ['SR']}

    # Reasoning regarding PET-CT: Some PACS allocate study modality PT, some CT, some depending on order received.
    # If ModalitiesInStudy is used for matching on C-Find, the CT from PET-CT will be picked up.
    # If not, then the PET-CT will be returned with everything else, and the CT will show up in the series level
    # query. Therefore, there is no need to search for PT at any stage.
    for m in all_mods:
        if m in modalities:
            all_mods[m]['inc'] = True

    # query for all requested studies
    modalities_returned, modality_matching = _query_for_each_modality(all_mods, query, d, assoc)

    # Now we have all our studies. Time to throw duplicates and away any we don't want
    logger.debug(u"Time to throw away any studies or series that are not useful before requesting moves")
    distinct_rsp = query.dicomqrrspstudy_set.all().distinct('study_instance_uid')
    try:
        distinct_rsp.count()  # To trigger error if using SLQite3 or other unsupported db for distinct()
        study_rsp = distinct_rsp
    except NotImplementedError:
        study_rsp = query.dicomqrrspstudy_set.all()

    # Performing some cleanup if modality_matching=True (prevents having to retrieve unnecessary series)
    # We are assuming that if remote matches on modality it will populate ModalitiesInStudy and conversely
    # if remote doesn't match on modality it won't return a populated ModalitiesInStudy.
    if modalities_returned and inc_sr:
        logger.info(u"Modalities_returned is true and we only want studies with only SR in; removing everything else.")
        for study in study_rsp:
            mods = study.get_modalities_in_study()
            if mods != ['SR']:
                study.delete()
        logger.debug(u"Finished removing studies that have anything other than SR in.")

    filter_logs = []
    if filters['study_desc_inc']:
        filter_logs += [u"study description includes {0}, ".format(u", ".join(filters['study_desc_inc']))]
    if filters['study_desc_exc']:
        filter_logs += [u"study description excludes {0}, ".format(u", ".join(filters['study_desc_exc']))]
    if filters['stationname_inc']:
        filter_logs += [u"station name includes {0}, ".format(u", ".join(filters['stationname_inc']))]
    if filters['stationname_exc']:
        filter_logs += [u"station name excludes {0}, ".format(u", ".join(filters['stationname_exc']))]

    query.stage = u"Pruning study responses based on inc/exc options"
    query.save()
    logger.info(u"Pruning study responses based on inc/exc options: {0}".format(u"".join(filter_logs)))
    _prune_study_responses(query, filters)
    study_rsp = query.dicomqrrspstudy_set.all()

    query.stage = u"Querying at series level to get more details about studies"
    query.save()
    for rsp in study_rsp:
        # Series level query
        d2 = Dataset()
        d2.StudyInstanceUID = rsp.study_instance_uid
        _query_series(assoc, d2, rsp, query_id)
        if not modalities_returned:
            _generate_modalities_in_study(rsp)

    if not modality_matching:
        mods_in_study_set = set(val for dic in study_rsp.values('modalities_in_study') for val in dic.values())
        logger.debug(u"mods in study are: {0}".format(study_rsp.values('modalities_in_study')))
        query.stage = u"Deleting studies we didn't ask for"
        query.save()
        logger.info(u"Deleting studies we didn't ask for")
        logger.debug(u"mods_in_study_set is {0}".format(mods_in_study_set))
        for mod_set in mods_in_study_set:
            logger.info(u"mod_set is {0}".format(mod_set))
            delete = True
            for mod_choice, details in all_mods.items():
                logger.info(u"mod_choice {0}, details {1}".format(mod_choice, details))
                if details['inc']:
                    for mod in details['mods']:
                        logger.info(u"mod is {0}, mod_set is {1}".format(mod, mod_set))
                        if mod in mod_set:
                            delete = False
                            continue
                        if inc_sr and mod_set == ['SR']:
                            delete = False
            if delete:
                study_rsp.filter(modalities_in_study__exact=mod_set).delete()
        logger.info(u'Now have {0} studies'.format(study_rsp.count()))

    query.stage = u"Pruning series responses"
    query.save()
    logger.debug(u"Pruning series responses")
    _prune_series_responses(assoc, query, all_mods, filters, get_toshiba_images)

    study_rsp = query.dicomqrrspstudy_set.all()
    logger.info(u'Now have {0} studies'.format(study_rsp.count()))

    if remove_duplicates:
        query.stage = u"Removing any responses that match data we already have in the database"
        query.save()
        _remove_duplicates(query, study_rsp, assoc, query_id)

    # done
    my_ae.Quit()
    query.complete = True
    time_took = datetime.now() - debug_timer
    query.stage = u"Query complete. Query took {0} seconds and we are left with {1} studies to move.".format(
        time_took, study_rsp.count())
    query.save()

    logger.debug(u"Query {0} complete. Move is {1}. Query took {2}".format(
        query.query_id, move, time_took))

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(u"Query result contains the following studies / series:")
        studies = query.dicomqrrspstudy_set.all()
        for study in studies:
            for series in study.dicomqrrspseries_set.all():
                logger.debug(
                    u"    Study: {0} ({1}) modalities: {2}, Series: {3}, modality: {4} containing {5} objects.".format(
                        study.study_description, study.study_instance_uid, study.get_modalities_in_study(),
                        series.series_instance_uid, series.modality, series.number_of_series_related_instances))

    if move:
        movescu.delay(str(query.query_id))


def _move_req(my_ae, assoc, d, study_no, series_no):
    move_generator = assoc.StudyRootMoveSOPClass.SCU(d, my_ae.getName(), 1)
    try:
        for move_status in move_generator:
            if u'Pending' in move_status:
                logger.info(u"Move of study {0}, series {1} status is {2} "
                            u"(i.e. one object processed)".format(
                    study_no, series_no, move_status))
            else:
                logger.warning(u"Move of study {0}, series {1} status is {2}".format(study_no, series_no, move_status))
    except KeyError as e:
        logger.error(u"{0} in qrscu._move_req. Request is {1}, study {2} series {3}".format(e, d, study_no, series_no))


@shared_task(name='remapp.netdicom.qrscu.movescu')  # (name='remapp.netdicom.qrscu.movescu', queue='qr')
def movescu(query_id):
    """
    C-Move request element of query-retrieve service class user
    :param query_id: UUID of query in the DicomQuery table
    :return: None
    """
    from time import sleep
    from dicom.dataset import Dataset
    from remapp.models import DicomQuery

    logger.debug(u"Query_id {0}: Starting move request".format(query_id))
    try:
        query = DicomQuery.objects.get(query_id=query_id)
    except ObjectDoesNotExist:
        logger.warning(u"Move called with invalid query_id {0}. Move abandoned.".format(query_id))
        return 0
    query.move_complete = False
    query.failed = False
    query.save()
    qr_scp = query.qr_scp_fk
    store_scp = query.store_scp_fk

    my_ae = create_ae(store_scp.aetitle.encode('ascii', 'ignore'))
    my_ae.start()
    logger.debug(u"Move AE my_ae {0} started".format(my_ae))

    # remote application entity
    if qr_scp.hostname:
        rh = qr_scp.hostname
    else:
        rh = qr_scp.ip
    remote_ae = dict(Address=rh, Port=qr_scp.port, AET=qr_scp.aetitle.encode('ascii', 'ignore'))

    logger.debug(u"Query_id {0}: Requesting move association".format(query_id))
    assoc = my_ae.RequestAssociation(remote_ae)
    logger.info(u"Query_id {0}: Move association requested".format(query_id))

    query.stage = u"Preparing to start move request"
    query.save()
    logger.info(u"Query_id {0}: Preparing to start move request".format(query_id))

    studies = query.dicomqrrspstudy_set.all()
    query.stage = u"Requesting move of {0} studies".format(studies.count())
    query.save()
    logger.info(u"Query_id {0}: Requesting move of {1} studies".format(query_id, studies.count()))

    study_no = 0
    for study in studies:
        study_no += 1
        logger.debug(u"Mv: study_no {0}".format(study_no))
        series_no = 0
        for series in study.dicomqrrspseries_set.all():
            series_no += 1
            logger.debug(u"Mv: study no {0} series no {1}".format(study_no, series_no))
            d = Dataset()
            d.StudyInstanceUID = study.study_instance_uid
            d.QueryRetrieveLevel = "SERIES"
            d.SeriesInstanceUID = series.series_instance_uid
            if series.number_of_series_related_instances:
                num_objects = u" Series contains {0} objects".format(series.number_of_series_related_instances)
            else:
                num_objects = u""
            query.stage = u"Requesting move: modality {0}, study {1} (of {2}) series {3} (of {4}).{5}".format(
                study.modality, study_no, studies.count(), series_no, study.dicomqrrspseries_set.all().count(),
                num_objects
            )
            logger.info(u"Requesting move: modality {0}, study {1} (of {2}) series {3} (of {4}).{5}".format(
                study.modality, study_no, studies.count(), series_no, study.dicomqrrspseries_set.all().count(),
                num_objects
            ))
            query.save()
            if not assoc.is_alive:
                logger.warning(u"Query_id {0}: Association has aborted, attempting to reconnect".format(query_id))
                assoc.Release(0)
                assoc = my_ae.RequestAssociation(remote_ae)
                if not assoc.is_alive:
                    logger.error(u"Query_id {0}: Association could not be re-established".format(query_id))
                    assoc.Release(0)
                    my_ae.Quit()
                    logger.debug(u"Query_id {0}: Move AE my_ae quit".format(query_id))
                    query.delete()
                    exit()
            logger.debug(u"_move_req launched")
            if series.image_level_move:
                d.QueryRetrieveLevel = "IMAGE"
                for image in series.dicomqrrspimage_set.all():
                    d.SOPInstanceUID = image.sop_instance_uid
                    logger.debug(u"Image-level move - d is: {0}".format(d))
                    _move_req(my_ae, assoc, d, study_no, series_no)
            else:
                logger.debug(u"Series-level move - d is: {0}".format(d))
                _move_req(my_ae, assoc, d, study_no, series_no)

    query.move_complete = True
    query.save()
    logger.info(u"Move complete")

    logger.debug(u"Query_id {0}: Releasing move association".format(query_id))
    assoc.Release(0)
    logger.info(u"Query_id {0}: Move association released".format(query_id))

    my_ae.Quit()
    logger.debug(u"Query_id {0}: Move AE my_ae quit".format(query_id))

    sleep(10)
    query.delete()


# def parse_args():
    # """Parse the command line args for the openrem_qr.py script.
    #
    # :param argv: sys.argv[1:] from command line call
    # :return: Dict of processed args
    # """
def _create_parser():
    import argparse

    parser = argparse.ArgumentParser(description='Query remote server and retrieve to OpenREM')
    parser.add_argument('qr_id', type=int, help='Database ID of the remote QR node')
    parser.add_argument('store_id', type=int, help='Database ID of the local store node')
    parser.add_argument('-ct', action="store_true", help='Query for CT studies. Do not use with -sr')
    parser.add_argument('-mg', action="store_true", help='Query for mammography studies. Do not use with -sr')
    parser.add_argument('-fl', action="store_true", help='Query for fluoroscopy studies. Do not use with -sr')
    parser.add_argument('-dx', action="store_true", help='Query for planar X-ray studies. Do not use with -sr')
    parser.add_argument('-f', '--dfrom', help='Date from, format yyyy-mm-dd', metavar='yyyy-mm-dd')
    parser.add_argument('-t', '--duntil', help='Date until, format yyyy-mm-dd', metavar='yyyy-mm-dd')
    parser.add_argument('-e', '--desc_exclude',
                        help='Terms to exclude in study description, comma separated, quote whole string',
                        metavar='string')
    parser.add_argument('-i', '--desc_include',
                        help='Terms that must be included in study description, comma separated, quote whole string',
                        metavar='string')
    parser.add_argument('-sne', '--stationname_exclude',
                        help='Terms to exclude in station name, comma separated, quote whole string',
                        metavar='string')
    parser.add_argument('-sni', '--stationname_include',
                        help='Terms to include in station name, comma separated, quote whole string',
                        metavar='string')
    parser.add_argument('-toshiba', action="store_true",
                        help='Advanced: Attempt to retrieve CT dose summary objects and one image from each series')
    parser.add_argument('-sr', action="store_true",
                        help='Advanced: Use if store has RDSRs only, no images. Cannot be used with -ct, -mg, -fl, -dx')
    parser.add_argument('-dup', action="store_true",
                        help="Advanced: Retrieve duplicates (objects that have been processed before)")

    return parser


def _process_args(parser_args, parser):
    import datetime
    from remapp.netdicom.tools import echoscu

    logger.info(u"qrscu script called")

    modalities = []
    if parser_args.ct:
        modalities += ['CT']
    if parser_args.mg:
        modalities += ['MG']
    if parser_args.fl:
        modalities += ['FL']
    if parser_args.dx:
        modalities += ['DX']
    if parser_args.sr:
        if modalities:
            parser.error(u"The sr option can not be combined with any other modalities")
        else:
            modalities += ['SR']

    if not modalities:
        parser.error(u"At least one modality must be specified")
    else:
        logger.info(u"Modalities are {0}".format(modalities))

    # Check if dates are in the right format, but keep them as strings
    try:
        if parser_args.dfrom:
            datetime.datetime.strptime(parser_args.dfrom, '%Y-%m-%d')
            logger.info(u"Date from: {0}".format(parser_args.dfrom))
        if parser_args.duntil:
            datetime.datetime.strptime(parser_args.duntil, '%Y-%m-%d')
            logger.info(u"Date until: {0}".format(parser_args.duntil))
    except ValueError:
        parser.error(u"Incorrect data format, should be YYYY-MM-DD")

    if parser_args.desc_exclude:

        study_desc_exc = [x.strip().lower() for x in parser_args.desc_exclude.split(u',')]
        logger.info(u"Study description exclude terms are {0}".format(study_desc_exc))
    else:
        study_desc_exc = None
    if parser_args.desc_include:
        study_desc_inc = [x.strip().lower() for x in parser_args.desc_include.split(u',')]
        logger.info(u"Study description include terms are {0}".format(study_desc_inc))
    else:
        study_desc_inc = None

    if parser_args.stationname_exclude:
        stationname_exc = [x.strip().lower() for x in parser_args.stationname_exclude.split(u',')]
        logger.info(u"Stationname exclude terms are {0}".format(stationname_exc))
    else:
        stationname_exc = None
    if parser_args.stationname_include:
        stationname_inc = [x.strip().lower() for x in parser_args.stationname_include.split(u',')]
        logger.info(u"Stationname include terms are {0}".format(stationname_inc))
    else:
        stationname_inc = None

    filters = {
                'stationname_inc' : stationname_inc,
                'stationname_exc' : stationname_exc,
                'study_desc_inc'  : study_desc_inc,
                'study_desc_exc'  : study_desc_exc,
              }

    remove_duplicates = not(parser_args.dup)  # if flag, duplicates will be retrieved.

    get_toshiba = parser_args.toshiba

    qr_node_up = echoscu(parser_args.qr_id, qr_scp=True)
    store_node_up = echoscu(parser_args.store_id, store_scp=True)

    if qr_node_up is not "Success" or store_node_up is not "Success":
        logger.error(u"Query-retrieve aborted: DICOM nodes not ready. QR SCP echo is {0}, Store SCP echo is {1}".format(
            qr_node_up, store_node_up))
        sys.exit(u"Query-retrieve aborted: DICOM nodes not ready. QR SCP echo is {0}, Store SCP echo is {1}".format(
            qr_node_up, store_node_up))

    return_args = {'qr_id': parser_args.qr_id,
                   'store_id': parser_args.store_id,
                   'modalities': modalities,
                   'remove_duplicates': remove_duplicates,
                   'dfrom': parser_args.dfrom,
                   'duntil': parser_args.duntil,
                   'filters': filters,
                   'get_toshiba': get_toshiba}

    return return_args


def qrscu_script():
    """Query-Retrieve function that can be called by the openrem_qr.py script. Always triggers a move.

    :param args: sys.argv from command line call
    :return:
    """

    parser = _create_parser()
    args = parser.parse_args()
    processed_args = _process_args(args, parser)
    sys.exit(
        qrscu.delay(qr_scp_pk=processed_args['qr_id'],
                    store_scp_pk=processed_args['store_id'],
                    move=True,
                    modalities=processed_args['modalities'],
                    remove_duplicates=processed_args['remove_duplicates'],
                    date_from=processed_args['dfrom'],
                    date_until=processed_args['duntil'],
                    filters=processed_args['filters'],
                    get_toshiba_images=processed_args['get_toshiba']
                    )
    )


# if __name__ == "__main__":
#     parser = _create_parser()
#     args = parser.parse_args()
#     processed_args = _process_args(args, parser)
#     sys.exit(
#         qrscu.delay(qr_scp_pk=processed_args['qr_id'],
#                     store_scp_pk=processed_args['store_id'],
#                     move=True,
#                     modalities=processed_args['modalities'],
#                     remove_duplicates=processed_args['remove_duplicates'],
#                     date_from=processed_args['dfrom'],
#                     date_until=processed_args['duntil'],
#                     filters=processed_args['filters'],
#                     get_toshiba_images=processed_args['get_toshiba']
#                     )
#     )
