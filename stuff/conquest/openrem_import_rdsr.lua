-- It is assumed that 'openrem_rdsr.py' is in the Python scripts folder, and that
-- this and the Python executable location are included in the system path.

-- It is assumed that this code has been called from an ImportConverter within
-- a Conquest dicom.ini file, and passed the complete filename and path of a
-- DICOM object, e.g.
--   ImportConverter0 = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.67"; {save to C:\dicom\%o.dcm; openrem_import_rdsr.lua("C:\dicom\%o.dcm"); destroy}

local file_name_and_path = command_line

system('d:\\Server_Apps\\python27\\python.exe d:\\Server_Apps\\python27\\Scripts\\openrem_rdsr.py ' .. file_name_and_path)
system('c:\\Windows\\system32\\cmd.exe /C del ' .. file_name_and_path)