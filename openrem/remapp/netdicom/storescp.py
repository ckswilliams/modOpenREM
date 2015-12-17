#!/usr/bin/python
"""
Storage SCP example.

This demonstrates a simple application entity that support a number of
Storage service classes. For this example to work, you need an SCU
sending to this host on specified port.

For help on usage,
python storescp.py -h
"""
import errno
import logging
import os
import sys

import django

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

try:
    import netdicom
    from distutils.version import StrictVersion

    if StrictVersion(netdicom.__version__.__version__) <= StrictVersion('0.8.1'):
        sys.exit('Pynedicom > 0.8.1 needs to be installed, see http://docs.openrem.org/en/latest/install.html')
except ImportError:
    sys.exit('Pynedicom > 0.8.1 needs to be installed, see http://docs.openrem.org/en/latest/install.html')
from netdicom import AE
from netdicom.SOPclass import StorageSOPClass, VerificationSOPClass
from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian
from dicom.dataset import Dataset, FileDataset
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

# callbacks
def OnAssociateRequest(association):
    logger.info("Store SCP: association requested")


def OnAssociateResponse(association):
    logger.info("Store SCP: Association response received")


def OnReceiveEcho(self):
    logger.info("Store SCP: Echo received")


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


@csrf_exempt
def OnReceiveStore(SOPClass, DS):
    from remapp.extractors.dx import dx
    from remapp.extractors.mam import mam
    from remapp.extractors.rdsr import rdsr
    from remapp.extractors.ct_philips import ct_philips
    from remapp.models import DicomDeleteSettings
    from openremproject.settings import MEDIA_ROOT

    try:
        logger.info("Received C-Store. Stn name %s, Modality %s, SOPClassUID %s, Study UID %s and Instance UID %s",
                     DS.StationName, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID)
    except:
        try:
            logger.info(
                "Received C-Store - station name missing. Modality %s, SOPClassUID %s, Study UID %s and Instance UID %s",
                DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID)
        except:
            logger.info("Received C-Store - error in logging details")

    if 'TransferSyntaxUID' in DS:
        del DS.TransferSyntaxUID  # Don't know why this has become necessary

    del_settings = DicomDeleteSettings.objects.get()
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = DS.SOPClassUID
    file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID
    file_meta.ImplementationClassUID = "1.3.6.1.4.1.45593.1.0.7.0.6"
    file_meta.ImplementationVersionName = "OpenREM_0.7.0b6"
    path = os.path.join(
        MEDIA_ROOT, "dicom_in"
    )
    mkdir_p(path)
    filename = os.path.join(path, "{0}.dcm".format(DS.SOPInstanceUID))
    ds = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
    ds.update(DS)
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    try:
        ds.save_as(filename)
    except ValueError as e:
        try:
            station_name = DS.StationName
        except:
            station_name = "missing"
        logger.error(
            "ValueError on DCM save {0}. Stn name {1}, modality {2}, SOPClass UID {3}, Study UID {4}, Instance UID {5}".format(
                e.message, station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID,
                DS.SOPInstanceUID))
        return SOPClass.Success
    except:
        logger.error(
            "Unexpected error on DCM save: {0}. Stn name {1}, modality {2}, SOPClass UID {3}, Study UID {4}, Instance UID {5}".format(
                sys.exc_info()[0], DS.StationName, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
        return SOPClass.Success

    logger.info("File %s written", filename)
    if (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.67'  # X-Ray Radiation Dose SR
        or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.22'  # Enhanced SR, as used by GE
        ):
        logger.info("Processing as RDSR")
        rdsr.delay(filename)
    elif (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1'  # CR Image Storage
          or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.1'  # Digital X-Ray Image Storage for Presentation
          or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.1.1'  # Digital X-Ray Image Storage for Processing
          ):
        logger.info("Processing as DX")
        dx.delay(filename)
    elif (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.2'  # Digital Mammography X-Ray Image Storage for Presentation
          or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.2.1'  # Digital Mammography X-Ray Image Storage for Processing
          or (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7'  # Secondary Capture Image Storage, for processing
              and DS.Modality == 'MG'  # Selenia proprietary DBT projection objects
              and 'ORIGINAL' in DS.ImageType
              )
          ):
        logger.info("Processing as MG")
        mam.delay(filename)
    elif DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7':
        try:
            manufacturer = DS.Manufacturer
            series_description = DS.SeriesDescription
        except:
            if del_settings.del_no_match:
                os.remove(filename)
                logger.info("Secondary capture object with either no manufacturer or series description. Deleted.")
            return SOPClass.Success
        if manufacturer == 'Philips' and series_description == 'Dose Info':
            logger.info("Processing as Philips Dose Info series")
            ct_philips.delay(filename)
        elif del_settings.del_no_match:
            os.remove(filename)
            logger.info("Can't find anything to do with this file - it has been deleted")
    elif del_settings.del_no_match:
        os.remove(filename)
        logger.info("Can't find anything to do with this file - it has been deleted")

    # must return appropriate status
    return SOPClass.Success


def web_store(store_pk=None):
    import time
    from remapp.models import DicomStoreSCP
    from django.core.exceptions import ObjectDoesNotExist

    try:
        conf = DicomStoreSCP.objects.get(pk__exact=store_pk)
        aet = conf.aetitle
        port = conf.port
        conf.task_id = web_store.request.id
        conf.run = True
        conf.save()
    except ObjectDoesNotExist:
        sys.exit("Attempt to start DICOM Store SCP with an invalid database pk")

    # logging.basicConfig(level=logging.INFO)

    # setup AE
    MyAE = AE(
        aet, port, [],
        [StorageSOPClass, VerificationSOPClass],
        [ExplicitVRLittleEndian, ImplicitVRLittleEndian]
    )
    MyAE.OnAssociateRequest = OnAssociateRequest
    MyAE.OnAssociateResponse = OnAssociateResponse
    MyAE.OnReceiveStore = OnReceiveStore
    MyAE.OnReceiveEcho = OnReceiveEcho

    # start AE
    conf.status = "Starting AE... AET:{0}, port:{1}".format(aet, port)
    conf.save()
    logger.info("Starting AE... AET:{0}, port:{1}".format(aet, port))
    MyAE.start()
    conf.status = "Started AE... AET:{0}, port:{1}".format(aet, port)
    conf.save()
    logger.info("Started AE... AET:%s, port:%s", aet, port)
    #    print "Started AE... AET:{0}, port:{1}".format(aet, port)

    while 1:
        time.sleep(1)
        stay_alive = DicomStoreSCP.objects.get(pk__exact=store_pk)
        if not stay_alive.run:
            MyAE.Quit()
            logger.info("Stopped AE... AET:%s, port:%s", aet, port)
            #            print "AE Stopped... AET:{0}, port:{1}".format(aet, port)
            break


def _interrupt(store_pk=None):
    from remapp.models import DicomStoreSCP
    stay_alive = DicomStoreSCP.objects.get(pk__exact=store_pk)
    stay_alive.run = False
    stay_alive.status = "Store interrupted from the shell"
    stay_alive.save()
