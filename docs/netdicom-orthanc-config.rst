Orthanc Store configuration
===========================

Create Lua file
---------------

Create a file called ``openrem.lua`` *somewhere*, and copy and paste the following content into the file:

..  sourcecode:: lua

    local python_bin_path = ''
    local python_executable = ''
    local temp_path = ''
    local mkdir_cmd = ''
    local dir_sep = ''

    function ToAscii(s)
       -- http://www.lua.org/manual/5.1/manual.html#pdf-string.gsub
       -- https://groups.google.com/d/msg/orthanc-users/qMLgkEmwwPI/6jRpCrlgBwAJ
       return s:gsub('[^a-zA-Z0-9-/-:-\\ ]', '_')
    end

    function ReceivedInstanceFilter(dicom, origin)
        -- Only allow incoming objects we can use
        local mod = dicom.Modality
        if (mod ~= 'SR') and (mod ~= 'CT') and (mod ~= 'MG') and (mod ~= 'CR') and (mod ~= 'DX') then
            return false
        else
            return true
        end
    end

    function OnStoredInstance(instanceId, tags)
        -- Retrieve the DICOM instance from Orthanc
        local dicom = RestApiGet('/instances/' .. instanceId .. '/file')

        -- Work out if file can be used, if not delete from Orthanc?
        local import_script = ''
        if tags['SOPClassUID'] == '1.2.840.10008.5.1.4.1.1.88.67' then
            import_script = 'openrem_rdsr.py'
        elseif tags['SOPClassUID'] == '1.2.840.10008.5.1.4.1.1.88.22' then
            -- Enhanced SR used by GE CT Scanners
            import_script = 'openrem_rdsr.py'
        elseif tags['Modality'] == 'MG' then
            import_script = 'openrem_mg.py'
        elseif (tags['Modality'] == 'CR') or (tags['Modality'] == 'DX') then
            import_script = 'openrem_dx.py'
        elseif (tags['SOPClassUID'] == '1.2.840.10008.5.1.4.1.1.7') and string.match(string.lower(tags['Manufacturer']), 'philips') then
            -- Secondary Capture object that might be Philips CT Dose Info image
            import_script = 'openrem_ctphilips.py'
        elseif (tags['Modality'] == 'CT') and (string.lower(tags['Manufacturer']) == 'toshiba') then
            -- Might be useful Toshiba import, leave it in the database until the study has finished importing
            return true
        else
            Delete(instanceId)
            return true
        end

        -- Write the DICOM content to some temporary file
        local temp_file_path = temp_path .. instanceId .. '.dcm'
        local target = assert(io.open(temp_file_path, 'wb'))
        target:write(dicom)
        target:close()

        -- Call OpenREM import script
        -- Runs as orthanc user in linux, so log files must be writable by orthanc
        os.execute(python_bin_path .. python_executable .. ' ' .. python_bin_path .. import_script .. ' ' .. temp_file_path)

        -- Remove the temporary DICOM file
        os.remove(temp_file_path)

        -- Remove study from Orthanc
        Delete(instanceId)
    end

    function OnStableStudy(studyId, tags, metadata)
        if (tags['Modality'] == 'CT') and (string.lower(tags['Manufacturer']) == 'toshiba') then

            print('This study is now stable, writing its instances on the disk: ' .. studyId)

            local patient = ParseJson(RestApiGet('/studies/' .. studyId .. '/patient')) ['MainDicomTags']
            local study = ParseJson(RestApiGet('/studies/' .. studyId)) ['MainDicomTags']
            local series = ParseJson(RestApiGet('/studies/' .. studyId)) ['Series']

            -- Create a string containing the folder path
            local temp_files_path = ToAscii(temp_path ..
                                  patient['PatientID'] .. dir_sep ..
                                  study['StudyDate'] .. dir_sep .. studyId)
            -- print('path is: ' .. temp_files_path)

            -- Create the folder
            os.execute(mkdir_cmd .. ' "' .. temp_files_path .. '"')
            -- print('Trying to create folder: ' .. mkdir_cmd .. ' "' .. temp_files_path .. '"')

            -- Loop through each series in the study
            for i, each_series in pairs(series) do
                -- Obtain a table of instances in the series
                local instances = ParseJson(RestApiGet('/series/' .. each_series)) ['Instances']

                -- Loop through each instance
                for j, instance in pairs(instances) do
                    -- Retrieve the DICOM file from Orthanc
                    local dicom = RestApiGet('/instances/' .. instance .. '/file')

                    -- Write the DICOM file to the folder created earlier
                    local target = assert(io.open(temp_files_path .. dir_sep .. instance .. '.dcm', 'wb'))
                    -- print('Trying to write file: ' .. temp_files_path .. dir_sep .. instance .. '.dcm')
                    target:write(dicom)
                    target:close()

                    -- Remove the instance from Orthanc
                    Delete(instance)
                end
            end

            -- Run the Toshiba extractor on the folder
            os.execute(python_bin_path .. python_executable.. ' ' .. python_bin_path .. 'openrem_cttoshiba.py' .. ' ' .. temp_files_path)

        end
    end

Customise Lua file
-------------------

Five variables need to be set in the Lua file:

**local python_bin_path = ''**

This should be set to the full path to where the Python executables are, including ``openrem_rdsr.py`` and python
itself. This might be similar one of the following examples and needs to include the final slash. On Windows, each
slash needs to be a double slash:

* Linux, not using virtualenv: ``local python_bin_path = '/usr/bin/'``
* Linux, using virtualenv: ``local python_bin_path = '/home/username/veopenrem/bin/'``
* Windows, not using virtualenv: ``local python_bin_path = 'C:\\Python27\\'``
* Windows, using virtualenv: ``local python_bin_path = 'C:\\path\\to\\virtualenv\\Scripts\\'``

**local python_executable = ''**

This needs to be the name of the Python executable:

* Linux: ``local python_executable = 'python'``
* Windows: ``local python_executable = 'python.exe'``

**local temp_path = ''**

This needs to be a folder where Orthanc can write files temporarily while they are imported by OpenREM. **The folder
should exist**:

* Linux: ``local temp_path = '/tmp/orthanc/'``
* Windows: ``local temp_path = 'C:\\Temp\\orthanc\\'``

*Remember to create the folder*

**local mkdir_cmd = ''**

This needs to be the command used to create a folder path on your system:

* Linux ``local mkdir_cmd = 'mkdir -p'``
* Windows ``local mkdir_cmd = 'mkdir'``

**local dir_sep = ''**

Finally, the directory separator used on your system:

* Linux ``local dir_sep = '/'``
* Windows ``local dir_sep = '\\'``

Configure Orthanc to make use of the openrem.lua file
-----------------------------------------------------

Edit ``orthanc.json`` which can be found in:

* Ubuntu linux: ``/etc/orthanc/``
* Windows: ``C:\Program Files\Orthanc Server\Configuration\``

Find and edit the section below:

Linux:

..  sourcecode:: json

    // List of paths to the custom Lua scripts that are to be loaded
    // into this instance of Orthanc
    "LuaScripts" : [
    "/path/to/openrem.lua"
    ],

Windows (note the double back-slash):

..  sourcecode:: json

    // List of paths to the custom Lua scripts that are to be loaded
    // into this instance of Orthanc
    "LuaScripts" : [
    "C:\\path\\to\\openrem.lua"
    ],

Check permissions
-----------------

**Stub**

* Linux: orthanc user needs to be able to write to the OpenREM logs
* Linux: orthanc user needs to be able to write to the temp directory we specified

Restart Orthanc
---------------

Ubuntu linux::

    sudo service orthanc force-reload

Windows::

    ?