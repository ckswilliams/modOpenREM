Modality send
*************

If you are able to configure your modalities to send DICOM Radiation Dose Structured Reports, DX images or MG images
directly to the OpenREM server automatically this is an ideal method to ensure all activity is recorded.

To do this, you need to have set up a DICOM Store service on the OpenREM server. You can use the in-built DICOM Store
that OpenREM can provide, particularly for testing, or you can use a third-party service such as Conquest.

In-built DICOM Store
====================

..  toctree::
    :maxdepth: 2

    netdicom-nodes

*TODO: extract all the third-party stuff from netdicom-nodes*


Conquest Store
==============

The instructions for installing Conquest were included in the :ref:`installdicomstore` docs.

Now OpenREM is installed, you need to configure ``dicom.ini`` and setup the import scripts

*TODO: Here will be instructions for dicom.ini and import scripts for Windows and linux*
