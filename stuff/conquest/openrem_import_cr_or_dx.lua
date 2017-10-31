require "openrem_string_split"

-- It is assumed that 'openrem_dx.py' is in the Python scripts folder, and that
-- this and the Python executable location are included in the system path.

-- It is assumed that this code has been called from an ImportConverter within
-- a Conquest dicom.ini file, and passed the complete filename and path of a
-- DICOM object, e.g.
--   ImportModality0 = CR
--   ImportConverter0 = save to C:\dicom\%o.dcm; openrem_import_cr_or_dx.lua("C:\dicom\%o.dcm"); destroy

local manufacturers_to_ignore = {'Agfa', 'Agfa-Gevaert', 'Agfa-Gevaert AG', 'Faxitron X-Ray LLC', 'Gendex-KaVo'}
local model_names_to_ignore = {'CR 85', 'CR 75', 'CR 35', 'CR 25', 'ADC_5146'}
local station_names_to_ignore = {'RU0', 'ru0', 'CR85 Main'}

local split_input_text = split(command_line, "::")
local file_name_and_path = split_input_text[1]
local manufacturer = split_input_text[2]
local model_name = split_input_text[3]
local station_name = split_input_text[4]
local software_versions = split_input_text[5]
local study_date = split_input_text[6]


-- If any of the entries in manufacturers_to_ignore is present then the image is
-- not useful.
for i = 1, #manufacturers_to_ignore do
  if manufacturer == manufacturers_to_ignore[i] then
    print('Ignoring and deleting: manufacturer is ' .. manufacturer)
    system('c:\\Windows\\system32\\cmd.exe /C del ' .. file_name_and_path)
    return
  end
end

-- If any of the entries in model_names_to_ignore is present then the image is
-- not useful.
for i = 1, #model_names_to_ignore do
  if model_name == model_names_to_ignore[i] then
    print('Ignoring and deleting: model name is ' .. model_name)
    system('c:\\Windows\\system32\\cmd.exe /C del ' .. file_name_and_path)
    return
  end
end

-- If any of the entries in station_names_to_ignore is present then the image is
-- not useful.
for i = 1, #station_names_to_ignore do
  if station_name == station_names_to_ignore[i] then
    print('Ignoring and deleting: station name is ' .. station_name)
    system('c:\\Windows\\system32\\cmd.exe /C del ' .. file_name_and_path)
    return
  end
end


-- If we've got to this point then the image must be useful, so import it.
print('Importing into openrem: openrem_dx.py')
system('d:\\Server_Apps\\python27\\python.exe d:\\Server_Apps\\python27\\Scripts\\openrem_dx.py ' .. file_name_and_path)
system('c:\\Windows\\system32\\cmd.exe /C del ' .. file_name_and_path)
