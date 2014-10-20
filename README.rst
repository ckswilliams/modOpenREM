This fork of OpenREM includes the ability to import data from radiographic DICOM images of "DX" and "CR" type. The data from these images is displayed under a "Radiography" heading alongside the existing "CT", "Fluoroscopy" and "Mammography" titles. The stored data can be filtered and exported to a csv or xlsx file.

The import of the data works in a similar way to the existing mammography import: the dx.py script must be run with the path to the DICOM file as an argument. For example:

python dx.py C:\\temp\\image.dcm.


=======
OpenREM
=======

OpenREM is a Django app to extract, store and export Radiation Exposure
Monitoring related information, primarily from DICOM files.

Full documentation can be found on Read the Docs: http://docs.openrem.org

**For upgrades**, please look at the `version 0.4.3 release notes <http://docs.openrem.org/en/latest/release-0.4.3.html>`_

For fresh installs, please look at the `install docs <http://docs.openrem.org/page/install.html>`_

Contribution of code, ideas, bug reports documentation is all welcome.
Please feel free to fork the repository and send me pull requests. See
`the website <http://openrem.org/getinvolved>`_ for more information.