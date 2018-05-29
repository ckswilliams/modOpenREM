local python_path = '/home/mcdonaghe/research/veOpenREM/bin/python'
local openrem_exe_path = '/home/mcdonaghe/research/veOpenREM/bin/'
local temp_path = '/tmp/'

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
    elseif tags['SOPClassUID'] == '1.2.840.10008.5.1.4.1.1.7' then
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
        -- need to make a directory, which might be platform specific
        -- then save the files  to that directory
        -- and pass directory to function.
end