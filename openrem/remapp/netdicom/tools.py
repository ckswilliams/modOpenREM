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

from celery import shared_task
import logging


# call back
def OnAssociateResponse(association):
    logging.info("Association response received")


def OnAssociateRequest(association):
    logging.info("Association resquested")
    return True


@shared_task
def echoscu(
        scp_pk=None, store_scp=False, qr_scp=False, *args, **kwargs):
    import uuid
    import json
    from netdicom.applicationentity import AE
    from netdicom.SOPclass import StudyRootFindSOPClass, StudyRootMoveSOPClass, VerificationSOPClass
    from dicom.dataset import Dataset, FileDataset
    from dicom.UID import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
    from remapp.models import GeneralStudyModuleAttr, DicomQuery, DicomRemoteQR, DicomStoreSCP
    from remapp.tools.dcmdatetime import make_date, make_dcm_date_range

    if store_scp and scp_pk:
        scp = DicomStoreSCP.objects.get(pk=scp_pk)
    elif qr_scp and scp_pk:
        scp = DicomRemoteQR.objects.get(pk=scp_pk)
    else:
        logging.warning("echoscu called without SCP information")
        return 0

    if scp.hostname:
        rh = scp.hostname
    else:
        rh = scp.ip
    rp = scp.port
    aec = scp.aetitle

    ts = [
        ExplicitVRLittleEndian,
        ImplicitVRLittleEndian,
        ExplicitVRBigEndian
        ]

    aet = "OPENREMECHO"

    # create application entity with just Verification SOP classes as SCU
    my_ae = AE(aet.encode('ascii','ignore'), 0, [VerificationSOPClass], [], ts)
    my_ae.OnAssociateResponse = OnAssociateResponse
    my_ae.OnAssociateRequest = OnAssociateRequest
    my_ae.start()

    # remote application entity
    remote_ae = dict(Address=rh, Port=rp, AET=aec.encode('ascii','ignore'))

    # create association with remote AE
    logging.debug("Request association with {0} {1} {2}".format(rh, rp, aec))
    assoc = my_ae.RequestAssociation(remote_ae)

    if not assoc:
        logging.debug("Accociation with {0} {1} {2} was not successful".format(rh, rp, aec))
        return 0
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
    trip = 0

    for selection, details in all_mods.iteritems():
        if details['inc']:  # No need to check for modality_matching here as modalities_left would also be false
            for mod in details['mods']:
                query.stage = 'Currently querying for {0} studies...'.format(mod)
                query.save()
                trip += 1
                if modality_matching:
                    d.ModalitiesInStudy = mod
                    query_id = uuid.uuid4()
                    _query_study(assoc, my_ae, RemoteAE, d, query, query_id)
                    study_rsp = query.dicomqrrspstudy_set.filter(query_id__exact=query_id)
                    for rsp in study_rsp:
                        if mod not in rsp.get_modalities_in_study():
                            modality_matching = False
                            break  # This indicates that there was no modality match, so we have everything already

    if inc_sr and modality_matching:
        query.stage = 'Currently querying for SR only studies'
        query.save()
        d.ModalitiesInStudy = 'SR'
        query_id = uuid.uuid4()
        _query_study(assoc, my_ae, RemoteAE, d, query, query_id)
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

    logging.info("Release association")
    assoc.Release(0)

    # done
    my_ae.Quit()
    query.complete = True
    query.stage = "Query complete"
    query.save()
