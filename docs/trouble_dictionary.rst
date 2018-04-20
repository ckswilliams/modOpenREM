******************
Invalid tag errors
******************

Background
==========

OpenREM versions 0.8 and earlier rely on pydicom 0.9.9 which has recently had a new release, version 1.0. A
replacement of pynetdicom is also being worked on and will be called pynetdicom3. When pynetdicom3 is released, OpenREM
will be revised to work the two new packages, but as they are both backwards-incompatible with the old versions you must
keep using the versions specified by the installation instructions until this happens. (The correct version of pydicom
is installed automatically when you install OpenREM).

The DICOM dictionary (the list of all the tags) supplied with pydicom 0.9.9 is old and doesn't have some of the newer
tags that some modalities are starting to include. This can lead to errors when you attempt to import a file with one of
these tags, and the file will not be imported.

Error message
=============

The error message will look something like this. The actual tag can be different, this is an example.

.. error::

    KeyError: 'Invalid tag (0018, 9559): "Unknown DICOM tag (0018, 9559) - can't look up VR"'

Work-around
===========