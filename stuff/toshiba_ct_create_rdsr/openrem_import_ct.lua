require "openrem_string_split"

-- It is assumed that 'openrem_rdsr.py' and 'openrem_ctphilips.py' are in the
-- Python scripts folder, and that this and the Python executable location are
-- included in the system path.

-- It is assumed that this code has been called from an ImportConverter within
-- a Conquest dicom.ini file, and passed the path of a folder of DICOM objects,
-- the manufacturer (0008,0070), model (0008,1090), software version (0018,1020)
-- and station name (0008,1010)
-- e.g.
-- # ImportConverter4 = save to E:\conquest\dicom\ct\%i\%o.dcm; process study by openrem_import_ct.lua(E:\conquest\dicom\ct\%i::%V0008,0070::%V0008,1090::%V0018,1020::%V0008,1010); destroy;

local split_input_text = split(command_line, '::')
local study_folder_path = split_input_text[1]
local manufacturer = split_input_text[2]
local model_name = split_input_text[3]
local software_version = split_input_text[4]
local station_name = split_input_text[5]

print(study_folder_path)
print(manufacturer)
print(model_name)
print(software_version)
print(station_name)


if (manufacturer == 'Philips' and model_name == 'Brilliance 64') then
  print('It is a Philips Brilliance 64')
  -- It is the Grantham Philips Brilliance 64.
  -- Look for a dose summary image and import it
  local files = assert(io.popen('dir /b ' .. study_folder_path))
  local output = files:read('*all')
  local file_list = split(output, '\n')

  for k, v in pairs(file_list) do
    current_file = study_folder_path .. '\\' .. v -- The fully qualified file name and path (Windows-specific)
    readdicom(current_file)
    if Data.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7' then
      system('d:\\Server_Apps\\python27\\python.exe d:\\Server_Apps\\python27\\Scripts\\openrem_ctphilips.py ' .. current_file)
      print('The system command to import a Philips CT dose image has been executed')
    end
  end
  -- Delete the study from disk
  print('Complete. Deleting study images.')
  system('c:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
end


-- CT1 and CT2 at Lincoln, and also Pilgrim main scanner
if (manufacturer == 'TOSHIBA' and model_name == 'Aquilion') then
  print('It is a Toshiba Aquilion. Running create_rdsr_from_toshiba_ct_dose_images.py script...')
  system('d:\\Server_Apps\\python27\\python.exe d:\\Server_Apps\\python27\\Scripts\\create_rdsr_from_toshiba_ct_dose_images.py ' .. study_folder_path)
  print('The system command has been executed to create the rdsr and import it')
  -- Note: the above python script deletes the study from disk once it's been imported in to OpenREM
end


-- Pilgrim modular scanner
if (manufacturer == 'TOSHIBA' and model_name == 'Aquilion PRIME') then
  print('It is a Toshiba Aquilion Prime. Cannot make use of these images - deleting them.')
  system('c:\\Windows\\system32\\cmd.exe /C rmdir /S /Q ' .. study_folder_path)
  print('The system command has been executed to delete the images from the server')
end
