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

import logging

# call back
def OnAssociateResponse(association):
    logging.info("Association response received")


def OnAssociateRequest(association):
    logging.info("Association resquested")
    return True

def _move_req(my_ae, remote_ae, d):
    logging.debug("Requesting move association")
    assocMove = my_ae.RequestAssociation(remote_ae)
    logging.info("Move association requested")
    gen = assocMove.StudyRootMoveSOPClass.SCU(d, my_ae.getName(), 1)
    for gg in gen:
        logging.info("gg is %s", gg)
    logging.debug("Releasing move association")
    assocMove.Release(0)
    logging.info("Move association released")


def _query_series(my_ae, remote_ae, d2, studyrsp):
    from time import sleep
    import uuid
    from remapp.tools.dcmdatetime import make_date
    from remapp.models import DicomQRRspSeries
    d2.QueryRetrieveLevel = "SERIES"
    d2.SeriesDescription = ''
    d2.SeriesNumber = ''
    d2.SeriesInstanceUID = ''
    d2.Modality = ''
    d2.NumberOfSeriesRelatedInstances = ''

    logging.debug('d2: {0}'.format(d2))

    assoc_series = my_ae.RequestAssociation(remote_ae)

    if not assoc_series:
        logging.warning("Query series association must have failed, trying again")
        sleep(2)
        assoc_series = my_ae.RequestAssociation(remote_ae)
        if not assoc_series:
            logging.error(
                "Query series association has failed. Me: {0}, Remote: {1}, StudyInstanceUID: {2}, SeriesInstanceUID: {3}".format(
                    my_ae, remote_ae, d2.StudyInstanceUID, d2.SeriesInstanceUID))
            return

    st2 = assoc_series.StudyRootFindSOPClass.SCU(d2, 1)

    query_id = uuid.uuid4()

    logging.debug('In _query_series')
    seRspNo = 0

    for series in st2:
        if not series[1]:
            continue
        seRspNo += 1
        logging.debug("Series Response {0}: {1}".format(seRspNo, series[1]))
        seriesrsp = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=studyrsp)
        seriesrsp.query_id = query_id
        # Mandatory tags
        seriesrsp.series_instance_uid= series[1].SeriesInstanceUID
        seriesrsp.modality = series[1].Modality
        seriesrsp.series_number = series[1].SeriesNumber
        # Optional useful tags
        try:
            seriesrsp.series_description = series[1].SeriesDescription.strip().lower()
        except AttributeError:
            pass
        try:
            seriesrsp.number_of_series_related_instances = series[1].NumberOfSeriesRelatedInstances
        except AttributeError:
            pass
        seriesrsp.save()

    assoc_series.Release(0)

def _query_study(assoc, my_ae, remote_ae, d, query, query_id):
    from decimal import Decimal
    from dicom.dataset import Dataset
    from remapp.models import DicomQRRspStudy
    from remapp.tools.dcmdatetime import make_date

    assoc_study = my_ae.RequestAssociation(remote_ae)
    st = assoc_study.StudyRootFindSOPClass.SCU(d, 1)
    logging.debug('_query_study done with status "%s"' % st)

    # TODO: Replace the code below to deal with find failure
    # if not st:
    #     query.failed = True
    #     query.message = "Study Root Find unsuccessful"
    #     query.complete = True
    #     query.save()
    #     MyAE.Quit()
    #     return

    rspno = 0

    for ss in st:
        if not ss[1]:
            continue
        rspno += 1
        logging.debug("Response {0}, ss1 is {1}".format(rspno, ss[1]))
        rsp = DicomQRRspStudy.objects.create(dicom_query=query)
        rsp.query_id = query_id
        # Unique key
        rsp.study_instance_uid = ss[1].StudyInstanceUID
        # Required keys - none of interest
        # Optional and special keys
        try:
            rsp.study_description = ss[1].StudyDescription
        except AttributeError:
            pass
        # Series level query
        d2 = Dataset()
        d2.StudyInstanceUID = rsp.study_instance_uid
        _query_series(my_ae, remote_ae, d2, rsp)
        # Populate modalities_in_study, stored as JSON
        try:
            rsp.set_modalities_in_study(ss[1].ModalitiesInStudy.split(','))
        except:
            series_rsp = rsp.dicomqrrspseries_set.all()
            rsp.set_modalities_in_study(list(set(val for dic in series_rsp.values('modality') for val in dic.values())))
        rsp.modality = None  # Used later
        rsp.save()

    assoc_study.Release(0)

from celery import shared_task

@shared_task
def qrscu(
        qr_scp_pk=None, store_scp_pk=None,
        implicit=False, explicit=False, move=False, query_id=None,
        date_from=None, date_until=None, modalities=None, inc_sr=True, duplicates=True, *args, **kwargs):
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
      inc_sr(bool, optional): Include studies that only have structured reports in (unknown modality) (Default value = True)
      duplicates(bool, optional): If True, studies that already exist in the database are removed from the query results (Default value = True)
      *args: 
      **kwargs: 

    Returns:
      : Series Instance UIDs are stored as rows in the database to be used by a move request. Move request is
      optionally triggered automatically.

    """


    import uuid
    import json
    from netdicom.applicationentity import AE
    from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
    from dicom.dataset import Dataset, FileDataset
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import GeneralStudyModuleAttr, DicomQuery, DicomRemoteQR, DicomStoreSCP
    from remapp.tools.dcmdatetime import make_date, make_dcm_date_range

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

    all_mods = {'CT': {'inc': False, 'mods': ['CT']},
                'MG': {'inc': False, 'mods': ['MG']},
                'FL': {'inc': False, 'mods': ['RF','XA']},
                'DX': {'inc': False, 'mods': ['DX','CR']}
                }
    # Reasoning regarding PET-CT: Some PACS allocate study modality PT, some CT, some depending on order received.
    # If ModalitiesInStudy is used for matching on C-Find, the CT from PET-CT will be picked up.
    # If not, then the PET-CT will be returned with everything else, and the CT will show up in the series level
    # query. Therefore, there is no need to search for PT at any stage.
    for m in all_mods:
        if m in modalities:
            all_mods[m]['inc'] = True

    # create application entity with Find and Move SOP classes as SCU
    MyAE = AE(aet.encode('ascii','ignore'), 0, [StudyRootFindSOPClass,
                                 StudyRootMoveSOPClass,
                                 VerificationSOPClass], [], ts)
    MyAE.OnAssociateResponse = OnAssociateResponse
    MyAE.OnAssociateRequest = OnAssociateRequest
    # MyAE.OnReceiveStore = OnReceiveStore
    MyAE.start()

    # remote application entity
    RemoteAE = dict(Address=rh, Port=rp, AET=aec.encode('ascii','ignore'))

    if not query_id:
        query_id = uuid.uuid4()

    query = DicomQuery.objects.create()
    query.query_id = query_id
    query.complete = False
    query.store_scp_fk = DicomStoreSCP.objects.get(pk=store_scp_pk)
    query.qr_scp_fk = qr_scp
    query.save()

    # create association with remote AE
    logging.debug("Request association with {0} {1} {2}".format(rh, rp, aec))
    assoc = MyAE.RequestAssociation(RemoteAE)

    if not assoc:
        query.failed = True
        query.message = "Association unsuccessful"
        query.complete = True
        query.save()
        MyAE.Quit()
        return
    logging.info("assoc is ... %s", assoc)

    # perform a DICOM ECHO
    logging.info("DICOM Echo ... ")
    echo = assoc.VerificationSOPClass.SCU(1)
    logging.info('done with status %s', echo)

    logging.info("DICOM FindSCU ... ")
    d = Dataset()
    d.QueryRetrieveLevel = "STUDY"
    d.PatientName = ''
    d.PatientID = ''
    d.AccessionNumber = ''
    d.ModalitiesInStudy = ''
    d.StudyDescription = ''
    d.StudyID = ''
    d.StudyInstanceUID = ''
    d.StudyTime = ''
    d.PatientAge = ''
    d.PatientBirthDate = ''
    d.NumberOfStudyRelatedSeries = ''

    d.StudyDate = make_dcm_date_range(date_from, date_until)
    if not d.StudyDate:
        d.StudyDate = ''

    modality_matching = True
    trip = 0

    for selection, details in all_mods.iteritems():
        if details['inc']:  # No need to check for modality_matching here as modalities_left would also be false
            for mod in details['mods']:
                query.stage = 'Currently querying for {0} studies...'.format(mod)
                query.save()
                logging.info('Currently querying for {0} studies...'.format(mod))
                trip += 1
                if modality_matching:
                    d.ModalitiesInStudy = mod
                    query_id = uuid.uuid4()
                    _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
                    study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
                    for rsp in study_rsp:
                        if mod not in rsp.get_modalities_in_study():
                            modality_matching = False
                            break  # This indicates that there was no modality match, so we have everything already

    if inc_sr and modality_matching:
        query.stage = 'Currently querying for SR only studies'
        query.save()
        logging.info('Currently querying for SR only studies')
        d.ModalitiesInStudy = 'SR'
        query_id = uuid.uuid4()
        _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
        # Nothing to gain by checking the response


    # Now we have all our studies. Time to throw away any we don't want
    study_rsp = query.dicomqrrspstudy_set.all()

    if duplicates:
        query.stage = 'Checking to see if any response studies are already in the OpenREM database'
        query.save()
        logging.info('Checking to see if any of the {0} studies are already in the OpenREM database'.format(study_rsp.count()))
        for uid in study_rsp.values_list('study_instance_uid', flat=True):
            if GeneralStudyModuleAttr.objects.filter(study_instance_uid=uid).exists():
                study_rsp.filter(study_instance_uid__exact = uid).delete()
        logging.info('Now have {0} studies'.format(study_rsp.count()))

    mods_in_study_set = set(val for dic in study_rsp.values('modalities_in_study') for val in dic.values())
    logging.debug("mods in study are: {0}".format(study_rsp.values('modalities_in_study')))
    query.stage = "Deleting studies we didn't ask for"
    query.save()
    logging.info("Deleting studies we didn't ask for")
    logging.debug("mods_in_study_set is {0}".format(mods_in_study_set))
    for mod_set in mods_in_study_set:
        logging.debug("mod_set is {0}".format(mod_set))
        delete = True
        for mod_choice, details in all_mods.iteritems():
            logging.debug("mod_choice {0}, details {1}".format(mod_choice, details))
            if details['inc']:
                for mod in details['mods']:
                    logging.info("mod is {0}, mod_set is {1}".format(mod, mod_set))
                    if mod in mod_set:
                        delete = False
                        continue
                    if inc_sr and 'SR' in mod_set:
                        delete = False
        if delete:
            studies_to_delete = study_rsp.filter(modalities_in_study__exact = mod_set)
            studies_to_delete.delete()
    logging.info('Now have {0} studies'.format(study_rsp.count()))

    # Now we need to delete any unwanted series
    query.stage = "Deleting series we can't use"
    query.save()
    logging.info("Deleting series we can't use")
    for study in study_rsp:
        if all_mods['MG']['inc'] and 'MG' in study.get_modalities_in_study():
            study.modality = 'MG'
            study.save()
            # ToDo: query each series at image level in case SOP Class UID is returned and raw/processed duplicates can
            # be weeded out
        if all_mods['DX']['inc']:
            if 'CR' in study.get_modalities_in_study() or 'DX' in study.get_modalities_in_study():
                study.modality = 'DX'
                study.save()
                # ToDo: query each series at image level in case SOP Class UID is returned and real CR can be removed
        if all_mods['FL']['inc']:
            if 'RF' in study.get_modalities_in_study() or 'XA' in study.get_modalities_in_study():
                study.modality = 'FL'
                study.save()
                # Assume structured reports have modality 'SR' at series level?
                series = study.dicomqrrspseries_set.all()
                for s in series:
                    if s.modality != 'SR':
                        s.delete()
        if all_mods['CT']['inc'] and 'CT' in study.get_modalities_in_study():
            study.modality = 'CT'
            study.save()
            if 'SR' in study.get_modalities_in_study():
                series = study.dicomqrrspseries_set.all()
                for s in series:
                    if s.modality != 'SR':
                        s.delete()
            else:
                series = study.dicomqrrspseries_set.all()
                series_descriptions = set(val for dic in series.values('series_description') for val in dic.values())
                if 'dose info' in series_descriptions:  # i.e. Philips dose info series
                    for s in series:
                        if s.series_description != 'dose info':
                            s.delete()
    logging.info('Now have {0} studies'.format(study_rsp.count()))

    logging.info("Release association")
    assoc.Release(0)

    # done
    MyAE.Quit()
    query.complete = True
    query.stage = "Query complete"
    query.save()

    if move:
        movescu(query.query_id)





@shared_task
def movescu(query_id):
    """C-Move request element of query-retrieve service class user

    Args:
      query_id: 

    Returns:

    """
    from time import sleep
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from dicom.dataset import Dataset
    from netdicom.applicationentity import AE
    from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
    from remapp.models import DicomQuery, DicomRemoteQR, DicomStoreSCP

    query = DicomQuery.objects.get(query_id = query_id)
    query.move_complete = False
    query.failed = False
    query.save()
    qr_scp = query.qr_scp_fk
    store_scp = query.store_scp_fk

    ts = [
        ExplicitVRLittleEndian,
        ImplicitVRLittleEndian,
        ExplicitVRBigEndian
        ]

    if qr_scp.hostname:
        rh = qr_scp.hostname
    else:
        rh = qr_scp.ip

    my_ae = AE(store_scp.aetitle.encode('ascii','ignore'), 0, [StudyRootFindSOPClass,
                                 StudyRootMoveSOPClass,
                                 VerificationSOPClass], [], ts)
    my_ae.OnAssociateResponse = OnAssociateResponse
    my_ae.OnAssociateRequest = OnAssociateRequest
    # MyAE.OnReceiveStore = OnReceiveStore
    my_ae.start()

    # remote application entity
    remote_ae = dict(Address=rh, Port=qr_scp.port, AET=qr_scp.aetitle.encode('ascii','ignore'))

    query.stage = "Preparing to start move request"
    query.save()
    logging.info("Preparing to start move request")

    studies = query.dicomqrrspstudy_set.all()
    query.stage = "Requesting move of {0} studies".format(studies.count())
    query.save()
    logging.info("Requesting move of {0} studies".format(studies.count()))

    study_no = 0
    for study in studies:
        study_no += 1
        logging.info("Mv: study_no {0}".format(study_no))
        d = Dataset()
        d.StudyInstanceUID = study.study_instance_uid
        series_no = 0
        for series in study.dicomqrrspseries_set.all():
            series_no += 1
            logging.info("Mv: study no {0} series no {1}".format(study_no, series_no))
            d.QueryRetrieveLevel = "SERIES"
            d.SeriesInstanceUID = series.series_instance_uid
            if series.number_of_series_related_instances:
                num_objects = ", {0} objects".format(series.number_of_series_related_instances)
            else:
                num_objects = ""
            query.stage = "Requesting move of {0}; series {3} of {4} of study {1} of {2}{5}".format(
                study.modality, study_no, studies.count(), series_no, study.dicomqrrspseries_set.all().count(),
                num_objects
            )
            logging.info("Requesting move of {0}; series {3} of {4} of study {1} of {2}{5}".format(
                study.modality, study_no, studies.count(), series_no, study.dicomqrrspseries_set.all().count(),
                num_objects
            ))
            query.save()
            _move_req(my_ae, remote_ae, d)
            logging.info("_move_req launched")

    query.move_complete = True
    query.save()
    logging.info("Move complete")

    my_ae.Quit()

    sleep(10)
    query.delete()


def qrscu_script(*args, **kwargs):
    """Query-Retrieve function that can be called by the openrem_qr.py script. Always triggers a move.

    Args:
        *args:
        **kwargs:

    Returns:

    """

    import argparse
    import datetime
    import django
    import os
    import sys

    # setup django/OpenREM
    basepath = os.path.dirname(__file__)
    projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
    if projectpath not in sys.path:
        sys.path.insert(1,projectpath)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
    django.setup()

    # parse commandline
    parser = argparse.ArgumentParser(description='Query remote server and retrieve to OpenREM')
    parser.add_argument('qrid', type=int, help='Database ID of the remote QR node')
    parser.add_argument('storeid', type=int, help='Database ID of the local store node')
    parser.add_argument('-ct', action="store_true", help='Query for CT studies')
    parser.add_argument('-mg', action="store_true", help='Query for mammography studies')
    parser.add_argument('-fl', action="store_true", help='Query for fluoroscopy studies')
    parser.add_argument('-dx', action="store_true", help='Query for planar X-ray studies')
    parser.add_argument('-sr', action="store_true", help='Query for structured report only studies')
    parser.add_argument('-dfrom', help='Date from, format yyyy-mm-dd')
    parser.add_argument('-duntil', help='Date until, format yyyy-mm-dd')
    parser.add_argument('-dup', action="store_true", help="Don't retrieve studies that are already in database")
    args = parser.parse_args()

    modalities = []
    if args.ct:
        modalities += ['CT']
    if args.mg:
        modalities += ['MG']
    if args.fl:
        modalities += ['FL']
    if args.dx:
        modalities += ['DX']

    try:
        if args.dfrom:
            datetime.datetime.strptime(args.dfrom, '%Y-%m-%d')
        if args.duntil:
            datetime.datetime.strptime(args.duntil, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    sys.exit(
        qrscu(qr_scp_pk=args.qrid, store_scp_pk=args.storeid, move=True, modalities=modalities, inc_sr=args.sr,
              duplicates=args.dup, date_from=args.dfrom, date_until=args.duntil
        )
    )
