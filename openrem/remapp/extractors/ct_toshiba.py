# This Python file uses the following encoding: utf-8
#    OpenREM - Radiation Exposure Monitoring tools for the physicist
#    Copyright (C) 2017  The Royal Marsden NHS Foundation Trust
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    Additional permission under section 7 of GPLv3:
#    You shall not make any use of the name of The Royal Marsden NHS
#    Foundation trust in connection with this Program in any press or
#    other public announcement without the prior written consent of
#    The Royal Marsden NHS Foundation Trust.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
..  module:: rdsr_toshiba_fct_from_dose_images.
    :synopsis: Module to create a radiation dose structured report from legacy Toshiba CT studies

..  moduleauthor:: David Platten
"""

import sys
import os
from openrem.remapp.extractors import rdsr
from openremproject.settings import JAVA_EXE, JAVA_OPTIONS, PIXELMED_JAR, PIXELMED_JAR_OPTIONS
import shutil
import django
import logging
import traceback
from celery import shared_task

# setup django/OpenREM
base_path = os.path.dirname(__file__)
project_path = os.path.abspath(os.path.join(base_path, "..", ".."))
if project_path not in sys.path:
    sys.path.insert(1, project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

# logger is explicitly named so that it is still handled when using __main__
logger = logging.getLogger('remapp.extractors.ct_toshiba')


def _find_dose_summary_objects(folder_path):
    """ This function looks for objects with a SOPClassUID of "Secondary
    Capture Image Storage" and an ImageType with a length of 2.

    Dose summary objects have a 2-element ImageType:
        ImageType is ['DERIVED', 'SECONDARY']
    Other secondary capture storage objects have a 3-element ImageType:
        ImageType is ['DERIVED', 'SECONDARY', 'MULTI_FORMAT_RASTER']
        ImageType is ['DERIVED', 'SECONDARY', 'DISPLAY']
        ImageType is ['DERIVED', 'SECONDARY', 'MPR']

    The above are from a virtual colonoscopy study.

    Args:
        folder_path: a string containing the path to the folder containing the
        DICOM objects

    Returns:
        A list of structures, each containing the elements "fileName",
        "studyTime" and "instanceNumber".
    """
    import dicom
    from dicom.filereader import InvalidDicomError

    sop_class_uid = "Secondary Capture Image Storage"
    dose_summary_object_list = []

    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            try:
                dcm = dicom.read_file(os.path.join(folder_path, file_name))
                if str(dcm.SOPClassUID) == str(sop_class_uid) and len(dcm.ImageType) == 2:
                    dose_summary_object_list.append({"fileName": file_name,
                                                     "studyTime": dcm.StudyTime,
                                                     "instanceNumber": dcm.InstanceNumber})

            except InvalidDicomError as e:
                logger.debug("Invalid DICOM error: {0} when trying to read {1}".format(e.message, os.path.join(folder_path, file_name)))
            except Exception:
                logger.debug(traceback.format_exc())

    return dose_summary_object_list


def _copy_files_from_a_to_b(src_folder, dest_folder):
    """Copy files in src_folder to dest_folder
    """
    src_files = os.listdir(src_folder)
    for file_name in src_files:
        full_file_name = os.path.join(src_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest_folder)


def _split_by_studyinstanceuid(dicom_path):
    """Parse a folder of files, creating a sub-folder for each StudyInstanceUID found in any DICOM files. Each DICOM
    file is copied into the folder that matches its StudyInstanceUID. The files are renamed to have integer names
    starting with 0 and incrementing by 1 for each additional file copied.

    Args:
        dicom_path (str): The full path to a folder containing DICOM objects.

    Returns:
        list: A list of paths that contain the DICOM objects corresponding to each StudyInstanceUID present in the
        original dicom_path.

    """
    import dicom

    from dicom.filereader import InvalidDicomError

    folder_list = []
    file_counter = 0

    for filename in os.listdir(dicom_path):
        if os.path.isfile(os.path.join(dicom_path, filename)):
            try:
                dcm = dicom.read_file(os.path.join(dicom_path, filename))

                subfolder_path = os.path.join(dicom_path, dcm.StudyInstanceUID)
                if not os.path.isdir(subfolder_path):
                    os.mkdir(subfolder_path)
                    folder_list.append(subfolder_path)

                shutil.copy2(os.path.join(dicom_path, filename), os.path.join(subfolder_path, str(file_counter)))
                file_counter += 1
            except InvalidDicomError as e:
                logger.debug('Invalid DICOM error: {0} when trying to read {1}'.format(e.message, os.path.join(dicom_path, filename)))
            except Exception:
                logger.debug(traceback.format_exc())

    return folder_list


def _find_extra_info(dicom_path):
    """Parses a folder of files,  obtaining DICOM tag information on each acquisition present.

    Args:
        dicom_path (str): A string containing the full path to the folder.

    Returns:
        list: A two element list. The first element contains study-level information. The second element is a list of
        dictionaries, one per acquisition found in the files. Each dictionary contains the following information about
        each acquisition, if present:

        AcquisitionNumber
        ProtocolName
        ExposureTime
        SpiralPitchFactor
        CTDIvol
        ExposureModulationType
        NominalTotalCollimationWidth
        NominalSingleCollimationWidth
        DeviceSerialNumber
        StudyDescription
        RequestedProcedureDescription
        DLP
        SoftwareVersions
        DeviceSerialNumber

    """
    import dicom

    from dicom.filereader import InvalidDicomError

    from struct import unpack

    logger.debug('Starting _find_extra_info routine for images in {0}'.format(dicom_path))

    acquisition_info = []
    acquisitions_collected = []
    study_info = {}

    for filename in os.listdir(dicom_path):
        if os.path.isfile(os.path.join(dicom_path, filename)):
            try:
                dcm = dicom.read_file(os.path.join(dicom_path, filename))

                try:
                    # Only look at the tags if the combination of AcquisitionNumber and AcquisitionTime is new
                    acquisition_code = str(dcm.AcquisitionNumber) + '_' + dcm.AcquisitionTime
                    if acquisition_code not in acquisitions_collected:
                        logger.debug("acquisition_code is {0}".format(acquisition_code))
                        acquisitions_collected.append(acquisition_code)

                        info_dictionary = {}

                        try:
                            info_dictionary['AcquisitionNumber'] = dcm.AcquisitionNumber
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            info_dictionary['AcquisitionTime'] = dcm.AcquisitionTime
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            info_dictionary['ProtocolName'] = dcm.ProtocolName
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            info_dictionary['ExposureTime'] = dcm.ExposureTime
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            info_dictionary['KVP'] = dcm.KVP
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            # For some Toshiba CT scanners there is information on the detector configuration
                            if dcm.Manufacturer.lower() == 'toshiba':
                                info_dictionary['NominalSingleCollimationWidth'] = float(dcm[0x7005, 0x1008].value)
                                info_dictionary['NominalTotalCollimationWidth'] = dcm[0x7005, 0x1009].value.count('1') * float(dcm[0x7005, 0x1008].value)
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            info_dictionary['SpiralPitchFactor'] = dcm.SpiralPitchFactor
                        except AttributeError:
                            try:
                                # For some Toshiba CT scanners, stored as a decimal string (DS)
                                info_dictionary['SpiralPitchFactor'] = dcm[0x7005, 0x1023].value
                            except KeyError:
                                pass
                            except Exception:
                                logger.debug(traceback.format_exc())
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            # For some Toshiba CT scanners, stored as a floating point double (FD) by the
                            # scanner, but encoded by PACS as hex
                            if dcm[0x7005, 0x1063].VR == 'FD':
                                info_dictionary['CTDIvol'] = dcm[0x7005, 0x1063].value
                                logger.debug('CTDIvol found in VR==FD format in dcm[0x7005,0x1063] ({0}).'.format(dcm[0x7005, 0x1063].value))
                            else:
                                info_dictionary['CTDIvol'] = unpack('<d', ''.join(dcm[0x7005, 0x1063]))[0]
                                logger.debug('CTDIvol unpacked from dcm[0x7005,0x1063] ({0}).'.format(unpack('<d', ''.join(dcm[0x7005, 0x1063]))[0]))
                        except KeyError:
                            logger.debug('There was a key error when finding CTDIvol. Trying elsewhere.')
                            try:
                                info_dictionary['CTDIvol'] = dcm.CTDIvol
                                logger.debug('CTDIvol found in dcm.CTDIvol ({0}).'.format(dcm.CTDIvol))
                            except AttributeError:
                                pass
                            except Exception:
                                logger.debug(traceback.format_exc())
                        except TypeError:
                            logger.debug('There was a type error when finding CTDIvol. Trying elsewhere.')
                            try:
                                info_dictionary['CTDIvol'] = dcm.CTDIvol
                                logger.debug('CTDIvol found in dcm.CTDIvol ({0}).'.format(dcm.CTDIvol))
                            except AttributeError:
                                pass
                            except Exception:
                                logger.debug(traceback.format_exc())
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            info_dictionary['ExposureModulationType'] = dcm.ExposureModulationType
                        except AttributeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        try:
                            # For some Toshiba CT scanners, stored as a floating point double (FD) by the
                            # scanner, but encoded by PACS as hex
                            if dcm[0x7005, 0x1040].VR == 'FD':
                                info_dictionary['DLP'] = dcm[0x7005, 0x1040].value
                                logger.debug('DLP found in VR==FD format in dcm[0x7005,0x1040] ({0}).'.format(dcm[0x7005, 0x1040].value))
                            else:
                                info_dictionary['DLP'] = unpack('<d', ''.join(dcm[0x7005, 0x1040]))[0]
                                logger.debug('DLP unpacked from dcm[0x7005,0x1040] ({0}).'.format(unpack('<d', ''.join(dcm[0x7005, 0x1040]))[0]))
                        except KeyError:
                            logger.debug('There was a key error when finding DLP.')
                        except TypeError:
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                        acquisition_info.append(info_dictionary)

                    # Update the study-level information, whether this acquisition number has been seen yet or not
                    try:
                        if dcm.StudyDescription != '':
                            try:
                                if study_info['StudyDescription'] == '':
                                    # Only update study_info['StudyDescription'] if it's empty
                                    study_info['StudyDescription'] = dcm.StudyDescription
                            except KeyError:
                                # study_info['StudyDescription'] isn't present, so add it
                                study_info['StudyDescription'] = dcm.StudyDescription
                            except Exception:
                                logger.debug(traceback.format_exc())
                    except AttributeError:
                        # dcm.StudyDescription isn't present. Try looking at the CodeMeaning of
                        # ProcedureCodeSequence instead
                        try:
                            if dcm.ProcedureCodeSequence[0].CodeMeaning != '':
                                try:
                                    if study_info['StudyDescription'] == '':
                                        # Only update study_info['StudyDescription'] if it's empty
                                        study_info['StudyDescription'] = dcm.ProcedureCodeSequence[0].CodeMeaning
                                except KeyError:
                                    # study_info['StudyDescription'] isn't present, so add it
                                    study_info['StudyDescription'] = dcm.ProcedureCodeSequence[0].CodeMeaning
                                except Exception:
                                    logger.debug(traceback.format_exc())
                        except AttributeError:
                            # dcm.ProcedureCodeSequence[0].CodeMeaning isn't present either
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())
                    except Exception:
                        logger.debug(traceback.format_exc())

                    try:
                        if dcm.RequestedProcedureDescription != '':
                            try:
                                if study_info['RequestedProcedureDescription'] == '':
                                    # Only update study_info['RequestedProcedureDescription'] if it's empty
                                    study_info['RequestedProcedureDescription'] = dcm.RequestedProcedureDescription
                            except KeyError:
                                # study_info['RequestedProcedureDescription'] doesn't exist yet, so create it
                                study_info['RequestedProcedureDescription'] = dcm.RequestedProcedureDescription
                            except Exception:
                                logger.debug(traceback.format_exc())
                    except AttributeError:
                        # dcm.RequestedProcedureDescription isn't present. Try looking at the
                        # RequestedProcedureDescription of RequestAttributesSequence instead
                        try:
                            if dcm.ProcedureCodeSequence[0].CodeMeaning != '':
                                try:
                                    if study_info['RequestedProcedureDescription'] == '':
                                        # Only update study_info['RequestedProcedureDescription'] if it's empty
                                        study_info['RequestedProcedureDescription'] = dcm.ProcedureCodeSequence[0].CodeMeaning
                                except KeyError:
                                    # study_info['RequestedProcedureDescription'] isn't present, so add it
                                    study_info['RequestedProcedureDescription'] = dcm.ProcedureCodeSequence[0].CodeMeaning
                                except Exception:
                                    logger.debug(traceback.format_exc())
                        except AttributeError:
                            # dcm.ProcedureCodeSequence[0].CodeMeaning isn't present either
                            pass
                        except Exception:
                            logger.debug(traceback.format_exc())

                    try:
                        if dcm.SoftwareVersions != '':
                            try:
                                if study_info['SoftwareVersions'] == '':
                                    # Only update study_info['SoftwareVersions'] if it's empty
                                    study_info['SoftwareVersions'] = dcm.SoftwareVersions
                            except KeyError:
                                # study_info['SoftwareVersions'] doesn't exist yet, so create it
                                study_info['SoftwareVersions'] = dcm.SoftwareVersions
                            except Exception:
                                logger.debug(traceback.format_exc())
                    except AttributeError:
                        pass

                    try:
                        if dcm.DeviceSerialNumber != '':
                            try:
                                if study_info['DeviceSerialNumber'] == '':
                                    # Only update study_info['DeviceSerialNumber'] if it's empty
                                    study_info['SoftwareVersions'] = dcm.DeviceSerialNumber
                            except KeyError:
                                # study_info['DeviceSerialNumber'] doesn't exist yet, so create it
                                study_info['DeviceSerialNumber'] = dcm.DeviceSerialNumber
                            except Exception:
                                logger.debug(traceback.format_exc())
                    except AttributeError:
                        pass

                except AttributeError:
                    pass
                except Exception:
                    logger.debug(traceback.format_exc())

            except InvalidDicomError:
                pass
            except Exception:
                logger.debug(traceback.format_exc())

    logger.debug('Reached the end of _find_extra_info for images in {0}'.format(dicom_path))
    logger.debug('study_info is: {0}'.format(study_info))
    logger.debug('acquisition_info is: {0}'.format(acquisition_info))
    return [study_info, acquisition_info]


def _make_explicit_vr_little_endian(folder, dcmconv_exe):
    """Parse folder of files, making each DICOM file explicit VR little endian using the DICOM toolkit dcmconv.exe
    command. See http://support.dcmtk.org/docs/dcmconv.html for documentation.

    Args:
        folder (string): Full path containing DICOM objects.
        dcmconv_exe (str): A string containing the dcmconv command

    """
    # Security implications of using subprocess have been considered - it is necessary for this function to work.
    import subprocess  # nosec

    for filename in os.listdir(folder):
        command = dcmconv_exe + ' +te ' + os.path.join(folder, filename) + ' ' + os.path.join(folder, filename)
        subprocess.call(command.split())  # nosec


def _make_dicomdir(folder, dcmmkdir_exe):
    """Parse folder of files, making a DICOMDIR for it using the DICOM toolkit dcmmkdir.exe command. See
    http://support.dcmtk.org/docs/dcmmkdir.html for documentation.

    Args:
        folder (string): Full path containing DICOM objects.
        dcmmkdir_exe (str): A string containing the dcmmkdir command

    """
    # Security implications of using subprocess have been considered - it is necessary for this function to work.
    import subprocess  # nosec

    command = dcmmkdir_exe + ' --recurse --output-file ' + os.path.join(folder, 'DICOMDIR') + ' --input-directory ' + folder
    subprocess.call(command.split())  # nosec


def _make_dicom_rdsr(folder, pixelmed_jar_command, sr_filename):
    """Parse folder of files, making a DICOM RDSR using pixelmed.jar.

    Args:
        folder (string): Full path containing DICOM objects.
        pixelmed_jar_command (str): A string containing the pixelmed_jar command and options.
        sr_filename (str): A string containing the filename to use when creating the rdsr.

    """
    # Security implications of using subprocess have been considered - it is necessary for this function to work.
    import subprocess  # nosec

    command = pixelmed_jar_command + ' ' + folder + ' ' + os.path.join(folder, sr_filename)
    subprocess.call(command.split())  # nosec


def _update_dicom_rdsr(rdsr_file, additional_study_info, additional_acquisition_info, new_rdsr_file):
    """Try to update information in an RDSR file using pydicom. Match the pair of CTDIvol and DLP values found in the
    RDSR CT Acquisition with a pair of CTDIvol and DLP values in additional_info. If a match is found, use the other
    information in the additional_info element to update the corresponding CT Acquisition in the RDSR.

    Args:
        rdsr_file (str): A fully qualified RDSR filename.
        additional_study_info (list): A list of dictionaries containing information on the CT study.
        additional_acquisition_info (list): A list of dictionaries containing information on each acquisition in the CT
        study.

    Returns:
        integer (int): 1 on success; 0 if the rdsr_file could not be read.

    """
    import dicom
    from dicom.dataset import Dataset
    from dicom.sequence import Sequence

    logger.debug('Trying to open initial RDSR file')
    try:
        dcm = dicom.read_file(rdsr_file)
        logger.debug('RDSR file opened: {0}'.format(rdsr_file))
    except IOError as e:
        logger.debug('I/O error({0}): {1} when trying to read {2}'.format(e.errno, e.strerror, rdsr_file))
        return 0
    except Exception:
        logger.debug(traceback.format_exc())

    # Update the study-level information if it does not exist, or is an empty string. Over-write DeviceSerialNumber
    # even if it is already present (Dose Utility generates a unique DeviceSerialNumber, but I'd prefer to use the
    # real one)
    logger.debug('Updating study-level data')
    for key, val in additional_study_info.items():
        try:
            rdsr_val = getattr(dcm, key)
            logger.debug('{0}: {1}'.format(key, val))
            if rdsr_val == '':
                setattr(dcm, key, val)
            if key == 'DeviceSerialNumber':
                setattr(dcm, key, val)
        except AttributeError:
            setattr(dcm, key, val)
        except Exception:
            logger.debug(traceback.format_exc())
    logger.debug('Study level data updated')

    # Now go through each CT Aquisition container in the rdsr file and see if any of the information should be updated.
    logger.debug('Updating acquisition data')
    for container in dcm.ContentSequence:
        if container.ValueType == 'CONTAINER':
            if container.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition':
                for container2 in container.ContentSequence:
                    # The Acquisition protocol would go in at this level I think
                    if container2.ValueType == 'CONTAINER':
                        if container2.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose':
                            logger.debug('Found CT Dose container')
                            current_dlp = '0'
                            current_ctdi_vol = '0'
                            for container3 in container2.ContentSequence:
                                if container3.ConceptNameCodeSequence[0].CodeMeaning == 'DLP':
                                    current_dlp = container3.MeasuredValueSequence[0].NumericValue
                                    logger.debug('Found DLP value: {0}'.format(current_dlp))
                                if container3.ConceptNameCodeSequence[0].CodeMeaning == 'Mean CTDIvol':
                                    current_ctdi_vol = container3.MeasuredValueSequence[0].NumericValue
                                    logger.debug('Found CTDIvol value: {0}'.format(current_ctdi_vol))

                            # Check to see if the current DLP and CTDIvol pair matches any of the acquisitions in
                            # additional_info
                            for acquisition in additional_acquisition_info:
                                try:
                                    logger.debug('Trying to match DLP and CTDIvol. Current values: {0}, {1}'.format(float(acquisition['DLP']), float(acquisition['CTDIvol'])))
                                    if float(acquisition['CTDIvol']) == float(current_ctdi_vol) and float(acquisition['DLP']) == float(current_dlp):
                                        logger.debug('DLP and CTDIvol match')
                                        # There's a match between CTDIvol and DLP, so see if things can be updated or added.
                                        try:
                                            for key, val in acquisition.items():
                                                if key != 'CTDIvol' and key != 'DLP':
                                                    logger.debug("{0} -> {1}".format(key, str(val)))
                                                    ##############################################
                                                    # Code here to add / update the data...
                                                    coding = Dataset()
                                                    coding2 = Dataset()
                                                    if key == 'ProtocolName':
                                                        # First, check if there is already a ProtocolName container that has a protocol in it.
                                                        data_exists = False
                                                        for container2b in container.ContentSequence:
                                                            for container3b in container2b:
                                                                try:
                                                                    if container3b[0].CodeValue == '125203':
                                                                        data_exists = True
                                                                        if container2b.TextValue == '':
                                                                            # Update the protocol if it is blank
                                                                            container2b.TextValue = val
                                                                except AttributeError:
                                                                    pass
                                                                except Exception:
                                                                    logger.debug(traceback.format_exc())

                                                        if not data_exists:
                                                            # If there is no protocol then add it
                                                            #    (0040, a010) Relationship Type                   CS: 'CONTAINS'
                                                            #    (0040, a040) Value Type                          CS: 'TEXT'
                                                            #    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
                                                            #       (0008, 0100) Code Value                          SH: '125203'
                                                            #       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
                                                            #       (0008, 0104) Code Meaning                        LO: 'Acquisition Protocol'
                                                            #       ---------
                                                            #    (0040, a160) Text Value                          UT: 'TAP'
                                                            # Create the inner coding bit
                                                            coding.CodeValue = '125203'
                                                            coding.CodingSchemeDesignator = "DCM"
                                                            coding.CodeMeaning = "Acquisition Protocol"
                                                            # Create the outer container bit, including the protocol name
                                                            prot_container = Dataset()
                                                            prot_container.RelationshipType = "CONTAINS"
                                                            prot_container.ValueType = "TEXT"
                                                            prot_container.TextValue = val
                                                            # Add the coding sequence into the container.
                                                            # Sequences are lists.
                                                            prot_container.ConceptNameCodeSequence = Sequence([coding])
                                                            container.ContentSequence.append(prot_container)

                                                    if key == 'SpiralPitchFactor':
                                                        # First, check if there is already a SpiralPitchFactor container that has a value in it.
                                                        data_exists = False

                                                        for container2b in container.ContentSequence:
                                                            if container2b.ValueType == 'CONTAINER':
                                                                if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeValue == '113828':
                                                                                    data_exists = True
                                                                            except AttributeError:
                                                                                pass
                                                                            except Exception:
                                                                                logger.debug(traceback.format_exc())

                                                                    if not data_exists:
                                                                        # If there is no pitch then add it
                                                                        #       ---------
                                                                        #       (0040, a010) Relationship Type                   CS: 'CONTAINS'
                                                                        #       (0040, a040) Value Type                          CS: 'NUM'
                                                                        #       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
                                                                        #          (0008, 0100) Code Value                          SH: '113828'
                                                                        #          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
                                                                        #          (0008, 0104) Code Meaning                        LO: 'Pitch Factor'
                                                                        #          ---------
                                                                        #       (0040, a300)  Measured Value Sequence   1 item(s) ----
                                                                        #          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
                                                                        #             (0008, 0100) Code Value                          SH: '{ratio}'
                                                                        #             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
                                                                        #             (0008, 0103) Coding Scheme Version               SH: '1.4'
                                                                        #             (0008, 0104) Code Meaning                        LO: 'ratio'
                                                                        #             ---------
                                                                        #          (0040, a30a) Numeric Value                       DS: '0.6'
                                                                        #          ---------
                                                                        #       ---------
                                                                        # Create the first inner coding bit
                                                                        coding.CodeValue = '113828'
                                                                        coding.CodingSchemeDesignator = "DCM"
                                                                        coding.CodeMeaning = "Pitch Factor"
                                                                        # Create the second inner coding bit
                                                                        coding2.CodeValue = '{ratio}'
                                                                        coding2.CodingSchemeDesignator = "UCUM"
                                                                        coding2.CodingSchemeVersion = "1.4"
                                                                        coding2.CodeMeaning = "ratio"
                                                                        measurement_units_container = Dataset()
                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding2])
                                                                        measurement_units_container.NumericValue = val
                                                                        measured_value_sequence = Sequence([measurement_units_container])
                                                                        # Create the outer container bit
                                                                        pitch_container = Dataset()
                                                                        pitch_container.RelationshipType = "CONTAINS"
                                                                        pitch_container.ValueType = "NUM"
                                                                        # Add the coding sequence into the container.
                                                                        # Sequences are lists.
                                                                        pitch_container.ConceptNameCodeSequence = Sequence([coding])
                                                                        pitch_container.MeasuredValueSequence = measured_value_sequence
                                                                        container2b.ContentSequence.append(pitch_container)

                                                    if key == 'NominalSingleCollimationWidth':
                                                        # First, check if there is already a NominalSingleCollimationWidth container that has a value in it.
                                                        data_exists = False

                                                        for container2b in container.ContentSequence:
                                                            if container2b.ValueType == 'CONTAINER':
                                                                if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeValue == '113826':
                                                                                    data_exists = True
                                                                            except AttributeError:
                                                                                pass
                                                                    if not data_exists:
                                                                        # If there is no NominalSingleCollimationWidth then add it
                                                                        #       ---------
                                                                        #       (0040, a010) Relationship Type                   CS: 'CONTAINS'
                                                                        #       (0040, a040) Value Type                          CS: 'NUM'
                                                                        #       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
                                                                        #          (0008, 0100) Code Value                          SH: '113826'
                                                                        #          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
                                                                        #          (0008, 0104) Code Meaning                        LO: 'Nominal Single Collimation Width'
                                                                        #          ---------
                                                                        #       (0040, a300)  Measured Value Sequence   1 item(s) ----
                                                                        #          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
                                                                        #             (0008, 0100) Code Value                          SH: 'mm'
                                                                        #             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
                                                                        #             (0008, 0103) Coding Scheme Version               SH: '1.4'
                                                                        #             (0008, 0104) Code Meaning                        LO: 'mm'
                                                                        #             ---------
                                                                        #          (0040, a30a) Numeric Value                       DS: '0.6'
                                                                        #          ---------
                                                                        #       ---------
                                                                        # Create the first inner coding bit
                                                                        coding.CodeValue = '113826'
                                                                        coding.CodingSchemeDesignator = "DCM"
                                                                        coding.CodeMeaning = "Nominal Single Collimation Width"
                                                                        # Create the second inner coding bit
                                                                        coding2.CodeValue = 'mm'
                                                                        coding2.CodingSchemeDesignator = "UCUM"
                                                                        coding2.CodingSchemeVersion = "1.4"
                                                                        coding2.CodeMeaning = "mm"
                                                                        measurement_units_container = Dataset()
                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding2])
                                                                        measurement_units_container.NumericValue = val
                                                                        measured_value_sequence = Sequence(
                                                                            [measurement_units_container])
                                                                        # Create the outer container bit
                                                                        pitch_container = Dataset()
                                                                        pitch_container.RelationshipType = "CONTAINS"
                                                                        pitch_container.ValueType = "NUM"
                                                                        # Add the coding sequence into the container.
                                                                        # Sequences are lists.
                                                                        pitch_container.ConceptNameCodeSequence = Sequence([coding])
                                                                        pitch_container.MeasuredValueSequence = measured_value_sequence
                                                                        container2b.ContentSequence.append(pitch_container)

                                                    if key == 'NominalTotalCollimationWidth':
                                                        # First, check if there is already a NominalSingleCollimationWidth container that has a value in it.
                                                        data_exists = False

                                                        for container2b in container.ContentSequence:
                                                            if container2b.ValueType == 'CONTAINER':
                                                                if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeValue == '113827':
                                                                                    data_exists = True
                                                                            except AttributeError:
                                                                                pass
                                                                            except Exception:
                                                                                logger.debug(traceback.format_exc())

                                                                    if not data_exists:
                                                                        # If there is no NominalSingleCollimationWidth then add it
                                                                        #       ---------
                                                                        #       (0040, a010) Relationship Type                   CS: 'CONTAINS'
                                                                        #       (0040, a040) Value Type                          CS: 'NUM'
                                                                        #       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
                                                                        #          (0008, 0100) Code Value                          SH: '113827'
                                                                        #          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
                                                                        #          (0008, 0104) Code Meaning                        LO: 'Nominal Total Collimation Width'
                                                                        #          ---------
                                                                        #       (0040, a300)  Measured Value Sequence   1 item(s) ----
                                                                        #          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
                                                                        #             (0008, 0100) Code Value                          SH: 'mm'
                                                                        #             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
                                                                        #             (0008, 0103) Coding Scheme Version               SH: '1.4'
                                                                        #             (0008, 0104) Code Meaning                        LO: 'mm'
                                                                        #             ---------
                                                                        #          (0040, a30a) Numeric Value                       DS: '38.4'
                                                                        #          ---------
                                                                        #       ---------
                                                                        # Create the first inner coding bit
                                                                        coding.CodeValue = '113827'
                                                                        coding.CodingSchemeDesignator = "DCM"
                                                                        coding.CodeMeaning = "Nominal Total Collimation Width"
                                                                        # Create the second inner coding bit
                                                                        coding2.CodeValue = 'mm'
                                                                        coding2.CodingSchemeDesignator = "UCUM"
                                                                        coding2.CodingSchemeVersion = "1.4"
                                                                        coding2.CodeMeaning = "mm"
                                                                        measurement_units_container = Dataset()
                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding2])
                                                                        measurement_units_container.NumericValue = val
                                                                        measured_value_sequence = Sequence([measurement_units_container])
                                                                        # Create the outer container bit
                                                                        pitch_container = Dataset()
                                                                        pitch_container.RelationshipType = "CONTAINS"
                                                                        pitch_container.ValueType = "NUM"
                                                                        # Add the coding sequence into the container.
                                                                        # Sequences are lists.
                                                                        pitch_container.ConceptNameCodeSequence = Sequence([coding])
                                                                        pitch_container.MeasuredValueSequence = measured_value_sequence
                                                                        container2b.ContentSequence.append(pitch_container)

                                                    if key == 'ExposureModulationType':
                                                        # First, check if there is already an ExposureModulationType container that has a value in it.
                                                        data_exists = False
                                                        for container2b in container.ContentSequence:
                                                            for container3b in container2b:
                                                                try:
                                                                    if container3b[0].CodeValue == '113842':
                                                                        data_exists = True
                                                                        if container2b.TextValue == '':
                                                                            # Update the X-Ray Modulation Type if it is blank
                                                                            container2b.TextValue = val
                                                                except AttributeError:
                                                                    pass
                                                                except Exception:
                                                                    logger.debug(traceback.format_exc())

                                                        if not data_exists:
                                                            # Create the inner coding bit
                                                            coding.CodeValue = '113842'
                                                            coding.CodingSchemeDesignator = "DCM"
                                                            coding.CodeMeaning = "X-Ray Modulation Type"
                                                            # Create the outer container bit, including the protocol name
                                                            prot_container = Dataset()
                                                            prot_container.RelationshipType = "CONTAINS"
                                                            prot_container.ValueType = "TEXT"
                                                            prot_container.TextValue = val
                                                            # Add the coding sequence into the container.
                                                            # Sequences are lists.
                                                            prot_container.ConceptNameCodeSequence = Sequence([coding])
                                                            container.ContentSequence.append(prot_container)

                                                    if key == 'KVP':
                                                        # First, check if there is already a kVp value in an x-ray source parameters container inside
                                                        # a CT Acquisition Parameters container
                                                        source_parameters_exists = False
                                                        kvp_data_exists = False

                                                        for container2b in container.ContentSequence:
                                                            if container2b.ValueType == 'CONTAINER':
                                                                if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                    source_parameters_exists = True

                                                                                    for container5b in container4b:
                                                                                        try:
                                                                                            if container5b[0].ConceptNameCodeSequence[0].CodeValue == '113733':
                                                                                                kvp_data_exists = True
                                                                                        except AttributeError:
                                                                                            pass
                                                                                        except Exception:
                                                                                            logger.debug(traceback.format_exc())
                                                                            except AttributeError:
                                                                                # Likely there's no ConceptNameCodeSequence attribute
                                                                                pass
                                                                            except Exception:
                                                                                logger.debug(traceback.format_exc())

                                                                    if not source_parameters_exists:
                                                                        # There is no x-ray source parameters section, so add it
                                                                        # Create the x-ray source container
                                                                        source_container = Dataset()
                                                                        source_container.RelationshipType = "CONTAINS"
                                                                        source_container.ValueType = "CONTAINER"
                                                                        coding = Dataset()
                                                                        coding.CodeValue = '113831'
                                                                        coding.CodingSchemeDesignator = "DCM"
                                                                        coding.CodeMeaning = "CT X-Ray Source Parameters"
                                                                        source_container.ConceptNameCodeSequence = Sequence([coding])

                                                                        # Create the kVp container that will go in to the x-ray source container
                                                                        kvp_container = Dataset()
                                                                        kvp_container.RelationshipType = "CONTAINS"
                                                                        kvp_container.ValueType = "NUM"
                                                                        coding2 = Dataset()
                                                                        coding2.CodeValue = '113733'
                                                                        coding2.CodingSchemeDesignator = "DCM"
                                                                        coding2.CodeMeaning = "KVP"
                                                                        kvp_container.ConceptNameCodeSequence = Sequence([coding2])
                                                                        coding3 = Dataset()
                                                                        coding3.CodeValue = 'kV'
                                                                        coding3.CodingSchemeDesignator = "UCUM"
                                                                        coding3.CodingSchemeVersion = "1.4"
                                                                        coding3.CodeMeaning = "kV"
                                                                        measurement_units_container = Dataset()
                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding3])
                                                                        measurement_units_container.NumericValue = val
                                                                        measured_value_sequence = Sequence([measurement_units_container])
                                                                        kvp_container.MeasuredValueSequence = measured_value_sequence

                                                                        # Put the kVp container inside the x-ray source container
                                                                        source_container.ContentSequence = Sequence([kvp_container])

                                                                        # Add the source_container to the rdsr contents
                                                                        try:
                                                                            # Append it to an existing ContentSequence
                                                                            container2b.ContentSequence.append(source_container)
                                                                        except TypeError:
                                                                            # ContentSequence doesn't exist, so add it
                                                                            container2b.ContentSequence = Sequence([source_container])
                                                                        except Exception:
                                                                            logger.debug(traceback.format_exc())

                                                                        source_parameters_exists = True
                                                                        kvp_data_exists = True

                                                                    elif not kvp_data_exists:
                                                                        # CT X-ray Source Parameters exists, but there is no kVp data
                                                                        for container3b in container2b:
                                                                            for container4b in container3b:
                                                                                try:
                                                                                    if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                        # Create the kVp container that will go in to the x-ray source container
                                                                                        kvp_container = Dataset()
                                                                                        kvp_container.RelationshipType = "CONTAINS"
                                                                                        kvp_container.ValueType = "NUM"
                                                                                        coding2 = Dataset()
                                                                                        coding2.CodeValue = '113733'
                                                                                        coding2.CodingSchemeDesignator = "DCM"
                                                                                        coding2.CodeMeaning = "KVP"
                                                                                        kvp_container.ConceptNameCodeSequence = Sequence([coding2])
                                                                                        coding3 = Dataset()
                                                                                        coding3.CodeValue = 'kV'
                                                                                        coding3.CodingSchemeDesignator = "UCUM"
                                                                                        coding3.CodingSchemeVersion = "1.4"
                                                                                        coding3.CodeMeaning = "kV"
                                                                                        measurement_units_container = Dataset()
                                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding3])
                                                                                        measurement_units_container.NumericValue = val
                                                                                        measured_value_sequence = Sequence([measurement_units_container])
                                                                                        kvp_container.MeasuredValueSequence = measured_value_sequence

                                                                                        # Add the kVp container inside the x-ray source container
                                                                                        container4b.ContentSequence.append(kvp_container)

                                                                                        kvp_data_exists = True

                                                                                except AttributeError:
                                                                                    # Likely there's no ConceptNameCodeSequence attribute
                                                                                    pass
                                                                                except Exception:
                                                                                    logger.debug(traceback.format_exc())

                                                    if key == 'ExposureTime':
                                                        # First, check if there is already an exposure time per rotation value in an x-ray source parameters container inside
                                                        # a CT Acquisition Parameters container.
                                                        source_parameters_exists = False
                                                        exposure_time_per_rotation_data_exists = False

                                                        for container2b in container.ContentSequence:
                                                            if container2b.ValueType == 'CONTAINER':
                                                                if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                    source_parameters_exists = True

                                                                                    for container5b in container4b:
                                                                                        try:
                                                                                            if container5b[0].ConceptNameCodeSequence[0].CodeValue == '113843':
                                                                                                exposure_time_per_rotation_data_exists = True
                                                                                        except AttributeError:
                                                                                            pass
                                                                                        except Exception:
                                                                                            logger.debug(traceback.format_exc())
                                                                            except AttributeError:
                                                                                # Likely there's no ConceptNameCodeSequence attribute
                                                                                pass
                                                                            except Exception:
                                                                                logger.debug(traceback.format_exc())

                                                                    if not source_parameters_exists:
                                                                        # There is no x-ray source parameters section, so add it
                                                                        # Create the x-ray source container
                                                                        source_container = Dataset()
                                                                        source_container.RelationshipType = "CONTAINS"
                                                                        source_container.ValueType = "CONTAINER"
                                                                        coding = Dataset()
                                                                        coding.CodeValue = '113831'
                                                                        coding.CodingSchemeDesignator = "DCM"
                                                                        coding.CodeMeaning = "CT X-Ray Source Parameters"
                                                                        source_container.ConceptNameCodeSequence = Sequence([coding])

                                                                        # Create the kVp container that will go in to the x-ray source container
                                                                        exposure_time_per_rotation_container = Dataset()
                                                                        exposure_time_per_rotation_container.RelationshipType = "CONTAINS"
                                                                        exposure_time_per_rotation_container.ValueType = "NUM"
                                                                        coding2 = Dataset()
                                                                        coding2.CodeValue = '113843'
                                                                        coding2.CodingSchemeDesignator = "DCM"
                                                                        coding2.CodeMeaning = "Exposure Time per Rotation"
                                                                        exposure_time_per_rotation_container.ConceptNameCodeSequence = Sequence([coding2])
                                                                        coding3 = Dataset()
                                                                        coding3.CodeValue = 's'
                                                                        coding3.CodingSchemeDesignator = "UCUM"
                                                                        coding3.CodingSchemeVersion = "1.4"
                                                                        coding3.CodeMeaning = "s"
                                                                        measurement_units_container = Dataset()
                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding3])
                                                                        measurement_units_container.NumericValue = str(float(val) / 1000)
                                                                        measured_value_sequence = Sequence([measurement_units_container])
                                                                        exposure_time_per_rotation_container.MeasuredValueSequence = measured_value_sequence

                                                                        # Put the exposure time per rotation container inside the x-ray source container
                                                                        source_container.ContentSequence = Sequence([exposure_time_per_rotation_container])

                                                                        # Add the source_container to the rdsr contents
                                                                        try:
                                                                            # Append it to an existing ContentSequence
                                                                            container2b.ContentSequence.append(source_container)
                                                                        except TypeError:
                                                                            # ContentSequence doesn't exist, so add it
                                                                            container2b.ContentSequence = Sequence([source_container])
                                                                        except Exception:
                                                                            logger.debug(traceback.format_exc())

                                                                        source_parameters_exists = True
                                                                        exposure_time_per_rotation_data_exists = True

                                                                    elif not exposure_time_per_rotation_data_exists:
                                                                        # CT X-ray Source Parameters exists, but there is no exposure time per rotation data
                                                                        for container3b in container2b:
                                                                            for container4b in container3b:
                                                                                try:
                                                                                    if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                        # Create the exposure time per rotation container that will go in to the x-ray source container
                                                                                        exposure_time_per_rotation_container = Dataset()
                                                                                        exposure_time_per_rotation_container.RelationshipType = "CONTAINS"
                                                                                        exposure_time_per_rotation_container.ValueType = "NUM"
                                                                                        coding2 = Dataset()
                                                                                        coding2.CodeValue = '113843'
                                                                                        coding2.CodingSchemeDesignator = "DCM"
                                                                                        coding2.CodeMeaning = "Exposure Time per Rotation"
                                                                                        exposure_time_per_rotation_container.ConceptNameCodeSequence = Sequence([coding2])
                                                                                        coding3 = Dataset()
                                                                                        coding3.CodeValue = 's'
                                                                                        coding3.CodingSchemeDesignator = "UCUM"
                                                                                        coding3.CodingSchemeVersion = "1.4"
                                                                                        coding3.CodeMeaning = "s"
                                                                                        measurement_units_container = Dataset()
                                                                                        measurement_units_container.MeasurementUnitsCodeSequence = Sequence([coding3])
                                                                                        measurement_units_container.NumericValue = str(float(val) / 1000)
                                                                                        measured_value_sequence = Sequence([measurement_units_container])
                                                                                        exposure_time_per_rotation_container.MeasuredValueSequence = measured_value_sequence

                                                                                        # Add the exposure time per rotation container inside the x-ray source container
                                                                                        container4b.ContentSequence.append(exposure_time_per_rotation_container)

                                                                                        exposure_time_per_rotation_data_exists = True

                                                                                except AttributeError:
                                                                                    # Likely there's no ConceptNameCodeSequence attribute
                                                                                    pass
                                                                                except Exception:
                                                                                    logger.debug(traceback.format_exc())
                                        except KeyError, e:
                                            logger.debug(traceback.format_exc())
                                        except Exception, e:
                                            logger.debug(traceback.format_exc())
                                            # The end of updating the RDSR
                                            ##############################################
                                except KeyError:
                                    # Either CTDIvol or DLP data is not present
                                    pass
                                except ValueError:
                                    # Perhaps the contents of the DLP or CTDIvol are not values
                                    pass
                                except Exception:
                                    logger.debug(traceback.format_exc())

    logger.debug('Updated acquisition data')
    logger.debug('Saving updated RDSR file')
    dcm.save_as(new_rdsr_file)
    logger.debug('Updated RDSR file saved')
    return 1


@shared_task(name="remapp.extractors.ct_toshiba.ct_toshiba")
def ct_toshiba(folder_name):
    """Function to create radiation dose structured reports from a folder of dose images.

    :param folder_name: Path to folder containing Toshiba DICOM objects - dose summary and images
    """
    import dicom

    rdsr_name = 'sr.dcm'
    updated_rdsr_name = 'sr_updated.dcm'
    combined_rdsr_name = 'sr_combined.dcm'

    # Split the folder of images by StudyInstanceUID. This is required because pixelmed.jar will only process the
    # first dose summary image it finds. Splitting the files by StudyInstanceUID should mean that there is only one
    # dose summary per folder. N.B. I think Conquest may do this by default with incoming DICOM objects. This
    # routine also renames the files using integer file names to ensure that they are accepted by dcmmkdir later on.
    logger.debug('Splitting into folders by StudyInstanceUID for {0}'.format(folder_name))
    folders = _split_by_studyinstanceuid(folder_name)
    logger.debug('Splitting into folders by StudyInstanceUID complete for {0}'.format(folder_name))

    # Obtain additional information from the image tags in each folder and add this information to the RDSR file.
    for folder in folders:

        # Check to see if there's just one dose summary in the folder
        dose_summary_object_info = _find_dose_summary_objects(folder)
        logger.debug("dose_summary_object_info is {0}".format(dose_summary_object_info))

        # For Toshiba scanners each dose summary consists of two objects
        number_of_dose_summary_objects = len(dose_summary_object_info) // 2

        if number_of_dose_summary_objects > 1:
            # There's more than one pair of dose summary objects, so duplicate the
            # contents of folder number_of_dose_summary_objects times.
            unique_study_times = {item["studyTime"] for item in dose_summary_object_info}
            subfolder_paths = []
            for unique_study_time in unique_study_times:
                subfolder_path = os.path.join(folder, unique_study_time)
                subfolder_paths.append(subfolder_path)
                if not os.path.isdir(subfolder_path):
                    os.mkdir(subfolder_path)
                _copy_files_from_a_to_b(folder, subfolder_path)

            # Delete all but one pair of dose summary objects from each subfolder
            for unique_study_time in unique_study_times:
                for dose_summary_object in dose_summary_object_info:
                    if dose_summary_object["studyTime"] != unique_study_time:
                        # Delete the corresponding dose_summary_object file from the
                        # x subfolder in folder
                        os.remove(os.path.join(folder, unique_study_time, dose_summary_object["fileName"]))

            # Now create an RDSR in each subfolder in subfolder_paths
            for sub_folder in subfolder_paths:
                # Create a DICOM RDSR for the sub-folder using pixelmed.jar.
                logger.debug('Trying to make initial DICOM RDSR object in {0}'.format(sub_folder))
                combined_command = JAVA_EXE + ' ' + JAVA_OPTIONS + ' ' + PIXELMED_JAR + ' ' + PIXELMED_JAR_OPTIONS
                _make_dicom_rdsr(sub_folder, combined_command, rdsr_name)
                # Check that the initial RDSR exists
                initial_rdsr_name_and_path = os.path.join(sub_folder, rdsr_name)
                if not os.path.isfile(initial_rdsr_name_and_path):
                    logger.debug('Failed to create initial DICOM RDSR object created in {0}. Skipping.'.format(sub_folder))
                    # Remove this sub_folder from subfolder_paths list as it can't be used
                    subfolder_paths.remove(sub_folder)
                    continue
                logger.debug('Initial DICOM RDSR object created in {0}'.format(sub_folder))

                logger.debug('Gathering extra information from images in {0}'.format(sub_folder))
                extra_information = _find_extra_info(sub_folder)
                extra_study_information = extra_information[0]
                extra_acquisition_information = extra_information[1]
                logger.debug('Gathered extra information from images in {0}'.format(sub_folder))

                # Use the extra information to update the initial rdsr file created by DoseUtility
                logger.debug('Updating information in rdsr in {0}'.format(sub_folder))
                updated_rdsr_name_and_path = os.path.join(sub_folder, updated_rdsr_name)
                result = _update_dicom_rdsr(initial_rdsr_name_and_path, extra_study_information,
                                            extra_acquisition_information, updated_rdsr_name_and_path)
                # Check that the updated RDSR exists
                if result == 1:
                    logger.debug('Updated information in rdsr')
                else:
                    logger.debug('Failed to update the initial DICOM RDSR object in {0}. Skipping.'.format(sub_folder))
                    # Remove this sub_folder from subfolder_paths list as it can't be used
                    subfolder_paths.remove(sub_folder)
                    continue

            # Now combine the data contained in the RDSRs
            first_subfolder = True
            for sub_folder in subfolder_paths:
                if first_subfolder == True:
                    shutil.copy(os.path.join(sub_folder, updated_rdsr_name), os.path.join(folder, combined_rdsr_name))
                    combined_rdsr = dicom.read_file(os.path.join(folder, combined_rdsr_name))
                    for content_sequence in combined_rdsr.ContentSequence:
                        if content_sequence.ConceptNameCodeSequence[0].CodeMeaning == 'CT Accumulated Dose Data':
                            combined_rdsr_accumulated_dose_data = content_sequence
                    first_subfolder = False
                else:
                    current_rdsr = dicom.read_file(os.path.join(sub_folder, updated_rdsr_name))
                    for content_sequence in current_rdsr.ContentSequence:
                        if content_sequence.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition':
                            combined_rdsr.ContentSequence.append(content_sequence)
                        if content_sequence.ConceptNameCodeSequence[0].CodeMeaning == 'CT Accumulated Dose Data':
                            # Total Number of Irradiation Events
                            logger.debug("Trying to update total number of irradiation events")
                            for item in content_sequence.ContentSequence:
                                if item.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Irradiation Events':
                                    additional_amount = item.MeasuredValueSequence[0].NumericValue
                                    logger.debug("Found extra events: {0}".format(additional_amount))
                            for item in combined_rdsr_accumulated_dose_data.ContentSequence:
                                if item.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Irradiation Events':
                                    logger.debug("Found current events: {0}".format(item.MeasuredValueSequence[0].NumericValue))
                                    item.MeasuredValueSequence[0].NumericValue = str(int(item.MeasuredValueSequence[0].NumericValue + additional_amount))
                                    logger.debug("Updated to: {0}".format(item.MeasuredValueSequence[0].NumericValue))

                            # CT Dose Length Product Total
                            logger.debug("Trying to update total DLP")
                            extra_ct_dlp_total_content_sequence = None
                            for content_seq in content_sequence.ContentSequence:
                                if content_seq.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose Length Product Total':
                                    additional_amount = content_seq.MeasuredValueSequence[0].NumericValue
                                    logger.debug("Found extra DLP: {0}".format(additional_amount))
                                    extra_ct_dlp_total_content_sequence = content_seq
                                    # If the total DLP is not zero
                                    if float(additional_amount):
                                        # Find out which dosimetry phantom this value is for
                                        for cont_seq in content_seq.ContentSequence:
                                            if cont_seq.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIw Phantom Type':
                                                additional_type = cont_seq.ConceptCodeSequence[0].CodeMeaning

                            for i, content_seq in enumerate(combined_rdsr_accumulated_dose_data.ContentSequence):
                                if content_seq.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose Length Product Total':
                                    current_amount = content_seq.MeasuredValueSequence[0].NumericValue
                                    logger.debug("Found current total DLP: {0}".format(current_amount))
                                    # If the total DLP is not zero
                                    total_type = None
                                    if float(current_amount):
                                        # Find out which dosimetry phantom this value is for
                                        for cont_seq in content_seq.ContentSequence:
                                            if cont_seq.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIw Phantom Type':
                                                total_type = cont_seq.ConceptCodeSequence[0].CodeMeaning

                                    if current_amount and additional_amount:
                                        # If combined_rdsr total DLP and new one use the same dosimetry phantom then just add them together.
                                        if total_type == additional_type:
                                            content_seq.MeasuredValueSequence[0].NumericValue = "%.2f" % (content_seq.MeasuredValueSequence[0].NumericValue + additional_amount)
                                        # If additional DLP is to 16 cm head phantom then divide it by 2 before adding.
                                        elif "head" in additional_type.lower():
                                            content_seq.MeasuredValueSequence[0].NumericValue = "%.2f" % (content_seq.MeasuredValueSequence[0].NumericValue + (additional_amount/2.0))
                                        # If current total DLP is to 16 cm head phantom then divide it by 2 before adding the 32 cm additional.
                                        else:
                                            content_seq.MeasuredValueSequence[0].NumericValue = "%.2f" % ((content_seq.MeasuredValueSequence[0].NumericValue/2.0) + additional_amount)
                                        logger.debug("Updated to: {0}".format(content_seq.MeasuredValueSequence[0].NumericValue))
                                    elif current_amount:
                                        # There is no additional DLP to add
                                        logger.debug("No additional DLP to add")
                                    else:
                                        # There is no current DLP, but we do have extra, so over-write the current content sequence with extra_ct_dlp_total_content_sequence
                                        logger.debug("Current total DLP is zero. Replacing with extra {0} mGy.cm.".format(additional_amount))
                                        combined_rdsr_accumulated_dose_data.ContentSequence[i] = extra_ct_dlp_total_content_sequence

            if len(subfolder_paths) > 0:
                combined_rdsr.save_as(os.path.join(folder, combined_rdsr_name+'_updated'))
                logger.debug('Importing updated combined rdsr in to OpenREM ({0})'.format(os.path.join(folder, combined_rdsr_name+'_updated')))
                rdsr(os.path.join(folder, combined_rdsr_name+'_updated'))
                logger.debug('Imported in to OpenREM')
            else:
                logger.debug('RDSRs could not be created for any subfolders')

        else:
            # Create a DICOM RDSR for the sub-folder using pixelmed.jar.
            logger.debug('Trying to make initial DICOM RDSR object in {0}'.format(folder))
            combined_command = JAVA_EXE + ' ' + JAVA_OPTIONS + ' ' + PIXELMED_JAR + ' ' + PIXELMED_JAR_OPTIONS
            _make_dicom_rdsr(folder, combined_command, rdsr_name)
            # Check that the initial RDSR exists
            initial_rdsr_name_and_path = os.path.join(folder, rdsr_name)
            if os.path.isfile(initial_rdsr_name_and_path):
                logger.debug('Initial DICOM RDSR object created in {0}'.format(folder))

                logger.debug('Gathering extra information from images in {0}'.format(folder))
                extra_information = _find_extra_info(folder)
                extra_study_information = extra_information[0]
                extra_acquisition_information = extra_information[1]
                logger.debug('Gathered extra information from images in {0}'.format(folder))

                # Use the extra information to update the initial rdsr file created by DoseUtility
                logger.debug('Updating information in rdsr in {0}'.format(folder))
                updated_rdsr_name_and_path = os.path.join(folder, updated_rdsr_name)
                result = _update_dicom_rdsr(initial_rdsr_name_and_path, extra_study_information,
                                            extra_acquisition_information, updated_rdsr_name_and_path)
                logger.debug('Updated information in rdsr')

                # Now import the updated rdsr into OpenREM using the Toshiba extractor
                if result == 1:
                    logger.debug('Importing updated rdsr in to OpenREM ({0})'.format(updated_rdsr_name_and_path))
                    rdsr(updated_rdsr_name_and_path)
                    logger.debug('Imported in to OpenREM')
                else:
                    logger.debug('Not imported to OpenREM. Result is: {0}'.format(result))
            else:
                logger.debug('Failed to create initial DICOM RDSR object created in {0}. Skipping.'.format(folder))

    # Now delete the image folder
    logger.debug('Removing study folder')
    shutil.rmtree(folder_name)
    logger.debug('Removing study folder complete')
    logger.debug('Reached end of ct_toshiba routine')
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Error: supply exactly one argument - the folder containing the DICOM objects')

    sys.exit(ct_toshiba(sys.argv[1]))

