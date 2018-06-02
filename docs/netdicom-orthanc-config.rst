Orthanc Store configuration
===========================

Create Lua file
---------------

Open the following link in a new tab, create a file called ``openrem.lua`` *somewhere*, and copy and paste the
content into the file:

* https://bitbucket.org/openrem/openrem/src/issue635OrthancExperiment/stuff/openrem.lua

Edit the top two sections
-------------------------

..  sourcecode:: lua

    -- OpenREM python environment and other settings

    -- Set this to the path and name of the python executable used by OpenREM
    local python_executable = 'D:\\Server_Apps\\python27\\python.exe'

    -- Set this to the path of the python scripts folder used by OpenREM
    local python_scripts_path = 'D:\\Server_Apps\\python27\\Scripts\\'

    -- Set this to the path where you want Orthanc to temporarily store DICOM files
    local temp_path = 'E:\\conquest\\dicom\\'

    -- Set this to 'mkdir' on Windows, or 'mkdir -p' on Linux
    local mkdir_cmd = 'mkdir'

    -- Set this to '\\'' on Windows, or '/' on Linux
    local dir_sep = '\\'

    -- Set this to the path where you want to keep physics-related DICOM images
    local physics_to_keep_folder = 'E:\\conquest\\dicom\\physics\\'
    -------------------------------------------------------------------------------------


    -------------------------------------------------------------------------------------
    -- User-defined lists that determine how Orthanc deals with certain studies

    -- A list to check against patient name and ID to see if the images should be kept.
    -- Orthanc will put anything that matches this in the physics_to_keep_folder.
    local physics_to_keep = {'physics'}

    -- Lists of things to ignore. Orthanc will ignore anything matching the content of
    -- these lists: they will not be imported into OpenREM.
    local manufacturers_to_ignore = {'Agfa', 'Agfa-Gevaert', 'Agfa-Gevaert AG', 'Faxitron X-Ray LLC', 'Gendex-KaVo'}
    local model_names_to_ignore = {'CR 85', 'CR 75', 'CR 35', 'CR 25', 'ADC_5146', 'CR975'}
    local station_names_to_ignore = {'CR85 Main', 'CR75 Main'}
    local software_versions_to_ignore = {'VixWin Platinum v3.3'}
    local device_serial_numbers_to_ignore = {'SCB1312016'}

    -- A list of CT make and model pairs that are known to have worked with the Toshiba CT extractor
    local toshiba_extractor_systems = {
            {'GE Medical Systems', 'Discovery 710'},
            {'GE Medical Systems', 'Discovery ste'},
            {'GE Medical Systems', 'Brightspeed'},
            {'GE Medical Systems', 'Lightspeed Plus'},
            {'GE Medical Systems', 'Lightspeed16'},
            {'GE Medical Systems', 'Lightspeed Pro 32'},
            {'GE Medical Systems', 'Lightspeed VCT'},
            {'Siemens', 'Biograph64'},
            {'Siemens', 'Somatom Definition'},
            {'Siemens', 'Somatom Definition Edge'},
            {'Siemens', 'Somatom Definition Flash'},
            {'Siemens', 'Somatom Force'},
            {'Toshiba', 'Aquilion'},
            {'Toshiba', 'Aquilion Prime'},
            {'Toshiba', 'Aquilion One'}
    }
    -------------------------------------------------------------------------------------

**OpenREM python environment and other settings**

* Set this to the path and name of the python executable used by OpenREM::

    # Linux, no virtualenv example:
    local python_executable = '/usr/bin/python'
    # Linux, using virtualenv example:
    local python_executable = '/home/username/veopenrem/bin/python'
    # Windows, not using virtualenv example:
    local python_executable = 'C:\\Python27\\python.exe'
    # Windows, using virtualenv example:
    local python_executable = 'C:\\path\\to\\virtualenv\\Scripts\\python.exe'

* Set this to the path of the python scripts folder used by OpenREM::

    # Linux, no virtualenv example:
    local python_scripts_path = '/usr/local/bin/'
    # Linux, using virtualenv example:
    local python_scripts_path = '/home/username/veopenrem/bin/'
    # Windows, not using virtualenv example:
    local python_scripts_path = 'C:\\Python27\\Scripts\\'
    # Windows, using virtualenv example:
    local python_scripts_path = 'C:\\path\\to\\virtualenv\\Scripts\\'

* Set this to the path where you want Orthanc to temporarily store DICOM files. Note: the folder must exist::

    # Linux example:
    local temp_path = '/tmp/orthanc/'
    # Windows example:
    local temp_path = 'E:\\conquest\\dicom\\'

* Set this to 'mkdir' on Windows, or 'mkdir -p' on Linux::

    # Linux:
    local mkdir_cmd = 'mkdir -p'
    # Windows:
    local mkdir_cmd = 'mkdir'

* Set this to '\\'' on Windows, or '/' on Linux::

    # Linux:
    local dir_sep = '/'
    # Windows:
    local dir_sep = '\\'

* *Optional* Set this to the path where you want to keep physics-related DICOM images::

    local physics_to_keep_folder = 'E:\\conquest\\dicom\\physics\\'


**User-defined lists that determine how Orthanc deals with certain studies**

* A list to check against patient name and ID to see if the images should be kept.
  Orthanc will put anything that matches this in the ``physics_to_keep_folder``::

    local physics_to_keep = {'physics'}

* Lists of things to ignore. Orthanc will ignore anything matching the content of
  these lists: they will not be imported into OpenREM::

    local manufacturers_to_ignore = {'Agfa', 'Agfa-Gevaert', 'Agfa-Gevaert AG', 'Faxitron X-Ray LLC', 'Gendex-KaVo'}
    local model_names_to_ignore = {'CR 85', 'CR 75', 'CR 35', 'CR 25', 'ADC_5146', 'CR975'}
    local station_names_to_ignore = {'CR85 Main', 'CR75 Main'}
    local software_versions_to_ignore = {'VixWin Platinum v3.3'}
    local device_serial_numbers_to_ignore = {'SCB1312016'}

* A list of CT make and model pairs that are known to have worked with the Toshiba CT extractor::

    local toshiba_extractor_systems = {
            {'GE Medical Systems', 'Discovery 710'},
            {'GE Medical Systems', 'Discovery ste'},
            {'GE Medical Systems', 'Brightspeed'},
            {'GE Medical Systems', 'Lightspeed Plus'},
            {'GE Medical Systems', 'Lightspeed16'},
            {'GE Medical Systems', 'Lightspeed Pro 32'},
            {'GE Medical Systems', 'Lightspeed VCT'},
            {'Siemens', 'Biograph64'},
            {'Siemens', 'Somatom Definition'},
            {'Siemens', 'Somatom Definition Edge'},
            {'Siemens', 'Somatom Definition Flash'},
            {'Siemens', 'Somatom Force'},
            {'Toshiba', 'Aquilion'},
            {'Toshiba', 'Aquilion Prime'},
            {'Toshiba', 'Aquilion One'}
    }


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

    Run ``Services.msc`` as an administrator
    Right-hand click on the Orthanc entry and select ``Restart``
