#!/usr/bin/python
"""
Storage SCP example.

This demonstrates a simple application entity that support a number of
Storage service classes. For this example to work, you need an SCU
sending to this host on specified port.

For help on usage,
python storescp.py -h
"""
import argparse
from netdicom import AE, StorageSOPClass, VerificationSOPClass, debug
from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from dicom.dataset import Dataset, FileDataset
import tempfile

# parse commandline
parser = argparse.ArgumentParser(description='storage SCP example')
parser.add_argument('port', type=int)
parser.add_argument('-aet', help='AE title of this server', default='PYNETDICOM')
args = parser.parse_args()

debug(True)

# callbacks
def OnAssociateRequest(association):
    print "association requested"


def OnAssociateResponse(association):
    print "Association response received"


def OnReceiveEcho(self):
    print "Echo received"


def OnReceiveStore(SOPClass, DS):
    import os, sys
    # temp path manipulation as dev location isn't on path
    sys.path.extend(['/home/mcdonaghe/research/bbOpenREM'])
    from openrem.remapp.extractors.dx import dx
    from openrem.remapp.extractors.mam import mam
    from openrem.remapp.extractors.rdsr import rdsr
    from openrem.remapp.extractors.ct_philips import ct_philips

    print "Received C-STORE"
    # do something with dataset. For instance, store it on disk.
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = DS.SOPClassUID
    file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID
    file_meta.ImplementationClassUID = "1.2.826.0.1.3680043.9.5224.1.0.6.0.1"  # Using Medical Connections allocated UID
    filename = '%s/%s.dcm' % (tempfile.gettempdir(), DS.SOPInstanceUID)
    ds = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
    ds.update(DS)
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    ds.save_as(filename)
    print "File %s written" % filename
    print "Institution name is {0}".format(DS.InstitutionName)
    print DS.SOPClassUID
    if (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.67'     # X-Ray Radiation Dose SR
        or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.22'  # Enhanced SR, as used by GE
    ):
        print "RDSR"
        rdsr(filename)
    elif ( DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1'      # CR Image Storage
        or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.1'    # Digital X-Ray Image Storage for Presentation
        or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.1.1'  # Digital X-Ray Image Storage for Processing
    ):
        print "DX"
        dx(filename)
    elif ( DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.2'    # Digital Mammography X-Ray Image Storage for Presentation
        or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.2.1'  # Digital Mammography X-Ray Image Storage for Processing
        or (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7'     # Secondary Capture Image Storage, for processing
            and DS.Modality == 'MG'                           # Selenia proprietary DBT projection objects
            and 'ORIGINAL' in DS.ImageType
        )
    ):
        print "Mammo"
        mam(filename)
    elif (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7'
          and DS.Manufacturer == 'Philips'
          and DS.SeriesDescription == 'Dose Info'
    ):
        print "Philips CT Dose Info image"
        ct_philips(filename)

    # must return appropriate status
    return SOPClass.Success


# setup AE
MyAE = AE(args.aet, args.port, [], [StorageSOPClass, VerificationSOPClass], [ExplicitVRLittleEndian])
MyAE.OnAssociateRequest = OnAssociateRequest
MyAE.OnAssociateResponse = OnAssociateResponse
MyAE.OnReceiveStore = OnReceiveStore
MyAE.OnReceiveEcho = OnReceiveEcho

# start AE
print "starting AE ... ",
MyAE.start()
print "done"
MyAE.QuitOnKeyboardInterrupt()