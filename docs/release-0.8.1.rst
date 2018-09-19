########################
Upgrade to OpenREM 0.8.1
########################

****************
Headline changes
****************

* Documentation: improved docs and added one-page complete install on Ubuntu instructions
* Install: temporary fix for dependency error
* Interface: added feature to allow users to change their own password
* Charts: fixed problem where a blank category name may not be displayed correctly
* Imports: reduced list of scanners that work with the legacy Toshiba CT extractor
* Imports: improved handling of non-conformant DX images with text in filter thickness fields
* Query-Retrieve: added non-standard option to work-around bug in Impax C-FIND SCP
* Exports: fixed bug in mammography NHSBSP exports that incorrectly reported the filter material in some circumstances
* Exports: fixed bug where sorting by AGD would cause duplicate entries for bilateral studies
* Exports: fixed another non-ASCII bug

If upgrading from 0.7.4, see also :doc:`release-0.8.0`


***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Follow the instructions found at :doc:`upgrade-offline`, before returning here to update the database and configuration.


*************************************
Upgrading from version 0.7.4 or 0.8.0
*************************************

Upgrade
=======

* Back up your database

    * For PostgreSQL on linux you can refer to :ref:`backup-psql-db`
    * For PostgreSQL on Windows you can refer to :ref:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* Consider temporarily disabling your DICOM Store SCP, or redirecting the data to be processed later

* If you are using a virtualenv, activate it

* Install the new version of OpenREM:

.. sourcecode:: bash

    pip install openrem==0.8.1

..  _upgradefrom074:

Update the configuration
========================
*no changes should be required if upgrading from 0.8.0*

Locate and edit your local_settings file

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/openremproject/local_settings.py``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openremproject\local_settings.py``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\openremproject\local_settings.py``

Date format
^^^^^^^^^^^
Set the date format for xlsx exports (need to check csv situation). Copy the following code into your
``local_settings.py`` file if you want to change it from ``dd/mm/yyy``:

.. sourcecode:: python

    # Date format for exporting data to Excel xlsx files.
    # Default in OpenREM is dd/mm/yyyy. Override it by uncommenting and customising below; a full list of codes is available
    # at https://msdn.microsoft.com/en-us/library/ee634398.aspx.
    # XLSX_DATE = 'mm/dd/yyyy'

Time zone and language
^^^^^^^^^^^^^^^^^^^^^^

Consider setting the timezone and language in ``local_settings.py``. See ``local_settings.py.example``.

Add additional log file configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

    If the configuration is not added for the new ``openrem_extractor.log`` you will find it being created whereever
    you start the webserver from, and starting the webserver may fail.

Add the new extractor log file configuration to the ``local_settings.py`` - you can copy the 'Logging
configuration' section from  ``local_settings.py.example`` if you haven't made many changes to this section. See the
:ref:`local_settings_logfile` settings in the install instructions.

.. warning::

    If you are upgrading from an earlier beta with the Toshiba RDSR creation logs defined, this has changed names
    and must be modified in ``local_settings.py`` before the migration below. It should be changed to::

        LOGGING['loggers']['remapp.extractors.ct_toshiba']['level'] = 'INFO'  # Toshiba RDSR creation extractor logs

    substituting ``INFO`` for whichever level of logging is desired.

Adding legacy Toshiba CT functionality
======================================
*No change required if upgrading from 0.8.0*

If you need to import data from older Toshiba CT scanners into OpenREM then the following tools need to be available
on the same server as OpenREM:

    * The `Offis DICOM toolkit`_
    * `Java`_
    * pixelmed.jar from the `PixelMed Java DICOM Toolkit`_

The paths to these must be set in ``local_settings.py`` for your system:

.. sourcecode:: python

    # Locations of various tools for DICOM RDSR creation from CT images
    DCMTK_PATH = 'C:/Apps/dcmtk-3.6.0-win32-i386/bin'
    DCMCONV = os.path.join(DCMTK_PATH, 'dcmconv.exe')
    DCMMKDIR = os.path.join(DCMTK_PATH, 'dcmmkdir.exe')
    JAVA_EXE = 'C:/Apps/doseUtility/windows/jre/bin/java.exe'
    JAVA_OPTIONS = '-Xms256m -Xmx512m -Xss1m -cp'
    PIXELMED_JAR = 'C:/Apps/doseUtility/pixelmed.jar'
    PIXELMED_JAR_OPTIONS = '-Djava.awt.headless=true com.pixelmed.doseocr.OCR -'

The example above is for Windows. On linux,
if you have installed the Offis DICOM toolkit with ``sudo apt install dcmtk`` or similar, you can find the path for the
configuration above using the command ``which dcmconv``. This will be something like ``/usr/bin/dcmconv``, so the
``DCMTK_PATH`` would be ``'/usr/bin`` and the ``DCMCONV`` would be ``os.path.join(DCMTK_PATH, 'dcmconv')``. Similarly
for ``DCMMKDIR`` and ``JAVA_EXE``, which might be ``/usr/bin/java``. The pixelmed.jar file should be downloaded from
the link above, and you will need to provide the path to where you have saved it.

The list of CT scanners that the extractor works with has been reduced. You can add to this list, but you will need to
verify that any systems you configure to use this extractor produce data in OpenREM that you expect.


Migrate the database
====================

In a shell/command window, move into the ``openrem`` folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\``

.. sourcecode:: bash

    python manage.py makemigrations remapp
    # if changes are detected (not expected between most beta versions)
    python manage.py migrate remapp


Update static files
===================

In the same shell/command window as you used above run the following command to clear the static files
belonging to your previous OpenREM version and replace them with those belonging to the version you have
just installed (assuming you are using a production web server...):

.. sourcecode:: bash

    python manage.py collectstatic --clear


Restart all the services
========================

Follow the guide at :doc:`startservices`.

..  _@rijkhorst: https://bitbucket.org/rijkhorst/
.. _`Offis DICOM toolkit`: http://dicom.offis.de/dcmtk.php.en
.. _`Java`: http://java.com/en/download/
.. _`PixelMed Java DICOM Toolkit`: http://www.pixelmed.com/dicomtoolkit.html
