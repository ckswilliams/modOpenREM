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


# call back
def OnAssociateResponse(association):
    print "Association response received"


def OnAssociateRequest(association):
    print "Association resquested"
    return True

def _move_req(my_ae, remote_ae, d):
    assocMove = my_ae.RequestAssociation(remote_ae)
    print "Move association requested"
    print "d is {0}".format(d)
    gen = assocMove.StudyRootMoveSOPClass.SCU(d, 'STOREOPENREM', 1)
    for gg in gen:
        print "gg is {0}".format(gg)
    assocMove.Release(0)
    print "Move association released"

def _try_query_return(rsp, tag):
    try:
        x = rsp.tag
    except:
        x = None
    return x

def _query_series(my_ae, remote_ae, d2, studyrsp):
    import uuid
    from remapp.tools.dcmdatetime import make_date
    from remapp.models import DicomQRRspSeries
    d2.QueryRetrieveLevel = "SERIES"
    d2.SeriesDescription = ''
    d2.SeriesNumber = ''
    d2.SeriesInstanceUID = ''
    d2.Modality = ''
    d2.NumberOfSeriesRelatedInstances = ''

    print 'd2: {0}'.format(d2)

    assoc_series = my_ae.RequestAssociation(remote_ae)

    st2 = assoc_series.StudyRootFindSOPClass.SCU(d2, 1)

    query_id = uuid.uuid4()

    print 'In _query_series'
    seRspNo = 0

    for series in st2:
        if not series[1]:
            continue
        seRspNo += 1
        print "Series Response {0}: {1}".format(seRspNo, series[1])
        seriesrsp = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=studyrsp)
        seriesrsp.query_id = query_id
        # Mandatory tags
        seriesrsp.series_instance_uid= series[1].SeriesInstanceUID
        seriesrsp.modality = series[1].Modality
        seriesrsp.series_number = series[1].SeriesNumber
        # Optional useful tags
        seriesrsp.series_description = _try_query_return(series[1], 'SeriesDescription')
        seriesrsp.number_of_series_related_instances = _try_query_return(series[1], 'NumberOfSeriesRelatedInstances')
        seriesrsp.save()

    assoc_series.Release(0)

def _query_study(assoc, my_ae, remote_ae, d, query, query_id):
    from decimal import Decimal
    from remapp.models import DicomQRRspStudy
    from remapp.tools.dcmdatetime import make_date

    assoc_study = my_ae.RequestAssociation(remote_ae)
    st = assoc_study.StudyRootFindSOPClass.SCU(d, 1)
    # print 'done with status "%s"' % st

    # TODO: Replace the code below to deal with find failure
    # if not st:
    #     query.failed = True
    #     query.message = "Study Root Find unsuccessful"
    #     query.complete = True
    #     query.save()
    #     MyAE.Quit()
    #     return

#    rspno = 0

    for ss in st:
        if not ss[1]:
            continue
#        rspno += 1
#        print "Response {0}".format(rspno)
        rsp = DicomQRRspStudy.objects.create(dicom_query=query)
        rsp.query_id = query_id
        # Unique key
        rsp.study_instance_uid = ss[1].StudyInstanceUID
        # Required keys - none of interest
        # Optional and special keys
        rsp.study_description = _try_query_return( ss[1], 'StudyDescription')
        # Series level query
        _query_series(my_ae, remote_ae, ss[1], rsp)
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
        rh=None, rp=None, aet="OPENREM", aec="STOREDCMTK", implicit=False, explicit=False, move=False, query_id=None,
        date_from=None, date_until=None, modalities=None, inc_sr=True, duplicates=True, *args, **kwargs):
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
    print "Request association with {0} {1} {2}".format(rh, rp, aec)
    assoc = MyAE.RequestAssociation(RemoteAE)

    if not assoc:
        query.failed = True
        query.message = "Association unsuccessful"
        query.complete = True
        query.save()
        MyAE.Quit()
        return
    print "assoc is ... {0}".format(assoc)

    # perform a DICOM ECHO
    print "DICOM Echo ... ",
    echo = assoc.VerificationSOPClass.SCU(1)
    print 'done with status "%s"' % echo

    print "DICOM FindSCU ... ",
    d = Dataset()
    d.QueryRetrieveLevel = "STUDY"
    d.PatientName = ''
    d.PatientID = ''
    d.SOPInstanceUID = ''
    d.AccessionNumber = ''
    d.Modality = ''
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
    modalities_left = True

    while modalities_left:
        for selection, details in all_mods.iteritems():
            if details['inc']:  # No need to check for modality_matching here as modalities_left would also be false
                for mod in details['mods']:
                    query.stage = 'Currently querying for {0} studies...'.format(mod)
                    query.save()
                    if modality_matching:
                        d.ModalitiesInStudy = mod
                        query_id = uuid.uuid4()
                        _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
                        study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
                        for rsp in study_rsp:
                            if mod not in rsp.get_modalities_in_study():
                                modality_matching = False
                                modalities_left = False
                                break  # This indicates that there was no modality match, so we have everything already
        if inc_sr and modality_matching:
            query.stage = 'Currently querying for SR only studies'
            query.save()
            d.ModalitiesInStudy = 'SR'
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            # Nothing to gain by checking the response


    # Now we have all our studies. Time to throw away any we don't want
    study_rsp = query.dicomqrrspstudy_set.all()

    if duplicates:
        query.stage = 'Checking to see if any response studies are already in the OpenREM database'
        query.save()
        for uid in study_rsp.values_list('study_instance_uid', flat=True):
            if GeneralStudyModuleAttr.objects.filter(study_instance_uid=uid).exists():
                study_rsp.filter(study_instance_uid__exact = uid).delete()

    mods_in_study_set = set(val for dic in study_rsp.values('modalities_in_study') for val in dic.values())
    query.stage = "Deleting studies we didn't ask for"
    query.save()
    for mod_set in mods_in_study_set:
        delete = True
        for mod_choice, details in all_mods.iteritems():
            if details['inc']:
                for mod in details['mods']:
                    if mod in mod_set:
                        delete = False
                        continue
                    if inc_sr and 'SR' in mod_set:
                        delete = False
        if delete:
            studies_to_delete = study_rsp.filter(modalities_in_study__exact = mod_set)
            studies_to_delete.delete()

    # Now we need to delete any unwanted series
    query.stage = "Deleting series we can't use"
    query.save()
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
                if 'Dose Info' in series_descriptions:  # i.e. Philips dose info series
                    for s in series:
                        if s.series_description != 'Dose Info':
                            s.delete()

    print "Release association"
    assoc.Release(0)

    # done
    MyAE.Quit()
    query.complete = True
    query.save()



if __name__ == "__main__":
    import sys
    import argparse

    # parse commandline
    parser = argparse.ArgumentParser(description='storage SCU example')
    parser.add_argument('remotehost')
    parser.add_argument('remoteport', type=int)
    parser.add_argument('-aet', help='calling AE title', default='OPENREM')
    parser.add_argument('-aec', help='called AE title', default='STOREDCMTK')
    parser.add_argument('-implicit', action='store_true', help='negociate implicit transfer syntax only', default=False)
    parser.add_argument('-explicit', action='store_true', help='negociate explicit transfer syntax only', default=False)
    parser.add_argument('-move', action='store_true', help='automatically request objects to be moved', default=False)

    args = parser.parse_args()

    sys.exit(
        qrscu(
            rh=args.remotehost, rp=args.remoteport, aet=args.aet, aec=args.aec,
            implicit=args.implicit, explicit=args.explicit, move=args.move
        )
    )


@shared_task
def movescu(query_id):
    from netdicom.applicationentity import AE
    from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import DicomQuery, DicomRemoteQR, DicomStoreSCP
    from dicom.dataset import Dataset

    query = DicomQuery.objects.get(query_id = query_id)
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



    for study in query.dicomqrrspstudy_set.all():
        d = Dataset()
        d.StudyInstanceUID = study.study_instance_uid
        for series in study.dicomqrrspseries_set.all():
            d.QueryRetrieveLevel = "SERIES"
            d.SeriesInstanceUID = series.series_instance_uid
            _move_req(my_ae, remote_ae, d)


    my_ae.Quit()


# (0008, 0018) SOP Instance UID                    UI:
# (0008, 0020) Study Date                          DA: ''
# (0008, 0050) Accession Number                    SH: ''
# (0008, 0052) Query/Retrieve Level                CS: 'SERIES'
# (0008, 0060) Modality                            CS: ''
# (0008, 0062) SOP Classes in Study                UI:
# (0008, 0070) Manufacturer                        LO: ''
# (0008, 1010) Station Name                        SH: ''
# (0008, 1030) Study Description                   LO: ''
# (0008, 103e) Series Description                  LO: ''
# (0010, 0020) Patient ID                          LO: ''
# (0020, 000d) Study Instance UID                  UI: 1.3.6.1.4.1.23849.1666612369.116.1635621988901632614
# (0020, 000e) Series Instance UID                 UI:
# (0020, 0011) Series Number                       IS: ''
# (0020, 1202) Number of Patient Related Series    IS: ''
# (0020, 1204) Number of Patient Related Instances IS: ''
# (0020, 1206) Number of Study Related Series      IS: ''
# (0020, 1208) Number of Study Related Instances   IS: ''
# (0020, 1209) Number of Series Related Instances  IS: ''



# If one or more than one modality selected:
#     Query with first modality in 'ModalitiesInStudy' field
#         1/ Respected as match, repeat with other modalities
#         2/ Not respected as match, but returned in rsp - not likely
#         3/ Ignored, returned all modalities

# Detect 1/ because none of rsp have ModalitiesInStudy that don't include modality, or because field is not empty?
# If 3/, don't repeat query with other modality selected - will get same results
# If 3/, need to filter on rsp before presenting results or requesting move

# Always go to series level query, and do move on series level.


# From series level query function

        # if series[1].Modality == 'SR':
        #     # Not sure if they will be SR are series level but CT at study level?
        #     # If they are, send C-Move request
        #     #print "C-Move request for series with modality type SR"
        #     if move:
        #         _move_req(MyAE, RemoteAE, series[1])
        #     continue
        # seNum = str(series[1].SeriesNumber)
        # if (seNum == '502') or (seNum == '998') or (seNum == '990') or (seNum == '9001'):
        #     # Find Siemens (502 CT, 990 RF) and GE (998 CT) RDSR or Enhanced SR
        #     # Added 9001 for Toshiba XA based on a sample of 1
        #     # Then Send a C-Move request for that series
        #     #print "C-Move request for series with number {0}".format(seNum)
        #     if move:
        #         _move_req(MyAE, RemoteAE, series[1])
        #     continue
        # try:
        #     if series[1].SeriesDescription == 'Dose Info':
        #         # Get Philips Dose Info series - not SR but enough information in the header
        #         #print "C-Move request for series with description {0}".format(series[1].SeriesDescription)
        #         if move:
        #             _move_req(MyAE, RemoteAE, series[1])
        #         continue
        # except AttributeError:
        #     # Try an image level find?
        #     pass
        # # Do something for Toshiba CT...

# More rambling thoughts...
#