# This Python file uses the following encoding: utf-8
#!/usr/bin/python

"""
Query/Retrieve SCU AE example.

This demonstrates a simple application entity that support the Patient
Root Find and Move SOP Classes as SCU. In order to receive retrieved
datasets, this application entity must support the CT Image Storage
SOP Class as SCP as well. For this example to work, there must be an
SCP listening on the specified host and port.

For help on usage,
python qrscu.py -h
"""

from celery import shared_task
import django
import logging
import os
import sys
import uuid
import collections


# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

logger = logging.getLogger('remapp.netdicom.qrscu')  # Explicitly named so that it is still handled when using __main__

from remapp.netdicom.tools import _create_ae


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


def _prune_series_responses(MyAE, RemoteAE, assoc, query, all_mods, filters):
    """
    For each study level response, remove any series that we know can't be used.
    :param MyAE: Calling AE Tile
    :param RemoteAE: Called AE Title
    :param query: Current DicomQuery object
    :param all_mods: Ordered dict of dicts detailing modalities we are interested in
    :param filters: Include and exclude lists for StationName (and StudyDescription)
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
        if all_mods['MG']['inc'] and 'MG' in study.get_modalities_in_study():
            study.modality = u'MG'
            study.save()

            if 'SR' in study.get_modalities_in_study() and _check_sr_type_in_study(
                    MyAE, RemoteAE, assoc, study, query.query_id) == 'RDSR':
                logger.debug(u"Found RDSR in MG study, so keep SR and delete all other series")
                series = study.dicomqrrspseries_set.all()
                series.exclude(modality__exact='SR').delete()
            elif 'SR' in study.get_modalities_in_study():
                logger.debug(u"SR in DX study not RDSR, so deleting")
                series = study.dicomqrrspseries_set.all()
                series.filter(modality__exact='SR').delete()

            # ToDo: query each series at image level in case SOP Class UID is returned and raw/processed duplicates can
            # be weeded out
        elif all_mods['DX']['inc'] and any(mod in study.get_modalities_in_study() for mod in ('CR', 'DX')):
            study.modality = u'DX'
            study.save()

            if 'SR' in study.get_modalities_in_study() and _check_sr_type_in_study(
                    MyAE, RemoteAE, assoc, study, query.query_id) == 'RDSR':
                logger.debug(u"Found RDSR in DX study, so keep SR and delete all other series")
                series = study.dicomqrrspseries_set.all()
                series.exclude(modality__exact='SR').delete()
            elif 'SR' in study.get_modalities_in_study():
                logger.debug(u"SR in DX study not RDSR, so deleting")
                series = study.dicomqrrspseries_set.all()
                series.filter(modality__exact='SR').delete()

        elif all_mods['FL']['inc'] and any(mod in study.get_modalities_in_study() for mod in ('XA', 'RF')):
            study.modality = 'FL'
            study.save()
            sr_type = _check_sr_type_in_study(MyAE, RemoteAE, assoc, study, query.query_id)
            logger.debug(u"FL study, check_sr_type returned {0}".format(sr_type))
            series = study.dicomqrrspseries_set.all()
            series.exclude(modality__exact='SR').delete()

        elif all_mods['CT']['inc'] and 'CT' in study.get_modalities_in_study():
            study.modality = 'CT'
            study.save()
            series = study.dicomqrrspseries_set.all()
            if 'SR' in study.get_modalities_in_study():
                SR_type = _check_sr_type_in_study(MyAE, RemoteAE, assoc, study, query.query_id)
                if SR_type == 'RDSR':
                    logger.debug(u"Found RDSR in CT study, so keep SR and delete all other series")
                    series.exclude(modality__exact='SR').delete()
                elif SR_type == 'ESR':  # GE CT's with ESR instead of RDSR
                    logger.debug(u"Found ESR in CT study, so keep SR and delete all other series")
                    series.exclude(modality__exact='SR').delete()
                else:
                    # non-dose SR, so check for Philips dose info series
                    series_descriptions = set(val for dic in series.values('series_description') for val in dic.values())
                    if (series_descriptions != set([None])):
                        series.exclude(series_description__iexact='dose info').delete()
                    else:
                        series.filter(number_of_series_related_instances__gt=5).delete()
            else:
                # if SR not present in study, only keep Philips dose info series
                # skip this step for PACS systems returning (only) empty seriesdescriptions
                series_descriptions = set(val for dic in series.values('series_description') for val in dic.values())
                if (series_descriptions != set([None])):
                    series.exclude(series_description__iexact='dose info').delete()
                else:
                    series.filter(number_of_series_related_instances__gt=5).delete()

        elif all_mods['SR']['inc']:
            sr_type = _check_sr_type_in_study(MyAE, RemoteAE, assoc, study, query.query_id)
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
def _check_sr_type_in_study(my_ae, remote_ae, assoc, study, query_id):
    """
    Checks at an image level whether SR in study is RDSR, ESR, or something else (Radiologist's report for example)
    :param my_ae: Calling AE Title
    :param remote_ae: Called AE Title
    :param study: Study to check SR type of
    :return: String of 'RDSR', 'ESR', or 'no_dose_report'
    """
    # select series with modality SR
    series_sr = study.dicomqrrspseries_set.filter(modality__exact='SR')
    logger.info(u"Number of series with SR {0}".format(series_sr.count()))
    sopclasses = set()
    for sr in series_sr:
        _query_images(my_ae, remote_ae, assoc, sr, query_id)
        images = sr.dicomqrrspimage_set.all()
        if images.count() == 0:
            logger.debug(u"Oops, series {0} of study instance UID {1} doesn't have any images in!".format(
                sr.series_number, study.study_instance_uid))
            continue
        sopclasses.add(images[0].sop_class_uid)
        sr.sop_class_in_series = images[0].sop_class_uid
        sr.save()
        logger.info(u"studyuid: {0}   seriesuid: {1}   nrimages: {2}   sopclasses: {3}".format(
            study.study_instance_uid, sr.series_instance_uid, images.count(), sopclasses))
    logger.info(u"sopclasses: {0}".format(sopclasses))
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


def _query_images(my_ae, remote_ae, assoc, seriesrsp, query_id):
    from remapp.models import DicomQRRspImage
    from dicom.dataset import Dataset

    logger.debug(u'Query_id {0}: In _query_images'.format(query_id))

    d3 = Dataset()
    d3.QueryRetrieveLevel = "IMAGE"
    d3.SeriesInstanceUID = seriesrsp.series_instance_uid
    d3.SOPInstanceUID = ''
    d3.SOPClassUID = ''
    d3.InstanceNumber = ''
    d3.SpecificCharacterSet = ''

    logger.debug(u'Query_id {0}: query is {1}'.format(query_id, d3))

    # assoc_images = my_ae.RequestAssociation(remote_ae)

    # if not assoc_images:
    #     logger.warning(u"Query_id {0}: Query series association must have failed, trying again".format(query_id))
    #     sleep(2)
    #     assoc_images = my_ae.RequestAssociation(remote_ae)
    #     if not assoc_images:
    #         logger.error(
    #            u"Query_id {0}: Query instance association failed. Me: {1}, Remote: {2}, Study UID: {3}, "
    #            u"Se UID {4}, Im {5}".format(
    #                query_id, my_ae, remote_ae, d3.SOPInstanceUID, d3.SeriesInstanceUID, d3.InstanceNumber))
    #         return

    st3 = assoc.StudyRootFindSOPClass.SCU(d3, 1)

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

    # assoc_images.Release(0)


def _query_series(my_ae, remote_ae, assoc, d2, studyrsp, query_id):
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

    logger.debug(u'Query_id {0}: In _query_series'.format(query_id))
    logger.debug(u'Query_id {0}: series query is {1}'.format(query_id, d2))

    # assoc_series = my_ae.RequestAssociation(remote_ae)

    # if not assoc_series:
    #     logger.warning(u"Query_id {0}: Query series association must have failed, trying again".format(query_id))
    #     sleep(2)
    #     assoc_series = my_ae.RequestAssociation(remote_ae)
    #     if not assoc_series:
    #         logger.error(
    #             u"Query_id {0}: Query series association has failed. Me: {1}, Remote: {2}, StudyInstanceUID: {3},"
    #             u" SeriesInstanceUID: {4}".format(
    #                 query_id, my_ae, remote_ae, d2.StudyInstanceUID, d2.SeriesInstanceUID))
    #         return

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
        logger.debug(u"Series Response {0}: Modality {1}, StationName {2}, StudyUID {3}, Series No. {4}, "
                     u"Series description {5}".format(
                            seRspNo, seriesrsp.modality, seriesrsp.station_name, d2.StudyInstanceUID,
                            seriesrsp.series_number, seriesrsp.series_description))

        seriesrsp.save()

    # assoc_series.Release(0)


def _query_study(my_ae, remote_ae, assoc, d, query, query_id):
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
    # assoc = my_ae.RequestAssociation(remote_ae)
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

    # assoc.Release(0)
    # logger.debug(u'Query_id {0}: Study level association released'.format(query_id))



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


def _query_for_each_modality(all_mods, query, d, MyAE, RemoteAE, assoc):
    """
    Uses _query_study for each modality we've asked for, and populates study level response data in the database
    :param all_mods: dict of dicts indicating which modalities to request
    :param query: DicomQuery object
    :param d: Dataset object containing StudyDate
    :param MyAE: Calling AE Title
    :param RemoteAE: Called AE Title
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
                    query_id = uuid.uuid4()
                    _query_study(MyAE, RemoteAE, assoc, d, query, query_id)
                    study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
                    logger.debug(u"Queried for {0}, now have {1} study level responses".format(mod, study_rsp.count()))
                    for rsp in study_rsp:  # First check if modalities in study has been populated
                        if rsp.get_modalities_in_study():
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
      *args:
      **kwargs:

    Returns:
      : Series Instance UIDs are stored as rows in the database to be used by a move request. Move request is
      optionally triggered automatically.

    """

    from datetime import datetime

    from dicom.dataset import Dataset
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import GeneralStudyModuleAttr, DicomQuery, DicomRemoteQR, DicomStoreSCP
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

    my_ae = _create_ae(aet.encode('ascii', 'ignore'), transfer_syntax=ts)
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
    modalities_returned, modality_matching = _query_for_each_modality(all_mods, query, d, my_ae, remote_ae, assoc)

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

    # FIXME: why not perform at series level? Fixes the problem of additional series that might be missed, but
    # would need to be  combined with changes to extractor scripts
    if remove_duplicates:
        logger.debug(u"About to remove any studies we already have in the database")
        query.stage = u'Checking to see if any response studies are already in the OpenREM database'
        try:
            query.save()
        except Exception as e:
            logger.error(u"query.save in remove duplicates didn't work because of {0}".format(e))
        logger.info(
            u'Checking to see if any of the {0} studies are already in the OpenREM database'.format(study_rsp.count()))
        for uid in study_rsp.values_list('study_instance_uid', flat=True):
            if GeneralStudyModuleAttr.objects.filter(study_instance_uid=uid).exists():
                study_rsp.filter(study_instance_uid__exact=uid).delete()
        study_rsp = query.dicomqrrspstudy_set.all()
        logger.info(u'After removing studies we already have in the db, {0} studies are left'.format(study_rsp.count()))

    filter_logs = []
    if filters['study_desc_inc']:
        filter_logs += [u"study description includes {0}, ".format(u", ".join(filters['study_desc_inc']))]
    if filters['study_desc_exc']:
        filter_logs += [u"study description excludes {0}, ".format(u", ".join(filters['study_desc_exc']))]
    if filters['stationname_inc']:
        filter_logs += [u"station name includes {0}, ".format(u", ".join(filters['stationname_inc']))]
    if filters['stationname_exc']:
        filter_logs += [u"station name excludes {0}, ".format(u", ".join(filters['stationname_exc']))]

    logger.info(u"Pruning study responses based on inc/exc options: {0}".format(u"".join(filter_logs)))
    _prune_study_responses(query, filters)
    study_rsp = query.dicomqrrspstudy_set.all()
    logger.info(u'Now have {0} studies'.format(study_rsp.count()))

    for rsp in study_rsp:
        # Series level query
        d2 = Dataset()
        d2.StudyInstanceUID = rsp.study_instance_uid
        _query_series(my_ae, remote_ae, assoc, d2, rsp, query_id)
        if not modalities_returned:
            logger.debug(u"modalities_returned = False, so building from series info")
            series_rsp = rsp.dicomqrrspseries_set.all()
            rsp.set_modalities_in_study(list(set(val for dic in series_rsp.values('modality') for val in dic.values())))

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

    logger.debug(u"Pruning series responses")
    _prune_series_responses(my_ae, remote_ae, assoc, query, all_mods, filters)

    study_rsp = query.dicomqrrspstudy_set.all()
    logger.info(u'Now have {0} studies'.format(study_rsp.count()))

    # done
    my_ae.Quit()
    query.complete = True
    query.stage = u"Query complete"
    query.save()

    logger.debug(u"Query {0} complete. Move is {1}. Query took {2}".format(
        query.query_id, move, datetime.now() - debug_timer))

    if move:
        movescu.delay(str(query.query_id))


def _move_req(my_ae, remote_ae, assoc, d, study_no, series_no):
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
    query = DicomQuery.objects.get(query_id=query_id)
    query.move_complete = False
    query.failed = False
    query.save()
    qr_scp = query.qr_scp_fk
    store_scp = query.store_scp_fk

    my_ae = _create_ae(store_scp.aetitle.encode('ascii', 'ignore'))
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
        d = Dataset()
        d.StudyInstanceUID = study.study_instance_uid
        series_no = 0
        for series in study.dicomqrrspseries_set.all():
            series_no += 1
            logger.debug(u"Mv: study no {0} series no {1}".format(study_no, series_no))
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
            _move_req(my_ae, remote_ae, assoc, d, study_no, series_no)

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


def parse_args(argv):
    """
    Parse the command line args for the openrem_qr.py script.
    :param argv: sys.argv[1:] from command line call
    :return: Dict of processed args
    """

    import argparse
    import datetime
    from remapp.netdicom.tools import echoscu

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
    parser.add_argument('-sr', action="store_true",
                        help='Advanced: Query for structured report only studies. Cannot be used with -ct, -mg, -fl, -dx')
    parser.add_argument('-dup', action="store_true",
                        help="Advanced: Retrieve duplicates (studies that are already in database)")
    args = parser.parse_args(argv)

    logger.info(u"qrscu script called")

    modalities = []
    if args.ct:
        modalities += ['CT']
    if args.mg:
        modalities += ['MG']
    if args.fl:
        modalities += ['FL']
    if args.dx:
        modalities += ['DX']
    if args.sr:
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
        if args.dfrom:
            datetime.datetime.strptime(args.dfrom, '%Y-%m-%d')
            logger.info(u"Date from: {0}".format(args.dfrom))
        if args.duntil:
            datetime.datetime.strptime(args.duntil, '%Y-%m-%d')
            logger.info(u"Date until: {0}".format(args.duntil))
    except ValueError:
        parser.error(u"Incorrect data format, should be YYYY-MM-DD")

    if args.desc_exclude:

        study_desc_exc = [x.strip().lower() for x in args.desc_exclude.split(u',')]
        logger.info(u"Study description exclude terms are {0}".format(study_desc_exc))
    else:
        study_desc_exc = None
    if args.desc_include:
        study_desc_inc = [x.strip().lower() for x in args.desc_include.split(u',')]
        logger.info(u"Study description include terms are {0}".format(study_desc_inc))
    else:
        study_desc_inc = None

    if args.stationname_exclude:
        stationname_exc = [x.strip().lower() for x in args.stationname_exclude.split(u',')]
        logger.info(u"Stationname exclude terms are {0}".format(stationname_exc))
    else:
        stationname_exc = None
    if args.stationname_include:
        stationname_inc = [x.strip().lower() for x in args.stationname_include.split(u',')]
        logger.info(u"Stationname include terms are {0}".format(stationname_inc))
    else:
        stationname_inc = None

    filters = {
                'stationname_inc' : stationname_inc,
                'stationname_exc' : stationname_exc,
                'study_desc_inc'  : study_desc_inc,
                'study_desc_exc'  : study_desc_exc,
              }

    remove_duplicates = not(args.dup)  # if flag, duplicates will be retrieved.

    qr_node_up = echoscu(args.qr_id, qr_scp=True)
    store_node_up = echoscu(args.store_id, store_scp=True)

    if qr_node_up is not "Success" or store_node_up is not "Success":
        logger.error(u"Query-retrieve aborted: DICOM nodes not ready. QR SCP echo is {0}, Store SCP echo is {1}".format(
            qr_node_up, store_node_up))
        sys.exit(u"Query-retrieve aborted: DICOM nodes not ready. QR SCP echo is {0}, Store SCP echo is {1}".format(
            qr_node_up, store_node_up))

    processed_args = {'qr_id': args.qr_id,
                      'store_id': args.store_id,
                      'modalities': modalities,
                      'remove_duplicates': remove_duplicates,
                      'dfrom': args.dfrom,
                      'duntil': args.duntil,
                      'filters': filters}

    return processed_args


def qrscu_script():
    """
    Query-Retrieve function that can be called by the openrem_qr.py script. Always triggers a move.
    :param args: sys.argv from command line call
    :return:
    """

    parsed_args = parse_args(sys.argv[1:])
    sys.exit(
        qrscu.delay(qr_scp_pk=parsed_args['qr_id'],
                    store_scp_pk=parsed_args['store_id'],
                    move=True,
                    modalities=parsed_args['modalities'],
                    remove_duplicates=parsed_args['remove_duplicates'],
                    date_from=parsed_args['dfrom'],
                    date_until=parsed_args['duntil'],
                    filters=parsed_args['filters'],
                    )
    )


if __name__ == "__main__":
    qrscu_script()
