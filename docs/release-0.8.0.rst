########################
Upgrade to OpenREM 0.8.0
########################

****************
Headline changes
****************

* This release has extensive automated testing for large parts of the codebase (for the first time)
* Code quality is much improved, reduced duplication, better documentation, many bugs fixed
* Imports: RDSR from a wider range of systems now import properly
* Imports: Better distinction and control over defining RDSR studies as RF or DX
* Imports: Code and instructions to generate and import RDSR from older Toshiba CT scanners
* Imports: DICOM Query-Retrieve functionality has been overhauled
* Imports, display and export: Better handling of non-ASCII characters
* Interface: More detailed, consistent and faster rendering of the data in the web interface
* Interface: Maps of fluoroscopy radiation exposure incident on a phantom (Siemens RDSRs only)
* Interface: More and better charts, including scatter plots for mammography
* Exports: Much faster, and more consistent

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Follow the instructions found at :doc:`upgrade-offline`, before returning here to update the database and configuration.

****************************
Upgrading from version 0.7.4
****************************

Upgrade
=======

* Back up your database

    * For PostgreSQL you can refer to :ref:`backup-psql-db`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* If you are using a virtualenv, activate it

* Install the new version of OpenREM:

.. sourcecode:: bash

    pip install openrem==0.8.0b1

..  _upgradefrom074:

Migrate the database
====================

In a shell/command window, move into the openrem folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``Lib\site-packages\openrem\``

.. sourcecode:: bash

    python manage.py makemigrations remapp
    python manage.py migrate remapp

Update the configuration
========================

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

    If the configuration is not added for the new ``openrem_extractor.log`` is not configured, you will find it being
    created whereever you start the webserver from, and starting the webserver may fail.

Add the new extractor log file configuration to the ``local_settings.py`` - you can copy the 'Logging
configuration' section from  ``local_settings.py.example`` if you haven't made many changes to this section. See the
:ref:`local_settings_logfile` settings in the install instructions.

Adding legacy Toshiba CT functionality
======================================

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


Restart all the services
========================

Follow the guide at :doc:`startservices`.

..  _@rijkhorst: https://bitbucket.org/rijkhorst/
.. _`Offis DICOM toolkit`: http://dicom.offis.de/dcmtk.php.en
.. _`Java`: http://java.com/en/download/
.. _`PixelMed Java DICOM Toolkit`: http://www.pixelmed.com/dicomtoolkit.html
