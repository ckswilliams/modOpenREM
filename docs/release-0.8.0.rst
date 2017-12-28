########################
Upgrade to OpenREM 0.8.0
########################

****************
Headline changes
****************

* Imports: Can now create RDSR for import from legacy Toshiba CT studies using Offis DCMTK and Pixelmed
* Imports: No longer tries to import non-dose report Enhanced Structured Reports
* Imports: Hologic DBT proprietary projection images now have laterality and accumulated AGD extracted correctly
* Imports: Format of comment field constructed when importing from Philips Dose Info series no longer uses XML styling
* Charts: Added mammography scatter plot, thanks to `@rijkhorst`_
* Exports: Now much faster
* Exports: DX and RF exports work with multiple filters, and will be displayed to max 4 sf
* Interface/Imports: Now possible to define a modality as DX or fluoro when RDSR is ambiguous
* Interface: Detail and filter views now faster, AJAX introduced to home page and exports
* Interface: Operator's name is now displayed in the details page for each modality, along with the performing
  physician's name for CT and fluoro

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************


****************************
Upgrading from version 0.7.4
****************************

* Set the date format for xlsx exports (need to check csv situation). Copy the following code into your
  ``local_settings.py`` file if you want to change it from ``dd/mm/yyy``:

.. sourcecode:: python

    # Date format for exporting data to Excel xlsx files.
    # Default in OpenREM is dd/mm/yyyy. Override it by uncommenting and customising below; a full list of codes is available
    # at https://msdn.microsoft.com/en-us/library/ee634398.aspx.
    # XLSX_DATE = 'mm/dd/yyyy'

* Consider setting the timezone and language in ``local_settings.py``. See ``local_settings.py.example``.


**************************************
Adding legacy Toshiba CT functionality
**************************************

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



..  _@rijkhorst: https://bitbucket.org/rijkhorst/
.. _`Offis DICOM toolkit`: http://dicom.offis.de/dcmtk.php.en
.. _`Java`: http://java.com/en/download/
.. _`PixelMed Java DICOM Toolkit`: http://www.pixelmed.com/dicomtoolkit.html
