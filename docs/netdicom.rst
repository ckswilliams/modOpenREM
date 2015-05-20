###########################
DICOM Networking in OpenREM
###########################

***********************
Functionality available
***********************

This is an initial preview release in 0.6.0, with the following features:

* DICOM Store service class provider
* DICOM objects are fed directly into appropriate routine for data extraction
* Extraction jobs are handled by Celery
* Configuration is via the ``local_settings.py`` file

*************
Configuration
*************

The following settings need to be in your ``local_settings.py`` file:

.. code-block:: python

    STORE_AET = "STOREOPENREM"
    STORE_PORT = 8104
    RM_DCM_NOMATCH = True
    RM_DCM_RDSR = False
    RM_DCM_MG = False
    RM_DCM_DX = False
    RM_DCM_CTPHIL = False


STORE_AET
=========

This is the AET you use when configuring send nodes from your modalities.

Set this to your chosen value - any combination of letters and numbers up to 16 characters. No spaces or other
characters allowed.

In the current implementation, the actual value is not actually important - the AET is not checked when a DICOM object
is received.

STORE_PORT
==========

This is the port you send DICOM objects to. The standard port for DICOM servers is port 104. However, on many operating
systems starting a service on a port lower than 1025 requires additional privileges. That is why the suggested port is
8104.

Depending on your network setup you may have to configure the firewall accordingly.

RM_DCM_NOMATCH
==============

When DICOM objects are received they are checked for suitability to have dose related data extracted using any of the
current extraction routines.

If you want the DICOM object to be deleted if it can't be used, set ``RM_DCM_NOMATCH`` to ``True``. Otherwise set this
to ``False``.

Setting this to ``True`` is advisable as otherwise your disk can fill up very quickly if enture CT studies get sent
through for example.

RM_DCM_RDSR, RM_DCM_MG, RM_DCM_DX and RM_DCM_CTPHIL
===================================================

Set these to ``True`` to delete the DICOM objects once the dose related data had been extracted. Otherwise set them to
``False``, and the DICOM objects will be stored in a folder called ``dicom_in`` in the ``MEDIA_ROOT`` folder.

The ``RDSR`` setting is for Radiation Dose Structured Reports (usually from CT or fluoroscopy), ``MG`` is for
mammography images, ``DX`` is for radiography images and ``CTPHIL`` is for Philips CT dose screen images.

Setting these to ``True`` is advisable, especially for the images as again the disk can fill up quickly.

**********************************
How to use the DICOM store service
**********************************

Open a command window or shell::

    openrem_store.py

You should see the following output, depending on your configuration::

    starting AE... AET:STOREOPENREM, port:8104 done

Make sure that the Celery task manager is running, as all extraction jobs are passed to Celery.

*****************************************
Planned functionality for future releases
*****************************************

DICOM Store
===========

* Configuration will move to the database with a web interface
* Web interface view of activity and logs

DICOM Query-Retrieve
====================

* Function to query retrieve the PACS or modality
* Ad hoc or scheduled
* Web interface for configuration, activating, monitoring success and logs
