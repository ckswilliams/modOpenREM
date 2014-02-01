Importing data to OpenREM
*************************


Importing dose related data from DICOM files
============================================


..  versionchanged:: 0.3.3

    The scripts now have a ``.py`` suffix

..  warning::

    Installs of OpenREM earlier than 0.3.3 will break on upgrade if the scripts are called from other programs

If you are using linux or have put ```"C:\Python27\Lib\site-packages\openrem\scripts"`` and
``"C:\Python27\Lib\site-packages\openrem"`` onto your path, you should be able to import from the command line:

* For Radiation Dose Structured Reports

 * ``openrem_rdsr.py filename.dcm``

* For mammography DICOM images (see restrictions on testing)

 * ``openrem_mg.py filename.dcm``

* For CT dose summary files from Philips CT scanners

 * ``openrem_ctphilips.py filename.dcm``
