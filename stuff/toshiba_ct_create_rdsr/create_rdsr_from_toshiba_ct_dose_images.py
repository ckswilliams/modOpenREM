#!D:\Server_Apps\python27\python.exe
# scripts/create_rdsr_from_toshiba_ct_dose_images

import sys
import os
from glob import glob
from openrem.remapp.extractors import rdsr

dcmtk_path = 'C:\\Users\\David\\Apps\\dcmtk-3.6.0-win32-i386\\bin'
dcmconv = os.path.join(dcmtk_path, 'dcmconv.exe')
dcmmkdir = os.path.join(dcmtk_path, 'dcmmkdir.exe')
java_exe = 'C:\\Users\\David\\Apps\\doseUtility\\windows\\jre\\bin\\java.exe'
java_options = '-Xms256m -Xmx512m -Xss1m -cp'
pixelmed_jar = 'C:\\Users\\David\\Apps\\doseUtility\\pixelmed.jar'
pixelmed_jar_options = '-Djava.awt.headless=true com.pixelmed.doseocr.OCR -'


def split_by_studyinstanceuid(dicom_path):
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


def find_extra_info(dicom_path):
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
        DeviceSerialNumber
        StudyDescription
        RequestedProcedureDescription
        DLP

    """
    import dicom

    from dicom.filereader import InvalidDicomError

    acquisition_info = []
    acquisitions_collected = []
    study_info = {}

    for filename in os.listdir(dicom_path):
        if os.path.isfile(os.path.join(dicom_path, filename)):
            try:
                dcm = dicom.read_file(os.path.join(dicom_path, filename))

                try:
                    # Only look at the tags if this AcquisitionNumber is new
                    if dcm.AcquisitionNumber not in acquisitions_collected:
                        acquisitions_collected.append(dcm.AcquisitionNumber)

                        info_dictionary = {}
                        try:
                            info_dictionary['AcquisitionNumber'] = dcm.AcquisitionNumber
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['ProtocolName'] = dcm.ProtocolName
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['ExposureTime'] = dcm.ExposureTime
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['KVP'] = dcm.KVP
                        except AttributeError:
                            pass
                        try:
                            info_dictionary['SpiralPitchFactor'] = dcm.SpiralPitchFactor
                        except AttributeError:
                            try:
                                # For some Toshiba CT scanners
                                info_dictionary['SpiralPitchFactor'] = dcm[0x7005, 1023].value
                            except KeyError:
                                pass
                        try:
                            info_dictionary['CTDIvol'] = dcm.CTDIvol
                        except AttributeError:
                            try:
                                # For some Toshiba CT scanners
                                info_dictionary['CTDIvol'] = dcm[0x7005, 0x1063].value
                            except KeyError:
                                pass
                        try:
                            info_dictionary['ExposureModulationType'] = dcm.ExposureModulationType
                        except AttributeError:
                            pass
                        try:
                            # For some Toshiba CT scanners
                            info_dictionary['DLP'] = dcm[0x7005, 0x1040].value
                        except KeyError:
                            pass

                        acquisition_info.append(info_dictionary)

                    # Update the study-level information, whether this acquisition # has been seen yet or not
                    try:
                        print dcm.StudyDescription
                        if dcm.StudyDescription != '':
                            try:
                                if study_info['StudyDescription'] == '':
                                    # Only update study_info['StudyDescription'] if it's empty
                                    study_info['StudyDescription'] = dcm.StudyDescription
                            except KeyError:
                                # study_info['StudyDescription'] doesn't exist yet, so create it
                                study_info['StudyDescription'] = dcm.StudyDescription
                    except AttributeError:
                        # dcm.StudyDescription isn't present
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
                        # dcm.RequestedProcedureDescription isn't present
                        pass

                except AttributeError:
                    pass

            except InvalidDicomError:
                pass

    return [study_info, acquisition_info]


def make_explicit_vr_little_endian(folder_list, dcmconv_exe):
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


def make_dicomdir(folder_list, dcmmkdir_exe):
    """Parse folders of files, making a DICOMDIR for each using the DICOM toolkit dcmmkdir.exe command. See
    http://support.dcmtk.org/docs/dcmmkdir.html for documentation.

    Args:
        folder_list (list): A list of full paths containing DICOM objects.
        dcmmkdir_exe (str): A string containing the dcmmkdir command

    """
    import subprocess

    for current_folder in folder_list:
        command = dcmmkdir_exe + ' --recurse --output-file ' + \
                  os.path.join(current_folder, 'DICOMDIR') + ' --input-directory ' + current_folder
        subprocess.call(command.split())


def make_dicom_rdsr(folder_list, pixelmed_jar_command, sr_filename):
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


def update_dicom_rdsr(rdsr_file, additional_study_info, additional_acquisition_info):
    """Try to update information in an RDSR file using pydicom. Match the pair of CTDIvol and DLP values found in the
    RDSR CT Acquisition with a pair of CTDIvol and DLP values in additional_info. If a match is found, use the other
    information in the additional_info element to update the corresponding CT Acquisition in the RDSR.

    Args:
        rdsr_file (str): A fully qualified RDSR filename.
        additional_study_info (list): A list of dictionaries containing information on the CT study.
        additional_acquisition_info (list): A list of dictionaries containing information on each acquisition in the CT
        study.

    """
    import dicom
    from dicom.dataset import Dataset
    from dicom.sequence import Sequence

    try:
        dcm = dicom.read_file(rdsr_file)
    except IOError as e:
        print 'I/O error({0}): {1} when trying to read {2}'.format(e.errno, e.strerror, rdsr_file)
        return

    # Update the study-level information if it does not exist, or is an empty string.
    for key, val in additional_study_info.items():
        try:
            rdsr_val = getattr(dcm, key)
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
                                    # print str(acquisition['CTDIvol']) + ', ' + str(current_ctdi_vol) + '; ' + \
                                    #      str(acquisition['DLP']) + ', ' + str(current_dlp)
                                    # NB. the if statement below is a bit iffy, as I think there may be an issue
                                    # with comparing floats, but it does appear to work...
                                    if float(acquisition['CTDIvol']) == float(current_ctdi_vol) and \
                                                    float(acquisition['DLP']) == float(current_dlp):
                                        # There's a match between CTDIvol and DLP, so see if things can be updated or
                                        # added.
                                        # print 'There is a match'
                                        # print str(acquisition['CTDIvol']) + ', ' + str(current_ctdi_vol) + '; ' + \
                                        #      str(acquisition['DLP']) + ', ' + str(current_dlp)
                                        for key, val in acquisition.items():
                                            if key != 'CTDIvol' and key != 'DLP':
                                                # print key + ' -> ' + str(val)
                                                ##############################################
                                                # Code here to add / update the data...
                                                coding = Dataset()
                                                coding2 = Dataset()
                                                # DJP note: need to know or look up the three things below for each item
                                                # that needs to be added.
                                                if key == 'ProtocolName':
                                                    # First, check if there is already a ProtocolName container that has
                                                    # a protocol in it.
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

                                                # The end of updating the RDSR
                                                ##############################################
                                except KeyError:
                                    # Either CTDIvol or DLP data is not present
                                    pass
    dcm.save_as(rdsr_file + '_updated.dcm')
    return rdsr_file + '_updated.dcm'


if len(sys.argv) < 2:
    sys.exit('Error: supply at least one argument - the folder containing the DICOM objects')

for arg in sys.argv[1:]:
    rdsr_name = 'sr.dcm'
    for folder_name in glob(arg):
        # Split the folder of images by StudyInstanceUID. This is required because pixelmed.jar will only process the
        # first dose summary image it finds. Splitting the files by StudyInstanceUID should mean that there is only one
        # dose summary per folder. N.B. I think Conquest may do this by default with incoming DICOM objects. This
        # routine also renames the files using integer file names to ensure that they are accepted by dcmmkdir later on.
        print 'Splitting into folders by StudyInstanceUID'
        folders = split_by_studyinstanceuid(folder_name)

        # Make all the DICOM objects explicit VR little endian. This is required by dcmmkdir.
        print 'Making explicit VR little endian'
        make_explicit_vr_little_endian(folders, dcmconv)

        # Now create a DICOMDIR for each sub-folder using dcmmkdir.
        # This is required by pixelmed.jar when creating RDSRs.
        print 'Creating DICOMDIR files'
        make_dicomdir(folders, dcmmkdir)

        # Now create a DICOM RDSR for each sub-folder using pixelmed.jar.
        print 'Making initial DICOM RDSR objects'
        combined_command = java_exe + ' ' + java_options + ' ' + pixelmed_jar + ' ' + pixelmed_jar_options
        make_dicom_rdsr(folders, combined_command, rdsr_name)

        # Obtain additional information from the image tags in each folder and add this information to the RDSR file.
        for folder in folders:
            print 'Gathering extra information from images in ' + folder
            extra_information = find_extra_info(folder)
            extra_study_information = extra_information[0]
            extra_acquisition_information = extra_information[1]

            # Use the extra information to update the initial rdsr file created by DoseUtility
            print 'Updating information in rdsr in ' + folder
            updated_rdsr_file = update_dicom_rdsr(os.path.join(folder, rdsr_name), extra_study_information,
                                                  extra_acquisition_information)

            # Now import the updated rdsr into OpenREM using the Toshiba extractor
            print 'Importing updated rdsr in to OpenREM (' + updated_rdsr_file + ')'
            rdsr(updated_rdsr_file)

            # Now delete all the files and folders that have been created
            # ...

sys.exit()

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
