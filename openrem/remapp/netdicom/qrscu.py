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
        file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here
        filename = '%s/%s.dcm' % (tempfile.gettempdir(), DS.SOPInstanceUID)
        ds = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
        ds.update(DS)
        ds.save_as(filename)
        print "File %s written" % filename
    except:
        pass
    # must return appropriate status
    return SOPClass.Success

def CTSeriesQuery(d2):
    d2.QueryRetrieveLevel = "SERIES"
    d2.SeriesDescription = ''
    d2.SeriesNumber = ''
    d2.SeriesInstanceUID = ''

    assoc2 = MyAE.RequestAssociation(RemoteAE)
    st2 = assoc2.PatientRootFindSOPClass.SCU(d2, 1)

    for series in st2:
        if not series[1]:
            continue
        if series[1].Modality == 'SR':
            # Not sure if they will be SR are series level but CT at study level?
            # If they are, send C-Move request
            continue
        if ('502' or '998') in str(series[1].SeriesNumber):
            # Find Siemens and GE RDSR or Enhanced SR
            # Then Send a C-Move request for that series
            continue
        if series[1].SeriesDescription == 'Dose Info':
            # Get Philips Dose Info series - not SR but enough information in the header
            continue
        # Do something for Toshiba...

# create application entity with Find and Move SOP classes as SCU and
# Storage SOP class as SCP
MyAE = AE(args.aet, args.p, [PatientRootFindSOPClass,
                             PatientRootMoveSOPClass,
                             VerificationSOPClass], [StorageSOPClass], ts)
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

for ss in st:
    if not ss[1]:
        continue
    if ('CT' in ss[1].Modality) or ('PT' in ss[1].Modality):
        # new query for series level information
        CTSeriesQuery(ss[1])
    if ('DX' in ss[1].Modality) or ('CR' in ss[1].Modality):
        # get everything
        pass
    if 'MG' in ss[1].Modality:
        # get everything
        pass
    if 'SR' in ss[1].Modality:
        # get it - you may as well
        pass
    if ('RF' in ss[1].Modality) or ('XA' in ss[1].Modality):
        # Don't know if you need both...
        # Get series level information to look for SR
        pass

    print ss[1].PatientID
    print ss[1].Modality
    print ss[1].StudyDate




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
