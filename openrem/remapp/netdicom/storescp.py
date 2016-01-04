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

logger = logging.getLogger(name='remapp.netdicom.storescp')


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
    ds_new = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
    ds_new.update(DS)
    ds_new.is_little_endian = True
    ds_new.is_implicit_VR = True

    while True:
        try:
            station_name = DS.StationName
        except:
            station_name = "missing"
        try:
            ds_new.save_as(filename)
            break
        except ValueError as e:
            # Black magic pydicom method suggested by Darcy Mason: https://groups.google.com/forum/?hl=en-GB#!topic/pydicom/x_WsC2gCLck
            if "Invalid tag (0018, 7052)" in e.message or "Invalid tag (0018, 7054)" in e.message:
                logger.info("Found illegal use of multiple values of filter thickness using comma. Changing before saving.")
                thickmin = dict.__getitem__(ds_new, 0x187052)
                thickvalmin = thickmin.__getattribute__('value')
                if ',' in thickvalmin:
                    thickvalmin = thickvalmin.replace(',', '\\')
                    thicknewmin = thickmin._replace(value = thickvalmin)
                    dict.__setitem__(ds_new, 0x187052, thicknewmin)
                thickmax = dict.__getitem__(ds_new, 0x187054)
                thickvalmax = thickmax.__getattribute__('value')
                if ',' in thickvalmax:
                    thickvalmax = thickvalmax.replace(',', '\\')
                    thicknewmax = thickmax._replace(value = thickvalmax)
                    dict.__setitem__(ds_new, 0x187054, thicknewmax)
            elif "Invalid tag (01f1, 1027)" in e.message:
                logger.warning("Invalid value in tag (01f1,1027), 'exposure time per rotation'. Tag value deleted. Stn name {0}, modality {1}, SOPClass UID {2}, Study UID {3}, Instance UID {4}".format(
                    station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
                priv_exp_time = dict.__getitem__(ds_new, 0x1f11027)
                blank_val = priv_exp_time._replace(value='')
                dict.__setitem__(ds_new, 0x1f11027, blank_val)
            elif "Invalid tag (01f1, 1033)" in e.message:
                logger.warning("Invalid value in unknown private tag (01f1,1033). Tag value deleted. Stn name {0}, modality {1}, SOPClass UID {2}, Study UID {3}, Instance UID {4}".format(
                    station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
                priv_tag = dict.__getitem__(ds_new, 0x1f11033)
                blank_val = priv_tag._replace(value='')
                dict.__setitem__(ds_new, 0x1f11033, blank_val)
            else:
                logger.error(
                    "ValueError on DCM save {0}. Stn name {1}, modality {2}, SOPClass UID {3}, Study UID {4}, Instance UID {5}".format(
                        e.message, station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
                return SOPClass.Success
        except IOError as e:
            logger.error(
                    "IOError on DCM save {0} - does the user running storescp have write rights in the {1} folder?".format(
                        e.message, path
                    ))
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
    import socket
    import time
    from remapp.models import DicomStoreSCP
    from django.core.exceptions import ObjectDoesNotExist

    try:
        conf = DicomStoreSCP.objects.get(pk__exact=store_pk)
        aet = conf.aetitle
        port = conf.port
        conf.run = True
        conf.save()
    except ObjectDoesNotExist:
        sys.exit("Attempt to start DICOM Store SCP with an invalid database pk")

    # logging.basicConfig(level=logging.INFO)

    # setup AE
    try:
        MyAE = AE(
            aet, port, [],
            [StorageSOPClass, VerificationSOPClass],
            [ExplicitVRLittleEndian, ImplicitVRLittleEndian]
        )
        MyAE.MaxAssociationIdleSeconds = 120
        MyAE.MaxNumberOfAssociations = 25
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

        while 1:
            time.sleep(1)
            stay_alive = DicomStoreSCP.objects.get(pk__exact=store_pk)
            if not stay_alive.run:
                MyAE.Quit()
                logger.info("Stopped AE... AET:%s, port:%s", aet, port)
                break
    except socket.error as serr:
        if serr.errno != errno.EADDRINUSE:
            conf.status = "Starting AE AET:{0}, port:{1} failed; see logfile".format(aet, port)
            logger.error("Starting AE AET:{0}, port:{1} failed: {2}".format(aet, port, serr))
        else:
            conf.status = "Starting AE AET:{0}, port:{1} failed; address already in use!".format(aet, port)
            logger.warning("Starting AE AET:{0}, port:{1} failed: {2}".format(aet, port, serr))


def _interrupt(store_pk=None):
    from remapp.models import DicomStoreSCP
    stay_alive = DicomStoreSCP.objects.get(pk__exact=store_pk)
    stay_alive.run = False
    stay_alive.status = "Store interrupted from the shell"
    stay_alive.save()
