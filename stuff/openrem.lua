local python_path = '/home/mcdonaghe/research/veOpenREM/bin/python'
local openrem_exe_path = '/home/mcdonaghe/research/veOpenREM/bin/'

function OnStoredInstance(instanceId, tags)
    -- Retrieve the DICOM instance from Orthanc
    local dicom = RestApiGet('/instances/' .. instanceId .. '/file')

    -- Work out if file can be used, if not delete from Orthanc?

    -- assume at this point we have RDSR
    local import_script = 'openrem_rdsr.py'

    -- Write the DICOM content to some temporary file
    local path = instanceId .. '.dcm'
    local target = assert(io.open('/tmp/' .. path, 'wb'))
    target:write(dicom)
    target:close()

    -- Call OpenREM import script
    -- Runs as orthanc user in linux, so log files must be writable by orthanc
    os.execute(python_path .. ' ' .. openrem_exe_path .. import_script .. ' ' .. '/tmp/' .. path)

    -- Remove the temporary DICOM file
    os.remove('/tmp/' .. path)

    -- Remove study from Orthanc
    Delete(instanceId)

end