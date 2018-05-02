# This Python file uses the following encoding: utf-8

# OpenREM root UID: 1.2.826.0.1.3680043.9.5224.
# Provided by Medical Connections https://www.medicalconnections.co.uk/FreeUID

# OpenREM root UID: 1.3.6.1.4.1.45593.
# Provided by IANA as a private enterprise number

# ImplementationUID 1.2.826.0.1.3680043.9.5224.1.0.6.0.1
# = 1.2.826.0.1.3680043.9.5224.1.versionnumber.betanumber
# IANA version
# = 1.3.6.1.4.1.45593.1.0.7.0.1

# UID root for objects
# = 1.2.826.0.1.3680043.9.5224.2.machine-root.machineID.numberperimage
# where numberperimage  might consist of yyyymmddhhmmssss.number

# pydicom has a UID generator of the form:
# root + mac + pid + second + microsecond, eg
# 1.2.826.0.1.3680043.9.5224.2.+8796759879378+15483+44+908342
# 1.2.826.0.1.3680043.9.5224.2.87967598793781548344908342
# which is 54 characters but process ID could be longer.

# 1.3.6.1.4.1.45593.1.2.879675987937815483yyyymmddssssssss
# would be 55 characters - process ID could be longer.
# Includes an extra 1. after the root UID to enable future use for
# anthing else.

import logging
from netdicom.applicationentity import AE
from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian

logger = logging.getLogger(__name__)
qr_logger = logging.getLogger('remapp.netdicom.qrscu')


# call back
def OnAssociateResponse(association):
    logger.info(u"Association response received")


def OnAssociateRequest(association):
    logger.info(u"Association resquested")
    return True


def echoscu(scp_pk=None, store_scp=False, qr_scp=False, *args, **kwargs):
    """
    Function to check if built-in Store SCP or remote Query-Retrieve SCP returns a DICOM echo
    :param scp_pk: Primary key if either Store or QR SCP in database
    :param store_scp: True if checking Store SCP
    :param qr_scp: True if checking QR SCP
    :param args:
    :param kwargs:
    :return: 'AssocFail', Success or ?
    """
    from remapp.models import DicomRemoteQR, DicomStoreSCP

    if store_scp and scp_pk:
        scp = DicomStoreSCP.objects.get(pk=scp_pk)
        rh = "localhost"
        aet = "OPENREMECHO"
    elif qr_scp and scp_pk:
        scp = DicomRemoteQR.objects.get(pk=scp_pk)
        if scp.hostname:
            rh = scp.hostname
        else:
            rh = scp.ip
        aet = scp.callingaet
        if not aet:
            aet = "OPENREMECHO"
    else:
        logger.warning(u"echoscu called without SCP information")
        return 0

    rp = scp.port
    aec = scp.aetitle

    ts = [
        ExplicitVRLittleEndian,
        ImplicitVRLittleEndian,
        ExplicitVRBigEndian
        ]



    # create application entity with just Verification SOP classes as SCU
    my_ae = AE(aet.encode('ascii', 'ignore'), 0, [VerificationSOPClass], [], ts)
    my_ae.OnAssociateResponse = OnAssociateResponse
    my_ae.OnAssociateRequest = OnAssociateRequest
    my_ae.start()

    # remote application entity
    remote_ae = dict(Address=rh, Port=rp, AET=aec.encode('ascii', 'ignore'))

    # create association with remote AE
    logger.debug(u"Request association with {0} {1} {2}".format(rh, rp, aec))
    assoc = my_ae.RequestAssociation(remote_ae)

    if not assoc:
        logger.info(u"Association with {0} {1} {2} was not successful".format(rh, rp, aec))
        return "AssocFail"
    logger.debug(u"assoc is ... %s", assoc)

    # perform a DICOM ECHO
    logger.debug(u"DICOM Echo... {0} {1} {2}".format(rh, rp, aec))
    echo = assoc.VerificationSOPClass.SCU(1)
    logger.debug(u'done with status %s', echo)

    logger.debug(u"Release association from {0} {1} {2}".format(rh, rp, aec))
    assoc.Release(0)

    # done
    my_ae.Quit()
    if echo.Type is "Success":
        logger.info(u"Returning Success response from echo to {0} {1} {2}".format(rh, rp, aec))
        return "Success"
    else:
        logger.info(u"Returning EchoFail response from echo to {0} {1} {2}. Type is {3}.".format(rh, rp, aec, echo.Type))
        return "EchoFail"


def create_ae(aet, port=None, sop_scu=None, sop_scp=None, transfer_syntax=None):
    """
    Function to create an application entity
    :param aet: string, AE Title
    :param sop_classes: list of supported SOP classes from netdicom.SOPclass to override default set
    :param transfer_syntax: list of supported transfer syntax from dicom.UID to override default set
    :return: application entity object ready to be started
    """
    qr_logger.debug(u"Create AE called with AET {0}, port {1}, SOP SCUs {2}, SOP SCPs {3} and transfer syntax {4} "
                 u"(None if default)".format(aet, port, sop_scu, sop_scp, transfer_syntax))
    if port is None:
        port = 0
    if sop_scu is None:
        sop_scu = [StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass]
    if sop_scp is None:
        sop_scp = []
    if transfer_syntax is None:
        transfer_syntax = [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]

    qr_logger.debug(u"Creating AE with AET {0}, port {1}, SOP SCUs {2}, SOP SCPs {3} and transfer syntax {4}".format(
        aet, port, sop_scu, sop_scp, transfer_syntax))
    my_ae = AE(aet, port, sop_scu, sop_scp, transfer_syntax)
    my_ae.OnAssociateResponse = OnAssociateResponse
    my_ae.OnAssociateRequest = OnAssociateRequest

    return my_ae
