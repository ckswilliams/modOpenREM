local python_executable_path = 'D:\\Server_Apps\\python27\\'
local python_executable = 'python.exe'
local python_scripts_path = 'D:\\Server_Apps\\python27\\Scripts\\'
local temp_path = 'E:\\conquest\\dicom\\'
local mkdir_cmd = 'mkdir'
local dir_sep = '\\'
local physics_to_keep_folder = 'E:\\conquest\\dicom\\physics\\'

-- A list to check against patient name and ID to see if the images should be kept
local physics_to_keep = {'physics'}

-- A list of CT make / models to use the Toshiba CT extractor routine on
local toshiba_extractor_systems = {
        {'ge medical systems', 'discovery 710'},
        {'ge medical systems', 'discovery ste'},
        {'ge medical systems', 'brightspeed'},
        {'ge medical systems', 'lightspeed plus'},
        {'ge medical systems', 'lightspeed16'},
        {'ge medical systems', 'lightspeed pro 32'},
        {'ge medical systems', 'lightspeed vct'},
        {'siemens', 'biograph64'},
        {'siemens', 'somatom definition'},
        {'siemens', 'somatom definition edge'},
        {'siemens', 'somatom definition flash'},
        {'siemens', 'somatom force'},
        {'toshiba', 'aquilion'},
        {'toshiba', 'aquilion prime'},
        {'toshiba', 'aquilion one'}
}

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


    -- See if the images are physics tests
    for i = 1, #physics_to_keep do
        if string.match(tags['PatientName'], physics_to_keep[i]) or string.match(tags['PatientID'], physics_to_keep[i]) then
            -- It is a physics image - keep it
            return true
        end
    end


    -- Work out if file can be used by the RDSR, MG, DX or ctphilips extractors
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
    end


    -- Work out if the Toshiba CT extractor should be used - must be CT and a match with a make/model pair in toshiba_extractor_systems
    local use_toshiba_extractor = 0
    for i = 1, #toshiba_extractor_systems do
        if (tags['Modality'] == 'CT') and (string.lower(tags['Manufacturer']) == toshiba_extractor_systems[i][1]) and (string.lower(tags['ManufacturerModelName']) == toshiba_extractor_systems[i][2]) then
            -- Might be useful Toshiba import, leave it in the database until the study has finished importing
            use_toshiba_extractor = 1
            return true
        end
    end


    -- If we're not using the Toshiba CT extractor and import_script is empty then delete the instance
    if (use_toshiba_extractor == 0) and (import_script == '') then
        Delete(instanceId)
        return true
    end


    -- Write the DICOM content to a temporary file
    local temp_file_path = temp_path .. instanceId .. '.dcm'
    local target = assert(io.open(temp_file_path, 'wb'))
    target:write(dicom)
    target:close()

    -- Call OpenREM import script. Runs as orthanc user in linux, so log files must be writable by Orthanc
    os.execute(python_executable_path .. python_executable .. ' ' .. python_scripts_path .. import_script .. ' ' .. temp_file_path)

    -- Remove the temporary DICOM file
    os.remove(temp_file_path)

    -- Remove study from Orthanc
    Delete(instanceId)
end

function OnStableStudy(studyId, tags, metadata)
    -- print('This study is now stable, writing its instances on the disk: ' .. studyId)

    local patient = ParseJson(RestApiGet('/studies/' .. studyId .. '/patient')) ['MainDicomTags']
    local study = ParseJson(RestApiGet('/studies/' .. studyId)) ['MainDicomTags']
    local series = ParseJson(RestApiGet('/studies/' .. studyId)) ['Series']


    -- See if any of the physics strings are in patient name or ID
    local first_series = 1
    local temp_files_path = ''
    for i = 1, #physics_to_keep do
        if string.match(patient['PatientName'], physics_to_keep[i]) or string.match(patient['PatientID'], physics_to_keep[i]) then
            -- It is a physics patient - save them to the physics folder
            for i, current_series in pairs(series) do

                if first_series == 1 then
                    -- Create a string containing the folder path.
                    temp_files_path = ToAscii(physics_to_keep_folder .. study['StudyDate'] .. dir_sep .. patient['PatientNameID'])
                    -- print('temp_files_path is: ' .. temp_files_path)

                    -- Create the folder
                    os.execute(mkdir_cmd .. ' "' .. temp_files_path .. '"')
                    -- print('Just tried to create folder: ' .. mkdir_cmd .. ' "' .. temp_files_path .. '"')

                    first_series = 0
                end

                local instances = ParseJson(RestApiGet('/series/' .. current_series)) ['Instances']

                -- Loop through each instance in the current_series
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
        end
    end

    if first_series == 0 then
        -- Exit the function, as a physics study was found above
        return true
    end


    -- No physics study was found, so we must need to use the CT Toshiba extractor
    first_series = 1
    temp_files_path = ''

    for i, current_series in pairs(series) do
        local series_modality = ParseJson(RestApiGet('/series/' .. current_series)) ['MainDicomTags']['Modality']
        local series_manufacturer = ParseJson(RestApiGet('/series/' .. current_series)) ['MainDicomTags']['Manufacturer']
        -- print('Modality and manufacturer of series are: ' .. series_modality .. '; ' .. series_manufacturer)

        if first_series == 1 then
            -- Create a string containing the folder path. This needs to be a single folder so that the Toshiba CT extractor
            -- is able to remove it once the data has been imported into OpenREM.
            temp_files_path = ToAscii(temp_path .. study['StudyDate'] .. '_' .. patient['PatientID'] .. '_' .. studyId)
            -- print('temp_files_path is: ' .. temp_files_path)

            -- Create the folder
            os.execute(mkdir_cmd .. ' "' .. temp_files_path .. '"')
            -- print('Just tried to create folder: ' .. mkdir_cmd .. ' "' .. temp_files_path .. '"')

            first_series = 0
        end

        -- Obtain a table of instances in the series
        local instances = ParseJson(RestApiGet('/series/' .. current_series)) ['Instances']

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

    -- Run the Toshiba extractor on the folder. The extractor will remove the temp_files_path folder.
    -- print('Trying to run: ' .. python_executable_path .. python_executable.. ' ' .. python_scripts_path .. 'openrem_cttoshiba.py' .. ' ' .. temp_files_path)
    os.execute(python_executable_path .. python_executable.. ' ' .. python_scripts_path .. 'openrem_cttoshiba.py' .. ' ' .. temp_files_path)

end