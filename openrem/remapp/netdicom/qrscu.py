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

def _move_req(MyAE, RemoteAE, d):
    assocMove = MyAE.RequestAssociation(RemoteAE)
    print "Move association requested"
    print "d is {0}".format(d)
    gen = assocMove.StudyRootMoveSOPClass.SCU(d, 'STOREOPENREM', 1)
    for gg in gen:
        print "gg is {0}".format(gg)
    assocMove.Release(0)
    print "Move association released"

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

    rspno = 0

    for ss in st:
        if not ss[1]:
            continue
        rspno += 1
        print "Response {0}".format(rspno)
        rsp = DicomQRRspStudy.objects.create(dicom_query=query)
        rsp.query_id = query_id
        rsp.patient_id = ss[1].PatientID
        rsp.sop_instance_uid = ss[1].SOPInstanceUID
        rsp.modality = ss[1].Modality
        rsp.study_description = ss[1].StudyDescription
        rsp.study_instance_uid = ss[1].StudyInstanceUID
        rsp.study_date = make_date(ss[1].StudyDate)
        rsp.save()
        print 'Study IUID: {0}, SOP Instance UID: {1}, Modality: {2}, Study Desc: {3}, Date: {4}'.format(
            rsp.study_instance_uid, rsp.sop_instance_uid, rsp.modality, rsp.study_description, rsp.study_date)
        _query_series(my_ae, remote_ae, ss[1], rsp)

        try:
            rsp.set_modalities_in_study(ss[1].ModalitiesInStudy.split(','))
#            rsp.modalities_in_study = ss[1].ModalitiesInStudy.split(',')
            print "Modalities_in_study was populated. It's value is {0} which becomes {1}".format(
                ss[1].ModalitiesInStudy, rsp.modalities_in_study)
        except:
            series_rsp = rsp.dicomqrrspseries_set.all()
            rsp.set_modalities_in_study(list(set(val for dic in series_rsp.values('modality') for val in dic.values())))
            print "Modalities in study wasn't populated. We've created {0}".format(rsp.modalities_in_study)
        rsp.save()

    assoc_study.Release(0)


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
        # try:
        #     series[1].SeriesInstanceUID
        # except:
        #     break
        seRspNo += 1
        print "Series Response {0}: {1}".format(seRspNo, series[1])
        seriesrsp = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=studyrsp)
        # try:  # Some series level responses were nonsense
        #     seriesrsp.series_instance_uid= series[1].SeriesInstanceUID
        # except:
        #     seriesrsp.delete()
        #     continue
        seriesrsp.series_instance_uid= series[1].SeriesInstanceUID
        seriesrsp.query_id = query_id
        seriesrsp.patient_id = series[1].PatientID
        seriesrsp.sop_instance_uid = series[1].SOPInstanceUID
        seriesrsp.modality = series[1].Modality
        seriesrsp.study_description = series[1].StudyDescription
        seriesrsp.study_instance_uid = series[1].StudyInstanceUID
        seriesrsp.study_date = make_date(series[1].StudyDate)
        seriesrsp.series_number = series[1].SeriesNumber
        try:  # CR images for example don't always have series information
            seriesrsp.series_description = series[1].SeriesDescription
        except:
            pass
        seriesrsp.save()

    assoc_series.Release(0)


from celery import shared_task

@shared_task
def qrscu(
        rh=None, rp=None, aet="OPENREM", aec="STOREDCMTK", implicit=False, explicit=False, move=False, query_id=None,
        date_from=None, date_until=None, modalities=None, *args, **kwargs):
    import uuid
    import json
    from netdicom.applicationentity import AE
    from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
    from dicom.dataset import Dataset, FileDataset
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import DicomQRRspStudy, DicomQuery
    from remapp.tools.dcmdatetime import make_date, make_dcm_date_range

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

    all_mods = {'CT': {'inc': False, 'mods': ['CT','SR']},
           'MG': {'inc': False, 'mods': ['MG','SR']},
           'FL': {'inc': False, 'mods': ['RF','XA','SR']},
           'DX': {'inc': False, 'mods': ['DX','CR','SR']}
           }
    for m in all_mods:
        if m in modalities:
            all_mods[m]['inc'] = True

    # create application entity with Find and Move SOP classes as SCU
    MyAE = AE(aet, 0, [StudyRootFindSOPClass,
                                 StudyRootMoveSOPClass,
                                 VerificationSOPClass], [], ts)
    MyAE.OnAssociateResponse = OnAssociateResponse
    MyAE.OnAssociateRequest = OnAssociateRequest
    # MyAE.OnReceiveStore = OnReceiveStore
    MyAE.start()

    # remote application entity
    RemoteAE = dict(Address=rh, Port=rp, AET=aec)

    if not query_id:
        query_id = uuid.uuid4()

    query = DicomQuery.objects.create()
    query.query_id = query_id
    query.complete = False
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

    d.StudyDate = make_dcm_date_range(date_from, date_until)
    if not d.StudyDate:
        d.StudyDate = ''

    modality_matching = True
    modalities_left = True

    while modalities_left:
        if all_mods['MG']['inc']:
            d.ModalitiesInStudy = 'MG'
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            print "I've just completed a query for MG"
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'MG' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break  # This indicates that there was no modality match, so we have everything already
        if all_mods['DX']['inc'] and modality_matching:
            d.ModalitiesInStudy = 'DX'  # DX could be DX or CR
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'DX' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break
        if all_mods['DX']['inc'] and modality_matching:
            d.ModalitiesInStudy = 'CR'  # DX could be DX or CR
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'CR' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break
        if all_mods['FL']['inc'] and modality_matching:
            d.ModalitiesInStudy = 'RF'  # Fluoroscopy could be RF or XA
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'RF' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break
        if all_mods['FL']['inc'] and modality_matching:
            d.ModalitiesInStudy = 'XA'  # Fluoroscopy could be RF or XA
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'XA' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break
        if all_mods['CT']['inc'] and modality_matching:
            d.ModalitiesInStudy = 'CT'
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'CT' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break
        if all_mods['CT']['inc'] and modality_matching:
            # Not sure we need this one. If modsinstudy is respected, we'll catch them. If not, we'll have it anyway.
            d.ModalitiesInStudy = 'PT'
            query_id = uuid.uuid4()
            _query_study(assoc, MyAE, RemoteAE, d, query, query_id)
            study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
            for rsp in study_rsp:
                if 'PT' not in rsp.get_modalities_in_study():
                    modality_matching = False
                    modalities_left = False
                    break

    # NOW we have all our studies. Time to throw away any we don't want
    study_rsp =query.dicomqrrspstudy_set.all()
    mods_in_study_set = set(val for dic in study_rsp.values('modalities_in_study') for val in dic.values())
    for mod_set in mods_in_study_set:
        delete = True

        for mod_choice, details in all_mods.iteritems():
            if details['inc']:
                for mod in details['mods']:
                    if mod in mod_set:
                        delete = False
        if delete:
            studies_to_delete = study_rsp.filter(modalities_in_study__exact = mod_set)
            studies_to_delete.delete()

    # Now we need to delete any unwanted series








    # d.ModalitiesInStudy = modalities[0]
    # _query_study(assoc, d, query, query_id)
    # study_rsp = query.dicomqrrspstudy_set.all()
    # study_rsp_mods = study_rsp.values('modality').annotate(count=Count('pk'))
    # study_rsp_mods_in_study = study_rsp.values('modalities_in_study').annotate(count=Count('pk'))
    # if len(modalities) is 1:
    #     if study_rsp[0].modalities_in_study:  # Then reasonable bet it can match on this
    #         for rsp in study_rsp:
    #             if modalities[0] not in rsp.modalities_in_study:
    #                 rsp.delete()  # We shouldn't get here
    #     else:
    #         for rsp in study_rsp:
    #             if modalities[0] not in rsp.modality:
    #                 ser_rsp = rsp.dicomqrrspseries_set.all()
    #                 if ser_rsp:
    #                     for srsp in ser_rsp:
    #                         if modalities[0] not in srsp.modality and
    #
    #     # delete any that don't match
    #
    # else:
    #     # see if any responses have only modalities we haven't asked for
    #         # delete others, finish (ready for retrieve)
    #     # if not, modalitiesinstudy is being respected, and we need to ask for the others
    #         # set next modality, _query_study
    #     pass

    # Now have full study level response - look at it and decide what to do next



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