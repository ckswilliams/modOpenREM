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



def _query_series(MyAE, RemoteAE, d2, move, studyrsp):
    import uuid
    from remapp.tools.dcmdatetime import make_date
    from remapp.models import DicomQRRspSeries
    d2.QueryRetrieveLevel = "SERIES"
    d2.SeriesDescription = ''
    d2.SeriesNumber = ''
    d2.SeriesInstanceUID = ''
    d2.Modality = ''
    d2.NumberOfSeriesRelatedInstances

    assoc2 = MyAE.RequestAssociation(RemoteAE)
    st2 = assoc2.StudyRootFindSOPClass.SCU(d2, 1)

    query_id = uuid.uuid4()

    print 'In _querySeriesCT'
    seRspNo = 0

    for series in st2:
        if not series[1]:
            continue
        seRspNo += 1
        seriesrsp = DicomQRRspSeries.objects.create(dicom_qr_rsp_study=studyrsp)
        seriesrsp.query_id = query_id
        seriesrsp.patient_id = series[1].PatientID
        seriesrsp.sop_instance_uid = series[1].SOPInstanceUID
        seriesrsp.modality = series[1].Modality
        seriesrsp.study_description = series[1].StudyDescription
        seriesrsp.study_instance_uid = series[1].StudyInstanceUID
        seriesrsp.study_date = make_date(series[1].StudyDate)
        try:
            seriesrsp.series_description = series[1].SeriesDescription
        except:
            pass
        seriesrsp.series_instance_uid= series[1].SeriesInstanceUID
        seriesrsp.series_number = series[1].SeriesNumber
        seriesrsp.save()
#        print "Series response number {0}".format(seRspNo)
        if series[1].Modality == 'SR':
            # Not sure if they will be SR are series level but CT at study level?
            # If they are, send C-Move request
            #print "C-Move request for series with modality type SR"
            if move:
                _move_req(MyAE, RemoteAE, series[1])
            continue
        seNum = str(series[1].SeriesNumber)
        if (seNum == '502') or (seNum == '998') or (seNum == '990') or (seNum == '9001'):
            # Find Siemens (502 CT, 990 RF) and GE (998 CT) RDSR or Enhanced SR
            # Added 9001 for Toshiba XA based on a sample of 1
            # Then Send a C-Move request for that series
            #print "C-Move request for series with number {0}".format(seNum)
            if move:
                _move_req(MyAE, RemoteAE, series[1])
            continue
        try:
            if series[1].SeriesDescription == 'Dose Info':
                # Get Philips Dose Info series - not SR but enough information in the header
                #print "C-Move request for series with description {0}".format(series[1].SeriesDescription)
                if move:
                    _move_req(MyAE, RemoteAE, series[1])
                continue
        except AttributeError:
            # Try an image level find?
            pass
        # Do something for Toshiba CT...

    assoc2.Release(0)
    print "Released series association"

from celery import shared_task

@shared_task
def qrscu(
        rh=None, rp=None, aet="OPENREM", aec="STOREDCMTK", implicit=False, explicit=False, move=False, query_id=None,
        date_from=None, date_until=None, modalities=None, *args, **kwargs
    ):
    import uuid
    from decimal import Decimal
    from netdicom.applicationentity import AE
    from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
    from dicom.dataset import Dataset, FileDataset
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import DicomQRRspStudy, DicomQuery
    from remapp.tools.dcmdatetime import make_date

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
    d.StudyDate = ''
    d.StudyTime = ''
    d.PatientAge = ''
    d.PatientBirthDate = ''

    if date_from and date_until:
        df =

    st = assoc.StudyRootFindSOPClass.SCU(d, 1)
    # print 'done with status "%s"' % st

    responses = True
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
        if ss[1].PatientBirthDate and ss[1].StudyDate:
            dob = make_date(ss[1].PatientBirthDate)
            rsp.patient_age_decimal = Decimal((rsp.study_date.date() - dob.date()).days)/Decimal('365.25')
        elif ss[1].PatientAge:
            if ss[1].PatientAge[-1:]=='Y':
                rsp.patient_age_decimal = Decimal(ss[1].PatientAge[:-1])
            elif ss[1].PatientAge[-1:]=='M':
                rsp.patient_age_decimal = Decimal(ss[1].PatientAge[:-1])/Decimal('12')
            elif ss[1].PatientAge[-1:]=='D':
                rsp.patient_age_decimal = Decimal(ss[1].PatientAge[:-1])/Decimal('365.25')
        rsp.save()

        if ('CT' in ss[1].Modality) or ('PT' in ss[1].Modality):
            # new query for series level information
            # print "Starting a series level query for modality type {0}".format(ss[1].Modality)
            _query_series(MyAE, RemoteAE, ss[1], move, rsp)
            continue
        if ('DX' in ss[1].Modality) or ('CR' in ss[1].Modality):
            # get everything
            if move:
                # print "Getting a study with modality type {0}".format(ss[1].Modality)
                _move_req(MyAE, RemoteAE, ss[1])
            continue
        if 'MG' in ss[1].Modality:
            # get everything
            if move:
                # print "Getting a study with modality type {0}".format(ss[1].Modality)
                _move_req(MyAE, RemoteAE, ss[1])
            continue
        if 'SR' in ss[1].Modality:
            # get it - you may as well
            if move:
                # print "Getting a study with modality type {0}".format(ss[1].Modality)
                _move_req(MyAE, RemoteAE, ss[1])
            continue
        if ('RF' in ss[1].Modality) or ('XA' in ss[1].Modality):
            # Don't know if you need both...
            # Get series level information to look for SR
            # print "Starting a series level query for modality type {0}".format(ss[1].Modality)
            _query_series(MyAE, RemoteAE, ss[1], move, rsp)
            continue
        else:
            rsp.delete()

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