local python_path = 'D:\\David\\Documents\\Code\\Python\\OpenREM\\testbed\\openrem_develop\\Scripts\\python.exe'
local openrem_exe_path = 'D:\\David\\Documents\\Code\\Python\\OpenREM\\testbed\\openrem_develop\\Scripts\\'
local temp_path = 'D:\\David\\Temp\\'
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
    local path = temp_path .. instanceId .. '.dcm'
    local target = assert(io.open(path, 'wb'))
    target:write(dicom)
    target:close()

    -- Call OpenREM import script
    -- Runs as orthanc user in linux, so log files must be writable by orthanc
    os.execute(python_path .. ' ' .. openrem_exe_path .. import_script .. ' ' .. path)

    -- Remove the temporary DICOM file
    os.remove(path)

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
        local path = ToAscii(temp_path ..
                              patient['PatientID'] .. dir_sep ..
                              study['StudyDate'] .. dir_sep .. studyId)
        -- print('path is: ' .. path)

        -- Create the folder
        os.execute(mkdir_cmd .. ' "' .. path .. '"')
        -- print('Trying to create folder: ' .. mkdir_cmd .. ' "' .. path .. '"')

        -- Loop through each series in the study
        for i, each_series in pairs(series) do
            -- Obtain a table of instances in the series
            local instances = ParseJson(RestApiGet('/series/' .. each_series)) ['Instances']

            -- Loop through each instance
            for j, instance in pairs(instances) do
                -- Retrieve the DICOM file from Orthanc
                local dicom = RestApiGet('/instances/' .. instance .. '/file')

                -- Write the DICOM file to the folder created earlier
                local target = assert(io.open(path .. dir_sep .. instance .. '.dcm', 'wb'))
                -- print('Trying to write file: ' .. path .. dir_sep .. instance .. '.dcm')
                target:write(dicom)
                target:close()

                -- Remove the instance from Orthanc
                Delete(instance)
            end
        end

        -- Run the Toshiba extractor on the folder
        os.execute(python_path .. ' ' .. openrem_exe_path .. 'openrem_cttoshiba.py' .. ' ' .. path)

    end
end