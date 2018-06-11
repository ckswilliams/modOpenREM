Creating batch scripts on windows
*********************************

Create and save a bash script for each of RDSR, mammo, DX and Philips CT dose images, as required. They should have
content something like the following.

These scripts assume there is no virtualenv in use. If you are using one, simply refer to the python executable and
OpenREM script in your virtualenv rather than the system wide version.

* Radiation Dose Structured Reports

..  sourcecode:: bat

    C:\Python27\python.exe C:\Python27\scripts\openrem_rdsr.py %1
    del %1


* Mammography images

..  sourcecode:: bat

    C:\Python27\python.exe C:\Python27\scripts\openrem_my.py %1
    del %1


* Radiography images (DX, and CR that might be DX)

..  sourcecode:: bat

    C:\Python27\python.exe C:\Python27\scripts\openrem_dx.py %1
    del %1


* Philips CT dose info images for Philips CT systems with no RDSR

..  sourcecode:: bat

    C:\Python27\python.exe C:\Python27\scripts\openrem_ctphilips.py %1
    del %1
