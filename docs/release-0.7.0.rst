########################################
OpenREM Release Notes version 0.7.0 beta
########################################

.. Warning::

    This is a beta version for developer testing. It is not suitable for general use, and the instructions below are
    likely to be incorrect.

****************
Headline changes
****************

* System

    * Django upgraded to version 1.8
    * Median function added to the database if using PostgreSQL
    * Database modification to add study time in datetime format for use with workload charts
    * New user-defined display name for each unique system so that rooms with the same DICOM station name are displayed separately

        * Display names can be viewed via user options menu
        * Display names can be edited via the admin options menu

* Charts

    * Chart plotting status shown on the home page when a user is logged in
    * Bar chart data points sorted by frequency, value or name in ascending or descending order
    * New chart of DLP per requested procedure type and requested procedure frequency
    * Chart data returned using AJAX to make pages more responsive
    * Chart plotting options available via user options menu

* DICOM Networking

    * Configuring and running DICOM Store SCP is now managed in the web interface
    * Query retrieve function is now built in to query PACS systems or modalities

****************************
Upgrading from version 0.6.0
****************************

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* The 0.7.0 upgrade must be made from a 0.6.0 (or later) database, and a schema migration is required:

    Delete all numbered migration files in openrem's ``migrations`` folder.

.. sourcecode:: bash

    pip install openrem==0.7.0b5

    # Windows:
    python C:\Python27\Lib\site-packages\openrem\manage.py migrate --fake-initial
    python C:\Python27\Lib\site-packages\openrem\manage.py makemigrations remapp
    python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp --fake

* Now rename the file::

    0002_upgraded_openrem_add_median_function_and_populate_display_name_table.py.inactive

  to::

    0002_upgraded_openrem_add_median_function_and_populate_display_name_table.py

  and then run::

    # Windows:
    python C:\Python27\Lib\site-packages\openrem\manage.py makemigrations remapp
    python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

* Check/add the DICOM delete rules to the local_settings.py file. Should DICOM files be kept or deleted when they have
  been processed?

    ``RM_DCM_NOMATCH`` determines whether files that are not of any of the types we can get information from are deleted.
    This is only applicable if you use the DICOM Store SCP built into OpenREM. For example, if it receives a whole CT
    study instead of just the RDSR, with the setting as ``True``, the image series are deleted straight away.

    The other settings determine whether Radiation Dose Structured Reports, Mammography images, Radiography images and
    Philips CT images are kept (``False``) or deleted (``True``) when they have been processed.

    The initial setting is False, but it is recommended that at least the image types and ``NOMATCH`` are set to ``True``
    as they can fill the disk quickly if they are allowed to build up::

        RM_DCM_NOMATCH = True
        RM_DCM_RDSR = True
        RM_DCM_MG = True
        RM_DCM_DX = True
        RM_DCM_CTPHIL = True

    See :doc:`netdicom` for information about how to make use of the new functionality (docs not yet ready)


Restart the web server
======================

If you are using the built-in test web server (`not for production use`)::

    python manage.py runserver x.x.x.x:8000 --insecure

Otherwise restart using the command for your web server

Restart the Celery task queue
=============================

For testing, in a new shell:

Linux::

    # Linux: Debian/Ubuntu and derivatives
    cd /usr/local/lib/python2.7/dist-packages/openrem/
    # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
    cd /usr/local/lib/python2.7/site-packages/openrem/

    celery multi start stores default -A openremproject -c:stores 2 -c 3 \
    -Q:stores stores -Q default \
    --pidfile=/path/to/media/celery/%N.pid --logfile=/path/to/media/celery/%N.log

If you intend to use OpenREM to provide a DICOM Store SCP (ie you can DICOM send things to OpenREM without using
any other program, such as Conquest), then we need a Celery Queue just for the store. The node (and queue) created for
this is called ``stores`` and it needs to have a concurrency equal or greater than the number of store SCPs. This would
normally be just one. So set ``-c:stores 1`` or ``-c:stores 2`` etc as you see fit. The ``-c 3`` specifies how many
workers should be available for all the other jobs - exports; and imports when using the OpenREM Store SCP.

You must also specify the location for the pid file and for the log file. You might put these in the media folder, or
the logs might go in ``/var/log/``.

The ``\`` is added in to allow the single command to go over several lines.

Windows::

    cd C:\Python27\Lib\site-packages\openrem\
    celery multi start stores default -A openremproject -c:stores 2 -c 3 ^
    -Q:stores stores -Q default ^
    --pidfile=\path\to\media\celery\%N.pid --logfile=\path\to\media\celery\%N.log

This is the same as for Linux, but this time the line continuation character is ``^``.

For production use, see http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html

To stop the celery queues::

    celery multi stop stores default --pidfile=/path/to/media/celery/%N.pid

***********************
Summary of new features
***********************

Charts
======

Release 0.7.0 has several additions to the charts available in OpenREM. For detailed information, please see :doc:`charts`.
