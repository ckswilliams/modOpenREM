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

import argparse
from netdicom.applicationentity import AE
from netdicom.SOPclass import *
from dicom.dataset import Dataset, FileDataset
from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
import netdicom
import tempfile

# parse commandline
parser = argparse.ArgumentParser(description='storage SCU example')
parser.add_argument('remotehost')
parser.add_argument('remoteport', type=int)
#parser.add_argument('searchstring')
parser.add_argument('-p', help='local server port', type=int, default=8104)
parser.add_argument('-aet', help='calling AE title', default='OPENREM')
parser.add_argument('-aec', help='called AE title', default='STOREDCMTK')
parser.add_argument('-implicit', action='store_true', help='negociate implicit transfer syntax only', default=False)
parser.add_argument('-explicit', action='store_true', help='negociate explicit transfer syntax only', default=False)

args = parser.parse_args()

if args.implicit:
    ts = [ImplicitVRLittleEndian]
elif args.explicit:
    ts = [ExplicitVRLittleEndian]
else:
    ts = [
        ExplicitVRLittleEndian, 
        ImplicitVRLittleEndian, 
        ExplicitVRBigEndian
        ]

# call back
def OnAssociateResponse(association):
    print "Association response received"


def OnAssociateRequest(association):
    print "Association resquested"
    return True

def OnReceiveStore(SOPClass, DS):
    print "Received C-STORE", DS.PatientName
    try:
        # do something with dataset. For instance, store it.
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here
        file_meta.ImplementationClassUID = "1.3.5.1.4.1.45593.1.0.7.0.1"  # !!! Need valid UIDs here
        filename = '%s/%s.dcm' % (tempfile.gettempdir(), DS.SOPInstanceUID)
        ds = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
        ds.update(DS)
        ds.save_as(filename)
        print "File %s written" % filename
    except:
        pass
    # must return appropriate status
    return SOPClass.Success

def _querySeriesCT(d2):
    d2.QueryRetrieveLevel = "SERIES"
    d2.SeriesDescription = ''
    d2.SeriesNumber = ''
    d2.SeriesInstanceUID = ''
    d2.Modality = ''

    assoc2 = MyAE.RequestAssociation(RemoteAE)
    st2 = assoc2.PatientRootFindSOPClass.SCU(d2, 1)

    print 'In _querySeriesCT'
    seRspNo = 0

    for series in st2:
        if not series[1]:
            continue
        seRspNo += 1
        print "Series response number {0}".format(seRspNo)
        if series[1].Modality == 'SR':
            # Not sure if they will be SR are series level but CT at study level?
            # If they are, send C-Move request
            print "C-Move request for series with modality type SR"
            continue
        seNum = str(series[1].SeriesNumber)
        if (seNum == '502') or (seNum == '998') or (seNum == '990') or (seNum == '9001'):
            # Find Siemens (502 CT, 990 RF) and GE (998 CT) RDSR or Enhanced SR
            # Added 9001 for Toshiba XA based on a sample of 1
            # Then Send a C-Move request for that series
            print "C-Move request for series with number {0}".format(seNum)
            continue
        try:
            if series[1].SeriesDescription == 'Dose Info':
                # Get Philips Dose Info series - not SR but enough information in the header
                print "C-Move request for series with description {0}".format(series[1].SeriesDescription)
                continue
        except AttributeError:
            # Try an image level find?
            pass
        # Do something for Toshiba CT...

    assoc2.Release(0)
    print "Released series association"

# create application entity with Find and Move SOP classes as SCU and
# Storage SOP class as SCP
MyAE = AE(args.aet, args.p, [StudyRootFindSOPClass,
                             StudyRootMoveSOPClass,
                             VerificationSOPClass], [], ts)
MyAE.OnAssociateResponse = OnAssociateResponse
MyAE.OnAssociateRequest = OnAssociateRequest
MyAE.OnReceiveStore = OnReceiveStore
MyAE.start()


# remote application entity
RemoteAE = dict(Address=args.remotehost, Port=args.remoteport, AET=args.aec)

# create association with remote AE
print "Request association"
assoc = MyAE.RequestAssociation(RemoteAE)


# perform a DICOM ECHO
print "DICOM Echo ... ",
st = assoc.VerificationSOPClass.SCU(1)
print 'done with status "%s"' % st

print "DICOM FindSCU ... ",
d = Dataset()
d.QueryRetrieveLevel = "STUDY"
d.PatientID = ''
d.SOPInstanceUID = ''
d.Modality = ''
d.StudyDescription = ''
d.StudyInstanceUID = ''
d.StudyDate = ''

st = assoc.PatientRootFindSOPClass.SCU(d, 1)
# print 'done with status "%s"' % st

responses = True
rspno = 0

for ss in st:
    if not ss[1]:
        continue
    rspno += 1
    print "Response {0}".format(rspno)
    if ('CT' in ss[1].Modality) or ('PT' in ss[1].Modality):
        # new query for series level information
        print "Starting a series level query for modality type {0}".format(ss[1].Modality)
        _querySeriesCT(ss[1])
        continue
    if ('DX' in ss[1].Modality) or ('CR' in ss[1].Modality):
        # get everything
        print "Getting a study with modality type {0}".format(ss[1].Modality)
        continue
    if 'MG' in ss[1].Modality:
        # get everything
        print "Getting a study with modality type {0}".format(ss[1].Modality)
        continue
    if 'SR' in ss[1].Modality:
        # get it - you may as well
        print "Getting a study with modality type {0}".format(ss[1].Modality)
        continue
    if ('RF' in ss[1].Modality) or ('XA' in ss[1].Modality):
        # Don't know if you need both...
        # Get series level information to look for SR
        print "Starting a series level query for modality type {0}".format(ss[1].Modality)
        _querySeriesCT(ss[1])
    print "I got here"

#    print ss[1].PatientID
#    print ss[1].Modality
#    print ss[1].StudyDate




#for ss in st:
#    if not ss[1]: continue
#     try:
#         d.PatientID = ss[1].PatientID
#     except:
#         continue
#     print "Moving"
#     print d
#     assoc2 = MyAE.RequestAssociation(RemoteAE)
#     gen = assoc2.PatientRootMoveSOPClass.SCU(d, 'PYNETDICOM', 1)
#     for gg in gen:
#         print gg
#     assoc2.Release(0)

print "Release association"
assoc.Release(0)

# done
MyAE.Quit()


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