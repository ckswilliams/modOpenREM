Orthanc Store configuration
===========================

Create Lua file
---------------

Open the following link in a new tab and copy and paste the content into a text editor. Save this as a new file called
``openrem_orthanc_config.lua``. This can be saved anywhere, provided that Orthanc is able to access it:

* |openrem_orthanc_conf_link|


Edit the top two sections
-------------------------

..  sourcecode:: lua

    -------------------------------------------------------------------------------------
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

    -- Set this to true if you want Orthanc to keep physics test studies, and have it
    -- put them in the physics_to_keep_folder. Set it to false to disable this feature
    local use_physics_filtering = true

    -- Set this to the path where you want to keep physics-related DICOM images
    local physics_to_keep_folder = 'E:\\conquest\\dicom\\physics\\'

    -- Set this to the path and name of your zip utility, and include any switches that
    -- are needed to create an archive (used with physics-related images)
    -- You can install and use the 'zip' command on Linux without any switches
    local zip_executable = 'D:\\Server_Apps\\7zip\\7za.exe a'

    -- Set this to the path and name of your remove folder command, including switches
    -- for it to be quiet (used with physics-related images)
    -- You can use the command 'rm -r' if you are using Linux
    local rmdir_cmd = 'rmdir /s/q'
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

    -- Set this to true if you want to use the OpenREM Toshiba CT extractor. Set it to
    -- false to disable this feature.
    local use_toshiba_ct_extractor = true

    -- A list of CT make and model pairs that are known to have worked with the Toshiba CT extractor.
    -- You can add to this list, but you will need to verify that the dose data created matches what you expect.
    local toshiba_extractor_systems = {
            {'Toshiba', 'Aquilion'},
            {'GE Medical Systems', 'Discovery STE'},
    }
    -------------------------------------------------------------------------------------

Guide to customising Orthanc configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**python_executable** Set this to the path and name of the python executable used by OpenREM::

    # Linux, no virtualenv example:
    local python_executable = '/usr/bin/python'
    # Linux, using virtualenv example:
    local python_executable = '/home/username/veopenrem/bin/python'
    # Windows, not using virtualenv example:
    local python_executable = 'C:\\Python27\\python.exe'
    # Windows, using virtualenv example:
    local python_executable = 'C:\\path\\to\\virtualenv\\Scripts\\python.exe'

**python_scripts_path** Set this to the path of the python scripts folder used by OpenREM::

    # Linux, no virtualenv example:
    local python_scripts_path = '/usr/local/bin/'
    # Linux, using virtualenv example:
    local python_scripts_path = '/home/username/veopenrem/bin/'
    # Windows, not using virtualenv example:
    local python_scripts_path = 'C:\\Python27\\Scripts\\'
    # Windows, using virtualenv example:
    local python_scripts_path = 'C:\\path\\to\\virtualenv\\Scripts\\'

**temp_path** Set this to the path where you want Orthanc to temporarily store DICOM files.
Note: the folder must exist and Orthanc must be able to write to it. On Ubuntu Linux the user is ``orthanc``::

    # Linux example:
    local temp_path = '/tmp/orthanc/'
    # To create the directory:
    mkdir /tmp/orthanc
    sudo chown orthanc /tmp/orthanc/
    # Windows example:
    local temp_path = 'C:\\Temp\\orthanc\\'

* Using Orthanc to collect Physics QA images:

  **use_physics_filtering** set this to ``false`` if you don't want to use this facility. If this is false, the other
  physics image related values don't matter. If it is ``true``, the:

  **physics_to_keep_folder** *Optional* Set this to the path where you want to keep physics-related DICOM images::

      local physics_to_keep_folder = 'E:\\conquest\\dicom\\physics\\'

  **physics_to_keep** A list to check against patient name and ID to see if the images should be kept.
  Orthanc will put anything that matches this in the ``physics_to_keep_folder``::

      local physics_to_keep = {'physics'}

* Lists of things to ignore. Orthanc will ignore anything matching the content of
  these comma separated lists: they will not be imported into OpenREM::

    local manufacturers_to_ignore = {'Faxitron X-Ray LLC', 'Gendex-KaVo'}
    local model_names_to_ignore = {'CR 85', 'CR 75'}
    local station_names_to_ignore = {'CR85 Main', 'CR75 Main'}
    local software_versions_to_ignore = {'VixWin Platinum v3.3'}
    local device_serial_numbers_to_ignore = {'SCB1312016'}

* Attempting to get dose data from CT studies with no RDSR using the OpenREMToshiba CT extractor

  **use_toshiba_ct_extractor** set this to ``false`` if you haven't installed the additional
  :ref:`install_toshiba_resources` or do not wish to use this function. Otherwise:

  **toshiba_extractor_systems** A list of CT make and model pairs that you want to use with the Toshiba CT
  extractor. You can add to this list, but you will need to verify that the dose data created matches what
  you expect. These will only be considered if an RDSR is not found with the study, otherwise that will be
  used in preference. The format is ``{{'manufacturer', 'model'}, {'manufacturer two'}, {'model two'}}``
  etc. They will be matched against the names presented in the DICOM headers::

      local toshiba_extractor_systems = {
              {'Toshiba', 'Aquilion'},
              {'GE Medical Systems', 'Discovery STE'},
      }

Configure Orthanc to make use of the openrem_orthanc_config.lua file
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
    "/path/to/openrem_orthanc_config.lua"
    ],

Windows (note the double back-slash):

..  sourcecode:: json

    // List of paths to the custom Lua scripts that are to be loaded
    // into this instance of Orthanc
    "LuaScripts" : [
    "C:\\path\\to\\openrem_orthanc_config.lua"
    ],

Check permissions
-----------------

**Linux**

* orthanc user needs to be able to write to the OpenREM logs
* orthanc user needs to be able to write to the temp directory we specified

**Windows**

* Orthanc will be running as a local admin user, so should be able to function without any special consideration

Restart Orthanc
---------------

Ubuntu linux::

    sudo service orthanc force-reload

Windows:

* Run ``Services.msc`` as an administrator
* Right-hand click on the Orthanc entry and select ``Restart``
