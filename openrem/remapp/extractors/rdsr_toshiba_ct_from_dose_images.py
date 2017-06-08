import sys
import os
from glob import glob
from openrem.remapp.extractors import rdsr
from openremproject.settings import DCMCONV, DCMMKDIR, JAVA_EXE, JAVA_OPTIONS, PIXELMED_JAR, PIXELMED_JAR_OPTIONS
import shutil
import django
import logging

logger = logging.getLogger(__name__)

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

from celery import shared_task


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
    import shutil
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
                print 'Invalid DICOM error: {0} when trying to read {1}'.format(e.message, os.path.join(dicom_path, filename))
                pass

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

    """
    import dicom

    from dicom.filereader import InvalidDicomError

    from struct import unpack

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
                        print acquisition_code
                        acquisitions_collected.append(acquisition_code)

                        info_dictionary = {}
                        try:
                            info_dictionary['AcquisitionNumber'] = dcm.AcquisitionNumber
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['AcquisitionTime'] = dcm.AcquisitionTime
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['ProtocolName'] = dcm.ProtocolName
                            # print dcm.ProtocolName
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['ExposureTime'] = dcm.ExposureTime
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['KVP'] = dcm.KVP
                            # print dcm.KVP
                        except AttributeError:
                            pass
                        try:
                            # For some Toshiba CT scanners there is information on the detector configuration
                            if dcm.Manufacturer.lower() == 'toshiba':
                                info_dictionary['NominalSingleCollimationWidth'] = float(dcm[0x7005, 0x1008].value)
                                info_dictionary['NominalTotalCollimationWidth'] = dcm[0x7005, 0x1009].value.count('1') * float(dcm[0x7005, 0x1008].value)
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['SpiralPitchFactor'] = dcm.SpiralPitchFactor
                            # print dcm.SpiralPitchFactor
                        except AttributeError:
                            try:
                                # For some Toshiba CT scanners, stored as a decimal string (DS)
                                info_dictionary['SpiralPitchFactor'] = dcm[0x7005, 0x1023].value
                                # print dcm[0x7005, 0x1023].value
                            except KeyError:
                                pass
                        try:
                            # For some Toshiba CT scanners, stored as a floating point double (FD) by the
                            # scanner, but encoded by PACS as hex
                            if dcm[0x7005, 0x1063].VR == 'FD':
                                info_dictionary['CTDIvol'] = dcm[0x7005, 0x1063].value
                            else:
                                info_dictionary['CTDIvol'] = unpack('<d', ''.join(dcm[0x7005, 0x1063]))[0]
                        except KeyError:
                            print 'There was a key error when finding CTDIvol. Trying elsewhere.'
                            print dcm.CTDIvol
                            try:
                                info_dictionary['CTDIvol'] = dcm.CTDIvol
                            except AttributeError:
                                pass
                        except TypeError:
                            print 'There was a type error when finding CTDIvol. Trying elsewhere.'
                            try:
                                info_dictionary['CTDIvol'] = dcm.CTDIvol
                            except AttributeError:
                                pass
                        try:
                            info_dictionary['ExposureModulationType'] = dcm.ExposureModulationType
                        except AttributeError:
                            pass
                        try:
                            # For some Toshiba CT scanners, stored as a floating point double (FD) by the
                            # scanner, but encoded by PACS as hex
                            if dcm[0x7005, 0x1040].VR == 'FD':
                                info_dictionary['DLP'] = dcm[0x7005, 0x1040].value
                            else:
                                info_dictionary['DLP'] = unpack('<d', ''.join(dcm[0x7005, 0x1040]))[0]
                        except KeyError:
                            pass
                        except TypeError:
                            pass

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
                        except AttributeError:
                            # dcm.ProcedureCodeSequence[0].CodeMeaning isn't present either
                            pass

                    try:
                        if dcm.RequestedProcedureDescription != '':
                            try:
                                if study_info['RequestedProcedureDescription'] == '':
                                    # Only update study_info['RequestedProcedureDescription'] if it's empty
                                    study_info['RequestedProcedureDescription'] = dcm.RequestedProcedureDescription
                            except KeyError:
                                # study_info['RequestedProcedureDescription'] doesn't exist yet, so create it
                                study_info['RequestedProcedureDescription'] = dcm.RequestedProcedureDescription
                    except AttributeError:
                        # dcm.RequestedProcedureDescription isn't present. Try looking at the
                        # RequestedProcedureDescription of RequestAttributesSequence instead
                        try:
                            if dcm.ProcedureCodeSequence[0].CodeMeaning != '':
                                try:
                                    if study_info['RequestedProcedureDescription'] == '':
                                        # Only update study_info['RequestedProcedureDescription'] if it's empty
                                        study_info['RequestedProcedureDescription'] = dcm.ProcedureCodeSequence[
                                            0].CodeMeaning
                                except KeyError:
                                    # study_info['RequestedProcedureDescription'] isn't present, so add it
                                    study_info['RequestedProcedureDescription'] = dcm.ProcedureCodeSequence[
                                        0].CodeMeaning
                        except AttributeError:
                            # dcm.ProcedureCodeSequence[0].CodeMeaning isn't present either
                            pass

                except AttributeError:
                    pass

            except InvalidDicomError:
                pass

    return [study_info, acquisition_info]


def _make_explicit_vr_little_endian(folder_list, dcmconv_exe):
    """Parse folders of files, making each DICOM file explicit VR little endian using the DICOM toolkit dcmconv.exe
    command. See http://support.dcmtk.org/docs/dcmconv.html for documentation.

    Args:
        folder_list (list): A list of full paths containing DICOM objects.
        dcmconv_exe (str): A string containing the dcmconv command

    """
    import subprocess

    for path in folder_list:
        for filename in os.listdir(path):
            command = dcmconv_exe + ' +te ' + os.path.join(path, filename) + ' ' + os.path.join(path, filename)
            subprocess.call(command.split())


def _make_dicomdir(folder_list, dcmmkdir_exe):
    """Parse folders of files, making a DICOMDIR for each using the DICOM toolkit dcmmkdir.exe command. See
    http://support.dcmtk.org/docs/dcmmkdir.html for documentation.

    Args:
        folder_list (list): A list of full paths containing DICOM objects.
        dcmmkdir_exe (str): A string containing the dcmmkdir command

    """
    import subprocess

    for current_folder in folder_list:
        command = dcmmkdir_exe + ' --recurse --output-file ' + os.path.join(current_folder, 'DICOMDIR') + ' --input-directory ' + current_folder
        subprocess.call(command.split())


def _make_dicom_rdsr(folder_list, pixelmed_jar_command, sr_filename):
    """Parse folders of files, making a DICOM RDSR for each using pixelmed.jar.

    Args:
        folder_list (list): A list of full paths containing DICOM objects.
        pixelmed_jar_command (str): A string containing the pixelmed_jar command and options.
        sr_filename (str): A string containing the filename to use when creating the rdsr.

    """
    import subprocess

    for current_folder in folder_list:
        command = pixelmed_jar_command + ' ' + current_folder + ' ' + os.path.join(current_folder, sr_filename)
        subprocess.call(command.split())


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

    try:
        dcm = dicom.read_file(rdsr_file)
    except IOError as e:
        print 'I/O error({0}): {1} when trying to read {2}'.format(e.errno, e.strerror, rdsr_file)
        return 0

    # Update the study-level information if it does not exist, or is an empty string.
    for key, val in additional_study_info.items():
        try:
            rdsr_val = getattr(dcm, key)
            # print key, val
            if rdsr_val == '':
                setattr(dcm, key, val)
        except AttributeError:
            setattr(dcm, key, val)

    # Now go through each CT Aquisition container in the rdsr file and see if any of the information should be updated.
    for container in dcm.ContentSequence:
        if container.ValueType == 'CONTAINER':
            if container.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition':
                # print '###########################################'
                # print container
                # print '###########################################'
                for container2 in container.ContentSequence:
                    # The Acquisition protocol would go in at this level I think
                    if container2.ValueType == 'CONTAINER':
                        if container2.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose':
                            current_dlp = ''
                            current_ctdi_vol = ''
                            for container3 in container2.ContentSequence:
                                if container3.ConceptNameCodeSequence[0].CodeMeaning == 'DLP':
                                    current_dlp = container3.MeasuredValueSequence[0].NumericValue
                                    # print container3.MeasuredValueSequence[0].NumericValue
                                if container3.ConceptNameCodeSequence[0].CodeMeaning == 'Mean CTDIvol':
                                    current_ctdi_vol = container3.MeasuredValueSequence[0].NumericValue
                                    # print container3.MeasuredValueSequence[0].NumericValue

                            # Check to see if the current DLP and CTDIvol pair matches any of the acquisitions in
                            # additional_info
                            for acquisition in additional_acquisition_info:
                                try:
                                    print 'Current set is:'
                                    print float(acquisition['CTDIvol'])
                                    print float(current_ctdi_vol)
                                    print float(acquisition['DLP'])
                                    print float(current_dlp)
                                    if float(acquisition['CTDIvol']) == float(current_ctdi_vol) and float(acquisition['DLP']) == float(current_dlp):
                                        print '\nCTDIvol: {0} is equal to {1}'.format(float(acquisition['CTDIvol']), float(current_ctdi_vol))
                                        print '\nand'
                                        print '\nDLP: {0} is equal to {1}'.format(float(acquisition['DLP']), float(current_dlp))
                                        # There's a match between CTDIvol and DLP, so see if things can be updated or added.
                                        for key, val in acquisition.items():
                                            if key != 'CTDIvol' and key != 'DLP':
                                                print key + ' -> ' + str(val)
                                                ##############################################
                                                # Code here to add / update the data...
                                                coding = Dataset()
                                                coding2 = Dataset()
                                                # DJP note: need to know or look up the three things below for each item that needs to be added.
                                                if key == 'ProtocolName':
                                                    # First, check if there is already a ProtocolName container that has a protocol in it.
                                                    data_exists = False
                                                    for container2b in container.ContentSequence:
                                                        for container3b in container2b:
                                                            try:
                                                                if container3b[0].CodeValue == '125203':
                                                                    data_exists = True
                                                                    # print container2b.TextValue
                                                                    if container2b.TextValue == '':
                                                                        # Update the protocol if it is blank
                                                                        container2b.TextValue = val
                                                            except AttributeError:
                                                                pass
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
                                                    # First, check if there is already a SpiralPitchFactor container
                                                    # that has a value in it.
                                                    data_exists = False

                                                    for container2b in container.ContentSequence:
                                                        if container2b.ValueType == 'CONTAINER':
                                                            if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                for container3b in container2b:
                                                                    for container4b in container3b:
                                                                        try:
                                                                            if container4b.ConceptNameCodeSequence[0].CodeValue == '113828':
                                                                                data_exists = True
                                                                                # print container4b.MeasuredValueSequence[0].NumericValue
                                                                        except AttributeError:
                                                                            pass
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
                                                    # First, check if there is already a NominalSingleCollimationWidth container
                                                    # that has a value in it.
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

                                                if key == 'NominalTotalCollimationWidth':
                                                    # First, check if there is already a NominalSingleCollimationWidth container
                                                    # that has a value in it.
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
                                                    # First, check if there is already an ExposureModulationType container
                                                    # that has a value in it.
                                                    # First, check if there is already a ProtocolName container that has a protocol in it.
                                                    data_exists = False
                                                    for container2b in container.ContentSequence:
                                                        for container3b in container2b:
                                                            try:
                                                                if container3b[0].CodeValue == '113842':
                                                                    data_exists = True
                                                                    # print container2b.TextValue
                                                                    if container2b.TextValue == '':
                                                                        # Update the X-Ray Modulation Type if it is blank
                                                                        container2b.TextValue = val
                                                            except AttributeError:
                                                                pass
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
                                                    # a CT Acquisition Parameters container...
                                                    source_parameters_exists = False
                                                    kvp_data_exists = False

                                                    for container2b in container.ContentSequence:
                                                        if container2b.ValueType == 'CONTAINER':
                                                            if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                print 'Found CT Acquisition Parameters in KVP section...'
                                                                for container3b in container2b:
                                                                    for container4b in container3b:
                                                                        try:
                                                                            if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                source_parameters_exists = True

                                                                                for container5b in container4b:
                                                                                    try:
                                                                                        if container5b[0].ConceptNameCodeSequence[0].CodeValue == '113733':
                                                                                            print 'KVP data exists'
                                                                                            kvp_data_exists = True
                                                                                    except AttributeError:
                                                                                        print 'KVP data does not exist'
                                                                                        pass
                                                                        except AttributeError:
                                                                            # Likely there's no ConceptNameCodeSequence attribute
                                                                            pass

                                                                if not source_parameters_exists:
                                                                    print 'Creating source container in KVP section'
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
                                                                    print 'Creating KVP container'
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
                                                                        print 'Appended source container with KVP data in'
                                                                    except TypeError:
                                                                        # ContentSequence doesn't exist, so add it
                                                                        container2b.ContentSequence = Sequence([source_container])
                                                                        print 'Added source container with KVP data in'

                                                                    source_parameters_exists = True
                                                                    kvp_data_exists = True

                                                                elif not kvp_data_exists:
                                                                    print 'Source paramters exists but there is no KVP data - adding it'
                                                                    # CT X-ray Source Parameters exists, but there is no kVp data
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                    # Create the kVp container that will go in to the x-ray source container
                                                                                    print 'Found the CT X-ray Source Parameters sequence'
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
                                                                                    print 'Appended source container with KVP data in'

                                                                                    kvp_data_exists = True

                                                                            except AttributeError:
                                                                                # Likely there's no ConceptNameCodeSequence attribute
                                                                                pass

                                                if key == 'ExposureTime':
                                                    # First, check if there is already an exposure time per rotation value in an x-ray source parameters container inside
                                                    # a CT Acquisition Parameters container...
                                                    source_parameters_exists = False
                                                    exposure_time_per_rotation_data_exists = False

                                                    for container2b in container.ContentSequence:
                                                        if container2b.ValueType == 'CONTAINER':
                                                            if container2b.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                                                                print 'Found CT Acquisition Parameters in ExposureTime section...'
                                                                for container3b in container2b:
                                                                    for container4b in container3b:
                                                                        try:
                                                                            if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                source_parameters_exists = True

                                                                                for container5b in container4b:
                                                                                    try:
                                                                                        if container5b[0].ConceptNameCodeSequence[0].CodeValue == '113843':
                                                                                            print 'Exposure time per rotation data exists'
                                                                                            exposure_time_per_rotation_data_exists = True
                                                                                    except AttributeError:
                                                                                        print 'Exposure time per rotation data does not exist'
                                                                                        pass
                                                                        except AttributeError:
                                                                            # Likely there's no ConceptNameCodeSequence attribute
                                                                            pass

                                                                if not source_parameters_exists:
                                                                    print 'Creating source container in ExposureTime section'
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
                                                                    print 'Creating Exposure time per rotation container'
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
                                                                        print 'Appended source container with ExposureTime data in'
                                                                    except TypeError:
                                                                        # ContentSequence doesn't exist, so add it
                                                                        container2b.ContentSequence = Sequence([source_container])
                                                                        print 'Added source container with ExposureTime data in'

                                                                    source_parameters_exists = True
                                                                    exposure_time_per_rotation_data_exists = True

                                                                elif not exposure_time_per_rotation_data_exists:
                                                                    print 'Source paramters exists but there is no ExposureTime data - adding it'
                                                                    # CT X-ray Source Parameters exists, but there is no exposure time per rotation data
                                                                    for container3b in container2b:
                                                                        for container4b in container3b:
                                                                            try:
                                                                                if container4b.ConceptNameCodeSequence[0].CodeMeaning == 'CT X-Ray Source Parameters':
                                                                                    # Create the exposure time per rotation container that will go in to the x-ray source container
                                                                                    print 'Found the CT X-ray Source Parameters sequence'
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
                                                                                    print 'Appended source container with ExposureTime data in'

                                                                                    exposure_time_per_rotation_data_exists = True

                                                                            except AttributeError:
                                                                                # Likely there's no ConceptNameCodeSequence attribute
                                                                                pass

                                    # The end of updating the RDSR
                                    ##############################################
                                except KeyError:
                                    # Either CTDIvol or DLP data is not present
                                    pass
                                except ValueError:
                                    # Perhaps the contents of the DLP or CTDIvol are not values
                                    pass

    dcm.save_as(new_rdsr_file)
    return 1


@shared_task
def rdsr_toshiba_ct_from_dose_images(folder_name):
    rdsr_name = 'sr.dcm'
    updated_rdsr_name = 'sr_updated.dcm'

    # Split the folder of images by StudyInstanceUID. This is required because pixelmed.jar will only process the
    # first dose summary image it finds. Splitting the files by StudyInstanceUID should mean that there is only one
    # dose summary per folder. N.B. I think Conquest may do this by default with incoming DICOM objects. This
    # routine also renames the files using integer file names to ensure that they are accepted by dcmmkdir later on.
    print 'Splitting into folders by StudyInstanceUID'
    folders = _split_by_studyinstanceuid(folder_name)

    # Make all the DICOM objects explicit VR little endian. This is required by dcmmkdir.
    # print 'Making explicit VR little endian'
    # _make_explicit_vr_little_endian(folders, DCMCONV)

    # Now create a DICOMDIR for each sub-folder using dcmmkdir.
    # This is required by pixelmed.jar when creating RDSRs.
    # print 'Creating DICOMDIR files'
    # _make_dicomdir(folders, DCMMKDIR)

    # Now create a DICOM RDSR for each sub-folder using pixelmed.jar.
    print 'Making initial DICOM RDSR objects'
    combined_command = JAVA_EXE + ' ' + JAVA_OPTIONS + ' ' + PIXELMED_JAR + ' ' + PIXELMED_JAR_OPTIONS
    _make_dicom_rdsr(folders, combined_command, rdsr_name)

    # Obtain additional information from the image tags in each folder and add this information to the RDSR file.
    for folder in folders:
        print 'Gathering extra information from images in ' + folder
        extra_information = _find_extra_info(folder)
        extra_study_information = extra_information[0]
        print 'Extra study information is:'
        print extra_study_information
        extra_acquisition_information = extra_information[1]
        print 'Extra acquisition information is:'
        print extra_acquisition_information

        # Use the extra information to update the initial rdsr file created by DoseUtility
        print 'Updating information in rdsr in ' + folder
        initial_rdsr_name_and_path = os.path.join(folder, rdsr_name)
        updated_rdsr_name_and_path = os.path.join(folder, updated_rdsr_name)
        result = _update_dicom_rdsr(initial_rdsr_name_and_path, extra_study_information,
                                    extra_acquisition_information, updated_rdsr_name_and_path)

        # Now import the updated rdsr into OpenREM using the Toshiba extractor
        if result == 1:
            print 'Importing updated rdsr in to OpenREM (' + updated_rdsr_name_and_path + ')'
            rdsr(updated_rdsr_name_and_path)

    # Now delete the image folder
    shutil.rmtree(folder_name)
    return 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit('Error: supply exactly one argument - the folder containing the DICOM objects')

    sys.exit(rdsr_toshiba_ct_from_dose_images(sys.argv[1]))


# DoseUtility validation complaints - will be useful to work out codes etc for putting in things like pitch
# Found XRayRadiationDoseSR IOD
# Found Root Template TID_10011 (CTRadiationDose)
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 8] NUM (113824,DCM,"Exposure Time"): within 1.12.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10014 ScanningLength/[Row 1] NUM (113825,DCM,"Scanning Length"): within 1.12.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 10] NUM (113826,DCM,"Nominal Single Collimation Width"): within 1.12.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 11] NUM (113827,DCM,"Nominal Total Collimation Width"): within 1.12.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 13] NUM (113823,DCM,"Number of X-Ray Sources"): within 1.12.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 14] CONTAINER (113831,DCM,"CT X-Ray Source Parameters"): within 1.12.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 8] NUM (113824,DCM,"Exposure Time"): within 1.13.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 10] NUM (113826,DCM,"Nominal Single Collimation Width"): within 1.13.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 11] NUM (113827,DCM,"Nominal Total Collimation Width"): within 1.13.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 12] NUM (113828,DCM,"Pitch Factor"): within 1.13.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing conditional content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 13] NUM (113823,DCM,"Number of X-Ray Sources"): within 1.13.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 14] CONTAINER (113831,DCM,"CT X-Ray Source Parameters"): within 1.13.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 8] NUM (113824,DCM,"Exposure Time"): within 1.14.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 10] NUM (113826,DCM,"Nominal Single Collimation Width"): within 1.14.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 11] NUM (113827,DCM,"Nominal Total Collimation Width"): within 1.14.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 12] NUM (113828,DCM,"Pitch Factor"): within 1.14.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing conditional content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 13] NUM (113823,DCM,"Number of X-Ray Sources"): within 1.14.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Error: Template 10013 CTIrradiationEventData/[Row 1] CONTAINER (113819,DCM,"CT Acquisition")/[Row 7] CONTAINER (113822,DCM,"CT Acquisition Parameters")/[Row 14] CONTAINER (113831,DCM,"CT X-Ray Source Parameters"): within 1.14.4: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113819,DCM,"CT Acquisition")/CONTAINER (113822,DCM,"CT Acquisition Parameters"): Missing required content item
# Root Template Validation Complete
# Warning: 1.11.2.1: /CONTAINER (113701,DCM,"X-Ray Radiation Dose Report")/CONTAINER (113811,DCM,"CT Accumulated Dose Data")/NUM (113813,DCM,"CT Dose Length Product Total")/CODE (113835,DCM,"CTDIw Phantom Type"): Content Item not in template
# IOD validation complete



# Example spiral CT Acquisition from a Siemens RDSR:
# ###########################################
# (0040, a010) Relationship Type                   CS: 'CONTAINS'
# (0040, a040) Value Type                          CS: 'CONTAINER'
# (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#    (0008, 0100) Code Value                          SH: '113819'
#    (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#    (0008, 0104) Code Meaning                        LO: 'CT Acquisition'
#    ---------
# (0040, a050) Continuity Of Content               CS: 'SEPARATE'
# (0040, a730)  Content Sequence   9 item(s) ----
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'TEXT'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '125203'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'Acquisition Protocol'
#       ---------
#    (0040, a160) Text Value                          UT: 'TAP'
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'CODE'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '123014'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'Target Region'
#       ---------
#    (0040, a168)  Concept Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: 'T-D4000'
#       (0008, 0102) Coding Scheme Designator            SH: 'SRT'
#       (0008, 0104) Code Meaning                        LO: 'Abdomen'
#       ---------
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'CODE'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '113820'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'CT Acquisition Type'
#       ---------
#    (0040, a168)  Concept Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: 'P5-08001'
#       (0008, 0102) Coding Scheme Designator            SH: 'SRT'
#       (0008, 0104) Code Meaning                        LO: 'Spiral Acquisition'
#       ---------
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'CODE'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: 'G-C32C'
#       (0008, 0102) Coding Scheme Designator            SH: 'SRT'
#       (0008, 0104) Code Meaning                        LO: 'Procedure Context'
#       ---------
#    (0040, a168)  Concept Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: 'P5-00100'
#       (0008, 0102) Coding Scheme Designator            SH: 'SRT'
#       (0008, 0104) Code Meaning                        LO: 'Diagnostic radiography with contrast media'
#       ---------
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'UIDREF'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '113769'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'Irradiation Event UID'
#       ---------
#    (0040, a124) UID                                 UI: 1.3.12.2.1107.5.1.4.73491.30000013051009133670300000019
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'CONTAINER'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '113822'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'CT Acquisition Parameters'
#       ---------
#    (0040, a050) Continuity Of Content               CS: 'SEPARATE'
#    (0040, a730)  Content Sequence   7 item(s) ----
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'NUM'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113824'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Exposure Time'
#          ---------
#       (0040, a300)  Measured Value Sequence   1 item(s) ----
#          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: 's'
#             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#             (0008, 0103) Coding Scheme Version               SH: '1.4'
#             (0008, 0104) Code Meaning                        LO: 's'
#             ---------
#          (0040, a30a) Numeric Value                       DS: '16.01'
#          ---------
#       ---------
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'NUM'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113825'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Scanning Length'
#          ---------
#       (0040, a300)  Measured Value Sequence   1 item(s) ----
#          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: 'mm'
#             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#             (0008, 0103) Coding Scheme Version               SH: '1.4'
#             (0008, 0104) Code Meaning                        LO: 'mm'
#             ---------
#          (0040, a30a) Numeric Value                       DS: '737'
#          ---------
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
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'NUM'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113823'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Number of X-Ray Sources'
#          ---------
#       (0040, a300)  Measured Value Sequence   1 item(s) ----
#          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: '{X-Ray sources}'
#             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#             (0008, 0103) Coding Scheme Version               SH: '1.4'
#             (0008, 0104) Code Meaning                        LO: 'X-Ray sources'
#             ---------
#          (0040, a30a) Numeric Value                       DS: '1'
#          ---------
#       ---------
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'CONTAINER'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113831'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'CT X-Ray Source Parameters'
#          ---------
#       (0040, a050) Continuity Of Content               CS: 'SEPARATE'
#       (0040, a730)  Content Sequence   5 item(s) ----
#          (0040, a010) Relationship Type                   CS: 'CONTAINS'
#          (0040, a040) Value Type                          CS: 'TEXT'
#          (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: '113832'
#             (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#             (0008, 0104) Code Meaning                        LO: 'Identification of the X-Ray Source'
#             ---------
#          (0040, a160) Text Value                          UT: 'A'
#          ---------
#          (0040, a010) Relationship Type                   CS: 'CONTAINS'
#          (0040, a040) Value Type                          CS: 'NUM'
#          (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: '113733'
#             (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#             (0008, 0104) Code Meaning                        LO: 'KVP'
#             ---------
#          (0040, a300)  Measured Value Sequence   1 item(s) ----
#             (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#                (0008, 0100) Code Value                          SH: 'kV'
#                (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#                (0008, 0103) Coding Scheme Version               SH: '1.4'
#                (0008, 0104) Code Meaning                        LO: 'kV'
#                ---------
#             (0040, a30a) Numeric Value                       DS: '120'
#             ---------
#          ---------
#          (0040, a010) Relationship Type                   CS: 'CONTAINS'
#          (0040, a040) Value Type                          CS: 'NUM'
#          (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: '113833'
#             (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#             (0008, 0104) Code Meaning                        LO: 'Maximum X-Ray Tube Current'
#             ---------
#          (0040, a300)  Measured Value Sequence   1 item(s) ----
#             (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#                (0008, 0100) Code Value                          SH: 'mA'
#                (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#                (0008, 0103) Coding Scheme Version               SH: '1.4'
#                (0008, 0104) Code Meaning                        LO: 'mA'
#                ---------
#             (0040, a30a) Numeric Value                       DS: '560'
#             ---------
#          ---------
#          (0040, a010) Relationship Type                   CS: 'CONTAINS'
#          (0040, a040) Value Type                          CS: 'NUM'
#          (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: '113734'
#             (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#             (0008, 0104) Code Meaning                        LO: 'X-Ray Tube Current'
#             ---------
#          (0040, a300)  Measured Value Sequence   1 item(s) ----
#             (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#                (0008, 0100) Code Value                          SH: 'mA'
#                (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#                (0008, 0103) Coding Scheme Version               SH: '1.4'
#                (0008, 0104) Code Meaning                        LO: 'mA'
#                ---------
#             (0040, a30a) Numeric Value                       DS: '176'
#             ---------
#          ---------
#          (0040, a010) Relationship Type                   CS: 'CONTAINS'
#          (0040, a040) Value Type                          CS: 'NUM'
#          (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: '113834'
#             (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#             (0008, 0104) Code Meaning                        LO: 'Exposure Time per Rotation'
#             ---------
#          (0040, a300)  Measured Value Sequence   1 item(s) ----
#             (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#                (0008, 0100) Code Value                          SH: 's'
#                (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#                (0008, 0103) Coding Scheme Version               SH: '1.4'
#                (0008, 0104) Code Meaning                        LO: 's'
#                ---------
#             (0040, a30a) Numeric Value                       DS: '0.5'
#             ---------
#          ---------
#       ---------
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'CONTAINER'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '113829'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'CT Dose'
#       ---------
#    (0040, a050) Continuity Of Content               CS: 'SEPARATE'
#    (0040, a730)  Content Sequence   3 item(s) ----
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'NUM'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113830'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Mean CTDIvol'
#          ---------
#       (0040, a300)  Measured Value Sequence   1 item(s) ----
#          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: 'mGy'
#             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#             (0008, 0103) Coding Scheme Version               SH: '1.4'
#             (0008, 0104) Code Meaning                        LO: 'mGy'
#             ---------
#          (0040, a30a) Numeric Value                       DS: '9.91'
#          ---------
#       ---------
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'CODE'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113835'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'CTDIw Phantom Type'
#          ---------
#       (0040, a168)  Concept Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113691'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'IEC Body Dosimetry Phantom'
#          ---------
#       ---------
#       (0040, a010) Relationship Type                   CS: 'CONTAINS'
#       (0040, a040) Value Type                          CS: 'NUM'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113838'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'DLP'
#          ---------
#       (0040, a300)  Measured Value Sequence   1 item(s) ----
#          (0040, 08ea)  Measurement Units Code Sequence   1 item(s) ----
#             (0008, 0100) Code Value                          SH: 'mGycm'
#             (0008, 0102) Coding Scheme Designator            SH: 'UCUM'
#             (0008, 0103) Coding Scheme Version               SH: '1.4'
#             (0008, 0104) Code Meaning                        LO: 'mGycm'
#             ---------
#          (0040, a30a) Numeric Value                       DS: '708.2'
#          ---------
#       ---------
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'TEXT'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '121106'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'Comment'
#       ---------
#    (0040, a160) Text Value                          UT: 'Internal technical scan parameters: Organ Characteristic = Abdomen, Body Size = Adult, Body Region = Body, X-ray Modulation Type = XYZ_EC'
#    ---------
#    (0040, a010) Relationship Type                   CS: 'CONTAINS'
#    (0040, a040) Value Type                          CS: 'CODE'
#    (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '113876'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'Device Role in Procedure'
#       ---------
#    (0040, a168)  Concept Code Sequence   1 item(s) ----
#       (0008, 0100) Code Value                          SH: '113859'
#       (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#       (0008, 0104) Code Meaning                        LO: 'Irradiating Device'
#       ---------
#    (0040, a730)  Content Sequence   3 item(s) ----
#       (0040, a010) Relationship Type                   CS: 'HAS PROPERTIES'
#       (0040, a040) Value Type                          CS: 'TEXT'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113878'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Device Manufacturer'
#          ---------
#       (0040, a160) Text Value                          UT: 'SIEMENS'
#       ---------
#       (0040, a010) Relationship Type                   CS: 'HAS PROPERTIES'
#       (0040, a040) Value Type                          CS: 'TEXT'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113879'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Device Model Name'
#          ---------
#       (0040, a160) Text Value                          UT: 'SOMATOM Definition Flash'
#       ---------
#       (0040, a010) Relationship Type                   CS: 'HAS PROPERTIES'
#       (0040, a040) Value Type                          CS: 'TEXT'
#       (0040, a043)  Concept Name Code Sequence   1 item(s) ----
#          (0008, 0100) Code Value                          SH: '113880'
#          (0008, 0102) Coding Scheme Designator            SH: 'DCM'
#          (0008, 0104) Code Meaning                        LO: 'Device Serial Number'
#          ---------
#       (0040, a160) Text Value                          UT: '73491'
#       ---------
#    ---------
# ###########################################
