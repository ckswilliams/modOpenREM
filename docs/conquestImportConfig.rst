Advanced Lua Conquest configuration (Windows)
*********************************************

*Drop/merge the non lua section of this document*

Configuring Conquest DICOM server to automatically forward data to OpenREM

Simple rules using the Conquest dicom.ini file
++++++++++++++++++++++++++++++++++++++++++++++

The Conquest DICOM server can be configured to automatically run tasks when it receives specific types of DICOM object.
For example, a script can be run when a DX image is received that will extract dose information into OpenREM; Conquest
will then delete the original image.

These actions are set up in the ``dicom.ini`` file, located in the root of the Conquest installation folder (an example
``dicom.ini`` file is available here: :doc:`conquestExampleDicomIni`).

An example import converter::

    ImportModality1   = MG
    ImportConverter1  = save to C:\conquest\dosedata\mammo\%o.dcm; system C:\conquest\openrem-mam-launch.bat C:\conquest\dosedata\mammo\%o.dcm; destroy

``ImportModality1 = MG`` tells Conquest that modality 1 is MG. The commands listed in the ``ImportConverter1`` line are
then run on all incoming MG images.

The ``ImportConverter`` instructions are separated by semicolons; the above example has three commands:

+ ``save to C:\conquest\dosedata\mammo\%o.dcm`` saves the incoming MG image to the specified folder with a file name set to the SOP instance UID contained in the image
+ ``system C:\conquest\openrem-mam-launch.bat C:\conquest\dosedata\mammo\%o.dcm`` runs a DOS batch file, using the newly saved file as the argument. On my system this batch file runs the OpenREM ``openrem_mg.py`` import script
+ ``destroy`` tells Conquest to delete the image that it has just received.

My system had three further import sections for DX, CR, and structured dose report DICOM objects::

    # Import of DX images
    ImportModality2   = DX
    ImportConverter2  = save to C:\conquest\dosedata\dx\%o.dcm; system C:\conquest\openrem-dx-launch.bat C:\conquest\dosedata\dx\%o.dcm; destroy

    # Import of CR images
    ImportModality3   = CR
    ImportConverter3  = save to C:\conquest\dosedata\dx\%o.dcm; system C:\conquest\openrem-dx-launch.bat C:\conquest\dosedata\dx\%o.dcm; destroy

    # Import of structured dose reports (this checks the DICOM tag 0008,0016 to see if it matches the value for a dose report)
    ImportConverter4  = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.67"; {save to C:\conquest\dosedata\sr\%o.dcm; system C:\conquest\openrem-sr-launch.bat "C:\conquest\dosedata\sr\%o.dcm"; destroy}

However, I have since moved to calling lua scripts from Conquest, as described in the next section.

Advanced Conquest DICOM object handling using lua scripts
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Conquest can be configured to use lua scripts to handle incoming DICOM objects. This enables more flexibility than the
examples provided in the section above. For example, you may wish to keep all incoming images that contain the word
``physics`` in the patient name or id fields. You may also wish to direct images from different makes and models of
CT scanner to different OpenREM import scripts. I use this technique to forward studies from some Toshiba Aquilion CX
and CXL scanners to an importer that creates a DICOM RDSR object from the Toshiba dose summary images and information
stored in the image tags. These particular scanners are not capable of producing their own RDSR objects directly. I use
the same script to delete images from CT scanners that I cannot extract data from.

A lua script designed to handle any objects with modality ``CT`` can be called from ``dicom.ini`` in the following way::

    ImportConverter6 = ifequal "%m", "CT"; { process patient after 0 by openrem_import_ct.lua %p::%V0008,0070::%V0008,1090::%V0018,1020::%V0008,1010::%V0010,0010::%V0010,0020::%V0008,0020::%V0018,1000; }

The above line will run a script called ``openrem_import_ct.lua`` once the complete patient data has been received by
Conquest and a delay of 10 minutes has elapsed (the default). The following information is passed on to the script:

    * ``%p``, the path to a folder of DICOM objects

    * ``%V0008,0070``, manufacturer

    * ``%V0008,1090``, model

    * ``%V0018,1020``, software version

    * ``%V0008,1010``, station name

    * ``%V0010,0010``, patient name

    * ``%V0010,0020``, patient id

    * ``%V0008,0020``, study date

    * ``%V0018,1000``, device serial number

An example ``openrem_import_ct.lua`` script is shown below. It receives the parameters passed to it as single string.
The individual parameters are recovered by splitting up the string using the ``::`` substring as a delimiter. The script
keeps any images that contain ``physics`` in the patient name or id fields; it looks for any Philips dose info objects
and imports these with the appropriate routine; it deletes images from scanners that cannot be used; it runs the Toshiba
RDSR creation importer on images from older Toshiba CT scanners:

.. sourcecode:: lua

    require "openrem_string_split"

    -- It is assumed that 'openrem_rdsr.py' and 'openrem_ctphilips.py' are in the Python scripts folder, and that this
    -- and the Python executable location are included in the system path.

    -- It is assumed that this code has been called from an ImportConverter within a Conquest dicom.ini file, and passed
    -- the following:
    --    path to a folder of DICOM objects
    --    the manufacturer (0008,0070)
    --    model (0008,1090)
    --    software version (0018,1020)
    --    station name (0008,1010)
    --    patient name (0010,0010)
    --    patient id (0010,0020)
    --    study date (0008,0020)
    --    device serial number (0018,1000)

    local physics_to_keep = {'physics'}
    local physics_folder = 'E:\\conquest\\dicom\\physics_images\\'

    local split_input_text = split(command_line, '::')
    local study_folder_path = split_input_text[1]
    local manufacturer = split_input_text[2]
    local model_name = split_input_text[3]
    local software_version = split_input_text[4]
    local station_name = split_input_text[5]

    local patient_name, patient_id, study_date, device_serial_number

    if split_input_text[6] == nil then
      patient_name = ''
    else
      patient_name = string.lower(split_input_text[6])
    end

    if split_input_text[7] == nil then
      patient_id = ''
    else
      patient_id = string.lower(split_input_text[7])
    end

    if split_input_text[8] == nil then
      study_date = 'blank'
    else
      study_date = split_input_text[8]
    end

    if split_input_text[9] == nil then
      device_serial_number = 'blank'
    else
      device_serial_number = split_input_text[9]
    end

    print(study_folder_path)

    -- If any of the entries in physics_to_keep are present in the patient name or ID then the image is assumed to be a
    -- physics test, and is kept.
    for i = 1, #physics_to_keep do
      if string.match(patient_name, physics_to_keep[i]) or string.match(patient_id, physics_to_keep[i]) then
        print('Keeping the image: patient name is ' .. patient_name)
        print('and patient ID is ' .. patient_id)
        print('Trying to create folder ' .. physics_folder .. '\\' .. study_date)
        system('c:\\Windows\\system32\\cmd.exe /C mkdir ' .. physics_folder .. '\\' .. study_date)
        print('Trying to copy to the following folder: ' .. study_folder_path .. ' ' .. physics_folder .. '\\' .. study_date .. '\\')
        system('c:\\Windows\\system32\\cmd.exe /C copy ' .. study_folder_path .. '\\*.* ' .. physics_folder .. '\\' .. study_date .. '\\')
        return
      end
    end

    if (manufacturer == 'Philips' and model_name == 'Brilliance 64') then
      print('It is a Philips Brilliance 64')
      -- Look for a dose summary image and import it
      local files = assert(io.popen('dir /b ' .. study_folder_path))
      local output = files:read('*all')
      local file_list = split(output, '\n')

      for k, v in pairs(file_list) do
        current_file = study_folder_path .. '\\' .. v -- The fully qualified file name and path (Windows-specific)
        readdicom(current_file)
        if Data.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7' then
          system('D:\\Server_Apps\\python27\\python.exe d:\\Server_Apps\\python27\\Scripts\\openrem_ctphilips.py ' .. current_file)
          print('The system command to import a Philips CT dose image has been executed on: ' .. current_file)
        end
      end

      -- Delete the study from disk
      print('Complete. Deleting study images.')
      system('C:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
      return
    end

    -- Check for images from a Toshiba CT simulator - images are of no use - need RDSR
    if (manufacturer == 'TOSHIBA' and station_name == 'AQ16LB_SCAN') then
      print('It is a Toshiba Aquilion LB study. Cannot make use of these images - deleting them.')
      system('C:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
      print('The system command has been executed to delete the images from the server')
      return
    end

    -- Toshiba Aquilion CX and CXL scanners - try and create an RDSR from the data
    if (manufacturer == 'TOSHIBA' and model_name == 'Aquilion') then
      print('It is a Toshiba Aquilion. Running openrem_rdsr_toshiba_ct_from_dose_images.py script: ' .. study_folder_path)
      system('d:\\Server_Apps\\python27\\python.exe d:\\Server_Apps\\python27\\Scripts\\openrem_rdsr_toshiba_ct_from_dose_images.py ' .. study_folder_path)
      print('The system command has been executed to create the rdsr and import it: ' .. study_folder_path)
      -- The openrem_rdsr_toshiba_ct_from_dose_images.py routine deletes the study from disk once the
      -- RDSR has been produced and imported in to OpenREM.
      return
    end

    -- Old Toshiba Asteion
    if (manufacturer == 'TOSHIBA' and model_name == 'Asteion') then
      print('It is a Toshiba Asteion. Cannot make use of these images - deleting them: ' .. study_folder_path)
      system('C:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
      print('The system command has been executed to delete the images from the server')
      return
    end

    -- Old Picker PQS
    if (manufacturer == 'Picker International, Inc.' and model_name == 'PQS') then
      print('It is a Picker PQS. Cannot make use of these images - deleting them: ' .. study_folder_path)
      system('C:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
      print('The system command has been executed to delete the images from the server')
      return
    end

    -- Image from a Vitrea workstation
    if (manufacturer == 'Vital Images, Inc' and model_name == 'Vitrea 2') then
      print('It is a Vitrea 2. Cannot make use of these images - deleting them: ' .. study_folder_path)
      system('C:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
      print('The system command has been executed to delete the images from the server')
      return
    end


The above script depends on ``openrem_string_split``:

.. sourcecode:: lua

    function split(str, pat)
       local t = {}  -- NOTE: use {n = 0} in Lua-5.0
       local fpat = "(.-)" .. pat
       local last_end = 1
       local s, e, cap = str:find(fpat, 1)
       while s do
          if s ~= 1 or cap ~= "" then
         table.insert(t,cap)
          end
          last_end = e+1
          s, e, cap = str:find(fpat, last_end)
       end
       if last_end <= #str then
          cap = str:sub(last_end)
          table.insert(t, cap)
       end
       return t
    end

Preventing Conquest from adding incoming DICOM objects to the Conquest database
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You may wish to prevent Conquest from adding patient data from incoming DICOM objects to the Conquest database, such as
patient names and IDs. To do this set the SQLServer to a blank in the Conquest ``dicom.ini`` file::

    # Host, database, username and password for database
    SQLHost = localhost
    # The SQLServer is blank below to prevent the incoming objects from being added to the Conquest database.
    SQLServer =

Setting the compression for Conquest incoming DICOM images and archives
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Setting the following options to ``ul`` within ``dicom.ini`` will make Conquest store DICOM objects using little endian
explicit encoding::

    # Configuration of compression for incoming images and archival
    DroppedFileCompression   = ul
    IncomingCompression      = ul
    ArchiveCompression       = ul

For my system the ``ul`` above matches the compression that is set for Conquest's known DICOM providers in the file
``acrnema.map``, such as the Trust PACS and imaging modalities that have been set up to send data directly to Conquest.