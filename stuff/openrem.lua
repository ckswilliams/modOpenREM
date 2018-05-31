local python_executable_path = 'D:\\Server_Apps\\python27\\'
local python_executable = 'python.exe'
local python_scripts_path = 'D:\\Server_Apps\\python27\\Scripts\\'
local temp_path = 'E:\\conquest\\dicom\\'
local mkdir_cmd = 'mkdir'
local dir_sep = '\\'

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
    os.execute(python_executable_path .. python_executable .. ' ' .. python_scripts_path .. import_script .. ' ' .. temp_file_path)

    -- Remove the temporary DICOM file
    os.remove(temp_file_path)

    -- Remove study from Orthanc
    Delete(instanceId)
end

function OnStableStudy(studyId, tags, metadata)
    print('This study is now stable, writing its instances on the disk: ' .. studyId)

    local patient = ParseJson(RestApiGet('/studies/' .. studyId .. '/patient')) ['MainDicomTags']
    local study = ParseJson(RestApiGet('/studies/' .. studyId)) ['MainDicomTags']
    local series = ParseJson(RestApiGet('/studies/' .. studyId)) ['Series']

    local first_series = 1

    local temp_files_path = ''
    
    for i, current_series in pairs(series) do
        print('Modality of series is: '     .. ParseJson(RestApiGet('/series/' .. current_series)) ['MainDicomTags']['Modality'])
        print('Manufacturer of series is: ' .. ParseJson(RestApiGet('/series/' .. current_series)) ['MainDicomTags']['Manufacturer'])
        local series_modality = ParseJson(RestApiGet('/series/' .. current_series)) ['MainDicomTags']['Modality']
        local series_manufacturer = ParseJson(RestApiGet('/series/' .. current_series)) ['MainDicomTags']['Manufacturer']

        if (series_modality == 'CT') and (string.lower(series_manufacturer) == 'toshiba') then
            if first_series == 1 then
                -- Create a string containing the folder path
                temp_files_path = ToAscii(temp_path ..
                                    patient['PatientID'] .. dir_sep ..
                                    study['StudyDate'] .. dir_sep .. studyId)
                print('path is: ' .. temp_files_path)

                -- Create the folder
                os.execute(mkdir_cmd .. ' "' .. temp_files_path .. '"')
                print('Trying to create folder: ' .. mkdir_cmd .. ' "' .. temp_files_path .. '"')
                
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
                print('Trying to write file: ' .. temp_files_path .. dir_sep .. instance .. '.dcm')
                target:write(dicom)
                target:close()

                -- Remove the instance from Orthanc
                Delete(instance)
            end
        else
            -- The series is not CT and Toshiba, so delete it from Orthanc
            Delete(current_series)
        end
    end

    print('first_series is: ' .. first_series)
    if first_series == 0 then
        -- Run the Toshiba extractor on the folder because at least one series is CT and toshiba
        print('Trying to run: ' .. python_executable_path .. python_executable.. ' ' .. python_scripts_path .. 'openrem_cttoshiba.py' .. ' ' .. temp_files_path)
        os.execute(python_executable_path .. python_executable.. ' ' .. python_scripts_path .. 'openrem_cttoshiba.py' .. ' ' .. temp_files_path)
    end
    
end